# -*- coding: utf-8 -*-
"""固定文案口径闸门（客户指定表 · 最高优先级）。

用法：
    python scripts/glossary_check.py <作业.json>
    python scripts/glossary_check.py <已生成的.docx>     # 只查违禁变体与固定文案是否落地

检查两件事：
  1. 固定文案表命中即须逐字照抄 —— 中文原文出现时，对应英文（含标点、大小写）必须出现。
  2. 违禁变体 —— Carbon Steel / Lamp Post / Backplate / Pearl Nickel / 单写 Shade /
     `Base — Metal` 式拼接 等，一律拦下。

退出码：0 = 通过（可能有 WARN）；2 = 有 FAIL，**先改文案再生成文档**。
"""

import json
import os
import re
import sys
import zipfile

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

# ── 固定文案表（与 references/translation-playbook.md 第〇节保持一致）────────────
# exact=True  → 整句逐字比对（大小写、标点都要一致）
# exact=False → 词条比对，忽略大小写
MANDATORY = [
    {"cn": "金属为骨，光影为魂", "en": "Metal as the framework, light as the soul.", "exact": True},
    {"cn": "碳素钢", "en": "Metal", "exact": False},
    {"cn": "灯杆", "en": "Lamp Pole", "exact": False},
    {"cn": "底座", "en": "Base", "exact": False},
    {"cn": "灯罩", "en": "Lampshade", "exact": False},
    {"cn": "一盏灯，照见三代人的团圆",
     "en": "A single lamp, illuminates the reunion of three generations.", "exact": True},
]

# ── 违禁变体 ────────────────────────────────────────────────────────────────
# hard=True  → 直接 FAIL；hard=False → 只有同一句对中文里出现 cn_key 时才 FAIL
FORBIDDEN = [
    {"re": r"carbon\s*steel", "tip": "「碳素钢」须译 Metal，不用 Carbon Steel", "hard": True},
    {"re": r"lamp\s*post", "tip": "「灯杆」须译 Lamp Pole，不用 Lamp Post", "hard": True},
    {"re": r"base\s*plate|back\s*plate|backplate",
     "tip": "「底座」须译 Base，不用 Base Plate / Backplate", "hard": True},
    {"re": r"pearl\s*nickel",
     "tip": "珍珠镍走色卡 Matte brushed nickel，不用 Pearl Nickel", "hard": True},
    {"re": r"(?<!lamp)\bshade\b", "tip": "「灯罩」须译 Lampshade（整词），不要单写 Shade",
     "hard": False, "cn_key": "灯罩"},
    # ── 部位文案「拼接式」：部位 + 材质 之间不许用破折号/斜杠连接 ──────────────
    # 原图自带的中文标签（碳素钢底座 / 白玉磨砂玻璃）是**文案**，要连贯翻译成英文名词短语，
    # 即「材质(形容词) + 部件(名词)」= Metal Base；`Base — Metal` 这类拼接视为生硬，拦下。
    # 注意：`Detail — Base & Arm` 这种**图注分隔**不算（Arm 不在材质词表里），不会误伤。
    {"re": r"\b(base|lamp\s*pole|lampshade)\s*[—–\-/]\s*"
           r"(metal|stainless|steel|brass|nickel|glass|aluminium|aluminum|acrylic|iron|copper|chrome|wood)\b",
     "tip": "部位文案须连贯翻译（碳素钢底座 → Metal Base），不要用破折号/斜杠把部位与材质拼起来",
     "hard": True},
    {"re": r"\b(metal|stainless|steel|brass|nickel|glass|aluminium|aluminum|acrylic|iron|copper|chrome|wood)"
           r"\s*[—–\-/]\s*(base|lamp\s*pole|lampshade)\b",
     "tip": "部位文案须连贯翻译（碳素钢底座 → Metal Base），不要用破折号/斜杠把材质与部位拼起来",
     "hard": True},
    {"re": r"\bbase\s+metal\b",
     "tip": "「金属底座」须写 Metal Base；Base Metal 是「贱金属」，完全另义",
     "hard": True},
    {"re": r"\bthree\s+generations", "cn_key": "团圆",
     "tip": "「一盏灯，照见三代人的团圆」须照抄固定文案，不要另译", "hard": False,
     # 正确译文本身也含 three generations —— 命中原文即放过
     "fixed_en": "A single lamp, illuminates the reunion of three generations."},
]

# 固定句的常见「差不多」写法（命中即 FAIL）
NEAR_MISS = [
    (r"metal\s+as\s+(the\s+)?framework(?!, light)",
     "Metal as the framework, light as the soul."),
    (r"light\s+as\s+the\s+soul(?!\s*\.)",
     "Metal as the framework, light as the soul."),
    (r"a\s+single\s+lamp,?\s+(lights?\s+up|illuminat\w*\s+the\s+reunion)",
     "A single lamp, illuminates the reunion of three generations."),
]

# 文首「注」里出现这些词，说明是在**解释口径**而不是在写文案 → 违禁命中降级为 WARN
RULE_NOTE_HINT = re.compile(r"不再写|不写|不用|禁用|避免|口径|统一译为|统一写法|改为|替换为")


