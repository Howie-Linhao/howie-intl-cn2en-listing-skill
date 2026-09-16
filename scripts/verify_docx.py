# -*- coding: utf-8 -*-
"""
docx 排版/内容校验（不依赖 doc_to_image 渲染服务）。

腾讯云端转换服务对十几张大图的 docx（7MB+）经常报 437009，
所以排版验证一律走本脚本直接解析 word/document.xml。

校验项：
  内容  图片数 = 图注数、句对成对（表格每行两格）、**英文格不得为空**、
        无译文的行必须是「/」、英寸标注齐全
  排版  每表表头行、行分隔线 tcBorders、单元格行距 w:line、
        行内边距 tblCellMar、图片与图注居中、分页保护 keepNext、列宽

用法：PYTHONIOENCODING=utf-8 python verify_docx.py <file.docx> [期望块数] [期望句对数]
"""
import re
import sys
import zipfile

PARA_RE = re.compile(r"<w:p[ >].*?</w:p>", re.S)
TBL_RE = re.compile(r"<w:tbl>.*?</w:tbl>", re.S)
TR_RE = re.compile(r"<w:tr[ >].*?</w:tr>", re.S)
TC_RE = re.compile(r"<w:tc>.*?</w:tc>", re.S)
# ⚠️ 必须写成 <w:t(?:\s[^>]*)?>：否则 <w:tblPr> / <w:tr> 会被当成 <w:t ...> 吃掉后面一大段 XML
TEXT_RE = re.compile(r"<w:t(?:\s[^>]*)?>(.*?)</w:t>", re.S)

NO_COPY = "/"
# 一行里出现 ≥2 个「数字+mm」= 多个尺寸挤在同一行（尺寸板块要求一个尺寸一行）
DIM_RE = re.compile(r"\d+(?:\.\d+)?\s*mm", re.I)
TIPS_MARK = "※ 提示"


def text_of(x):
    return "".join(TEXT_RE.findall(x))


def cell_margin_of(xml):
    m = re.search(r"<w:tblCellMar>(.*?)</w:tblCellMar>", xml, re.S)
    if not m:
        return {}
    return {k: int(v) for k, v in re.findall(r'<w:(\w+) w:w="(\d+)"', m.group(1))}


