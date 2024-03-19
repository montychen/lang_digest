<style>
pre {
    white-space: pre-wrap;
    word-wrap: break-word;
}
</style>

[Midjourney](https://www.midjourney.com/)

私信Midjourney Bot：这样就没有其它人打搅

- U1 U2 U3 U4 功能是将图片放大
- V1 V2 V3 V4 功能是对所选图片进行微整

- vary(region) 局部重绘，自己选择重绘区域



**prompts关键词**：切记，一组关键词间要用**英文的逗号`,`和一个空格**进行分隔。


# MJ prompts 构成： 风格 + 场景描述 

```prompts
(复古吉卜力风格)Retro Ghibli style, 拍摄角度 + 。。。场景描述。。。 + (角色设计图)character sheet , (白色背景)white background,  (让日式动漫风格更强烈) --niji 5
```
例如：
```
低角度、前视角，在19世纪的英国牧场，一个年轻的女孩拿着柳条篮，羊在背景中吃草，清晨，清澈的蓝天
```
low-angle, front view of a young girl in a 19th-century English pasture holding a wicker basket, sheep grazing in the background, early morning, clear blue sky

<pre style="white-space: pre-wrap; word-wrap: break-word;">
Retro Ghibli style,low-angle, front view of a young girl in a 19th-century English pasture holding a wicker basket, sheep grazing in the background, early morning, clear blue sky white background,  --niji 5
</pre>

# AI制作漫画最大的挑战：维持角色外观的一致性 `consistent style`
[使用这个B站视频提到的办法](https://www.bilibili.com/video/BV13u4y1r75u/?spm_id_from=333.337.search-card.all.click&vd_source=d1bae303e273c3b02ddcd7baf6b6a596)

### 人物一致性功能 `--cref url` 角色参考 Character Reference: 它的核心是`侧重维持人`的一致性

与`风格参考--sref`功能类似，`--cref`也是通过匹配参考图片来生成新的图像。但不同之处在于，`--cref`专注于匹配参考图片中角色的特征，如面部、发型和服装等，而不是整体风格。
- `--cw 数字` 可以用来调整一致性的“强度”，范围从0到100。默认强度为100，系统会参考人物的脸部、发型和衣着。将强度设置为0时，系统只会关注脸部，这对于更换服饰或发型很有帮助。

### `--sref url`  风格参考 style references：维持总体的一致性，不专门针对`人`

在正常prompts 后面加 `--sref 一张图片在MJ的url地址`(可以多张), MJ就会参考这张图片的风格、生成吻合内容(包括：风格、构图、颜色、光效、颜色。。。)
- `--sref`只在 v6 和 niji v6 及以上版本可用。 可以理解成是MJ 图生图
- 
- `--sref` 后面可以跟多张图片的url， 关键是用**空格来分隔**url。如：`--sref url1  url2`
  - 如果`--sref`后面跟了多个图的url，那么可以用` ::数字`，来声明每张图对结果的影响。如`--sref url1 ::5 url2 ::2`
- 后面还可以再加`--sw 数字` 控制所生成内容和原图的匹配程度，取值范围是`0--1000`。 数字越大，参考图对结果影响就越大；简单说就是值越大就越像。如：`--sref url --sw 20`

例子：
1. 先在MJ上传这张图片, 并获取它在MJ的URL地址

<img src="res/卡通.png" width="300"/>

2. 在`--sref`参数后面附上这张图片的URL，生成和这张照片风格一致的内容
```
a cute girl --niji 6 --sref https://s.mj.run/ZJzkg7D9pOA
```
<img src="res/sref_mj风格一致.webp" width="500">

3. 还可生成同样风格的其它动物，比如，狗
```
cute cat --niji 6 --sref https://s.mj.run/ZJzkg7D9pOA
```
<img src="res/sref_mj风格一致dog.webp" width="500">




### Pan 平移： 让画布朝上下、左右4个方向进行延伸
在延伸画布时，会参考本张画布原有的内容， 从而人物和服饰就会维持一致的风格。

- `/settings`调出MJ的设定面板, 选中`Remix mode`混合模式。 这样在选择Pan按钮进行延伸的时候，可以额外加入自己的prompts提示词进行干预。
- 在弹出的prompts输入框加入 **character sheet**角色设计图。 以及加入自己需要的promts， 比如添加多视角，人物不同的表情或动作。
  - full body 全身
  - turnaround 多视角
  - different expressions 不同表情

### 把预先上传到MJ的图片地址，放在提示词prompts前面， MJ就会生成吻合这些图片的东西

- 先把一些图片上传到MJ, 拷贝这些图片的MJ地址，一行一个。
- 然后把这些图片地址放在提示词prompts前面，MJ就会生成吻合这些图片的东东。

例如：
<pre>
图片在MJ的地址url1
图片在MJ的地址url2
。。。
图片在MJ的地址urln
Retro Ghibli style,low-angle, front view of a young girl in a 19th-century English pasture holding a wicker basket, sheep grazing in the background, early morning, clear blue sky white background,  --niji 5
</pre>

### 先用普通提示词生成图片， 然后再通过`vary(region) 局部重绘`进行替换
- `/settings`调出MJ的设定面板, 选中`Remix mode`混合模式。这样就可以额外加入自己的prompts提示词进行干预。
- 先用普通提示词生成图片， 选择`vary(region) 局部重绘`，选择需要重绘区域。
- 在提示词前面加入**图片在MJ的地址url**， 这样就会用这张图片对应的部分，对所选区域进行重绘。
例如：
<pre>
图片在MJ的地址url
Retro Ghibli style,low-angle, front view of a young girl in a 19th-century English pasture holding a wicker basket, sheep grazing in the background, early morning, clear blue sky white background,  --niji 5
</pre>


# 用chatGPT自动把`中文`翻译成`MJ的Prompt`
用下面这个命令，告诉chatGPT如何做：
<pre>
从现在开始，你是一名中英翻译，你会根据我输入的中文内容，翻译成对应英文。请注意，你翻译后的内容主要服务于一个名叫midjourney的绘画AI，它只能理解具象的描述而非抽象的概念，同时根据你对绘画AI的理解，比如它可能的训练模型、自然语言处理方式等方面，进行翻译优化。由于我的描述可能会很散乱，不连贯，你需要综合考虑这些问题，然后对翻译后的英文内容再次优化或重组，从而使绘画AI更能清楚我在说什么。请严格按照此条规则进行翻译，也只输出翻译后的英文内容。 例如，我输入：一只想家的小狗。 你不能输出： /imagine prompt: A homesick little dog. 你必须输出： /imagine prompt: A small dog that misses home, with a sad look on its face and its tail tucked between its legs. It might be standing in front of a closed door or a gate, gazing longingly into the distance, as if hoping to catch a glimpse of its beloved home. 如果你明白了，请回复"我准备好了"，当我输入中文内容后，请以"/imagine prompt:"作为开头，输出翻译后的英文内容。
</pre>


# 连贯动作
[参考文章1](https://www.uisdc.com/consistent-character-midjourney)
想要创建迷人的连贯动作，那么你需要在提示词当中加入如下关键词：

- Coherent action (连贯动作)
- Narrative sequence style（遵循叙事顺序）

然后再使用「panning」这一功能来拓展出更多的动作

### 提示词模板：
<pre>
Coherent action of [ 你要生成的角色 ] [ 角色的行为 ] , [ 角色的服装风格和细节 ] , multiple poses, facial expressions, coherent action poses, narrative sequence style, plain background
</pre>

#### 例子：
年轻的姑娘采用连贯动作跳舞，穿着红色的连衣裙，多种姿势，面部表情，连贯的动作姿态，叙事顺序风格，简单背景
<pre>
Coherent action of a beautiful young lady dancing, in a red dress, multiple poses, facial expressions, coherent action poses, narrative sequence style, plain background --ar 16:9 --niji  --s 180
</pre>



# MJ 常用命令
- `/imagine prompt ` 最常用的文生图命令
- `/describe img_url`  图生文指令。 不仅能分析所上传图片的画面内容， 还能精确的描述画面整体风格。
- `/blend` 多张图片融合, 最多6张，把上传的图片融合一起生成新的图片
- `/subscribe` 显示个人订购页面的链接；`

# MJ 常用参数
`--niji` 日本动漫风格模型, 是Midjourney 跟 Spellbrush 一起开发的。
`--ar`  指定生成图片的长宽比，例如：`--ar 9:16` 手机竖屏