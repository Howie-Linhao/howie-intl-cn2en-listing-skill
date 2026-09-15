# -*- coding: utf-8 -*-
"""
长图切分：把长图按图内自然空白带切成若干段，
使每段图片下方可以紧跟对应文案，便于中英逐句比对。

两种用法
--------
1) 自动模式（推荐；用户只给**一张多图整合的长图**时用这个）
   PYTHONIOENCODING=utf-8 python slice_long_images.py --src <长图路径> [--dst DIR] [--prefix P]
   脚本自动找空白带 → 切成 MAX_SEG 段以内 → 丢掉纯空段 → 输出切片 + 校验条带。

2) 指定模式（用户已给编号图，只想切其中几张时用）
   写一份 plan.json：{"prefix":"BD111","images":[{"match":"06","cands":[865],"bottom":null}]}
   PYTHONIOENCODING=utf-8 python slice_long_images.py --src <目录> --plan plan.json

⚠️ 无论哪种模式，都必须 Read 一遍校验条带（_cutcheck/cut_check.jpg）确认红线两侧是真空白：
   10 列采样会漏掉 1-2px 的水平细线，典型翻车是把切点切在按钮/输入框边框上。
"""
import argparse
import json
import os
import sys

try:
    from PIL import Image, ImageDraw
except ImportError:
    # 首次运行自动补装，避免整套流程被一个依赖卡住（装到当前解释器，不动全局环境）
    import subprocess
    print("[deps] 缺少 Pillow，正在自动安装 ...", flush=True)
    subprocess.run([sys.executable, "-m", "pip", "install", "--quiet", "--disable-pip-version-check", "pillow"],
                   check=False)
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        sys.exit("[deps] Pillow 自动安装失败，请手动执行：%s -m pip install pillow" % sys.executable)

Image.MAX_IMAGE_PIXELS = None

SPREAD_MAX = 12     # 视为「空白行」的列间极差阈值（灰度 0-255）
SPAN = 45           # 指定模式下候选点吸附搜索半径
MIN_GAP = 10        # 空白带最小高度，低于此不算分隔带
STRIP = 130         # 校验条带上下各取多少像素
MAX_SEG = 6         # 自动模式最多切几段
MIN_SEG_H = 260     # 自动模式单段最小高度，低于此就把切点往后挪
MAX_SEG_H = 1250    # 自动模式单段理想上限，超过就补一刀
INK_MIN = 5.0       # 段内平均行极差低于此视为「纯空白段」，丢弃


# ---------------- 基础工具 ----------------

def row_spread(gray):
    """10 列 BOX 缩放做行特征：每行的列间极差，越小越像空白行。"""
    w, h = gray.size
    sm = gray.resize((10, h), Image.BOX).convert("L")
    px = list(sm.getdata())
    return [max(px[y * 10:(y + 1) * 10]) - min(px[y * 10:(y + 1) * 10])
            for y in range(h)]


