# 中→英 详情页翻译手册（国际站 / 速卖通）

面向灯具、家居、五金类跨境产品详情页。目标是**海外买家读起来像本土品牌写的**，而不是「中文的英文版」。

---

## 〇、固定文案表（客户指定口径 · 最高优先级 · 一字不改）

下表是客户书面指定的统一译法。**只要中文原文出现在图里，英文列必须照抄下表右列**，
**不得**因为「换个词更顺」「这个词更专业」而改写、缩写、调序或换大小写。
口径冲突时**本表优先于后面第六节的通用术语表**。

| 中文（必须原文命中） | 英文（必须逐字照抄） |
|---|---|
| 金属为骨，光影为魂 | Metal as the framework, light as the soul. |
| 碳素钢 | Metal |
| 灯杆 | Lamp Pole |
| 底座 | Base |
| 灯罩 | Lampshade |
| 一盏灯，照见三代人的团圆 | A single lamp, illuminates the reunion of three generations. |

**执行要点**

1. **标点、句首大写、句末句号都照抄** —— 例如 slogan 末尾的 `.` 不能省。
2. **`Metal` 是碳素钢的专属口径**（不写 Carbon Steel）；同理「底座」只写 `Base`，**不再用 Backplate / Base Plate**；
   「灯罩」只写 `Lampshade`（一整词），**不单独写 Shade**；「灯杆」只写 `Lamp Pole`。
3. 表中的两句 slogan（金属为骨…／一盏灯…）属**品牌固定文案**，出现在角标、海报、主图上时都走这一译法。
4. 上表未覆盖的材质 / 颜色，再走**第六节术语表**与**第七节色卡**。
5. 生成本文前跑一次闸门自检（发现违禁变体或不一致会列出出处）：
   ```bash
   python scripts/glossary_check.py <作业.json>      # 退出码 2 = 有强制项不一致，需先改文案
   ```

> 命名规范：客户只认这 6 条。要新增固定文案时，**加在本表**，不要散落到后面的术语表里。

---

## 一、开工前先确认品牌与语言

**每次运行前都要先问用户这两项，不要沿用上一单的设置**：

| 项 | 说明 | 默认 |
|---|---|---|
| 品牌名 | 用于替换图内角标署名，例如 `designed by Aisilan` / `Designed by Aisilan` | **Aisilan** |
| 目标语言 / 风格 | 翻译成什么语言、什么调性 | **英语（美国）· 简洁 · 高端品牌风格** |

- 目标语言不是英语时，下面的术语表与意译范例**只作句式与结构参考**，词条要按目标语言重写；单位换算仍保留 `mm + 当地惯用单位`（如英语市场用 in）。
- 品牌名同时决定**角标署名的英文写法**（`Designed by <Brand>`）与文档抬头 `Brand:` 字段。
- 还要提醒用户：**可以上传已经分割好的图片，也可以上传一整张长图** —— 长图会自动按空白带切分。

## 二、总原则

**意译优先，准确兜底。** 文案分两类，处理方式完全不同：

| 类型 | 例子 | 处理方式 |
|---|---|---|
| 意境类（设计理念、slogan、场景描述） | 金属为骨，光影为魂 | **脱开中文句式重组**，追英文广告语的节奏；不保留中文的排比和对偶 |
| 规格类（材质、尺寸、功率、认证、标准号） | 碳素钢、IEC 60598、CRI≥97 | **逐项精确**；标准号、型号、符号原样保留 |

**四条硬规则**
1. 不出现中式英语：`Welcome to inquire` / `Good quality and low price` / `Our company has...` 一律删掉，改成陈述式产品语言。
2. 不用感叹号堆情绪，用短句 + 名词短语营造高级感。
3. 单位、符号规范化：`≥`、`Ø`（不用 φ）、`×`（不用 \*）、`°C`（不用 C 或 ℃）。
4. 平台适配：国际站 / 速卖通面向欧美买家 → 英式或美式拼写**全文统一**（建议美式：color / center；若参数名已用 colour 则统一不改）。

