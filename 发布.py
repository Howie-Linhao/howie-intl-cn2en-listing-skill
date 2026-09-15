# -*- coding: utf-8 -*-
"""
把 howie-intl-cn2en-listing-skill 发布到 GitHub（建仓库 + 推送 + 自检，一条命令搞定）

用法：
    python 发布.py --token <你的PAT>
    python 发布.py --token <PAT> --owner Howie-Linhao --repo howie-intl-cn2en-listing-skill

PAT 领发（fine-grained）：https://github.com/settings/tokens?type=beta
  权限只需要：Repository access = All repositories，Contents = Read and write
  用完请立刻到同一页面 Delete 掉这个 token。

安全说明：
  - token 只用在本次 push 的临时 URL 上，**不会写进 .git/config**；
  - 全程关闭交互式密码提示（GIT_TERMINAL_PROMPT=0），失败就直接报错；
  - 打印时 token 一律打码。
"""
import argparse
import json
import os
import subprocess
import sys
import urllib.error
import urllib.request

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

DEFAULT_OWNER = "Howie-Linhao"
DEFAULT_REPO = "howie-intl-cn2en-listing-skill"
DESC = "国际站速卖通中转英 —— 中文详情页图片文案意译为英文，输出中英逐句对照 Word"


def api(url, method="GET", token=None, payload=None):
    data = json.dumps(payload).encode() if payload else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("User-Agent", "intl-cn2en-publisher")
    if token:
        req.add_header("Authorization", "Bearer " + token)
    if data:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, json.loads(r.read().decode() or "{}")
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        try:
            body = json.loads(body)
        except Exception:
            pass
        return e.code, body
    except Exception as e:
        return 0, {"message": str(e)}


def git(args, cwd):
    env = dict(os.environ, GIT_TERMINAL_PROMPT="0", GIT_ASKPASS="echo")
    p = subprocess.run(["git"] + args, cwd=cwd, env=env,
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return p.returncode, p.stdout.decode("utf-8", "replace").strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--token", default=os.environ.get("GITHUB_TOKEN"))
    ap.add_argument("--owner", default=None, help="GitHub 用户名（默认用 token 自动识别，不用手填）")
    ap.add_argument("--repo", default=DEFAULT_REPO)
    ap.add_argument("--dir", default=None, help="仓库目录（默认：脚本旁的 howie-intl-cn2en-listing-skill）")
    ap.add_argument("--private", action="store_true", help="建私有仓库（默认公开）")
    args = ap.parse_args()

    if not args.dir:
        here = os.path.dirname(os.path.abspath(__file__))
        guess = os.path.join(here, DEFAULT_REPO)
        args.dir = guess if os.path.isfile(os.path.join(guess, "SKILL.md")) else here

    if not args.token:
        sys.exit("[x] 缺 token。用法：python 发布.py --token <你的PAT>\n"
                 "    领取：https://github.com/settings/tokens?type=beta")
    masked = args.token[:4] + "***" + args.token[-4:] if len(args.token) > 8 else "***"
    workdir = args.dir

    # 0. 用 token 认出你到底是谁（避免网站地址里用户名写错）
    if not args.owner:
        status, body = api("https://api.github.com/user", "GET", args.token)
        if status == 200 and isinstance(body, dict) and body.get("login"):
            args.owner = body["login"]
            print("[i] 已识别 GitHub 账号：%s" % args.owner)
        elif status == 401:
            sys.exit("[x] token 无效或已过期（401）。重新领一个。")
        else:
            args.owner = DEFAULT_OWNER
            print("[!] 没能识别账号（%s），暂用默认 %s；可用 --owner 你的用户名 指定" % (status, args.owner))
    full = "%s/%s" % (args.owner, args.repo)
    if args.owner != DEFAULT_OWNER:
        print("[!] 你的账号不是 %s，文档里示例链接需要同步改（改完再发给同事）" % DEFAULT_OWNER)

    # 本地仓库体检
    if not os.path.isfile(os.path.join(workdir, "SKILL.md")):
        sys.exit("[x] %s 里没找到 SKILL.md，--dir 指错了？" % workdir)
    rc, out = git(["rev-parse", "--is-inside-work-tree"], workdir)
    if rc != 0:
        sys.exit("[x] 这个目录还不是 git 仓库。先在技能目录里 git init + commit。")

    # 1. 建仓库（已存在就跳过）
    status, body = api("https://api.github.com/user/repos", "POST", args.token, {
        "name": args.repo,
        "description": DESC,
        "private": bool(args.private),
        "has_issues": True,
        "has_wiki": False,
        "auto_init": False,
    })
    if status == 201:
        print("[ok] 仓库已创建：https://github.com/%s" % full)
    elif status == 422:
        print("[i] 仓库已存在，直接推送：https://github.com/%s" % full)
    elif status == 401:
        sys.exit("[x] token 无效或已过期（401）。重新领一个。")
    elif status == 403:
        sys.exit("[x] token 权限不足（403）。请确认 Contents = Read and write。")
    else:
        sys.exit("[x] 建仓库失败：%s %s" % (status, body))

    # 2. 推送（token 只出现在这一次的 URL 里，不落盘）
    rc, out = git(["rev-parse", "--abbrev-ref", "HEAD"], workdir)
    branch = out.strip() or "main"
    push_url = "https://%s@github.com/%s.git" % (args.token, full)
    rc, out = git(["push", push_url, "%s:refs/heads/main" % branch], workdir)
    print(out.replace(args.token, masked) if out else "")
    if rc != 0:
        sys.exit("[x] 推送失败（上面是 git 原话）。常见原因：token 无 Contents 写权限、或网络不稳。")

    # 3. 顺手把 origin 配成干净 URL（不含 token），并本地设好 upstream
    rc, out = git(["remote", "get-url", "origin"], workdir)
    if rc != 0:
        git(["remote", "add", "origin", "https://github.com/%s.git" % full], workdir)
    else:
        git(["remote", "set-url", "origin", "https://github.com/%s.git" % full], workdir)
    git(["config", "branch.%s.remote" % branch, "origin"], workdir)
    git(["config", "branch.%s.merge" % branch, "refs/heads/main"], workdir)

    # 4. 自检：能拿到 200 才算同事装得动
    status, body = api("https://api.github.com/repos/" + full)
    print()
    if status == 200:
        print("=" * 64)
        print("发布成功，同事现在就能装。把下面这句发给同事：")
        print("    从这个仓库安装技能：https://github.com/%s" % full)
        print("=" * 64)
        print("以后更新：在 %s 里改完 → git add -A && git commit -m '更新' && git push" % workdir)
    else:
        print("[!] 自检返回 %s：如果 --private，请确认同事有该私有仓库权限" % status)

    print("\n[!] 现在请去 https://github.com/settings/tokens 把这个 token 删掉。")


if __name__ == "__main__":
    main()