def load_rows(path):
    """返回 rows = [(位置, 中文, 英文, 类型)]，类型 ∈ {pair, note, cap}。"""
    ext = os.path.splitext(path)[1].lower()
    if ext == ".json":
        data = json.load(open(path, encoding="utf-8"))
        rows = []
        for i, blk in enumerate(data.get("blocks", [])):
            cap = blk.get("cap", "块%d" % (i + 1))
            if blk.get("cap"):
                rows.append(("图注 %s" % cap, cap, cap, "cap"))
            for j, p in enumerate(blk.get("pairs", [])):
                if isinstance(p, (list, tuple)) and len(p) >= 2:
                    rows.append(("%s ｜ 句对%d" % (cap, j + 1), str(p[0]), str(p[1]), "pair"))
                elif isinstance(p, str):
                    rows.append(("%s ｜ 句对%d" % (cap, j + 1), "", p, "pair"))
        for i, n in enumerate(data.get("notes", [])):
            if isinstance(n, str):
                rows.append(("文首注%d" % (i + 1), n, n, "note"))
        for key in ("title_cn", "title_en"):
            if data.get(key):
                rows.append(("抬头 %s" % key, str(data[key]), str(data[key]), "note"))
        return rows
    if ext == ".docx":
        with zipfile.ZipFile(path) as z:
            xml = z.read("word/document.xml").decode("utf-8", "replace")
        txt = re.sub(r"<[^>]+>", "\n", xml)
        for a, b in (("&amp;", "&"), ("&lt;", "<"), ("&gt;", ">"), ("&quot;", '"')):
            txt = txt.replace(a, b)
        rows = []
        for i, line in enumerate(txt.split("\n")):
            line = line.strip()
            if line:
                rows.append(("docx 第%d段" % (i + 1), line, line, "pair"))
        return rows
    raise SystemExit("[x] 只认 .json 或 .docx，收到：%s" % path)


def scan(path):
    """扫描作业 JSON / docx，返回 {"rows":n, "fails":[...], "warns":[...], "oks":[...]}。"""
    rows = load_rows(path)
    all_cn = "\n".join(cn for _, cn, _, _ in rows)
    all_en = "\n".join(en for _, _, en, _ in rows)
    fails, warns, oks = [], [], []

    # ── 1. 固定文案全文级：中文出现则英文必须逐字出现 ──────────────────────
    for m in MANDATORY:
        if m["cn"] not in all_cn:
            continue
        hit = (m["en"] in all_en) if m["exact"] else bool(re.search(re.escape(m["en"]), all_en, re.I))
        if hit:
            oks.append("固定文案 ✓ %s → %s" % (m["cn"], m["en"]))
        else:
            fails.append("【固定文案漏译/不一致】中文「%s」已出现，但全文找不到逐字一致的英文：\n      %s"
                         % (m["cn"], m["en"]))

    # ── 2. 句对级（只查真正的句对，不查注）────────────────────────────────
    for where, cn, en, kind in rows:
        if kind != "pair" or not en:
            continue
        for m in MANDATORY:
            if m["cn"] not in cn:
                continue
            bad = (m["en"] not in en) if m["exact"] else not re.search(re.escape(m["en"]), en, re.I)
            if bad:
                fails.append("【同句对不一致】%s\n      中文：%s\n      英文：%s\n      应为：%s"
                             % (where, cn[:70], en[:90], m["en"]))

    # ── 3. 违禁变体 ───────────────────────────────────────────────────────
    for f in FORBIDDEN:
        for where, cn, en, kind in rows:
            if not en:
                continue
            # 正确译文里也含该词（如 three generations）→ 不算违禁
            if f.get("fixed_en") and f["fixed_en"].lower() in en.lower():
                continue
            mt = re.search(f["re"], en, re.I)
            if not mt:
                continue
            if kind == "note" and RULE_NOTE_HINT.search(en):
                warns.append("【提示·疑似规则说明非译文】%s 命中 %r —— 若这句本身是「注」里的口径解释，可忽略"
                             % (where, mt.group(0)))
            elif kind == "pair" and (f["hard"] or (f.get("cn_key") and f["cn_key"] in cn)):
                fails.append("【违禁变体】%s\n      %s\n      命中：%s ｜ 原文：%s"
                             % (where, f["tip"], mt.group(0), en[:80]))
            else:
                warns.append("【提示】%s 出现 %r —— %s" % (where, mt.group(0), f["tip"]))

    # ── 4. 固定句的「差不多」写法 ─────────────────────────────────────────
    for pat, right in NEAR_MISS:
        for where, cn, en, kind in rows:
            if not en:
                continue
            mt = re.search(pat, en, re.I)
            if mt and right not in en:
                fails.append("【近似但非固定文案】%s\n      命中：%r\n      应逐字照抄：%s"
                             % (where, mt.group(0), right))

    return {"rows": len(rows), "fails": fails, "warns": warns, "oks": oks}


def main():
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    src = sys.argv[1]
    if not os.path.isfile(src):
        raise SystemExit("[x] 文件不存在：%s" % src)
    r = scan(src)

    print("=" * 62)
    print("固定文案口径闸门 ｜ %s" % os.path.basename(src))
    print("句对/注/图注 %d ｜ FAIL %d ｜ WARN %d" % (r["rows"], len(r["fails"]), len(r["warns"])))
    print("=" * 62)
    for x in r["oks"]:
        print("  [OK]   " + x)
    for x in r["warns"]:
        print("  [WARN] " + x)
    for x in r["fails"]:
        print("  [FAIL] " + x)
    if not (r["oks"] or r["warns"] or r["fails"]):
        print("  （未命中任何固定文案，也没有违禁变体）")
    if r["fails"]:
        print("\n>>> 退出码 2：先按上面把文案改对，再跑 build_bilingual_doc.py。")
        return 2
    print("\n>>> [PASS] 固定文案口径一致，可以生成文档。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