**两条统一口径（品牌强制，优先级高于逐字直译）**
5. **材质：中文「碳素钢」一律译为 `Metal`**，不要写 Carbon Steel（见第六节术语表）。图上其余材质（玻璃、铝、不锈钢）照常精确翻译。
6. **颜色：一律查第七节《颜色标准译名表》**，按表取值，不得自由发挥（例：珍珠镍 → `Matte brushed nickel`，不是 Pearl Nickel）。遇到**同名多译色**（带 `*`，如砂岩黑）**必须先查产品材质表判定**：材质里只有金属、无布 → `Matte Black`；材质含亚麻/布艺 → `Linen black`；金属与布同时出现或材质表看不出 → **问用户确认**（详见 7.1）。表里没有的颜色先问用户，不要自造。

## 三、意译范例（BD111 实战，可直接作参照）

| 中文原文 | 英文文案 | 处理要点 |
|---|---|---|
| 金属为骨，光影为魂 | **Metal as the framework, light as the soul.** | 走**第〇节固定文案表**逐字照抄，不意译（`Framed in metal, ensouled by light.` 是早期写法，已废） |
| 不是要复刻宗教的庄严，而是想找回一种被现代生活释解的仪式感 | not to reenact the solemnity of faith, but to reclaim a sense of ritual as redefined by modern living | `复刻`→reenact、`释解`→redefined，保留 `not to... but to...` 转折 |
| 当夜幕降临、床头的一盏灯亮起，那不仅是照明，更是一场私人的光的仪式 | When night falls and the lamp beside the bed glows to life, it is never merely illumination — it is a private ceremony of light | `亮起`→glows to life；`不仅是…更是…`→never merely... it is... |
| 我们以科恩命名 | Named after Cohen | 中文主谓 → 英文过去分词起句 |
| 高端共创技术解构 | High-End Collaborative Technical Architecture | 直译"解构"会歧义，Architecture 更贴商品语境 |
| 详细内容 / 产品信息 | Detailed Content / Product Information | 保留斜杠分隔的多级小标题 |
| 搭配参考 / 空间展示 | Styling Reference / Display | 不用 Translation / Show |
| 具体光源质量标准 了解更多 | [Button] Detailed Light Source Quality Standards · Learn More | 图片内按钮加 `[Button]` 前缀，点分隔 |

## 四、断句与对照编排（决定文档好不好用）

文档**以句为单位做成两栏表格**：一个句对 = 表格一行，**左格中文原文（浅灰 9.5pt）、右格英文文案（深蓝 10.5pt）**，表头注明两侧含义，偶数行加浅底便于横向追读。断句规则：

1. **中文一句 = 表格一行**。以 `。`、`；` 和句意完整处切分。
2. **并列规格清单每行一个句对**：`MATERIAL：玻璃、碳素钢` / `COLOR：珍珠镍` / `POWER：3W` 各占一行 —— 不要让六行参数挤进一个句对。（**尺寸标注块另见 4.1**：一个尺寸一行 + 固定中文提示）
3. **长句不要硬拆**：逗号连接的长定语拆过头会毁掉英文语感，宁可一句长一点。
4. **一段里有两个独立意思必须拆**：
   例：「1. 电气安全：接地与绝缘、耐压测试、防触电保护：II 类灯具带电部件不可触及，基本绝缘部件不得暴露于外表面…」
   → 拆成 ①「1. 电气安全：接地与绝缘、耐压测试、防触电保护」+ ②「II 类灯具带电部件不可触及…」两个句对。
5. **图内只有英文的内容**：中文列写「CRI≥97（图内原英文：Approaching natural colors, Color highly restored）」，英文列给**润色后**的写法。
6. **只有角标、无其他文案的图**（纯细节图 / 场景图）**不要留空块**：中文格写一句说明（如「本图仅有产品细节画面与角标，无文案（角标见文首说明）。」），**英文格一律写 `/`**。
   - 用 `/` 而不是一句英文说明（`This image carries only ...`）：那种句子会被买家/运营**误当成可上架的 Listing 文案**复制走。`/` 一眼就懂是「此处无译文」。
   - 判定「无翻译内容」的行：`en` 缺失、空白、或本身是 `/`、`-`、`—`、`n/a` 等占位符 —— 生成脚本会自动降级为 `/`（见 `build_bilingual_doc.py` 的 `NO_COPY` / `en_cell()`）。
   - 文档开头「注」里要写一句：**英文栏为 `/` 表示该图没有可翻译的文案，不是漏译**。
7. **块内句对 ≥3 时加序号**（01/02/03，浅灰 8pt）便于定位；1-2 句不加。

### 4.1 尺寸板块（一行一个尺寸 + 中文提示）

