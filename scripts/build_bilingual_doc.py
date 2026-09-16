# -*- coding: utf-8 -*-
"""
国际站/速卖通 中英对照详情页 Word 生成器（表格版）。

用法：
    PYTHONIOENCODING=utf-8 python build_bilingual_doc.py job.json

job.json 结构见 job.example.json。每块 = 图片切片 → 图注 → **中英两栏对照表**
（一行一个句对：左列中文原文、右列英文文案），并对每组做分页保护与表格布局统一。

排版铁律（改动前先读 SKILL.md「排版原则」）
  1. HTML 块首个 1pt 占位段不可省 —— 否则图注会被并入图片所在段落。
  2. 对照表用 <table>，行分隔线靠 <td style="border-bottom:...">（tcBorders）。
  3. 单元格文字样式必须写在**内层 <span>**；写在 <td> 上的 color 会变成单元格底纹。
  4. 列宽 / 居中 / 外框颜色 / 行内边距靠 doc_set_table_properties(mode=manual) 后处理。
  5. 单元格行距必须包一层 <p style="line-height:150%">（裸 span 无效）；
     句与句之间的留白靠 cell_margin（上下各 60dxa = 3pt）。
  6. 图内无可翻译文案的行，英文栏一律输出「/」占位（见 NO_COPY），
     不要写「This image has no copy.」这类英文说明 —— 会被误当成上架文案。
  7. 同名多译色（砂岩黑 / 中国红）由 color_caliber 闸门把关：材质只有金属、无布
     → 自动取 Matte Black；材质含亚麻/布艺或判不出来 → **中止生成（退出码 2）**
     并输出待确认问题，由 Agent 去问用户。见手册 7.1。
  8. 尺寸板块（块内写 "kind": "size"）：一个尺寸 = 一行，禁止把 225/485/260/25mm
     挤进同一行（挤在一起分不清哪条引线对哪个数）；且该块自动带一条中文提示
     （部位文案仅定位，客户指定口径）。见 references/translation-playbook.md 4.1。
"""
import html
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import color_caliber as C  # noqa: E402
import edsdk_docx as S  # noqa: E402
import glossary_check as G  # noqa: E402

IMG_W = 540
COL_W = (4400, 5800)          # 两列列宽（dxa，合计 10200 ≈ A4 减 1.5cm 边距的正文宽）

CN_STYLE = "font-size:9.5pt;color:#777777"
EN_STYLE = "font-size:10.5pt;color:#14396A"
EN_NONE_STYLE = "font-size:10.5pt;color:#BBBBBB"   # 无对应文案时的「/」占位
HDR_STYLE = "font-size:9pt;color:#8A8A8A;font-weight:bold"
LINE = "border-bottom:1px solid #E8E8E8"     # 行分隔线（唯一能被引擎映射的边框方向）
HDR_BG = "background-color:#F2F5F9"          # 表头底色（td 上的 background-color 可映射为 shd）
ZEBRA = "background-color:#FBFCFE"           # 偶数行浅底，长表更易横向追读
LINE_H = "line-height:150%"                  # 单元格内行距（映射为 w:spacing w:line=360）

# 图内没有可翻译文案时，英文栏的占位符。用「/」而不是空白或一句英文说明，
# 避免读者把「说明性英文」误当成可直接上架的 Listing 文案。
NO_COPY = "/"
NO_COPY_ALIASES = {"", "/", "-", "—", "–", "n/a", "N/A", "None"}

# ---- 中文提示行（如尺寸板块的判读口径）----
# 与正文的「灰（中文）/ 深蓝（英文）」区分开，读者一眼看出这句是说明而不是文案。
TIP_STYLE = "font-size:9pt;color:#B26A00"

# 尺寸板块的固定中文提示（客户指定口径，逐字照抄）
SIZE_TIP = "部位文案仅为定位作用，如原图只有尺寸则忽略该英文文案，只取用 mm 及 inch 尺寸。"

# 哪些 kind 算「尺寸板块」：自动带提示 + 自动把一行多个尺寸拆成一个尺寸一行
SIZE_KINDS = ("size", "dimension", "dimensions", "尺寸", "尺寸标注")

# 「一行塞了多个尺寸」的判定：分隔符切分后，每一份中文都要含一个 mm 数值
SPLIT_SEP_RE = re.compile(r"\s*[/／|｜]\s*")
DIM_RE = re.compile(r"\d+(?:\.\d+)?\s*mm", re.I)


