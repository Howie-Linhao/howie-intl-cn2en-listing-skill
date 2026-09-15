---
name: 国际站速卖通中转英
description: 把中文电商详情页图片里的文案意译成有品牌高级感的英文，并生成「中文原图 + 中英对照表」的 Word 文档。对照表一行一个句对（左列中文原文、右列英文文案），逐句对齐、便于逐行核对；单元格行距加大、句与句之间留白充足，长表也易读；图内没有可翻译文案的行，英文栏统一写「/」避免被误当成上架文案；文案密集的长图按图内自然空白带自动切分，每段图下紧跟该段文案；图内重复出现的角标只在文首统一说明一次；材质「碳素钢」统一译为 Metal，颜色名统一走品牌色卡口径。适用于阿里巴巴国际站（Alibaba.com）、速卖通（AliExpress）、亚马逊等跨境平台上新时，把国产产品的中文详情页本地化为英文详情页。触发词：国际站速卖通中转英、详情页翻译、中文详情页转英文、Listing 本地化、中英对照 Word、逐句对照、句级对照、表格对照、行距调整、无文案斜杠、颜色口径统一、产品文案出海、详情页图片英文文案、详情页翻英文、长图切分、长图自动切割、图片切割比对。
author: Howie
agent_created: true
---

# 国际站 / 速卖通 中文详情页 → 英文文案（中英对照 Word）

> 制作者：**Howie**

把一个产品的整批中文详情页图（或**一张多图整合的长图**），意译成可直接上架阿里巴巴国际站 / 速卖通的英文详情页，并输出**中英对照 Word**（原图 + 逐句对照表），便于老板 / 设计逐行核对。

## 适用场景

用户给一批中文详情页图片（典型 990×1499 竖版长图，编号 01…NN）**或一张把多图拼在一起的长图** + 英文品牌名 + 目标语言，要求：
1. 图片里的中文文案**意译**成有品牌高级感的英文（**禁止逐字直译**）；
2. 输出 Word：每张原图下方附中英对照**表格**。

## 交付形态（六条铁律）

1. **逐句对照，用两栏表格** —— 中文一整段 + 英文一整段根本对不上。必须**以句为单位**做表：一行一个句对，**左列中文原文（浅灰 9.5pt）、右列英文文案（深蓝 10.5pt #14396A）**，首行表头注明两列含义。
2. **文案密集的长图要切分** —— 长图按图内自然空白带切成 2-3 段，每段图下紧跟该段文案；用户只给一张整合长图时**自动切**（见「长图切分」节）。
3. **重复的角标只说明一次** —— 同一枚角标出现在多张图时，只在**文首「注」里写一次**（含中文文案 + 统一英文写法），正文各图**不再重复列出**。
4. **品牌署名统一** —— 图内 `DESIGN BY xxx` 一律替换为本次确认的**品牌署名**（默认 `DESIGN BY AISILAN` / `Designed by Aisilan`），并提醒设计端同步改原图。
5. **没有可翻译文案的行，英文栏写 `/`** —— 纯细节图 / 场景图这类「图里没有文案」的情况，中文格写一句说明，**英文格一律 `/`**（浅灰显示）。**绝对不要**写 `This image carries only …` 这类英文说明句：它会被买家或运营误当成可直接上架的 Listing 文案复制走。文档开头「注」里要说明「`/` = 该图无译文，不是漏译」。
6. **材质与颜色走统一口径** —— 中文「碳素钢」**一律译 `Metal`**（不写 Carbon Steel）；颜色名**一律查 `references/translation-playbook.md` 第七节色卡**（如珍珠镍 → `Matte brushed nickel`，不是 Pearl Nickel）。口径优先级高于逐字直译。
7. **同名多译色按材质判定** —— 色卡里带 `*` 的色名（如**砂岩黑**）对应两个色号，**不得按出现顺序取值**：先读产品的**材质参数行**，材质里**只有金属、无布** → `Matte Black`；材质**含亚麻 / 布艺**（linen、fabric、布、织物、棉麻）→ `Linen black`（「亚麻黑」本是亚麻布用色）；**金属与布同时出现、或材质表缺失看不出 → 必须停下来问用户确认**。判定结论写进文档文首「注」留痕。详见手册 7.1。

## 开工前必须确认的参数（先问，不要边做边问）

**每次运行前，先把下面这几项一次问清：**

