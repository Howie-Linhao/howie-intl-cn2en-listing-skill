# -*- coding: utf-8 -*-
"""颜色口径校验：处理色卡里「一个中文名对应两个色号」的同名多译色。

规则（品牌强制，权威定义见 references/translation-playbook.md 第 7.1 节）：

    砂岩黑  ——  材质里只有金属、没有布  →  Matte Black（自动取值）
                材质里含亚麻 / 布艺     →  由用户确定（本模块返回待确认问题）
    中国红  ——  尚未裁定，一律问用户

设计意图：**判定不了就不要猜**。宁可停在中途让 Agent 去问用户，
也不要用一个可能错的色号铺满整份 Listing —— 色号错了等于给买家看错了颜色。

用法：
    import color_caliber as C
    resolved, questions = C.check(job)
    if questions:      # 非空 = 必须先问用户，不得继续生成
        ...
"""
import re

# 同名多译色：候选英文 + 「材质无布」时的自动取值（None 表示未裁定，永远问用户）
AMBIGUOUS = {
    "砂岩黑": {
        "candidates": ("Matte Black", "Linen black"),
        # 「砂岩黑」既是『哑黑（金属件喷砂黑）』的中文名，也是『亚麻黑（亚麻布染色）』的中文名
        "no_fabric": "Matte Black",
        "fabric_hint": "Linen black",
        "why": "同一中文名对应两个色号：金属哑黑 / 亚麻布染黑",
    },
    "中国红": {
        "candidates": ("Matte red", "Red"),
        "no_fabric": None,          # 未裁定：无论材质如何都先问用户
        "fabric_hint": "Red",
        "why": "同一中文名对应两个色号：哑光红 / 正红（尚未裁定）",
    },
}

# 出现任一关键词即视为「材质里有布」。中英并查，大小写不敏感。
FABRIC_WORDS = ("布", "亚麻", "织物", "棉麻", "绒", "linen", "fabric",
                "textile", "cloth", "canvas")


def _cells(block):
    """展开一块里的所有文案（pairs 格式或旧格式）。"""
    out = []
    if block.get("cap"):
        out.append(str(block["cap"]))
    for key in ("cn", "en"):
        if block.get(key):
            out.append(str(block[key]))
    for pair in (block.get("pairs") or []):
        for cell in list(pair)[:2]:
            if cell:
                out.append(str(cell))
    return out


def collect_text(job, include_notes=True):
    """把作业里所有可能含色名的文案拼起来（用于判断本型号用到了哪些色名）。

    include_notes=False 时**跳过文首「注」** —— 材质判定必须只看正文（listing 实际
    内容），否则一句「若材质含亚麻布则取 Linen black」的口径说明会把所有产品都判成
    「有布」。
    """
    chunks = []
    for key in ("title_cn", "title_en", "brand", "target_lang", "platforms"):
        if job.get(key):
            chunks.append(str(job[key]))
    if include_notes:
        chunks.extend(str(n) for n in (job.get("notes") or []))
    for block in (job.get("blocks") or []):
        chunks.extend(_cells(block))
    return "\n".join(chunks)


def material_text(job):
    """产品材质：以 job['material'] 为准，其次从**正文**的「材质 / MATERIAL」行抓取。

    材质是判定同名多译色的**唯一依据**：
      - 显式提供了 job['material'] → 直接采用（优先级最高，不再混入文案，避免噪声）；
      - 否则只扫正文里的材质参数行（如 `MATERIAL　材质：玻璃、碳素钢`），
        **不扫文首「注」**，也不用「口径」类说明行。
    """
    raw = job.get("material")
    if isinstance(raw, str) and raw.strip():
        return raw.strip()
    if isinstance(raw, (list, tuple)) and raw:
        return " ;; ".join(str(x) for x in raw)

    parts = []
    for line in collect_text(job, include_notes=False).split("\n"):
        if not re.search(r"材质|material", line, re.I):
            continue
        if "口径" in line or "统一译" in line:      # 说明性文字，不是产品参数
            continue
        parts.append(line)
    return " ;; ".join(parts)


def has_fabric(text):
    """返回命中的布类关键词；None 表示材质里没有布。"""
    low = text.lower()
    for word in FABRIC_WORDS:
        if word.lower() in low:
            return word
    return None


def check(job, verbose=True):
    """校验作业里的颜色口径。

    Returns: (resolved, questions)
        resolved  —— {中文色名: 应使用的英文}，可直接使用（无布时的自动取值）
        questions —— 待用户确认的问题文本列表；**非空即表示不得继续生成**
    """
    text = collect_text(job)
    hit = [cn for cn in AMBIGUOUS if cn in text]
    if not hit:
        return {}, []

    material = material_text(job)
    material_known = bool(material.strip())
    fabric = has_fabric(material) if material_known else None
    if verbose:
        print("[COLOR] 命中同名多译色：%s" % "、".join(hit), flush=True)
        print("[COLOR] 材质依据：%s" % (material or "（未找到材质信息）"), flush=True)
        print("[COLOR] 材质里有布：%s" % (fabric or ("否" if material_known else "未知")), flush=True)

    resolved, questions = {}, []
    for cn in hit:
        spec = AMBIGUOUS[cn]
        a, b = spec["candidates"]
        # 只有「材质明确、且没有布」才允许自动取金属色号；材质缺失一律问用户。
        # 宁可多问一句，也不要把 Matte Black 铺到一个其实是亚麻布的产品上。
        if spec["no_fabric"] and material_known and not fabric:
            resolved[cn] = spec["no_fabric"]
            if verbose:
                print("[COLOR] %s → %s（材质只有金属、无布，自动取值）" % (cn, spec["no_fabric"]),
                      flush=True)
            continue

        if not material_known:
            reason = "产品材质信息缺失，无法按材质判定"
        elif fabric:
            reason = "材质里检出布类材质（命中「%s」）" % fabric
        else:
            reason = "该色号尚未裁定（%s）" % spec["why"]
        questions.append(
            "「%s」取哪个色号？%s。\n"
            "      候选：%s / %s\n"
            "      材质依据：%s\n"
            "      原因：%s"
            % (cn, reason, a, b, material or "（未提供）", spec["why"]))

    return resolved, questions


def consistency_warnings(job, resolved):
    """轻量自检：自动取值后，正文里不应再出现被否掉的那个候选英文。"""
    warns = []
    text = collect_text(job)
    for cn, chosen in resolved.items():
        for other in AMBIGUOUS[cn]["candidates"]:
            if other != chosen and other in text:
                warns.append("「%s」已按材质判定为 %s，但文案里仍出现 %s，请核对"
                             % (cn, chosen, other))
    return warns


if __name__ == "__main__":
    import json
    import sys
    with open(sys.argv[1], "r", encoding="utf-8") as f:
        _job = json.load(f)
    _resolved, _questions = check(_job)
    for _w in consistency_warnings(_job, _resolved):
        print("[WARN]", _w)
    for _q in _questions:
        print("[ASK]", _q)
    print("[RESULT] resolved=%s questions=%d" % (_resolved, len(_questions)))