def esc(s):
    return html.escape(s or "", quote=False)


def escbr(s):
    return html.escape(s or "", quote=False).replace("\n", "<br>")


def build_title_html(job):
    parts = ['<h1 style="text-align:center">%s</h1>' % esc(job.get("title_cn", ""))]
    if job.get("title_en"):
        parts.append('<p style="text-align:center;color:#888888;font-size:10pt">%s</p>'
                     % esc(job["title_en"]))
    line = []
    if job.get("brand"):
        line.append("品牌 Brand: %s" % job["brand"])
    if job.get("target_lang"):
        line.append("目标语言 Language: %s" % job["target_lang"])
    if job.get("platforms"):
        line.append("适用平台 Platform: %s" % job["platforms"])
    if line:
        parts.append('<p style="text-align:center;color:#888888;font-size:10pt">%s</p>'
                     % esc(" ｜ ".join(line)))
    for note in job.get("notes", []):
        parts.append('<p style="font-size:9pt;color:#999999">%s</p>' % esc(note))
    parts.append("<hr>")
    return "".join(parts)


def en_cell(pair):
    """取出英文栏内容；无对应文案时返回占位符「/」。

    「无翻译内容」的判定：en 缺失 / 空白 / 本身就是斜杠或短横线等占位符。
    Returns: (要显示的文本, 是否为占位符)
    """
    raw = pair[1] if len(pair) > 1 else ""
    en = (raw or "").strip()
    if en in NO_COPY_ALIASES:
        return NO_COPY, True
    return en, False


def table_html(pairs):
    """一行一个句对的中英两栏对照表（这是本 skill 的核心排版）。

    - 表头行给出两列含义，读者不用猜哪边是中文；
    - 每个正文行 = 一个句对，中文与英文**严格同行对齐**，比「中文一段 + 英文一段」
      直观得多，也比逐句上下两行更省一半纵向空间；
    - 行分隔线：引擎只把 `<td>` 的 `border-bottom` 映射成 `tcBorders`，
      其余方向（top/left/right）与 `<table>` 的 CSS 一律被忽略 —— 不要浪费时间去试；
    - 两列之间的竖直分隔线来自表格默认的 `insideV`（CBCDD1），改不了色，正好够用；
    - 单元格内容包一层 `<p style="line-height:150%">` 才能设行距（实测映射为
      `w:spacing w:line=360`）；裸 `<span>` 设 line-height 无效。一层 `<p>` 不会
      产生多余空段，行高不会虚增。句与句之间的留白另由 style_tables 的
      `cell_margin` 提供（上下各 3pt）。
    """
    n = len(pairs)
    hdr = ('<tr>'
           '<td style="%s;%s"><p style="%s"><span style="%s">中文原文 · Chinese</span></p></td>'
           '<td style="%s;%s"><p style="%s"><span style="%s">English Copy</span></p></td>'
           '</tr>') % (HDR_BG, LINE, LINE_H, HDR_STYLE,
                       HDR_BG, LINE, LINE_H, HDR_STYLE)

    rows = []
    for i, pair in enumerate(pairs, 1):
        cn = pair[0]
        en, blank = en_cell(pair)
        # 句数 >=3 时才加浅灰序号：方便评审时说「第 3 行」，1-2 行加了反而啰嗦
        num = ('<span style="font-size:8pt;color:#BBBBBB">%02d</span> ' % i) if n >= 3 else ""
        cell = LINE + (";" + ZEBRA if i % 2 == 0 else "")
        rows.append(
            '<tr><td style="%s"><p style="%s"><span style="%s">%s%s</span></p></td>'
            '<td style="%s"><p style="%s"><span style="%s">%s</span></p></td></tr>'
            % (cell, LINE_H, CN_STYLE, num, esc(cn),
               cell, LINE_H, EN_NONE_STYLE if blank else EN_STYLE, esc(en))
        )
    return '<table style="width:100%">' + hdr + "".join(rows) + "</table>"


