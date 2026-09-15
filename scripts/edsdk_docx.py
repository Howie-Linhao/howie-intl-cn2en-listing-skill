# -*- coding: utf-8 -*-
"""
editor_sdk 调用封装（tencent-local-office-edit 通道）。

把本文件与 build_bilingual_doc.py 放在同一目录即可 import。
核心价值：把该 SDK 的几个"坑"（返回纯文本 vs JSON、批量段落参数、
文件被预览进程占用）都收敛在这里，业务脚本只关心数据。
"""
import glob
import json
import os
import re
import shutil
import subprocess
import sys

# ---- 环境：两处路径自动探测，换机器不用改代码 ----
# 也可用环境变量强制指定：
#   TENCENT_LOCAL_OFFICE_DIR = ...\skills\tencent-local-office-edit
#   EDS_PYTHON               = ...\python.exe
SKILL_SUBDIR = os.path.join("resources", "app.asar.unpacked", "resources",
                            "plugins", "workbuddy-builtin", "skills",
                            "tencent-local-office-edit")


def _find_skill_dir():
    """定位 tencent-local-office-edit（editor_sdk 所在插件目录）。

    cands 里存的都是 **WorkBuddy 安装根目录**，再统一拼上 SKILL_SUBDIR，
    这样显式候选与 glob 候选能共用同一套校验。
    """
    for env in ("TENCENT_LOCAL_OFFICE_DIR", "EDS_SKILL_DIR"):
        p = os.environ.get(env)
        if p and os.path.exists(os.path.join(p, "edsdk.py")):
            return p.replace("\\", "/")
    roots = [
        "D:/workbuddy", "C:/workbuddy",
        "C:/Program Files/WorkBuddy", "C:/Program Files (x86)/WorkBuddy",
        os.path.expanduser("~/AppData/Local/Programs/WorkBuddy"),
        os.path.expanduser("~/AppData/Local/WorkBuddy"),
    ]
    # 各盘符 1-2 层内的 WorkBuddy 安装目录（浅层 glob，很快）
    for drive in "CDEFGH":
        for pat in ("%s:/*/workbuddy" % drive, "%s:/*/WorkBuddy" % drive,
                    "%s:/*/*/WorkBuddy" % drive, "%s:/*/*/workbuddy" % drive):
            roots.extend(glob.glob(pat))
    for root in roots:
        full = os.path.join(root, SKILL_SUBDIR)
        if os.path.exists(os.path.join(full, "edsdk.py")):
            return full.replace("\\", "/")
    raise RuntimeError(
        "找不到 tencent-local-office-edit 插件目录（editor_sdk）。\n"
        "请在 WorkBuddy 里确认该内置插件可用，或设置环境变量 "
        "TENCENT_LOCAL_OFFICE_DIR 指向 plugins/workbuddy-builtin/skills/"
        "tencent-local-office-edit")


def _find_python():
    """定位带 editor_sdk 运行依赖的解释器：优先 WorkBuddy 托管 Python。"""
    for env in ("EDS_PYTHON", "WORKBUDDY_PYTHON"):
        p = os.environ.get(env)
        if p and os.path.exists(p):
            return p
    home = os.path.expanduser("~")
    pats = [
        os.path.join(home, ".workbuddy", "binaries", "python", "versions", "*", "python.exe"),
        os.path.join(home, ".workbuddy", "binaries", "python", "envs", "default", "Scripts", "python.exe"),
    ]
    found = []
    for pat in pats:
        found.extend(glob.glob(pat))
    if found:
        # 版本号大的优先
        def key(p):
            m = re.search(r"(\d+)\.(\d+)\.(\d+)", p)
            return tuple(int(x) for x in m.groups()) if m else (0, 0, 0)
        return sorted(found, key=key)[-1]
    for name in ("python", "python3"):
        p = shutil.which(name)
        if p:
            return p
    return sys.executable


SKILL_DIR = _find_skill_dir()
PYEXE = _find_python()


def _run(args):
    return subprocess.run(
        args, cwd=SKILL_DIR, capture_output=True, text=True,
        encoding="utf-8", errors="replace",
    )


def call(tool, params=None):
    """调用 edsdk 工具并把结果规整成 dict。

    SDK 的返回有两种形态：JSON 单行，或**纯文本描述**（如 save_file 成功时
    返回 'File saved to: ...'、create_doc 返回 'Created blank doc ... file_id=xxx'）。
    这里统一容错：JSON 优先，否则包成 {'_raw': text}。
    """
    r = _run([PYEXE, "edsdk.py", "call", tool, "--json",
              json.dumps(params or {}, ensure_ascii=False)])
    out = r.stdout or ""
    for line in reversed(out.strip().splitlines()):
        line = line.strip()
        if line.startswith("{"):
            try:
                d = json.loads(line)
            except Exception:
                continue
            if d.get("ok") is False:
                raise RuntimeError("%s -> %s" % (tool, d.get("error")))
            return d
    if out.strip() and r.returncode == 0:
        return {"_raw": out.strip()}
    raise RuntimeError("CALL FAILED %s\nSTDOUT:%s\nSTDERR:%s" % (tool, out, r.stderr))


