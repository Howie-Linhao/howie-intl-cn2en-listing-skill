# -*- coding: utf-8 -*-
"""
国际站速卖通中转英 · 一键安装器

用法（三种都行，任选其一）：

    python 安装.py                     # 在解压后的包里运行，自动找到 intl-cn2en-listing 装进去
    python 安装.py 某技能包.zip        # 直接把 zip 丢进来（自动解压 + 安装）
    python 安装.py --check             # 只体检，不写任何文件

做的事情：装到 WorkBuddy 技能目录 → 自动补装 Pillow → 校验 9 个文件齐不齐 → 打印结果。
不需要手工选目录、不需要手工解压、不需要改任何路径。
"""
import argparse
import os
import shutil
import subprocess
import sys
import tempfile
import zipfile

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

SKILL_NAME = "intl-cn2en-listing"
NEEDED = [
    "SKILL.md",
    "references/translation-playbook.md",
    "scripts/build_bilingual_doc.py",
    "scripts/color_caliber.py",
    "scripts/glossary_check.py",
    "scripts/edsdk_docx.py",
    "scripts/slice_long_images.py",
    "scripts/verify_docx.py",
    "scripts/job.example.json",
]
IGNORE = shutil.ignore_patterns("__pycache__", "*.pyc", ".git", ".DS_Store", "Thumbs.db")


# ---------------- 定位 ----------------

def find_skills_dir():
    """按 WorkBuddy 约定定位技能目录，不存在就创建。"""
    envs = [os.environ.get("WORKBUDDY_SKILLS_DIR")]
    cfg = os.environ.get("WORKBUDDY_CONFIG_DIR") or os.environ.get("CODEBUDDY_CONFIG_DIR")
    if cfg:
        envs.append(os.path.join(cfg, "skills"))
    home = os.path.expanduser("~")
    envs.append(os.path.join(home, ".workbuddy", "skills"))
    envs.append(os.path.join(home, ".codebuddy", "skills"))
    for d in envs:
        if not d:
            continue
        try:
            os.makedirs(d, exist_ok=True)
            return d
        except Exception:
            continue
    d = os.path.join(home, ".workbuddy", "skills")
    os.makedirs(d, exist_ok=True)
    return d


def find_source(explicit=None, here=None):
    """找技能源目录：显式路径 > 当前目录 > 当前目录下的同名文件夹 > 上一层。"""
    here = here or os.path.dirname(os.path.abspath(__file__))
    cands = []
    if explicit:
        cands.append(os.path.abspath(explicit))
    cands += [
        here,
        os.path.join(here, SKILL_NAME),
        os.path.dirname(here),
    ]
    for c in cands:
        if os.path.isfile(os.path.join(c, "SKILL.md")):
            return c
    return None


def unpack(zip_path):
    """把 zip 解到临时目录，返回（技能源目录, 临时目录）。"""
    tmp = tempfile.mkdtemp(prefix="intl-cn2en-")
    with zipfile.ZipFile(zip_path) as z:
        z.extractall(tmp)
    for root, dirs, files in os.walk(tmp):
        if "SKILL.md" in files:
            return root, tmp
    raise SystemExit("[x] 这个 zip 里没找到 SKILL.md，可能传错了包")


# ---------------- 动作 ----------------

def ensure_pillow():
    """Pillow 只给长图切分用，能装上就装上，装不上不影响其余功能。"""
    try:
        import PIL  # noqa: F401
        return "已有 %s" % getattr(PIL, "__version__", "?")
    except ImportError:
        pass
    print("[*] 正在补装 Pillow（长图自动切分用）...", flush=True)
    subprocess.run([sys.executable, "-m", "pip", "install", "--quiet",
                    "--disable-pip-version-check", "pillow"], check=False)
    try:
        import PIL  # noqa: F401
        return "已装好 %s" % getattr(PIL, "__version__", "?")
    except ImportError:
        return "未装上（不影响主流程，只在切长图时会用到）"


def verify(dst):
    missing = [rel for rel in NEEDED if not os.path.isfile(os.path.join(dst, rel))]
    if missing:
        print("[!] 少了这些文件，技能会跑不起来：")
        for m in missing:
            print("    -", m)
    else:
        print("[ok] %d 个核心文件齐全（主流程 + %d 个脚本 + 翻译手册 + 作业示例）"
              % (len(NEEDED), len(NEEDED) - 3))
    return not missing


def main():
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("package", nargs="?", help="技能包 zip 路径（可选）")
    ap.add_argument("--src", help="直接指定技能目录（可选）")
    ap.add_argument("--check", action="store_true", help="只体检，不安装")
    args = ap.parse_args()

    tmp = None
    try:
        if args.package and os.path.isfile(args.package):
            src, tmp = unpack(args.package)
            print("[*] 已解压技能包：%s" % os.path.basename(args.package))
        else:
            src = find_source(args.src)
        if not src:
            raise SystemExit("[x] 没找到 intl-cn2en-listing（要找含 SKILL.md 的那一层）。"
                             "把 安装.py 和 intl-cn2en-listing 放在一起再运行，或直接：python 安装.py 技能包.zip")

        skills_dir = find_skills_dir()
        dst = os.path.join(skills_dir, SKILL_NAME)
        exists = os.path.isdir(dst)

        print("源目录   : %s" % src)
        print("技能目录 : %s" % skills_dir)
        print("安装为   : %s  %s" % (dst, "(已存在，将覆盖更新)" if exists else "(新建)"))

        same = os.path.normcase(os.path.abspath(src)) == os.path.normcase(os.path.abspath(dst))
        if same:
            print("\n[i] 源目录和目标就是同一个位置，无需安装（已就地可用）。")
            print("[ok] Pillow：%s" % ensure_pillow())
            ok = verify(dst)
            if not ok:
                sys.exit(2)
            return

        if args.check:
            print("\n[check] 只体检，未写入任何文件。")
            check_tmp = tempfile.mkdtemp(prefix="intl-cn2en-chk-")
            probe = os.path.join(check_tmp, SKILL_NAME)
            shutil.copytree(src, probe, ignore=IGNORE)
            verify(probe)
            shutil.rmtree(check_tmp, ignore_errors=True)
            return

        shutil.copytree(src, dst, dirs_exist_ok=True, ignore=IGNORE)
        print("[ok] 文件已就位")
        print("[ok] Pillow：%s" % ensure_pillow())
        ok = verify(dst)

        print("\n" + "=" * 60)
        if ok:
            print("装好了。重开一个对话，直接说：")
            print("  用国际站速卖通中转英，把这个产品的详情页翻一下，图片在 <目录>")
            print("=" * 60)
        else:
            sys.exit(2)
    finally:
        if tmp:
            shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
