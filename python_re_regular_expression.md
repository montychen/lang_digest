python标准库自带的`re`模块提供了类似perl的正则表达式匹配方法，通过`import re`导入。

正则表达式是由基本字符、限定字符、位置字符、模式修正字符、特殊字符、大小写转换字符、方向引用字符、其他字符等构造出来的一种字符串。各种字符的类别、释义如下表所示。

## 普通字符串 & 原始字符串 & 正则转义

#### 1、普通字符串使用 **`\`作为转义字符**，
当普通字符串中出现反斜杠`\`，就会**自动尝试转义** 其后的字符：
  - 有对应的特殊字符，就完成转义，例如`"\n"`代表回车，`"\t"`代表制表符，而如果要输出反斜杠本身，就要用`\\`
  - 没有对应的特殊字符，就不会转义，继续维持原样。

#### 2、 `r"..."`原始字符串，不转义字符，所见即所得。
前缀是`r` 或者 `R`的字符串就是**原始字符串**，不再把 **`\`** 理解为转义字符，所见即所得。 因此 `r"\n"` 表示包含 `\` 和 `n` 两个字符的字符串，而 `"\n"` 则表示只包含一个换行符的字符串。

例如下面这个普通字符串的例子：`\W` 没有发生转义，因为 `\W`并不对应着特殊字符，不会转义，继续维持原样；中间的`\t` 会转义为制表符；最后的 **`\\\t`**, 前面两个`\\`转义成一个`\`, 后面的`\t`转义成制表符
```python
print('Hello\World\tPython\\\tmojo')  # 输出 Hello\World	Python\      mojo
```

如果现在要求变了，要求不对`\t`转义为制表符，而是原封不动输出为“Hello\World\tPython”，该怎么办呢？ 用原始字符串。
```python
print(r'Hello\World\tPython\\\tmojo')  # r表示这是原始字符串 Hello\World\tPython\\\tmojo
```
#### 3、正则转义，也是用`\`表示转义
正则表达式中也存在转义，姑且称其为**正则转义**，它也是用`\`表示转义，不过它的定义和**字符串转义**不同，比如`\d`匹配数字，`\s`匹配空白字符。
- 正则表达式也是用`\`表示转义， 所以在正则表达式的原始字符串里，用两个斜杠`\\`表示一个斜杠`\`

## 正则表达式
如果**正则表达式**使用的是**普通**字符串，则要先经过**字符串转义**，然后再到**正则转义**。

如果**正则表达式** 使用的是**原始**字符串，则没有**字符串转义**，而是直接到**正则转义**。

例子：用正则表达式提取 “3\8” 反斜杠之前的数字：
```python
import re

# 正则表达式 使用的是 普通字符串: 先字符串转义，在正则转义
match = re.search('(\d+)\\\\(\d+)', '3\8')
if match: print(f"{match.group(0)}, {match.group(1)} {match.group(2)}") # 3\8, 3 8

# 正则表达式 使用的是 原始字符串：直接进行正则转义
match = re.search(r'(\d+)\\(\d+)', '3\8')
if match: print(f"{match.group(0)}, {match.group(1)} {match.group(2)}") # 3\8, 3 8
```

>- **四合一 `"\\\\"`**：正则表达式`"\\\\"`用的是普通字符串表示，所以先经过**字符串转义**，前两个和后两个斜杠分别被转义成了一个斜杠，就得到两个斜杠`"\\"`； 然后**再进行正则转义**，也是两个斜杠`\\`表示一个`\`
>- **二合一** `r"\\"`：正则表达式`r"\\"`用的是原始字符串表示，所以**直接进行正则转义**，也是两个斜杠`\\`表示一个`\`




### `re`常用函数
- `re.match(pattern, string, flags=0) -> Match`: 是**从头开始匹配**的，而且是匹配到一个就返回，后面的就不会再尝试匹配了；如果字符串开头不满足正则表达式，就不会匹配成功，如果匹配不到就会返回`None`。如果你想从 string 的任意位置开始匹配，要用 `search()`。
- `re.search(pattern, string, flags=0) -> Match`: 和match()差不多，不同的就是可以不从头开始匹配，可以**从string的任意位置开始尝试匹配**，只要匹配到一个结果就结束。匹配不到就会返回`None`。

- `re.sub(pattern, repl, string, count=0, flags=0) -> str`: 替换满足条件的字符串，即匹配到pattern后替换为`repl`，也可以是个函数。，

- re.findall():搜索所有满足条件的字符串
  
```python
import re 