尺寸标注图（引线指部位 + 一串数值）最容易做错，单独定规矩：

1. **一个尺寸 = 一个句对（一行）**。
   ❌ 不许把 `225mm / 485mm / 260mm / 25mm / ø120mm` 塞进同一行 —— 图里每个数值都靠一条
   引线指向某处，挤在一起读者分不清哪个数配哪条线（客户原话：**「放在一起不直观」**）。
2. **部位名称单独成行**，中文列前缀写「部位文案（仅定位）：」，英文列**按英文语序连贯翻译**。
   原图那串中文标签**本身就是文案**，要读起来像一句正常英文，**不能用破折号/斜杠把「部位」和「材质」拼起来**：
   - ✅ `碳素钢底座` → `Metal Base`（材质修饰词在前、中心词在后 —— 英文习惯语序）
   - ✅ `白玉磨砂玻璃` → `Frosted White Jade Glass`
   - ❌ `Base — Metal` / `Base - Metal` / `Base / Metal`（生硬拼接，客户明确反对）
   - ❌ `Metal's Base` / `Base Metal`（前者不地道，后者是「贱金属」完全另义）
   组合时仍受**第〇节固定文案表**约束（碳素钢=`Metal`、底座=`Base`、灯罩=`Lampshade`、
   灯杆=`Lamp Pole`）—— 拼写一字不许改，**语序按英文习惯调**，两者不冲突。
   这条前缀**只用来告诉读者这条引线指的是哪儿**，不是上架文案。
3. **该板块必须带一条中文提示**（客户指定口径，逐字）：
   > 部位文案仅为定位作用，如原图只有尺寸则忽略该英文文案，只取用 mm 及 inch 尺寸。

   作业 JSON 里给该块写 `"kind": "size"`，生成脚本会自动带上这句；要换措辞就显式写
   `"tip_cn": "…"`（传 `""` 表示明确不要提示）。提示以琥珀色单独成段，排在
   **图注之后、表格之前**，读者先看到判读口径再看行。
4. **尺寸行的写法**：中文列写原图数字（`225mm`；直径写 `Ø120mm`，**不用 φ**），
   英文列补英寸 `225mm (8.86in)`（换算见第八节）。
5. **原图只有尺寸、没有部位名时，不要编部位名** —— 只列尺寸行。
6. 数值归属确实看不出来时照**第九节**处理（原样呈现 + 文首注里说明），英文侧**不硬套**
   Width / Height 这类带归属的词。
7. 脚本自带兜底：`kind` 属尺寸类的块，若某行的中文与英文能用**同一个**分隔符切成**同样多份**、
   且每份都含一个 `mm` 数值，会**自动拆成一行一个尺寸**并打 `[INFO]` 日志（不想被拆写
   `"no_split": true`）。`verify_docx.py` 复核「含 ≥2 个尺寸的行 = 0」。

## 五、重复角标的去重（国际站详情页高频）

同一枚角标反复出现在十几张图上（如 `Cohen Ambient Small Wall Lamp · DESIGN BY SAKA · 金属为骨，光影为魂`）：

**总口径：角标不重复翻译，但至少保留一处 —— 而且那一处必须放在文档最前面、足够醒目。**

1. **文首「注」区块里保留一处完整的角标说明**：中文原文 + 统一英文写法 + **它出现在哪些图**。
   这一处要**单独成段、加粗或居中**，让人一眼看到，不能被埋进其他说明里。
   > 角标说明（**统一口径，正文各图不再重复**）：图 02–05、08–13 图内右下角为同一枚产品角标，
   > 中文原文「… · DESIGN BY SAKA · 金属为骨，光影为魂」，
   > 英文统一写法「… · Designed by Aisilan · Metal as the framework, light as the soul.」。
2. **正文各块删掉角标行**；某图只有角标时用第 6 条的占位句（中文格说明 + 英文格 `/`）。
3. 角标文字有**细微差异**时在注里写明（如「图 02、03 仅前两段」）。
4. **署名替换单独写一条注**（如 `DESIGN BY SAKA` → `DESIGN BY AISILAN`）：给出英文写法 `Designed by Aisilan`，并**提醒设计端同步替换原图角标文字** —— 图内文字改不了，只能给替换后的文案。
5. **禁止的两种做法**：
   - ❌ 每张图都列一遍角标（表格被灌水，用户明确反对）；
   - ❌ 全文一处都不留（读者不知道角标存在、也不知道该写什么）。