def call_raw(tool, params=None):
    """拿原始 stdout 文本（解析字段不确定时用）。"""
    r = _run([PYEXE, "edsdk.py", "call", tool, "--json",
              json.dumps(params or {}, ensure_ascii=False)])
    if r.returncode != 0:
        raise RuntimeError("CALL FAILED %s\nSTDOUT:%s\nSTDERR:%s" % (tool, r.stdout, r.stderr))
    return (r.stdout or "").strip()


# ---------------- 常用动作 ----------------

def create_doc():
    """新建空白文档，返回 file_id。注意：SDK 返回的是纯文本，必须正则提。"""
    raw = call_raw("create_doc", {})
    m = re.search(r"file_id=([^,\s]+)", raw)
    if not m:
        raise RuntimeError("cannot parse create_doc output: " + raw)
    return m.group(1)


def set_margins(fid, left=42.5, right=42.5, top=45.0, bottom=45.0, section_index=0):
    """42.5pt ≈ 1.5cm，45pt ≈ 1.59cm。"""
    return call("doc_modify_section", {
        "file_id": fid, "section_index": section_index,
        "left_margin": left, "right_margin": right,
        "top_margin": top, "bottom_margin": bottom,
    })


def insert_html(fid, idx, html_text):
    """插入富文本块，返回新的 position（作为下一步 idx）。"""
    return call("doc_insert_html_content",
                {"file_id": fid, "idx": idx, "html_text": html_text})["position"]


def insert_image(fid, idx, image_path, w=540):
    """插图。idx 不能为负；文档开头用 0。返回新 position。"""
    return call("doc_insert_image",
                {"file_id": fid, "idx": idx,
                 "image_path": image_path.replace("\\", "/"), "w": w})["position"]


def save(fid, file_path):
    """保存到指定路径。原路径被预览进程占用时会报 Export file is occupied，
    此时传一个新路径另存，再用 safe_overwrite() 覆盖回正式文件名。"""
    return call("save_file", {"file_id": fid, "file_path": file_path.replace("\\", "/")})


def resolve_structure(fid):
    return call("doc_resolve_document_structure", {"file_id": fid})


def nodes_of(resp):
    for k in ("nodes", "structure", "paragraphs", "items"):
        v = resp.get(k)
        if isinstance(v, list):
            return v
    return []


def paragraphs_of(resp):
    return [n for n in nodes_of(resp)
            if str(n.get("type", "")).lower()
            in ("paragraph", "heading", "title", "subtitle")]


def text_preview(p):
    """结构树节点的文本字段是 text_preview（不是 text），且会被截断。"""
    return (p.get("text_preview") or p.get("text") or "").strip()


def _batch_modify(fid, paras, ranges, **attrs):
    """ranges 批量传（10-12 个/批稳定），失败再退回 paragraph_id 逐段。"""
    done = 0
    BATCH = 10
    for k in range(0, len(ranges), BATCH):
        chunk = ranges[k:k + BATCH]
        try:
            call("doc_modify_paragraph",
                 dict({"file_id": fid, "ranges": chunk}, **attrs))
            done += len(chunk)
        except Exception as ex:
            print("[WARN] ranges 批量失败，改逐段：%s" % str(ex)[:120])
            for r in chunk:
                pid = next((p.get("paragraph_id") for p in paras
                            if p.get("start_index") == r["begin"]), None)
                if not pid:
                    continue
                try:
                    call("doc_modify_paragraph",
                         dict({"file_id": fid, "paragraph_id": pid}, **attrs))
                    done += 1
                except Exception as ex2:
                    print("[WARN] 段落 %s 失败：%s" % (pid, str(ex2)[:80]))
    return done


def apply_keep_with_next(fid, struct, cap_prefix="图 "):
    """让每组「图片 → 图注」与紧随其后的对照表保持同页，避免被分页拆散。

    定位方式：图注段以 cap_prefix 开头；它的**前一段**是图片段。
    只给「图片段 + 图注段」设 keep_with_next（2 段/组）：图注段设了 keepNext 后，
    它会与**后面的表格**绑定同页；表格内段落拿不到段落属性，不设。
    自检：xml.count('<w:keepNext') ≈ 组数 × 2。
    """
    paras = paragraphs_of(struct)
    if not paras:
        print("[WARN] 结构树无段落节点，跳过分页保护")
        return 0
    ranges = []
    for i, p in enumerate(paras):
        if text_preview(p).startswith(cap_prefix) and i >= 1:
            for j in (i - 1, i):
                q = paras[j]
                b, e = q.get("start_index"), q.get("end_index")
                if isinstance(b, int) and isinstance(e, int):
                    ranges.append({"begin": b, "end": e})
    if not ranges:
        print("[WARN] 未定位到图注段落，跳过分页保护")
        return 0
    return _batch_modify(fid, paras, ranges, keep_with_next=True)