| 参数 | 说明 | 缺省 |
|---|---|---|
| **① 品牌名** | 用于替换角标署名（如 `designed by Aisilan`）。**必须问** | **Aisilan** |
| **② 目标语言** | 翻译成什么语言 / 什么风格。**必须问** | **英语（美国）· 简洁 · 高端品牌风格** |
| **③ 图片形态** | 提醒用户：**可以上传已经分割好的图片，也可以上传一整张长图**（长图会自动切分） | 按实际判断 |
| 图片位置 | 本地目录或网络共享盘 | 必问 |
| 图片顺序 | 用户 @ 的顺序**常是乱的**，按文件名序号 01→NN 排 | 自动按序号 |
| 目标平台 | 国际站 / 速卖通 / 亚马逊 | 必问 |
| 输出文件名 | `<产品名>-详情页中英文案对照.docx` | 自动 |

问法（一次问完，别挤牙膏）：

> 开工前确认 4 件事：
> 1）本次使用的**品牌名**？（用于替换图内角标署名，如 `designed by Aisilan`；默认 Aisilan）
> 2）**翻译语言与风格**？（默认：英语（美国）· 简洁 · 高端品牌风格）
> 3）图片是**已经分割好的一组图**，还是**一整张长图**？（两种都行 —— 长图会自动按空白带切分，每段配它自己的文案）
> 4）目标平台？（国际站 / 速卖通 / 亚马逊）

用户已在 prompt 里给了的信息不要重复问；用户说「默认」就按上面的缺省走。

## 执行流程

### Step 1 取图
- 网络共享盘在 Git Bash 里用 `//服务器/共享/子路径` 访问（Windows 反斜杠会翻倍）。
- **先整批复制到工作区** `assets/<产品编码>/`，后续插图全用本地绝对路径，避免网络盘抖动。
- 判断形态：**多张编号图** → 走 Step 3 的「指定模式」；**一张长图** → 走「自动模式」。

### Step 2 读文案
- 逐张 `Read` 图片，**按文件名序号升序**。
- 文案常跨图截断（上一张底部接下一张顶部），读取时留意拼接。
- 图里已有的英文（`DETAIL`、`DESIGN BY SAKA`、角标型号）也要抄进中文列，并给出规范英文写法。
- **顺手记录角标**：哪些图带角标、角标文字是否完全一致 —— 一致的走「去重」路径。
- 把每张图的文案**攒成一个 `job.json`**（不是边读边写文档），便于一次生成。

### Step 3 长图切分（见后面「长图切分」节）
- 多张编号图：只切**文案密集**的那几张，切点写在 `plan.json` 里（指定模式）。
- 单张整合长图：直接跑自动模式。

### Step 4 翻译 + 断句
原则、术语表、意译范例见 `references/translation-playbook.md`（**开工前必读**）。要点：
- 意境类（设计理念 / slogan）走**意译 + 品牌调性**；
- 技术规格类（材质、尺寸、功率、标准号、认证）**必须准确**，GB/IEC/ANSI 标准号原样保留；
- 中文按钮译成 `[Button] ...`；
- 不确定的品牌名 / 笔误 → 中性表达 + 文档开头「注」里说明，**不要猜**；
- 尺寸**保留原 mm，追加英寸**：`485mm (19.09in)`，换算 1in = 25.4mm 保留两位小数；
- 缺失数据写「暂无数据」，**禁止用 0 替代**。

**断句规则**（直接决定表格好不好用）：
- 中文一个句子 = 表格一行。以 `。；` 和句意完整处切分；并列的规格行（`MATERIAL.../COLOR...`）**每行一组**。
- 逗号连接的**长句不要硬拆**——拆过头会破坏英文语感，也会把表格撑得很长。
- 中文一段里包含两个独立意思（如「接地与绝缘、耐压测试、防触电保护」+「II 类灯具带电部件不可触及…」）时**必须拆成两行**。
- 图内只有英文的内容（如 `CRI >= 97 Approaching natural colors`），中文列写「图内原英文：…」，英文列给**润色后**的写法。
- 只有角标、没有其他文案的图（纯细节图 / 场景图）**不要留空块**：中文格用一句说明占位，**英文格写 `/`**（不要写英文说明句，会被误当上架文案）。
- 材质与颜色**先过一遍口径**：碳素钢 → `Metal`；颜色查色卡（第七节），表里没有的先问用户。
- 若色名带 `*`（同名多译，如**砂岩黑**）：**先查材质表的材质列**，按「有无亚麻/布」判定取 `Matte Black` 还是 `Linen black`；判不出来**问用户**。不要凭产品名或图片观感猜。