6. 角标里的 slogan 段（如「金属为骨，光影为魂」）走**第〇节固定文案表**，逐字照抄。

## 六、术语表（灯具类）

> **先看第〇节固定文案表。** 本节的「碳素钢 / 灯杆 / 底座 / 灯罩」已由第〇节接管，出现冲突以第〇节为准。

**材质 / 工艺**

| 中文 | 英文 |
|---|---|
| 碳素钢 | **Metal**（第〇节固定文案，不写 Carbon Steel） |
| 不锈钢 | Stainless Steel |
| 铝合金 / 压铸铝 | Aluminium Alloy / Die-Cast Aluminium |
| 拉丝镍 / 哑黑 | Brushed Nickel / Matte Black（颜色名以第七节色卡为准） |
| 白玉磨砂玻璃 | Frosted White Jade Glass（连字符 `White-Jade` 不写，读起来更顺） |
| 亚克力 / PC 罩 | Acrylic / Polycarbonate Diffuser |
| 电镀 / 烤漆 / 阳极氧化 | Electroplating / Baked Enamel / Anodising |
| 防锈处理 | Anti-Rust Treatment |
| 毛刺 / 锐边 | Burrs / Sharp Edges |

**参数 / 性能**

| 中文 | 英文 |
|---|---|
| 灯体尺寸 / 出墙 / 底座 | Body Size / Projection / **Base**（第〇节固定文案，不用 Backplate） |
| 灯杆 | **Lamp Pole**（第〇节固定文案） |
| 灯罩 / 灯头环 / 挂板 | **Lampshade**（第〇节固定文案，不单写 Shade）/ Lamp Holder Ring / Mounting Bracket |
| 功率 / 流明 / 色温 | Power / Luminous Flux / Colour Temperature |
| 显色指数 / 全光谱 | Colour Rendering Index (CRI) / Full Spectrum |
| 色容差 / 流明维持率 | Colour Tolerance (SDCM) / Lumen Maintenance (L70) |
| 光电转换效率 | Photoelectric Conversion Efficiency |
| 蓝光危害 | Blue Light Hazard |
| 结温 / 加速老化测试 | Junction Temperature (Tj) / Accelerated Ageing Test |
| 防护等级 | IP Rating |
| 说明书 / 膨胀胶塞 / 自攻螺丝 / 端子台 | Instructions / Expansion Plugs / Self-Tapping Screws / Terminal Block |
| 火线接 L，零线接 N | live wire to L, neutral wire to N |
| 环境：客厅、卧室、餐厅、商业空间 | APPLICATION: Living Room, Bedroom, Dining Room, Commercial Space |

**标准 / 场景**

| 中文 | 英文 |
|---|---|
| 符合国际安全标准：IEC 60598 系列 | Compliant with International Safety Standards: IEC 60598 Series |
| GB 7000.1 / GB 17743 / GB/T 26572 | 原样保留 |
| II 类灯具 | Class II Luminaires |
| 客厅 / 卧室 / 餐厅 / 玄关 / 走廊 / 吧台 / 休闲角 / 商业空间 | Living Room / Bedroom / Dining Room / Entryway / Corridor / Bar / Lounge Nook / Commercial Space |
| 安装 / 产品信息 / 品质标准 / 注意事项 | Install / Product Information / Quality Standards / Notice |

## 七、颜色标准译名表（统一口径）

**颜色名一律照此表取值**，不逐字直译、不自由发挥。文档抬头「注」里要写明本型号用的是哪一个色名。

标 `*` 的是**同名多译色**（一个中文名对应两个色号），取值规则见下方 **7.1**，按产品材质判定。