def legacy_html(item):
    """兼容旧格式（整段中文 + 整段英文，非表格）。无译文时同样降级为「/」。"""
    en, blank = en_cell([item.get("cn", ""), item.get("en", "")])
    return (
        '<p style="%s"><b>中文原文｜</b>%s</p>'
        '<p style="%s"><b>EN｜</b>%s</p>'
    ) % (CN_STYLE, escbr(item.get("cn", "")),
         EN_NONE_STYLE if blank else EN_STYLE, escbr(en))


def tip_lines(item):
    """本块要渲染的中文提示行的列表。

    取值优先级：
      1. 块内**显式** `tip_cn`（字符串或数组；传 "" / false / [] = 明确不要提示）；
      2. 否则若 `kind` 属尺寸类 → 固定提示 `SIZE_TIP`；
      3. 都不是 → 空。
    显式写了 `tip_cn` 就完全以它为准（哪怕块是尺寸块）——方便按单调整措辞。
    """
    if "tip_cn" in item:
        tip = item["tip_cn"]
    elif str(item.get("kind", "")).strip().lower() in SIZE_KINDS:
        tip = SIZE_TIP
    else:
        tip = ""
    if not tip:
        return []
    if isinstance(tip, str):
        tip = tip.split("\n")
    return [str(t).strip() for t in tip if str(t).strip()]


def tip_html(item):
    """中文提示段落：放在**图注之后、表格之前**，读者先看到判读口径再看行。"""
    return "".join('<p style="%s"><b>※ 提示：</b>%s</p>' % (TIP_STYLE, esc(t))
                   for t in tip_lines(item))


def split_size_pairs(item):
    """尺寸板块：「一个格子里塞了多个尺寸」的行拆成一行一个尺寸。

    为什么必须拆：尺寸图上每个数值都靠一条引线指向某个部位，五个数值挤在一行
    时读者分不清哪个数对应哪条线（客户明确反馈「放在一起不直观」）。

    只在**同时满足**以下条件时才拆，否则原样保留（绝不猜）：
      1. 本块 `kind` 属尺寸类，且未写 `"no_split": true`；
      2. 英文栏不是 `/` 之类占位；
      3. 中文栏与英文栏能用**同一个**分隔符（/ ／ | ｜）切成**同样份数**（≥2）；
      4. 切出来的**每一份中文都含一个 mm 数值**。
    Returns: (pairs 列表, 是否发生了拆分)
    """
    pairs = item.get("pairs") or []
    if str(item.get("kind", "")).strip().lower() not in SIZE_KINDS or item.get("no_split"):
        return pairs, False
    out, changed = [], False
    for pair in pairs:
        cn = pair[0] or ""
        en = (pair[1] if len(pair) > 1 else "") or ""
        if en.strip() in NO_COPY_ALIASES:
            out.append(pair)
            continue
        cps = SPLIT_SEP_RE.split(cn)
        eps = SPLIT_SEP_RE.split(en)
        if len(cps) < 2 or len(cps) != len(eps) or not all(DIM_RE.search(x) for x in cps):
            out.append(pair)
            continue
        out.extend([[c.strip(), e.strip()] for c, e in zip(cps, eps)])
        changed = True
    return out, changed


def block_html(item):
    """图片之后插入的 HTML 块：占位段 → 图注 → 中文提示 → 对照表。"""
    body = table_html(item["pairs"]) if item.get("pairs") else legacy_html(item)
    return (
        '<p style="font-size:1pt">&nbsp;</p>'
        '<p style="text-align:center;font-size:9pt;color:#999999">%s</p>%s%s'
    ) % (esc(item["cap"]), tip_html(item), body)