### Step 5 生成 Word
routing 判定：用户提供了源材料（图片）→ 属「source materials → document」，**不要**走 `tencent-docx`（它不摄入源材料），走 `tencent-local-office-edit` 的 editor_sdk 通道。

**做法：把数据写成 JSON，跑本 skill 自带脚本一次生成全文档**，不要手工一条条敲 call。

```bash
PYTHONIOENCODING=utf-8 <python> scripts/build_bilingual_doc.py job.json
```

⚠️ **颜色闸门会先跑**：作业里若用到同名多译色（砂岩黑 / 中国红），脚本按材质判定 —— 材质只有金属、无布 → 自动取 `Matte Black`；材质含亚麻/布艺、或材质信息缺失 → **中止生成（退出码 2）并打印待确认问题**。此时**必须去问用户**（不要改脚本绕开、不要凭观感选一个），拿到答案后写回 `job.json`（并把结论写进 `notes`）再重跑。
单独诊断可跑：`python scripts/color_caliber.py job.json`。
作业里的 `material` 字段写本型号材质清单（如 `["玻璃","碳素钢"]`）——它是颜色判定的**唯一权威依据**，优先级高于从文案里抓的材质行；缺了它，脚本会退化为只扫正文的材质参数行，扫不到就要求问用户。

作业文件用 `pairs` 存句对，`brand` / `target_lang` 存开工前确认的结果：
```json
{
  "title_cn": "...", "title_en": "...",
  "brand": "Aisilan",
  "target_lang": "English (US) · 简洁 · 高端品牌调性",
  "platforms": "阿里巴巴国际站 / 速卖通（AliExpress）",
  "notes": ["排版说明：…", "角标说明：…", "署名修改：…"],
  "image_root": "…/assets/bd111",
  "out": "…/产品名-详情页中英文案对照.docx",
  "blocks": [
    { "img": "slices/BD111_06_b.jpg",
      "cap": "图 06 · 规格参数（图下段 2/2） / Specifications (Part 2/2)",
      "pairs": [ ["MATERIAL　材质：玻璃、碳素钢", "MATERIAL: Glass, Carbon Steel"], ["…", "…"] ] }
  ]
}
```
`build_bilingual_doc.py` 负责：边距 42.5pt/45pt → 插图(w=540) → 图注(居中 9pt 灰) → **中英对照表** → 表格布局（列宽/居中/外框/行线）→ 分页保护 → 图片段居中 → `save_file`（原路径被占用则另存 + 重命名绕过）。

每块插入的 HTML 结构：
```html
<p style="font-size:1pt">&nbsp;</p>
<p style="text-align:center;font-size:9pt;color:#999999">图 06 · …（图下段 2/2） / … (Part 2/2)</p>
<table style="width:100%">
  <tr><td style="background-color:#F2F5F9;border-bottom:1px solid #E8E8E8"><p style="line-height:150%"><span style="…">中文原文 · Chinese</span></p></td>
      <td style="background-color:#F2F5F9;border-bottom:1px solid #E8E8E8"><p style="line-height:150%"><span style="…">English Copy</span></p></td></tr>
  <tr><td style="border-bottom:1px solid #E8E8E8"><p style="line-height:150%"><span style="font-size:9.5pt;color:#777777">中文原文</span></p></td>
      <td style="border-bottom:1px solid #E8E8E8"><p style="line-height:150%"><span style="font-size:10.5pt;color:#14396A">English copy</span></p></td></tr>
  <tr><td style="border-bottom:1px solid #E8E8E8"><p style="line-height:150%"><span style="font-size:9.5pt;color:#777777">本图仅有场景画面与角标，无文案。</span></p></td>
      <td style="border-bottom:1px solid #E8E8E8"><p style="line-height:150%"><span style="font-size:10.5pt;color:#BBBBBB">/</span></p></td></tr>
</table>
```
- **首个 1pt 占位段不可省**：HTML 块的第一个 `<p>` 会被并入图片所在段落，图注会挤在图片右侧。见「排版原则」。
- **单元格内容必须包一层 `<p style="line-height:150%">`** 才能设行距（实测映射为 `w:spacing w:line="360"`）；裸 `<span>` 上写 `line-height` 无效。一层 `<p>` 不会多出空段，行高不虚增。
- 序号 `<span>` **只在块内句对 ≥3 时加**（1-2 句加了反而啰嗦）。
- 偶数行加 `background-color:#FBFCFE` 做斑马纹，长表更容易横向追读。
- 无译文的英文格用 `color:#BBBBBB`（浅灰）呈现 `/`，与真实文案的深蓝一眼可分。
- 文本先 `html.escape(s, quote=False)`（中文列里的 `<` `>` `&` 必须转义）。