| 中文 | English | 中文 | English |
|---|---|---|---|
| 砂岩黑 \* | Matte Black（材质无布） | 薄荷蓝 | Mint Blue |
| 雪地白 | Matte white | 胡桃色 | Walnut Brown |
| 铜本色 | Brushed brass | 烟灰 | Dark Gray |
| 香槟金 | Matte brushed gold | 柚木色 | Teak Brown |
| **珍珠镍** | **Matte brushed nickel** | 原木色 | Natural Wood |
| 亮色镍 | Bright brushed nickel | 落日橙 | Orange Gradient |
| 镜面铬 | Mirror Silver Plating | 活力橙 | Glossy Orange |
| 珍珠黑 | Black Chrome Plating | 雾松绿 | Glossy Green |
| 中国红 | Matte red | 铂石灰 | Smoked Chrome |
| 摩卡棕 | Matte brown | 冰萤石 | Clear Glossy |
| 活力橙 | Glossy Orange | 釉光白 | Glossy White |
| 奶霜白 | Glossy White | 岩霜白 | Frosted White |
| 莓果红 | Glossy Red | 亚麻白 | Linen white |
| 森林绿 | Glossy Green | 云母白 | Mica White |
| 奶油黄 | Cream Yellow | 砂岩黑 \* | Linen black（材质含亚麻布） |
| 樱花粉 | Sakura Pink | 卡其 | Khaki |
| 薰衣草紫 | Lavender Purple | 中国红 | Red |

### 7.1 同名多译：**先查产品材质表，判定不了就问用户**

色卡里有两个中文色名对应了两种英文，原因是它们**本质是两个色号共用一个中文名**。遇到这类色名，**不要按出现顺序取值**，按下面的规则判定：

| 中文色名 | 候选英文 | 判定规则（看产品材质表） |
|---|---|---|
| **砂岩黑** | `Matte Black`<br>`Linen black` | **看材质里有没有布**：<br>· 材质**只有金属**、无织物 → **`Matte Black`**<br>· 材质**含亚麻 / 布艺**（linen、fabric、布） → **`Linen black`**（「亚麻黑」这个色号本来指亚麻布本色染黑）<br>· 材质表里金属与布**同时出现**，或材质表看不出/缺失 → **停下来问用户确认**，不要替他选 |
| **中国红** | `Matte red`<br>`Red` | 同机制，按**材质与表面工艺**判定：金属磨砂 → `Matte red`；亮面或布艺 → `Red`。**此条尚未经用户裁定**，暂取 `Matte red`，遇到时先问。 |
| 活力橙 | `Glossy Orange`（两条取值一致） | 重复条目，无冲突，直接用。 |

**判定动作**（写进流程，不是凭印象）：
1. 从产品的**材质参数行**读材质，如 `MATERIAL: Glass, Metal` / `碳素钢灯杆` / `亚麻布灯罩`；
2. 出现 `布 / 亚麻 / linen / fabric / 织物 / 棉麻` 任一关键词 → 视为**有布**；
3. 材质里只有金属/玻璃/木/亚克力等非织物 → 视为**无布**；
4. 判不出来（材质行缺失、或金属与布同时出现）→ **问用户**，并在文首「注」里留痕。

⚠️ 另两条通则：
- 表里**没有**的颜色**先问用户**，不要自造。
- 同一色名在不同产品上必须给**同一个英文**（材质判定结果不同除外），否则海外买家会认为是两种颜色。

## 八、单位换算（保留 mm，追加英寸）

换算 `1 in = 25.4 mm`，**保留两位小数**，格式 `485mm (19.09in)`。

| mm | in | mm | in | mm | in |
|---|---|---|---|---|---|
| 25 | 0.98 | 135 | 5.31 | 300 | 11.81 |
| 40 | 1.57 | 150 | 5.91 | 485 | 19.09 |
| 75 | 2.95 | 160 | 6.30 | 500 | 19.69 |
| 100 | 3.94 | 210 | 8.27 | 600 | 23.62 |
| 120 | 4.72 | 225 | 8.86 | 1000 | 39.37 |
| 130 | 5.12 | 260 | 10.24 | 1200 | 47.24 |

写法：
- 直径带 Ø：`Ø135mm (Ø5.31in)`
- 高宽对：`Ø135 × H260 mm (Ø5.31 × H10.24 in)`
- 原图用 cm 的（`19.09in (48.5cm)`）**统一改写成 mm**，与参数表口径一致
- 参数表里的 `SIZE` 行同样补英寸，别只改正文

⚠️ 修改时**按整串替换**：`25mm` 是 `225mm` 的子串，逐最小单位替换会误伤。

## 九、不确定信息怎么处理