def main(job_path):
    with open(job_path, "r", encoding="utf-8") as f:
        job = json.load(f)

    root = job["image_root"]
    blocks = job["blocks"]
    out = job["out"]

    # ---- 尺寸块拆行：一个尺寸一行（挤在一行不直观，客户明确要求分行）----
    # 必须在统计句对数**之前**做，否则 STAT 与 verify_docx 的期望值会对不上。
    for i, item in enumerate(blocks, 1):
        new_pairs, changed = split_size_pairs(item)
        if changed:
            print("[INFO] 块 %02d 尺寸块自动拆行：%d → %d 行（一个尺寸一行）"
                  % (i, len(item.get("pairs") or []), len(new_pairs)), flush=True)
            item["pairs"] = new_pairs

    n_pairs = sum(len(b.get("pairs") or [[b.get("cn", ""), b.get("en", "")]]) for b in blocks)
    n_blank = 0
    for b in blocks:
        pairs = b.get("pairs")
        if pairs:
            n_blank += sum(1 for p in pairs if en_cell(p)[1])
        elif en_cell([b.get("cn", ""), b.get("en", "")])[1]:
            n_blank += 1

    # ---- 颜色口径闸门：同名多译色（如砂岩黑）判定不了就停下来问用户，绝不猜 ----
    # 规则：材质里只有金属、无布 → Matte Black；材质含亚麻/布艺 → 由用户确定。
    resolved, questions = C.check(job)
    if questions:
        print("[STOP] 颜色口径需先与用户确认，已中止生成（尚未创建文档）：", flush=True)
        for q in questions:
            print("  [ASK] " + q, flush=True)
        raise SystemExit(2)
    for w in C.consistency_warnings(job, resolved):
        print("[WARN] " + w, flush=True)

    # ---- 固定文案口径闸门（客户指定译法，优先于一切通用术语）----
    # 命中第〇节固定文案表就须逐字照抄；有违禁变体（Carbon Steel / Backplate / 单写 Shade …）
    # 一律中止生成 —— 别把口径错的文档交付出去。确需跳过：加 --no-glossary-gate
    if "--no-glossary-gate" not in sys.argv:
        gr = G.scan(job_path)
        for w in gr["warns"]:
            print("[WARN] " + w, flush=True)
        if gr["fails"]:
            print("[STOP] 固定文案口径不一致，已中止生成（尚未创建文档）：", flush=True)
            for x in gr["fails"]:
                print("  [FAIL] " + x, flush=True)
            print("  改好 job.json 后重跑；确要跳过本闸门加 --no-glossary-gate", flush=True)
            raise SystemExit(2)
        print("[OK] 固定文案口径一致（命中固定文案 %d 项）" % len(gr["oks"]), flush=True)

    fid = S.create_doc()
    print("[OK] create_doc ->", fid, flush=True)
    S.set_margins(fid)
    print("[OK] margins 42.5pt / 45pt", flush=True)

    pos = S.insert_html(fid, 0, build_title_html(job))
    print("[OK] title block, pos =", pos, flush=True)

    for i, item in enumerate(blocks, 1):
        img_path = os.path.join(root, item["img"].replace("/", os.sep))
        if not os.path.exists(img_path):
            raise RuntimeError("missing image: " + img_path)
        pos = S.insert_image(fid, pos, img_path, IMG_W)
        pos = S.insert_html(fid, pos, block_html(item))
        print("[%02d/%d] %s -> pos=%s" % (i, len(blocks), os.path.basename(item["img"]), pos),
              flush=True)

    # ---- 后处理：表格布局 / 分页保护 / 图片居中 ----
    try:
        n_tab = S.style_tables(fid, COL_W)
        print("[OK] tables styled = %d / %d" % (n_tab, len(blocks)), flush=True)
    except Exception as ex:
        print("[WARN] 表格布局失败（不影响内容）：%s" % str(ex)[:200], flush=True)
    try:
        struct = S.resolve_structure(fid)
        n1 = S.apply_keep_with_next(fid, struct)
        n2 = S.center_image_paragraphs(fid, struct)
        print("[OK] keep_with_next=%d (期望 %d)  centered_images=%d" % (n1, len(blocks) * 2, n2),
              flush=True)
    except Exception as ex:
        print("[WARN] 排版后处理失败（不影响内容）：%s" % str(ex)[:200], flush=True)

    # 原路径若被预览进程占用，另存后再用「重命名绕过」覆盖回去
    try:
        S.save(fid, out)
    except Exception as ex:
        print("[WARN] 直接保存失败，另存后覆盖：%s" % str(ex)[:160], flush=True)
        tmp_out = os.path.splitext(out)[0] + ".tmp.docx"
        S.save(fid, tmp_out)
        S.safe_overwrite(tmp_out, out)

    print("[OK] saved ->", out, flush=True)
    print("[STAT] blocks=%d pairs=%d no_copy(/)%d tips=%d"
          % (len(blocks), n_pairs, n_blank, sum(len(tip_lines(b)) for b in blocks)),
          flush=True)
    print("FILE_ID=" + fid, flush=True)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit("usage: python build_bilingual_doc.py job.json")
    main(sys.argv[1])
