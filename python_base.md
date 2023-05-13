# 命名习惯
- **常量** 全大写，如多个单词，用下划线隔开, 如： `MAX_CONNECTION=100`
- **类名** 大驼峰命名，全部单词的首字母都大写，如： `class ClassName():`
- **函数、变量** 蛇形命名，单词全部小写，用下划线连接。 如： `max_value`

# print(...)输出
```python
print(*objects, sep=' ', end='\n', file=None, flush=False)
```
- 将 **objects** 打印输出至 **file** 指定的文本流，以 **sep** 分隔并在末尾加上 **end**。 
- sep、end、file 和 flush如果要提供参数值 必须以关键字参数的形式给出。
- file默认值为`None`， 表示打印输出到`sys.stdout`


### f-string 字符串拼接/格式化
**`f"xxx{var}"`** 是f-string格式化字符串常量（formatted string literals）的使用方式， 它是Python3.6 新增的，用大括号 **{ }** 表示被替换字段，是所有字符串格式中**速度最快的**，**推荐使用**
- **`f"xxx{var}"`** 如果 **`'`** 和 **`"`** 不足以满足要求，还可以使用 **`'''`** 和 **`"""`**
    ```python
    name = 'Xiaoming'
    a = f'Hello {name}'          # Hello Xiaoming
    b = f'Hello {name.upper()}'  # Hello XIAOMING
    print(a)
    print(b)
    print(f"直接在print函数里使用也是可以的{name}")
    ```
- **f-string**采用 **`{content:format}`** 设置字符串格式，其中 **content** 是替换并填入字符串的内容，可以是变量、表达式或函数等，**format** 是格式描述符。采用默认格式时不必指定 `{:format}`，如上面例子所示只写 `{content}` 即可。

以前老的字符串拼接有下面这3种方式，都不推荐使用
1. `+` 直接连接 `"abc" + "efg"`
2. `"***{}" .format(var,...)` 格式
    ```python
    a = "Hello, {}. You are {}.".format("dj", 100)   # Hello, dj. You are 100.
    b = "Hello, {1}. You are {0}.".format(100, "dj") # Hello, dj. You are 100.
    print(a)
    print(b)
    ```  
3. **`"***%" %(var,...)`** C语言风格的格式化。 格式化多个变量，需要把变量用括号括起来。 **不提倡使用。**
    ```python
    a= "abc%s, age=%d, efg=%.2f" %("100", 200, 33.3)
    print(a)  # abc100, age=200, efg=33.30
    ```





# `True` `False`真假判断 
`False`、`None`、`0` 以及所有数据结构的**空值**如`空列表[]`、`空元组()`、`空字典{}`、`空集合`等 (这些后面章节会介绍)，都会被解释器视为**假**，而其他值都视为**真**
```python
t = ()  # 空元组 tuple
l = []  # 空列表 list
d = {}  # 空字典 dict

s = set()   # {}是空字典，那空集合如何表达？空集合只能用set()函数转换或者直接设置

print(type(t), type(l), type(d), type(s))  # <class 'tuple'> <class 'list'> <class 'dict'> <class 'set'>
print(len(t), len(l), len(d), len(s))

# 输出 200
if None:
    print('100')
else:
    print('200')
```



# 运算符
### 除法`/`  取整除 `//`
- **`/`** 除法，结果是浮点数。  
    ```python
    print(10 / 5)  # 输出 2.0
    ```  
- **`//`** 取整除，返回商的整数部分。
    ```
    print(9 // 2)  # 输出 4
    ```

### `is` 和 `==` 的区别
在 Python 中**一切都是对象**，毫无例外整数也是对象，对象之间比较是否相等可以用 ==，也可以用 is。 `==`和 `is`操作的区别是：
- **`is`** 比较的是两个对象的id值是否相等，也就是比较俩对象**是否为同一个实例对象**，是否指向同一个内存地址。`a is b` 相当于 `id(a)==id(b)`，`id()` 能够获取对象的内存地址。

- **`==`** 比较的是两个对象的**内容是否相等**，默认会调用对象的 `eq()`方法。
>Python出于对性能的考虑，但凡是不可变对象，在同一个代码块中的对象，只有是值相同的对象，就不会重复创建，而是直接引用已经存在的对象。**但我们写代码的时候，不要依赖这种优化**， 而是要根据上面`is`和`==`的本意来使用。
```python
c = 257
def foo():
    a = 257
    b = 257
    print(a is b)  # true
    print(a is c)  # false

    print("id(a)", id(a))  # 输出 a 的内存地址， a 和 b的地址相同，所以是同一对象。
    print("id(b)", id(b))
    print("id(c)", id(c))  # c 的内存地址和a、b的不同

foo()
```

### 三元运算符 `X if C else Y`

```python
X if C else Y
```
**C** 是一个布尔表达式或条件语句，如果为真，则返回 **`X`** ；否则，返回 **`Y`** 。
```python
# 比较两个数字，输出较大的数字
a = 3
b = 5
max_num = a if a > b else b
print(max_num)  # 输出 5
```