text = "DJ is  a   handsome    boy"

# 将字符串中的空格 ' ' 替换成 '-'
str1 = re.sub(r"\s+", '_', text)     # DJ_is_a_handsome_boy
# 还可以使用 lambda 指定repl， 例如：将字符串中的空格 ' ' 替换成 '[ ]'
str2 = re.sub(r'\s+', lambda m: '[' + m.group(0) + ']', text, 0) # DJ[ ]is[  ]a[   ]handsome[    ]boy
print(str1)
print(str2)

```
  


#### `group()`获取匹配的内容
在正则表达式中，通过圆括号`( )`可以创建一个或多个**分组**，分组从 **1** 开始计数。
- `group()`或者`group(0)` 获取整个匹配的内容
- `group(1)` 获取第一个分组的内容(第一个括号)
- `group(n)` 获取第n个分组的内容(第n个括号)
- 如果正则表达式返回的是`None`，没有匹配成功，使用`group()`会报错

```python
import re

# 用 ( ) 创建了 3个分组
pattern = r'(\d{4})-(\d{1,2})-(\d{1,2})'   # 匹配日期格式  yyyy-mm-dd 或者 yyyy-m-d
date_string = '今天是 2024-05-8'

match = re.search(pattern, date_string)

if match:
    print("整个匹配的内容:", match.group())   # group()获取整个匹配的内容 2024-05-8
    
    print("年:", match.group(1))    # 第一个分组的内容 2024
    print("月:", match.group(2))    # 第二个分组的内容 05
    print("日:", match.group(3))    # 第三个分组的内容 8
else:
    print("没有匹配的内容")
```




## 正则表达式，如何去匹配字符串里的 `\` 和 `\\` 
普通字符串使用`\`作为转义字符，所以当字符串中如果出现反斜杠，则会自动转义其后的字符，例如`"\n"`代表回车，`"\t"`代表制表符等。
- 普通字符串用2个斜杠表示1个斜杠，即 `"\\"` 代表1个斜杠 `\`
- **原始字符串**里1个斜杠就表示1个斜杠, 因为原始字符串没有转义。 不过1个斜杠不能单独出现使用，所以仅有1个斜杠的时候，就要用2个斜杠来表示。
- 正则表达式里1个斜杠 **`\`** 是转义字符。

如果反斜杠`\`作为字符字面量（liberal）出现在字符串中，应该如何处理？

- re正则表达式，如果是原始字符串，就用2个斜杠匹配1个正常字符串里的斜杠。即 `r"\\"` 匹配 `"\"`
- re正则表达式，如果是普通字符串，就用4个斜杠匹配1个正常字符串里的斜杠。 即  `"\\\\"` 匹配 `"\"`

### flags 标志
- re.I (re.IGNORECASE): 忽略大小写
- re.M (re.MULTILINE): 多行模式，改变 `^` 和 `$` 的行为。 
  - 在默认情况下，`^` 只匹配字符串的开头，而`$`只匹配字符串的末尾和紧接在字符串末尾（可能存在的）换行符之前。
  - 在指定` re.M`之后， `^` 将匹配字符串的开始和每一行的开头（紧随在换行符之后）； `$` 将匹配字符串的末尾和每一行的末尾（紧接在换行符之前）。
- re.S (re.DOTALL): 默认 `.` 将匹配除去换行符以外的任意字符。在指定 `re.S `后，`.`将匹配任意字符，包括换行符；
- re.X (re.VERBOSE): 详细模式。这个模式下正则表达式可以写成多行，表达式中的空白符会被忽略，并可以加入注释。例如下面2个正则表达式是一样的。



### 正则表达式
![标量、向量、矩阵、张量的关系](./res/python_re.webp)