### Step 6 验证（不要依赖渲染服务）
```bash
PYTHONIOENCODING=utf-8 <python> scripts/verify_docx.py <输出.docx> <期望块数> <期望句对数>
```
自检项：图片数 = 图注数 = 块数 = **表格数**；表格行数 = 句对数 + 表头行数；**英文格无空格**（无译文行必须是 `/`）；`tcBorders = (行数 − 表格数) × 2`；图注段均 `jc=center`；`<w:keepNext` ≈ 块数 × 2；**`w:spacing w:line` ≈ (句对 + 表头) × 2**（行距生效）；**`tblCellMar` 的 top/bottom ≥ 60dxa**（句距生效）。

### Step 7 交付
- 输出 `.docx` 到工作区根目录，文件名带产品名（中文名可用）。
- **最后必须 `present_files`** 打开文档给用户预览。
- 文档开头按顺序放「注」：**排版说明（左中文右英文怎么读）、斜杠说明（`/` = 该图无译文，不是漏译）、材质口径（碳素钢→Metal）、颜色口径（本型号用的色卡译名）、角标说明（去重）、署名修改**、以及任何不确定表述的处理。
- 结尾主动列出 **2-3 个需要用户核对的点**（尺寸数字归属、疑似笔误、与海外主推名不一致的角标、色卡里冲突的颜色名）。

## 长图切分

痛点：一张长图塞了整段国标条款或参数表，图和文案隔了半屏，比对极累。
做法：**按图内自然空白带把长图切开，每段图下紧跟该段文案。切点必须落在真正的空白带上，不切断任何文字或图形。**

```bash
# 自动模式（用户只给一张多图整合的长图）
PYTHONIOENCODING=utf-8 <python> scripts/slice_long_images.py \
    --src <长图路径> --prefix <产品前缀> [--dst 输出目录]

# 指定模式（多张编号图，只想切其中几张）
PYTHONIOENCODING=utf-8 <python> scripts/slice_long_images.py \
    --src <图片目录> --prefix <产品前缀> --plan plan.json
# plan.json: {"prefix":"BD111","images":[{"match":"06","cands":[865],"bottom":null}]}
```

**自动模式选点策略**（顺序不能反，否则会把图切得很碎）：
1. 先取「**强分隔带**」——宽度 ≥ 其它空白带中位数 2.5 倍的那些带，通常就是多图整合长图里面板与面板之间的真实间隔；
2. 再看还有哪一段仍超过 `MAX_SEG_H`(1250px)，对这些段按等分点吸附补刀；
3. 任何切点都必须保证两侧段高 ≥ `MIN_SEG_H`(260px)，避免切出碎片；
4. 段内平均行极差 < `INK_MIN` 的**纯空白段直接丢弃**，不产出无用切片。

**共同要点**：
1. **定位切点（像素法）**：10 列 BOX 缩放做行特征，行内极差 < 12 视为空白行，连续 ≥ 10 行即一条空白带。
2. **必须目视复核（重要）**：⚠️ 10 列采样会**漏掉 1–2px 水平细线**——典型翻车是切点切在按钮 / 输入框边框上。脚本会把切点 ±130px 的条带**叠加红线拼成一张校验图** `_cutcheck/cut_check.jpg`，**必须 `Read` 一遍**确认两侧都是真空白。
   判定按钮等细边界时改用「逐行统计非背景像素数」：`sum(1 for x in range(0,w,2) if abs(px[x,y]-bg) > 14)`。
3. **切片命名用 ASCII**（`BD111_06_a.jpg`），避开中文路径坑；存 `assets/<产品>/slices/`。
4. **caption 标明位置**，让用户一眼对上号：
   ```
   图 06 · 尺寸标注（图上段 1/2） / Dimensions (Part 1/2)
   图 15 · 电源质量标准（图 2/3） / Power Supply Standards (Part 2/3)
   ```