def center_image_paragraphs(fid, struct):
    """把承载图片的段落设为居中。

    ⚠️ 用了 1pt 占位段方案后，图片段不再继承 text-align:center（原来靠被并入的
    首个 <p> 带过来），必须显式补一次。
    """
    paras = paragraphs_of(struct)
    ranges = []
    for p in paras:
        prev = text_preview(p)
        # 图片段的 preview 形如 "[Image]图 06 · ..."（会被截断）
        if prev.startswith("[Image]") or (p.get("has_image") is True):
            b, e = p.get("start_index"), p.get("end_index")
            if isinstance(b, int) and isinstance(e, int):
                ranges.append({"begin": b, "end": e})
    if not ranges:
        print("[WARN] 未从结构树识别到图片段，改用 XML 兜底（见 verify_docx）")
        return 0
    return _batch_modify(fid, paras, ranges, jc="center")


def list_tables(fid):
    """列出文档内所有表格（含 8 字符 table_id、行列数）。"""
    r = call("doc_list_tables", {"file_id": fid})
    return r.get("tables") or r.get("items") or []


def set_row_lines(fid, table_id, row_count, col_count,
                  color="E8E8E8", size=4, skip_last=True):
    """给每一行的单元格补下边框（= 行分隔线）。

    ⚠️ 实测：`doc_set_table_properties` 会把 `<td style="border-bottom">` 插入时生成的
    `tcBorders` **全部清掉**，必须在它之后用本函数补回来，否则整张表只剩外框、
    行与行之间没有分隔线，句对边界反而糊掉。
    最后一行的下边框由表格自身 bottom 提供，跳过以免重复。
    """
    prop = {"borders": {"bottom": {"style": "single", "size": size, "color": color}}}
    last = row_count - 1 if skip_last else row_count
    cells = [{"row": r, "col": c, "property": prop}
             for r in range(1, last + 1) for c in range(1, col_count + 1)]
    if not cells:
        return None
    return call("doc_set_table_cells",
                {"file_id": fid, "table_id": table_id, "cells": cells})


def style_tables(fid, col_widths_dxa=(4400, 5800), border_color="E8E8E8",
                 border_size=4, alignment="center",
                 cell_margin=(60, 60, 113, 113)):
    """统一中英对照表的布局：列宽、居中、外框浅灰、行内边距、逐行下边框。

    ⚠️ 实测：
      - 列宽必须走本工具（`mode=manual` + `col_widths_dxa`），HTML 的
        `style="width:47%"` 不生效（列宽恒等分）。
      - 只支持 6 向中的 outer 4 向改色；`insideH/insideV` 改不动（保持默认
        CBCDD1 浅灰，正好当两列的竖直分隔线，不必管）。
      - 本调用会清掉 tcBorders，所以**顺序必须是**：先 set_table_properties，
        再 set_row_lines 补回行线。
      - `cell_margin` 是「句与句之间留白」的主要手段（表格级 tblCellMar，
        1 dxa = 1/20 pt）。默认 (top 60, bottom 60, left 113, right 113)
        = 上下各 3pt、左右各 5.65pt；调大它 = 行与行更透气。
    Args:
        cell_margin: (top, bottom, left, right)，dxa 单位。
    Returns: 成功设置的表格数。
    """
    tabs = list_tables(fid)
    bd = {k: {"style": "single", "size": border_size, "color": border_color}
          for k in ("top", "bottom", "left", "right")}
    cm = {"top": cell_margin[0], "bottom": cell_margin[1],
          "left": cell_margin[2], "right": cell_margin[3]}
    done = 0
    for t in tabs:
        tid = t.get("table_id")
        if not tid or str(tid).startswith("tbl:"):
            continue
        ncol, nrow = t.get("col_count"), t.get("row_count")
        if isinstance(ncol, int) and ncol != len(col_widths_dxa):
            print("[WARN] 表格 %s 列数 %s ≠ %d，跳过列宽设置" % (tid, ncol, len(col_widths_dxa)))
            continue
        try:
            call("doc_set_table_properties", {
                "file_id": fid, "table_id": tid, "mode": "manual",
                "col_widths_dxa": list(col_widths_dxa), "alignment": alignment,
                "borders": bd, "cell_margin": cm,
            })
            set_row_lines(fid, tid, nrow or 0, ncol or 2,
                          color=border_color, size=border_size)
            done += 1
        except Exception as ex:
            print("[WARN] 表格 %s 布局失败：%s" % (tid, str(ex)[:120]))
    return done


def open_file(file_path):
    """隔轮再编辑时实例已失效，用它重开。返回的 file_id 就是路径字符串本身。"""
    return call("open_file", {"file_path": file_path.replace("\\", "/")})


def safe_overwrite(src, dst):
    """覆盖一个被预览进程占用的文件。

    该锁「允许重命名、不允许写入」，所以不能 cp/copyfile。
    步骤：mv dst -> _tmp；mv src -> dst；rm _tmp。
    """
    tmp = dst + ".old-tmp"
    if os.path.exists(tmp):
        os.remove(tmp)
    os.replace(dst, tmp)
    os.replace(src, dst)
    os.remove(tmp)
    return dst