def blank_bands(spread, h, min_gap=MIN_GAP):
    """返回所有空白带 [(lo, hi, center, length), ...]（已剔除贴边与过短的）。"""
    bands, y = [], 0
    while y < h:
        if spread[y] < SPREAD_MAX:
            lo = y
            while y < h and spread[y] < SPREAD_MAX:
                y += 1
            hi = y - 1
            if hi - lo + 1 >= min_gap and lo > 2 and hi < h - 3:
                bands.append((lo, hi, (lo + hi) // 2, hi - lo + 1))
        else:
            y += 1
    return bands


def snap(spread, h, cand, span=SPAN):
    """在候选点 ±span 内吸附到空白带中心：优先带宽，再看是否贴近候选点。"""
    best = None
    for y0 in range(max(1, cand - span), min(h - 2, cand + span + 1)):
        lo = y0
        while lo > 0 and spread[lo - 1] < SPREAD_MAX:
            lo -= 1
        hi = y0
        while hi < h - 1 and spread[hi + 1] < SPREAD_MAX:
            hi += 1
        length = hi - lo + 1
        center = (lo + hi) // 2
        score = (min(length, 200), -abs(center - cand))
        if best is None or score > best[0]:
            best = (score, center, lo, hi, length)
    return best


def ink_of(spread, top, bot):
    """段内「内容密度」：平均行极差。极低 = 纯空白段（可直接丢掉）。"""
    seg = spread[top:bot]
    return (sum(seg) / len(seg)) if seg else 0.0


def auto_cuts(spread, h, max_seg_h=MAX_SEG_H, min_seg_h=MIN_SEG_H):
    """自动选切点（用户只给一张多图整合长图时走这条路）。

    策略（顺序不能反，否则会把一张图切得很碎）：
      1) 先取「强分隔带」——宽度 ≥ 其它空白带中位数 2.5 倍的那些带，通常就是多图
         整合长图里面板与面板之间的真实间隔；
      2) 再看还有哪一段仍然超过 max_seg_h，对这些段按等分点吸附补刀；
      3) 任何切点都必须保证两侧段高 ≥ min_seg_h，避免切出碎片。
    """
    bands = blank_bands(spread, h)
    if not bands:
        return []
    widths = sorted(b[3] for b in bands)
    median = widths[len(widths) // 2] if widths else 10
    strong = sorted([b for b in bands if b[3] >= max(median * 2.5, 22)], key=lambda b: b[2])

    cuts = []

    def ok(c):
        return (min_seg_h <= c <= h - min_seg_h
                and all(abs(c - x) >= min_seg_h for x in cuts))

    for b in strong:
        if ok(b[2]):
            cuts.append(b[2])

    for _ in range(8):                       # 逐轮补刀，直到没有过长的段
        bounds = [0] + sorted(cuts) + [h]
        added = False
        for k in range(len(bounds) - 1):
            top, bot = bounds[k], bounds[k + 1]
            if bot - top <= max_seg_h:
                continue
            n = (bot - top + max_seg_h - 1) // max_seg_h
            for j in range(1, n):
                ideal = top + (bot - top) * j / n
                cands = [b for b in bands if ok(b[2])]
                if not cands:
                    continue
                # 越靠近等分点越好；同等距离优先更宽的空白带
                best = min(cands, key=lambda b: abs(b[2] - ideal) - min(b[3], 80) * 1.5)
                cuts.append(best[2])
                added = True
            break
        if not added:
            break

    return sorted(cuts)


# ---------------- 输出 ----------------

def save_sheet(strips, chk_dir, cuts_meta):
    if not strips:
        return None
    sw = max(s.width for s in strips)
    total = sum(s.height + 8 for s in strips)
    sheet = Image.new("RGB", (sw, total), (255, 255, 255))
    yy = 0
    for s in strips:
        sheet.paste(s, (0, yy))
        yy += s.height + 8
    out = os.path.join(chk_dir, "cut_check.jpg")
    sheet.save(out, quality=88)
    return out


def run_single(src, dst, chk, prefix, plan=None):
    """处理一张图。plan 为 None 时走自动模式。"""
    im = Image.open(src).convert("RGB")
    w, h = im.size
    gray = im.convert("L")
    spread = row_spread(gray)
    cuts, bottom = [], None

    if plan:
        for c in plan.get("cands", []):
            r = snap(spread, h, c)
            if r:
                cuts.append(r[1])
        bottom = plan.get("bottom")
        mode = "指定"
    else:
        cuts = auto_cuts(spread, h)
        mode = "自动"
        bands_info = blank_bands(spread, h)
        if bands_info:
            print("  可用空白带（候选切点）:")
            for lo, hi, c, ln in bands_info[:14]:
                print("    y %4d-%4d 宽 %3d  中心 %4d" % (lo, hi, ln, c))
            if len(bands_info) > 14:
                print("    …共 %d 条" % len(bands_info))

    tag = os.path.splitext(os.path.basename(src))[0]
    tag = tag if len(tag) <= 18 else tag[:18]
    print("【%s模式】%s  %dx%d  切点 %s" % (mode, os.path.basename(src), w, h, cuts or "无"))

    # 先看每段的内容密度，丢掉纯空白段
    bands = [0] + list(cuts) + [h]
    keep, dropped = [], []
    for k in range(len(bands) - 1):
        top, bot = bands[k], bands[k + 1]
        ink = ink_of(spread, top, bot)
        if ink < INK_MIN:
            dropped.append((top, bot, ink))
        else:
            keep.append((top, bot, ink))

    strips = []
    if not cuts:
        # 不需要切：整图作为一段输出
        slices = [("整图", 0, h, h)]
        name = "%s_full.jpg" % prefix
        im.save(os.path.join(dst, name), quality=92)
        keep = [(0, h, ink_of(spread, 0, h))]
        slices = [(name, 0, h, h)]
    else:
        slices = []
        letters = "abcdefghijklmn"
        for k, (top, bot, ink) in enumerate(keep):
            sl = im.crop((0, top, w, bot))
            name = "%s_%s_%s.jpg" % (prefix, tag[-2:] if tag[-2:].isdigit() else chr(97 + k), letters[k])
            sl.save(os.path.join(dst, name), quality=92)
            slices.append((name, top, bot, bot - top))
        for c in cuts:
            y1, y2 = max(0, c - STRIP), min(h, c + STRIP)
            strip = im.crop((0, y1, w, y2)).copy()
            d = ImageDraw.Draw(strip)
            d.line([(0, c - y1), (w, c - y1)], fill=(255, 0, 0), width=3)
            d.text((10, 6), "cut y=%d" % c, fill=(255, 0, 0))
            strip.save(os.path.join(chk, "strip_%d.jpg" % c), quality=90)
            strips.append(strip)

    print("  切片（有内容）:")
    for name, top, bot, hh in slices:
        print("    + %-28s y %4d-%4d  高 %4d" % (name, top, bot, hh))
    if dropped:
        print("  已丢弃纯空白段:", ["y%d-%d(ink=%.1f)" % d for d in dropped])
    print("  段数 = %d，校验条带 = %d 条，切点 = %s" % (len(slices), len(strips), cuts or "无"))
    return slices, strips


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True, help="图片目录，或单张长图路径")
    ap.add_argument("--dst", default=None, help="切片输出目录（默认 <src>/slices）")
    ap.add_argument("--prefix", default="P", help="切片文件名前缀（ASCII）")
    ap.add_argument("--plan", default=None, help="指定模式：plan.json 路径")
    args = ap.parse_args()

    src = args.src
    if os.path.isfile(src):
        base = os.path.dirname(os.path.abspath(src))
        dst = args.dst or os.path.join(base, "slices")
        chk = os.path.join(base, "_cutcheck")
        os.makedirs(dst, exist_ok=True)
        os.makedirs(chk, exist_ok=True)
        slices, strips = run_single(src, dst, chk, args.prefix)
        sheet = save_sheet(strips, chk, [])
        if sheet:
            print("\n校验图 ->", sheet, "（必须 Read 一遍再往下做）")
        print("\n下一步：Read 每个切片，只给**含文案**的切片写 pairs，再跑 build_bilingual_doc.py")
        return

    dst = args.dst or os.path.join(src, "slices")
    chk = os.path.join(src, "_cutcheck")
    os.makedirs(dst, exist_ok=True)
    os.makedirs(chk, exist_ok=True)
    plan = json.load(open(args.plan, encoding="utf-8")) if args.plan else None
    all_strips = []
    for f in sorted(os.listdir(src)):
        if not f.lower().endswith((".jpg", ".jpeg", ".png")):
            continue
        if plan:
            m = next((it for it in plan.get("images", [])
                      if str(it.get("match")) in f), None)
            if not m:
                continue
            p = m
        else:
            p = None
        slices, strips = run_single(os.path.join(src, f), dst, chk, args.prefix, p)
        all_strips += strips
    sheet = save_sheet(all_strips, chk, [])
    if sheet:
        print("\n校验图 ->", sheet, "（必须 Read 一遍再往下做）")


if __name__ == "__main__":
    main()