5. 切片后**逐片 Read**，只给**含文案**的切片写 `pairs`；纯画面片段不写文案就别塞进文档。

## 角标与重复内容去重

同一枚角标反复出现在十几张图上时（如 `Cohen Ambient Small Wall Lamp · DESIGN BY SAKA · 金属为骨，光影为魂`）：

1. 先在文首「注」里写一次：**中文文案 + 统一英文写法 + 说明它出现在哪些图**。
   > 角标说明：图 02–05、08–13 图内右下角均为同一枚产品角标，文案为「… · DESIGN BY AISILAN · …」，统一英文写法为「… · Designed by Aisilan · …」。因各图完全一致，正文不再逐图重复列出。
2. 正文各块**删掉角标行**；若某图**只有**角标没有其他文案，用一个句对占位，别留空块。
3. 角标文字有**细微差异**时（如部分图少了 slogan 段）在注里写明「图 02、03 仅前两段」。
4. **品牌署名替换**单独写一条注：说明用的是本次确认的品牌（默认 `Designed by Aisilan`）+ **提醒设计端同步替换原图角标文字**（图内文字改不了，只能给替换后的文案）。

## 排版原则（全部实测，改动前先读）

**(a) 图注必须换行在图片下方** —— HTML 块的**首个 `<p>` 会被并入图片所在段落**，短图注（如「图 12 · 吧台 / Bar」）会挤在图片右侧。
→ 在 HTML 最前面加一个 1pt 占位段破解。

**(b) 图片段补居中** —— 占位段方案会让图片段不再继承 `text-align:center`（原来是靠被并入的 `<p>` 带过来的）。
→ `doc_modify_paragraph({ranges: img_ranges, jc: "center"})`。

**(c) 分页保护按 2 段/组** —— 防止「图片 / 图注」与**其后的表格**被分页拆散：
→ `doc_modify_paragraph({ranges: [图片段, 图注段], keep_with_next: True})`
图注段设了 keepNext 后会与**后面的表格**绑定同页；表格内段落拿不到段落属性，不用设。

**(d) 表格样式一律写在内层 `<span>`** —— 写在 `<td>` 上的 `color` 会被引擎当**单元格底纹**（`<w:shd>`）；`<td>` 上只有 `background-color` 和 `border-bottom` 两个属性可用。

**(e) 行距靠「单元格内 `<p>` + 表格内边距」两级搞定**（这是「行距增大、易读」的唯一正确做法）：
- **单元格内行距**：内容包一层 `<p style="line-height:150%">` → 映射为 `w:spacing w:line="360"`（1.5 倍）。**写在裸 `<span>` 上无效**。
- **句与句之间的留白**：`doc_set_table_properties(cell_margin={top:60,bottom:60,left:113,right:113})`（dxa，1 dxa = 1/20pt）→ 表格级 `tblCellMar`，上下各 3pt。一个句对 = 一行，所以「行间距」就是「句间距」。想更透气就调大这两个值（实测 15dxa 是引擎默认值，太挤）。
- 备选：`row_heights_dxa`（`mode=manual`，生成 `trHeight hRule="atLeast"`）可设行高下限，但和 `cell_margin` 叠加会过空，二选一即可。

**(f) 没有译文的行，英文格写 `/`** —— 纯视觉图（细节图 / 场景图）不要把英文说明句当译文写进去，会被误当成上架文案。
→ 中文格保留一句说明，英文格 `/`；生成脚本对 `en` 为空 / `/` / `-` / `n/a` 一律自动降级为 `/`（`NO_COPY`）。

- 用 `doc_resolve_document_structure` 定位：节点字段是 **`text_preview`**（不是 `text`），图片段 preview 形如 `"[Image]图 06 · ..."` 且被截断，用 `startswith("图 ")` 匹配图注段。表格节点 type 是 `Table`，**不出现**其内部段落。
- `ranges` 是数组可**批量传**（实测 10-12 个/批稳定），远快于逐段传 `paragraph_id`。

## 表格能力清单（实测，别再试错）

