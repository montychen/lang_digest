[Midjourney](https://www.midjourney.com/)

私信Midjourney Bot：这样就没有其它人打搅

第一行的前4个按钮 U1 U2 U3 U4 功能是将图片放大
- vary(region) 自定义重绘区域

第二行的4个按钮V1 V2 V3 V4 功能是对所选图片进行微整

# MJ prompts 构成： 风格 + 场景描述 
```prompts
(复古吉卜力风格)Retro Ghibli style, 。。。场景描述。。。 ,(角色设计图)character sheet , (白色背景)white background,  (让日式动漫风格更强烈) --niji 5
```
例如：
```
Retro Ghibli style,An energetic and youthful girl, aged 16-18, with a slender yet healthy physique, embodying the rustic charm of 19th-century rural England. She has round, curious eyes full of life, a small nose, and lips slightly upturned in a constant optimistic smile. Her attire is a simple cotton dress, perhaps in soft blue or green, harmonizing with the countryside, complemented by practical shoes or cloth boots, and possibly a plain apron. Her hair, light brown or golden, is tied into a simple ponytail or two braids, reflecting her vibrant and lively nature，character sheet , white background,  --niji 5
```

# AI制作漫画最大的挑战：维持角色外观的一致性

MJ处理这个问题比较常见的技巧：是先制作 **角色设计图 character sheet**


# Pan 平移： 让画布朝上下、左右4个方向进行延伸

`/settings`调出MJ的设定面板, 选中`Remix mode`混合模式。  这样在选择Pan按钮进行延伸的时候，我就可以干预， 加入自己的prompt

在延伸画布时，会参考本张画布原有的内容， 从而人物和服饰就会维持一致的风格。




full body 全身
turnaround 多视角
different expressions 不同表情