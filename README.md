# 国际站速卖通中转英（howie-intl-cn2en-listing-skill）

> **制作者：Howie** ｜ 用起来有问题、想加功能、想改术语，找 Howie。

把中文电商详情页图片里的文案，意译成有品牌高级感的英文，输出「中文原图 + 中英逐句对照表」的 Word 文档。
面向阿里巴巴国际站 / 速卖通 / 亚马逊上新场景。

配套 Skill：`国际站速卖通中转英`（本仓库根目录的 `SKILL.md` 即主流程）。

## 一句话安装（同事版）

把这个仓库地址丢给 WorkBuddy，说一句：

> 从这个仓库安装技能：https://github.com/Howie-Linhao/howie-intl-cn2en-listing-skill

助手会自动 clone 到 `~/.workbuddy/skills/intl-cn2en-listing`。**不用下载、不用解压、不用手动放目录。**
你 push 了新版本后，同事说一句「更新一下这个技能」即可（等价 `git pull`）。

## 手工安装（不用助手时）

```bash
git clone https://github.com/Howie-Linhao/howie-intl-cn2en-listing-skill.git \
  ~/.workbuddy/skills/intl-cn2en-listing
```

或下载 zip 解压后运行一键安装器：

```bash
python 安装.py
```

## 前置条件

| 依赖 | 说明 |
|---|---|
| WorkBuddy 桌面端 | 需要自带内置插件 `tencent-local-office-edit`（脚本自动搜索，不用改路径） |
| Python 3 | 脚本自动使用 WorkBuddy 托管 Python |
| Pillow | 仅长图自动切分需要，**脚本已做首次运行自动补装** |

## 怎么用

> 用国际站速卖通中转英，把这个产品的详情页翻一下。图片在 `<目录>`，品牌 Aisilan，目标平台国际站 + 速卖通。

助手会先问：① 品牌名（默认 Aisilan）② 目标语言与风格（默认英语-美国·简洁·高端）③ 图片是分好组的一组图，还是一整张长图。

## 目录

```
SKILL.md                              主流程：排版原则 / 踩坑清单 / 自检项
scripts/build_bilingual_doc.py        主生成器（读 job.json 生成整份文档）
scripts/slice_long_images.py          长图切分（含校验条带）
scripts/verify_docx.py                交付前校验（不依赖渲染服务）
scripts/color_caliber.py              颜色口径闸门（同名多译色按材质判定）
scripts/glossary_check.py             固定文案口径闸门（客户指定译法 / 违禁变体）
scripts/edsdk_docx.py                 editor_sdk 调用封装（路径自动探测）
scripts/job.example.json              作业文件示例
references/translation-playbook.md    第〇节固定文案表 / 意译原则 / 术语表 / 色卡 / 单位换算
安装.py                                一键安装器
```

细节见 [`安装说明.md`](./安装说明.md)。