| 想要的效果 | 可行做法 | 结论 |
|---|---|---|
| 行与行之间的分隔线 | `<td style="border-bottom:1px solid #E8E8E8">` → 生成 `tcBorders` | ✅ 唯一能被映射的边框方向 |
| 单元格底色 / 斑马纹 | `<td style="background-color:#FBFCFE">` → `w:shd` | ✅ |
| 表头底色 | 同上（HTML）或 `doc_set_table_cells` 的 `property.color` | ✅ `fill_color` **无效**，要用 `background_color`/`color` |
| 列宽 | `doc_set_table_properties(mode="manual", col_widths_dxa=[4400,5800])` | ✅ HTML 的 `width:47%` **无效**（恒等分 4153） |
| 表格居中 | `doc_set_table_properties(alignment="center")` | ✅ |
| 表格外框改色 | `doc_set_table_properties(borders={top/bottom/left/right: {...}})` | ✅ 只有这 4 向能改 |
| 表格内竖线（两列分隔） | 靠默认 `insideV`（CBCDD1 浅灰） | ⚠️ `insideH/insideV` **改不动**，但默认值够用、别管它 |
| 单元格四边框（top/left/right） | — | ❌ 引擎只解析 `border-bottom`，其余方向静默忽略 |
| 表格内的分页保护 | — | ❌ 表格内段落拿不到 `keep_with_next`，靠图注段的 keepNext 绑定整表 |
| 单元格字体/字号/颜色 | `<span style="...">` 内层承载 | ✅ 写在 `<td>` 上会变成底纹 |
| 单元格内行距 | `<p style="line-height:150%">` → `w:spacing w:line="360"` | ✅ 必须包一层 `<p>`；写在裸 `<span>` 上**无效** |
| 句与句之间的留白（行间距） | `doc_set_table_properties(cell_margin={top,bottom,left,right})` → `tblCellMar` | ✅ 表格级；默认 15dxa 太挤，用 60dxa（=3pt） |
| 行高下限 | `doc_set_table_properties(mode="manual", row_heights_dxa=[…])` → `trHeight hRule="atLeast"` | ⚠️ 可用，但与 `cell_margin` 叠加会过空，二选一 |
| 单元格内插图 | `doc_set_table_cells` 的 `image` 字段 | ⚠️ 未验证；本项目图片一律走 `doc_insert_image` |

**⚠️ 最大的坑：`doc_set_table_properties` 会清掉所有 `tcBorders`。**
HTML 插入时生成的 `border-bottom`（`tcBorders`）在设完列宽/外框后会**全部消失**（实测 6 → 0），
整张表只剩外框、行间没有分隔线，句对边界反而糊掉。
→ **顺序必须是**：先 `doc_set_table_properties` 设列宽/居中/外框，**再用 `doc_set_table_cells` 的
`property={"borders": {"bottom": {...}}}` 逐行补回下边框**（`edsdk_docx.style_tables` 已内置这个顺序）。

## 二次编辑已有文档（尺寸 / 文案修正）

- 隔轮再编辑报 `document is not open`：上一轮实例已失效，`open_file file_path=<绝对路径>` 重开，**不要** `create_doc` 重建。此时返回的 **file_id 就是路径字符串本身**（不是 `new_doc_*`）。
- 文案修正用 `doc_find_and_replace`（不传 `scope` 即全文替换）。**整行/整串替换**，不要按最小单位替换——`25mm` 是 `225mm` 的子串，会误伤。
- 单位换算对照表见 `references/translation-playbook.md`。
- 改完 `save_file`（若原路径被占用就另存新路径），再用「重命名绕过」覆盖回正式文件名。
- **改完文档一定要把补丁同步回 `job.json`**，否则下次用脚本重跑会退回旧文案（这是本项目踩过的坑）。

## 踩坑清单（全部实测）