| 情况 | 处理 |
|---|---|
| 疑似品牌名 / 笔误（如「萨摩护眼灯光谱」） | 用中性表达 `Eye-Care Light Spectrum`，**在文档开头「注」里说明**，并在交付回复里请用户确认 |
| 图上数字没有明确归属（如 225mm / 25mm 未标注指向） | 按原图数字串**原样呈现并补英寸**，英文侧**不硬套** Shade Height / Backplate Depth 之类带归属的表述 |
| 图内已有英文与海外主推名不一致（角标写 Cohen，海外主推 Aisilan） | 保留原图英文，在交付回复里请用户示意是否改为 `Aisilan × Cohen` |
| 原图序号 / 标题疑似有误（如「三、五」与「二、四」重复） | **按原图忠实保留**，在文首「注」里标明「疑似有误，未自行改号」 |
| 数据缺失 | 写「暂无数据」，**禁止用 0 替代** |
| 图内没有任何可翻译文案 | 中文格写一句说明，**英文格写 `/`**（不要写英文说明句，会被误当上架文案） |

## 十、交付前自检清单

- [ ] **第〇节固定文案表是否逐字照抄**？（`Metal as the framework, light as the soul.` 的句末句号、
      `A single lamp, illuminates the reunion of three generations.` 的逗号都不能动）
- [ ] **跑过口径闸门了吗**：`python scripts/glossary_check.py <作业.json>` → 必须 `[PASS]`（退出码 0）；
      有 `[FAIL]` 一律先改文案，不要带着 FAIL 生成文档。
- [ ] 开工前是否问清了**品牌名**与**目标语言/风格**，并提醒了「可以传分好组的图，也可以传一整张长图」？
- [ ] 是否用**逐句中英对照表格**（一行一个句对，左中文右英文），而不是整段中文 + 整段英文？
- [ ] 并列规格行是否**每行一行**？长句是否没有硬拆？
- [ ] **尺寸板块是否一个尺寸一行**（有没有把多个尺寸挤进同一行）？**是否带了中文提示**
      「部位文案仅为定位作用，如原图只有尺寸则忽略该英文文案，只取用 mm 及 inch 尺寸。」？
      （`verify_docx.py` 里 `size rows` 应为 0、`tips` ≥ 尺寸块数）
- [ ] **部位文案是否连贯翻译成英文名词短语**（`碳素钢底座` → `Metal Base`、`白玉磨砂玻璃` → `Frosted White Jade Glass`）？
      有没有残留 `Base — Metal` 这类**破折号 / 斜杠拼接**（闸门 `glossary_check.py` 会 FAIL）？
- [ ] **无文案的行英文栏是否都是 `/`**？有没有残留 `This image carries only...` 这类会被误当文案的英文说明？
- [ ] **材质「碳素钢」是否已统一为 `Metal`**（不写 Carbon Steel）？**灯杆=`Lamp Pole`、底座=`Base`、灯罩=`Lampshade`** 是否都按第〇节走（没有 Lamp Post / Backplate / 单写 Shade）？
- [ ] **颜色是否全部取自色卡**（`verify` 时搜一遍还有没有 `Pearl Nickel`、`Carbon Steel` 之类的旧写法）？
- [ ] 用到**同名多译色**（砂岩黑 / 中国红）时，是否**先查了产品材质表**？材质只有金属、无布 → `Matte Black`；材质含亚麻/布艺或材质缺失 → **是否已经问过用户**（`color_caliber.py` 闸门返回非空就必须问，不得自行取值）？判定结论是否写进文首「注」？
- [ ] 表格是否每张都有**表头行 + 行分隔线**（`verify_docx.py` 的 `tcBorders` 项）？
- [ ] **行距是否够松**：单元格内 `line-height`（`w:spacing w:line`）+ 行内边距 `tblCellMar`（上下各 60dxa）是否都在？
- [ ] 重复角标是否**只在文首注里写一次（完整、加粗醒目），正文不再重复**，而且**至少留了这一处**（既不逐图灌水，也没有一处都不留）？
- [ ] 图内 `DESIGN BY xxx` 是否已替换成本次确认的品牌署名，并且注里提醒了设计端改原图？
- [ ] 意境类文案是否读起来像英文原创（不是中文语序）？
- [ ] 标准号、型号、认证是否原样保留且未漏项？
- [ ] 每个公制尺寸是否都补了英寸（图内出现的每一个数字）？
- [ ] 单位/符号是否统一（Ø、×、°C）？拼写风格（英式/美式）是否一致？
- [ ] 图注是否标注了切分位置（1/2、2/3），与切片一一对应？切点是否都目视复核过校验条带？
- [ ] 是否列出了 2-3 个需要用户核对的点？