def shaped(path, expect=None, expect_pairs=None):
    z = zipfile.ZipFile(path)
    xml = z.read("word/document.xml").decode("utf-8")
    paras = PARA_RE.findall(xml)
    tables_xml = TBL_RE.findall(xml)

    imgs = xml.count("<w:drawing")
    keep = xml.count("<w:keepNext")
    rows = len(re.findall(r"<w:tr[ >]", xml))
    tc_borders = xml.count("<w:tcBorders")
    shd = xml.count("<w:shd")
    line_sp = len(re.findall(r'<w:spacing w:line="\d+"', xml))
    grid = [int(x) for x in re.findall(r'<w:gridCol w:w="(\d+)"', xml)]
    cm = cell_margin_of(xml)
    caps = [text_of(p) for p in paras if text_of(p).strip().startswith("图 ")]
    centered_img = sum(1 for p in paras
                       if "<w:drawing" in p and re.search(r'<w:jc w:val="center"', p))
    centered_cap = sum(1 for p in paras
                       if text_of(p).strip().startswith("图 ")
                       and re.search(r'<w:jc w:val="center"', p))
    inches = len(re.findall(r"\((?:Ø)?[0-9.]+in\)", xml))

    # ---- 表格结构逐格分析（表格版） ----
    pairs_n = slash_n = empty_en = miss_cn = dim_multi = 0
    for tbl in tables_xml:
        body = TR_RE.findall(tbl)[1:]          # 跳过表头行
        for r in body:
            tcs = TC_RE.findall(r)
            if len(tcs) < 2:
                continue
            cn_txt, en_txt = text_of(tcs[0]).strip(), text_of(tcs[1]).strip()
            pairs_n += 1
            if en_txt == NO_COPY:
                slash_n += 1
            elif not en_txt:
                empty_en += 1
            if not cn_txt:
                miss_cn += 1
            if len(DIM_RE.findall(cn_txt)) >= 2:
                dim_multi += 1
    # 旧格式（整段中文 + 整段英文）兜底统计
    if not tables_xml:
        cn_rows = xml.count('w:val="777777"')
        en_rows = len(re.findall(r'w:val="14396[Aa]"', xml))
        pairs_n, empty_en = cn_rows, 0
    else:
        cn_rows = en_rows = pairs_n

    print("file        :", path)
    print("images      :", imgs)
    print("captions    :", len(caps))
    print("tables      : %d   rows=%d   tcBorders=%d   shd=%d"
          % (len(tables_xml), rows, tc_borders, shd))
    print("sentence rows: %d   (英文为「/」的行=%d)" % (pairs_n, slash_n))
    print("size rows   : %d   (含 ≥2 个尺寸的行，期望 0)" % dim_multi)
    print("tips        : %d   (中文提示段，尺寸板块须有 1 条)" % xml.count(TIPS_MARK))
    print("keepNext    :", keep, "  (期望 = 块数 × 2)")
    print("centered    : images=%d  captions=%d" % (centered_img, centered_cap))
    print("line spacing: w:line=%d   (期望 ≈ 句对×2 + 表头×2 = %d)"
          % (line_sp, (pairs_n + len(tables_xml)) * 2))
    print("cell margin : %s   (期望 top/bottom ≥ 60dxa 以拉开句距)"
          % (cm or "缺失"))
    print("inch marks  :", inches)
    if grid:
        print("col widths  :", sorted(set(grid)), " 合计=%.1f cm" % (sum(grid[:2]) / 567.0))

    ok = True
    if imgs != len(caps):
        print("[FAIL] 图片数与图注数不一致")
        ok = False
    if empty_en:
        print("[FAIL] 有 %d 个英文格为空（无译文的行必须写「%s」）" % (empty_en, NO_COPY))
        ok = False
    if miss_cn:
        print("[FAIL] 有 %d 个中文格为空" % miss_cn)
        ok = False
    if tables_xml and tc_borders != (rows - len(tables_xml)) * 2:
        print("[WARN] 行分隔线数量异常：tcBorders=%d，期望 (rows-tables)*2=%d（每表末行由外框兜底）"
              % (tc_borders, (rows - len(tables_xml)) * 2))
    if tables_xml and line_sp < pairs_n:
        print("[WARN] 单元格行距缺失：w:line=%d，至少应有 %d（每格一段都要 line-height）"
              % (line_sp, pairs_n))
    if tables_xml and cm.get("top", 0) < 60:
        print("[WARN] 行内边距偏小（tblCellMar top=%s），句与句之间会挤" % cm.get("top"))
    if dim_multi:
        print("[WARN] 有 %d 行把 ≥2 个尺寸塞在同一行 —— 尺寸板块应一个尺寸一行"
              "（挤在一起分不清哪条引线对哪个数）；见手册 4.1" % dim_multi)
    if centered_cap != len(caps):
        print("[FAIL] 有图注未居中")
        ok = False
    if centered_img != imgs:
        print("[WARN] 有图片段未居中（会左对齐显示）")
    if expect is not None:
        if imgs != expect:
            print("[FAIL] 期望 %d 块，实际 %d 块" % (expect, imgs))
            ok = False
        if tables_xml and len(tables_xml) != expect:
            print("[FAIL] 期望 %d 张对照表，实际 %d 张" % (expect, len(tables_xml)))
            ok = False
        if rows != (expect_pairs or 0) + expect:
            print("[WARN] 表格行数 %d ≠ 句对数+表头行 %d"
                  % (rows, (expect_pairs or 0) + expect))
    if expect_pairs is not None and pairs_n != expect_pairs:
        print("[FAIL] 期望 %d 个句对，实际 %d 个" % (expect_pairs, pairs_n))
        ok = False
    if keep < imgs * 2:
        print("[WARN] 分页保护数量偏少（期望 ≈ 块数 × 2），图文可能被分页拆散")
    if not caps:
        print("[WARN] 未找到以「图 」开头的图注段")
    else:
        print("--- captions ---")
        for c in caps:
            print("   ", c[:88])
    print("[%s]" % ("PASS" if ok else "CHECK FAILED"))
    return ok


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit(
            "usage: python verify_docx.py <file.docx> [expect_blocks] [expect_pairs]")
    exp = int(sys.argv[2]) if len(sys.argv) > 2 else None
    exp_p = int(sys.argv[3]) if len(sys.argv) > 3 else None
    sys.exit(0 if shaped(sys.argv[1], exp, exp_p) else 1)