| 现象 | 原因 / 解法 |
|---|---|
| `create_doc` 解析失败 | 它返回**纯文本** `Created blank doc ... file_id=xxx, file_path=yyy`，不是 JSON。正则提 `file_id=([^,\s]+)` |
| `doc_insert_image: 'idx' must be a non-negative integer (got: -1)` | 插图不能用 -1；文档开头用 `idx=0` |
| HTML 里 `<img>` 不显示 | 引擎对 HTML 内嵌 `<img>` 支持有限；图片**必须**走 `doc_insert_image(image_path=...)` |
| `<td>` 的 color 变成单元格底纹 | 引擎把 `style="color:…"` 解析为 `<w:shd>`。样式写到**内层 span/p** |
| 设了 `line-height` 但行距没变 | 写在了裸 `<span>` 上 → 必须包一层 `<p style="line-height:150%">`，否则不生成 `w:spacing w:line` |
| 行与行（句与句）挤在一起 | 表格 `tblCellMar` 默认只有 15dxa。用 `cell_margin` 提到 60dxa（上下各 3pt） |
| 英文栏写了 `This image carries only…` 被当成上架文案 | 无译文的行英文栏一律写 `/`（中文格保留说明）；生成脚本已内置 `NO_COPY` 降级 |
| **设完列宽后行分隔线全没了** | `doc_set_table_properties` 清掉 `tcBorders` → 之后必须用 `set_row_lines`（`doc_set_table_cells`）补回 |
| 材质判定被文首「注」污染 | `color_caliber` 若把 `notes` 一起扫，一句「若材质含亚麻布则取 Linen black」的口径说明会让**所有**产品都被判成「有布」。材质判定只扫**正文**（`include_notes=False`）；显式给了 `job["material"]` 就完全以它为准 |
| 材质缺失时别默认「无布」 | 「找不到材质」≠「材质里没有布」。缺材质就返回待确认问题（退出码 2），不要自动取 `Matte Black` —— 猜错方向等于给买家看错颜色 |
| `<td style="border-right/left/top">` 不生效 | 引擎只解析 `border-bottom`，其余方向静默忽略；竖直分隔线靠默认 `insideV` |
| `insideH/insideV` 改色无效 | 只能改 outer 4 向；`insideV` 恒为 CBCDD1 |
| `cell_fills` 报 "no properties specified" | 子字段名要用 `color`，写 `fill` / `fill_color` 会被当成空属性丢弃 |
| `doc_set_table_properties` 报 "ToCommands returned empty" | 该错误下**属性可能已部分生效**；传 `cell_margin` 等字段时更容易触发。把它当警告，落盘后解析 XML 复核 |
| `doc_set_table_cells` 报 "cannot resolve cell range at row=N" | row/col 是 1-based 且必须真实存在；先用 `doc_list_tables` 看 `row_count` |
| 正则 `<w:t[^>]*>` 读出大段 XML | 它会匹配上 `<w:tblPr>`/`<w:tr>`。必须写 `<w:t(?:\s[^>]*)?>` |
| `doc_to_image: file not found`（中文文件名） | 该工具对中文名路径解析异常；复制成英文名副本再转 |
| `doc_to_image: 服务繁忙 / 437009` | 该云端接口**长期不可用**（大文件必失败，小文件也常 50000）。**不要依赖它验证**，改用 `verify_docx.py` 解析 XML |
| 路径反斜杠翻倍 | `--json` 里写 `\\` 会被解析成双反斜杠；统一用**正斜杠** |
| 隔轮编辑报 `document is not open` | 见上节 |
| `save_file` 回原路径报 `Export file is occupied` | 原文件被预览进程独占 → `save_file` 传**新路径**另存 |
| `cp` / `shutil.copyfile` 覆盖报 `Device or resource busy` / `PermissionError` | 该锁**允许重命名、不允许写入**。解法：`mv 原名 _tmp.docx` → `mv 新文件 正式名` → `rm _tmp.docx`（实测可行，无需重启服务） |
| 替换后磁盘内容没变 | 替换只改内存，必须显式 `save_file` 才落盘，并立刻用 `verify_docx.py` 复验 |
| `save_file` 报 `CALL FAILED`，但文件其实已保存 | 它成功时可能返回**纯文本** `File saved to: ...`。用容错解析 |
| 图片和图注挤在同一段 | 加 1pt 占位段（见排版原则 a） |
| 图片段丢了居中 | 占位段副作用，补 `jc: "center"`（见排版原则 b） |
| 切点落在按钮边框上 | 10 列采样漏检 1–2px 细线；切完必须读校验条带目视复核 |
| 自动切割把图切得很碎 | 选点顺序反了；必须**先取强分隔带，再对过长段补刀**（见长图切分） |
| 替换命中错误位置 | 按最小单位替换会误伤（`25mm` ⊂ `225mm`）；整串替换 |

## 文件

| 文件 | 用途 |
|---|---|
| `scripts/build_bilingual_doc.py` | 主生成脚本，读作业 JSON 一次跑完全文档（`pairs` → 中英两栏对照表） |
| `scripts/job.example.json` | 作业文件示例（BD111 实战，含 brand / target_lang / 角标去重与句对写法） |
| `scripts/slice_long_images.py` | 长图切分：`--src` 单张长图走**自动模式**，`--plan` 走指定模式；含空白带检测、校验条带、纯空段丢弃 |
| `scripts/verify_docx.py` | 不依赖渲染服务的排版/内容校验（图片/表格/行数/英文空格/行线/行距/内边距） |
| `scripts/color_caliber.py` | 颜色口径闸门：同名多译色（砂岩黑 / 中国红）按**产品材质**判定；判不出来就返回待确认问题、由生成器中止（退出码 2）。可单独运行诊断 |
| `scripts/edsdk_docx.py` | editor_sdk 调用封装（容错解析、批量段落操作、`style_tables` 表格布局、安全覆盖） |
| `references/translation-playbook.md` | 意译原则、**材质口径（碳素钢→Metal）**、**颜色标准译名表**、术语表、单位换算、断句与交付自检清单 |

## 运行环境（跨机器复用需知）

本 skill 设计为**整包可移植**：拷走 `intl-cn2en-listing` 整个文件夹到 `~/.workbuddy/skills/` 即可，
**脚本里没有写死的机器路径**，以下两项自动探测：

| 目标 | 探测顺序 |
|---|---|
| editor_sdk 插件目录 | 环境变量 `TENCENT_LOCAL_OFFICE_DIR` / `EDS_SKILL_DIR` → 常见安装根（`D:/workbuddy`、`C:/Program Files/WorkBuddy`、`~/AppData/Local/...`）→ 各盘符 1-2 层浅层 glob。都找不到才报错 |
| Python 解释器 | 环境变量 `EDS_PYTHON` / `WORKBUDDY_PYTHON` → `~/.workbuddy/binaries/python/versions/*/python.exe`（取版本最高）→ 系统 `python` |

- 找不到插件时报错信息里直接给出了要设的环境变量，照抄即可。
- **Pillow 仅长图切分需要**，且已在 `slice_long_images.py` 里做了**首次运行自动补装**，不需要用户手动 `pip install`。
- 运行脚本时加 `PYTHONIOENCODING=utf-8`，避免中文输出在 Windows 控制台乱码。

## 交给别人用（分发方式）

**只给 `SKILL.md` 没用** —— 主流程引用了 `scripts/` 全部脚本与 `references/` 手册，缺一不可。
按省事程度：

| 方式 | 对方要做的 | 更新方式 |
|---|---|---|
| **A. GitHub 仓库（推荐）** | 在对话里说一句「从这个仓库安装技能：`https://github.com/Howie-Linhao/howie-intl-cn2en-listing-skill`」→ 助手自动 clone 到 `~/.workbuddy/skills/intl-cn2en-listing`。**零下载、零解压、零放目录** | 你重跑 `python push_api.py <PAT>` 追加一个提交（**本机 git push 走代理必失败，不要用**），对方说「更新一下这个技能」即可 |
| **B. 发 zip** | 把 `国际站速卖通中转英-skill.zip` 拖进 WorkBuddy 说「帮我安装这个技能包」→ 助手自己解压安装（包内含 `安装.py` 兜底） | 重新发一次新 zip |
| **C. 一键安装器** | 解压后跑 `python 安装.py`；`python 安装.py <包.zip>` 可直接吃 zip；`--check` 只体检 | 覆盖安装即可 |

> ⚠️ **方式 A 的前提是仓库已真实发布**。把链接发给对方**之前**先自己打开一次：
> 看到仓库页面才算成功，**404 说明仓库还没建** —— 此时对方照着装取不到技能，助手只能自由发挥，
> 出来的文档不会符合本技能的模板（会少两栏逐句对照表、`/` 占位、行距等固定形态）。
> 发布与更新用 **`push_api.py <PAT>`**：走 GitHub Git Data API 直传（blobs → tree → commit → refs），
> **不依赖本地 git、不写本地磁盘**。本机 `git push/fetch` 走代理会 `CONNECT tunnel failed 502`，
> 且 C 盘写满曾把本地 `.git` 写坏 —— **本机不要用 git 命令发布**。详见 `推送步骤.md`。
> 对方装完请他自检：问助手「列出 `.workbuddy/skills` 下的技能」应看到 `intl-cn2en-listing`；
> 触发时助手**应先反问品牌 / 语言 / 图片形态**，不问就动手 = 没装上。

**对方环境只要求：WorkBuddy 桌面端（自带 `tencent-local-office-edit` 插件）+ Python 3。** 其余自动。
