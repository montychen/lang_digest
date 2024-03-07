# 命名习惯
- **常量** 全大写，如多个单词，用下划线隔开, 如： `MAX_CONNECTION=100`
- **类名** 大驼峰命名，全部单词的首字母都大写，如： `class ClassName():`
- **函数、变量** 蛇形命名，单词全部小写，用下划线连接。 如： `max_value`

### python关键字，大写开头的关键字3个：`True/False`、`None`
Python 的关键字列表可以在 `keyword` 模块中找到， `keyword.kwlist`可以列出所有关键字。 其中**大写开头的关键字有3个**：`True/False`、`None`
```python
import keyword

print(keyword.kwlist)
```
输出：
```
['False', 'None', 'True', 'and', 'as', 'assert', 'async', 'await', 'break', 'class', 'continue', 
'def', 'del', 'elif', 'else', 'except', 'finally', 'for', 'from', 'global', 'if', 'import', 'in', 
'is', 'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'try', 'while', 'with', 'yield']
```
### 私有变量 or 方法
Python通过编码规范而不是语言机制来完成封装，具体而言，Python规定了对变量命名的公约，约定什么样的变量名表示变量是私有的，不应该被访问(而不是不能被访问)。
- 以`_`**单下划线开头**的成员变量或方法，是设计者不想暴露给外部的API，使用者不应该进行访问。 如果执意要访问该变量，**直接通过这个名字还是`可以访问`的。**
- 以`__`**双下划线开头**而且**最多一个下划线`_`结尾**的成员变量或方法，会进行名称转写。如果执意要访问该变量，**直接通过这个名字是`访问不了`的**，因为已经被改写成其它名称了。


### 为什么需要名称转写
**名称转写(name mangling)**：以双下划线开头，并以**最多**一个下划线`_`结尾的标识符，例如__X，会被转写为_classname__X，其中classname为类名。这个机制实现起来非常简单，而且很大程度避免了调用者的误访问，但并不能像Java的private限定符那样完全杜绝外部的访问。
```python
 class A():
     def __init__(self):
         self.__private_var = 7
 ​
 >>> a = A()
 >>> print(a.__private_var)
 AttributeError:
     'A' object has no attribute '__private_var'
 >>> print(a._A__private_var)
 7
```
需要注意的是，Python的魔术方法，比如__len__, __bool__等不受此限制，因为它们均以双下划线结尾。

既然单下划线开头的变量名约定足以提醒调用者这是一个非公开变量，为什么还需要双下划线开头的变量进行名称转写呢？这涉及到面向对象中另一个重要概念:**继承**。

在Java中，声明为private的成员不会从父类被继承到子类，而Python中没有这样的强制机制。而进行`名称转写`则**能有效避免子类中方法的命名冲突**。

举一个具体的例子，我们知道，定义子类的时候，经常会调用父类的__init__()方法，假如父类的__init__()方法调用了父类的非公开函数__initialize()，当我们在子类中也需要__initialize()函数时会造成父类__init__()的异常行为，而名称转写避免了这一冲突，父类的__init__()实际上调用的是_父类名_initialize()。

### 双下划线开头和结尾 的魔法方法Magic Methods
**双下划线开头和结尾**的魔法方法Magic Methods是Python**内置**的特殊方法，这些方法在进行特定的操作时会**自动被调用**，也称为双下划线方法(Dunder Methods)，例如：
  - **`__init__`对象构造函数**
  - **`__del__`** 类的析构函数
  - **`__call__(self, *args)`** 使对象的实例能够像函数一样被调用，同时不影响实例本身的生命周期
  - **`__iter__()`** 如果一个对象实现了这个方法，那么该对象就是一个可迭代对象iterable
> 单后缀下划线: 如果我们定义的名称和Python已有的关键字（如class，sum之类的）冲突, 那么可以在名称后面加一个下划线 **`_`** 来解决名字冲突。 但是不建议这样命名，容易引起混淆。

# print(...)输出
```python
print(*objects, sep=' ', end='\n', file=None, flush=False)
```
- 将 **objects** 打印输出至 **file** 指定的文本流，以 **sep** 分隔并在末尾加上 **end**。 
- sep、end、file 和 flush如果要提供参数值 必须以关键字参数的形式给出。
- file默认值为`None`， 表示打印输出到`sys.stdout`


# f-string 字符串拼接/格式化
**`f"xxx{var}"`** 是f-string格式化字符串常量（formatted string literals）的使用方式， 它是Python3.6 新增的，用大括号 **`{ }`** 表示被替换字段，是所有字符串格式中**速度最快的**，**推荐使用**
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





# `True` `False`真假判断 以及 `None`
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

### `None`
Python 中是没有 NULL 的，但存在相近意义的 `None`,它的类型是`NoneType`。在 Python 中， 我们可以使用 `None` 来表示一个空值，它具有以下特征。
- `None` 是一个特殊的 Python 对象，本身是占用一定内存的。
- `None` 不支持任何运算，也没有任何内建方法。
- `None` 和 0、空字符串、空列表是不一样的。
- `None` 和任何其他数据类型比较，都会返回 False。
- 一个函数没有使用 return 来显式返回一个值，那么 Python 就会自动在末尾加上一个 **`return None`**。


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
- **`is not`** 判断两个标识符**不是同一个对象**， `x is not y` ， 类似 `id(a) != id(b)`
>Python出于对性能的考虑，但凡是不可变对象，在同一个代码块中的对象，只有是值相同的对象，就不会重复创建，而是直接引用已经存在的对象。**但我们写代码的时候，不要依赖这种优化**， 而是要根据上面`is`和`==`的本意来使用。
```python
c = 257
def foo():
    a = 257
    b = 257
    print(a is b)  # true
    print(a is c)  # false
    print(a is not c) # true

    print("id(a)", id(a))  # 输出 a 的内存地址， a 和 b的地址相同，所以是同一对象。
    print("id(b)", id(b))
    print("id(c)", id(c))  # c 的内存地址和a、b的不同

foo()
```

### 三元/三目运算符
```python
exp1 if contion else exp2
```
condition 是判断条件，**exp1** 和 **exp2** 是两个表达式。如果 condition 结果为真，就执行 exp1，**并把 exp1 的结果作为整个表达式的结果**；如果 condition 结果为假，就执行 exp2，并把 exp2 的结果作为整个表达式的结果。

**用三元运算符：赋值**

a 是3， b是5， 所以 a> b 不成立，就把 b 作为整个表达式的值，并赋给变量 max_num。
```python
a, b = (3,5)
max_num = a if a > b else b
print(max_num)  # 输出 5
```
**用三元运算符：选择性的执行语句**

if 的判断条件为假，所以执行了 `else`后面的语句，pirnt语句没执行，所以看不到输出
 ```python
 print("执行else，所以这行的输出看不到") if 100<10 else None  # 看不到任何输出
 ```



# for 循环
在 Python 中，编写循环有两种方式:`for` 和 `while`，大多数情况下都 是使用 for 循环，而很少会去使用 while 循环。这是因为 for 循环使用起来，比 while 循环更加 简单方便。
```python
for 循环变量 in 可迭代对象iterable:
    循环代码块
```

例如， **`for i in range(n)`** n 是一个正整数。

### `for/while`循环的 `else`语句
在 Python 中，也可以在 while 循环或 for 循环中加入 else 子句。这是一种非常罕见的用法，只在 Python 这门语言中见 过，但这个功能是绝对值得拥有的。
```python
for 循环变量 in 可迭代对象iterable:
    循环代码块
else:
    代码块
```

```python
while 判断条件:
    循环代码块
else:
    代码块
```

如果一个循环语句后面接的有`else`语句，只有当**循环条件正常结束时**，**`else` 子句中的代码才会执行**。如果在循环结构中执行了 `break` 语句或发生了异常(即报错)，`else `子句中的代码都不会执行。

例如下面的例子，由于while循环中执行了`break`语句，所以`else`语句没有执行，程序输出的是： 5
```python
i=0
while i < 10:
    if i == 5: 
        print(i)
        break   # 执行了`break`语句，所以下面的`else`语句没有执行，程序输出的是： 5
    i += 1
else:
    print('Normal end!')
```

考虑下面这个例子，如果我们需要在一个列表中找到指定的数字，如果找到了就跳出循环。打印"找到了"，反之打印”没找到“。对于这个功能，相信你可能会这么写。
```python
nums = [1,2,3,4,5,6]
target = 5
flag = False
for n in nums:
    if n == target:
        flag = True
        break
if flag:
    print("找到了")
else:
    print("没找到")

# 程序输出： 找到了
```

但是如果你熟悉Python的for-else语法，那么我们可以把上述代码改成这样：
```python
nums = [1,2,3,4,5,6]
target = 4
for n in nums:
    if n == target:
        print("找到了")
        break
else:
    print("没找到")

# 程序输出： 找到了
```

# 可迭代对象iterable 和 迭代器iterator
**可迭代对象iterable**最重要特征就是可以使用 `__iter__()` 方法或 全局内置函数`iter()` 来获取它对应的迭代器iterator
```python
nums = [1, 2, 3, 4, 5]

# nums.__iter__() 和 iter(nums) 是等价的，都可以获取 nums 对应的迭代器。
print(nums.__iter__())
print(iter(nums))
```

可以使用 `__next__()` 方法或内置函数 `next()` 来获取下一次的迭代结果。

- 如果一个对象实现了 `__iter__()` 方法，该对象就是一个**可迭代对象iterable**
- 如果一个对象同时实现了 `__iter__()` 和 `__next__()` 方法，该对象就是一个**迭代器iterator**。


### `yield` 和 生成器函数 generator
在 Python 中，这种一边循环一边计算的机制，称为生成器（Generator）。

**生成器函数**是一种在函数内含有`yield`语句的特殊函数。在函数中使用 **`yield`** 语句来生成一个值并返回，然后**暂停函数执行并保留当前状态**，等待下一次调用时才会继续往下执行。生成器函数的优点是可以处理大量数据，因为它们只需要在内存中保存一个值，而不是全部保存在内存中。

  >`return` 语句会立即终止函数的运行并返回值。
```python
def get_even(n):
    for i in range(0, n):
        if i % 2 == 0: 
            yield i
            
for i in get_even(8):
    print(i)            # 输出  0  2  4  6  
```

**生成器是一种惰性的可迭代对象**，可以使用它来代替传统列表，从而节省内存和提升执行效率。

假设你要读取并处理数据流或大文件，如果按照下面的写法。 那么将会得到内存溢出的报错。原因就在 `file.read().split("\n")` 一次性将所有内容加载到内存中，导致内存溢出。
```python
def csv_reader(file_name):
    file = open(file_name)
    result = file.read().split("\n")
    return result
```
为了解决这个问题，可以改用生成器写。通过遍历，加载一行、处理一行，从而避免了内存溢出的问题。
```python
def csv_reader(file_name):
    for row in open(file_name, "r"):   # 缺点：没有关闭文件， 用下面 with ... as 会自动关闭文件
        yield row                      # 通过遍历，加载一行、处理一行，从而避免了内存溢出。
```
- **`yield`** 关键字是用来创建Generator生成器的，generator是**一种集合类型**，可以使用 **`list()`** 等函数把**生成器**转换为其他容器类型，并且还 可以使用 next() 函数来不断获取下一个值。
```python
import sys
nums = (n * 2 for n in range(1, 600))   # 元组生成器, 惰性的
print(nums)                 # <generator object <genexpr> at 0x109a5c9e0>
print(sys.getsizeof(nums))  # 这是惰性生成器，占用很少的空间， 只有 104
print(list(nums))           # 用 list()把 生成器 转换为其他容器类型
```

# 生成器表达式 & 推导式
可变类型如**列表list、字典dict、集合set等，可以使用推导式**的方式来生成。而不可变类型如元组、 字符串等，是无法使用推导式语法的。但是对于元组而言，可以使用类似的方式来生成生成器**元组生成器**。

#### 生成器表达式
```python
生成器表达式 = (表达式 for 变量 in 可迭代对象 if 条件)  # 如果要加条件，要把条件放在最后，不然会报错。
```
**生成器表达式**类似于列表推导式，但**使用圆括号`(...)`而不是方括号`[...]`**，并且**返回的是一个生成器对象而不是一个列表**。 生成器对象可以通过迭代访问，但不必事先将所有元素保存在内存中。


#### 推导式
```python
列表推导式 = [ 表达式 for 变量 in 可迭代对象 if 条件 ]  # 如果要加条件，要把条件放在最后，不然会报错。
集合推导式 = { 表达式 for 变量 in 可迭代对象 if 条件 }
字典推导式 = { key表达式: value表达式 for 变量 in 可迭代对象 if 条件 }
```
例子：
```python
# 列表推导式
nums = [3, 9, 1, 12, 50, 21]
lst = [num for num in nums if num > 10]  # 给列表推导式加上判断条件，需要把条件放在最后
print(lst)  # [12, 50, 21]

# 集合推导式, 集合是没有重复元素的
s = {x for x in 'abracadabra'}   
print(s)    # {'a', 'b', 'c', 'd', 'r'}

# 字典推导式
dic = {x: x**2 for x in (2, 4, 6)}
print(dic)  # {2: 4, 4: 16, 6: 36}
```


#### 生成器表达式 vs 列表推导式 
- **生成器表达式**返回的是生成器对象而不是一个列表，在内存中保存的只是一个生成器对象，所以**内存占用是很少**的。 
- **列表推导式**是直接生成整个列表， 所有的元素数据全部都保存在内存中，所以占用的内存空间就是全部列表元素的空间，因此**内存消耗大**。
```python
import sys

#生成器表达式 (...)
nums_g = (n * 2 for n in range(1, 600))
print(nums_g)     # 生成器表达式返回的是生成器对象而不是一个列表 <generator object <genexpr> at 0x109a5f300>
print(sys.getsizeof(nums_g))   # 内存占用 104 个字节

# 列表推导式 [...]
nums_l = [n * 2 for n in range(1, 600)]
print(nums_l)     # 列表推导式是直接生成整个列表 [2, 4, 6, 8, 10, 12, 14, 16, 18, 20,.......
print(sys.getsizeof(nums_l))  # 内存占用 5432 个字节
```
- 生成器表达式可以节省内存空间，但是如果需要多次使用生成器对象中的值，可以使用 **`list()`** 等函数把**生成器**转换为其他容器类型
- 生成器表达式中的变量作用域只在生成器表达式内部，不会泄露到外部。
    ```python
    x = 10
    gen = (x for x in range(1, 5))
    print(list(gen))    # 把生成器转换成列表list， 输出 [1, 2, 3, 4]
    print(x)    # 输出 10，说明 x 只在生成器表达式内部存在，不会影响外部变量 x 的值。
    ```



# 序列(sequence): 列表list、元组tuple、字符串
在 Python 中，序列有 3 种: 列表、元组和字符串。这三种序列的很多方法都是相似的。

### 列表list
定义一个空列表 `list_obj = []`
  
为什么 Python 把这种数据结构叫作**列表**，而不是叫作**数组**呢? 其实 Python 中也存在叫作“数组”的数据结构。其中，列表 这种数据结构是Python自带的，但是数组却需要引入numpy模块才能使用。numpy是数据分析中必备的一个模块。列表和数组这两种数据结构非常相似，但也存在以下 3 点区别。
- 数组元素的数据类型必须相同，但是列表元素却不需要。
- 数组可以进行四则运算，但是列表不可以。
- 数组和列表的很多操作方法不一样。
  
**列表中的元素可以是不同的数据类型**，这一点跟其他语言中的数组不太一样。
```python
lst = [1, 2, 'Python', True, False]
```



#### 列表添加元素
- `list_obj.insert(index, item_value) `方法是在列表的“index位置”插入一个新元素。
- `list_obj.append(item_value)` 方法是在列表的“末尾”增加一个新元素。

#### 列表删除元素
- `del list_obj[index]`
  ```python
    animals = ['11', '22', '33'] 
    del animals[2]
    print(animals)    # ['11', '22']
  ```
- `list_obj.pop(index)` 删除列表中的某一个元素，如果不指定index默认是最后一个元素， 并且返回该元素的值。 注意的是，`pop() `会修改原列表。
  ```python
    animals = ['11', '22', '33'] 
    animals.pop()
    print(animals)    # ['11', '22']
  ```
- `list_obj.remove(item_value)`是**根据值来**删除元素的。如果列表存在多个相同的值，那么 `remove() `只会删除“第一个匹配到的值”，**如果指定的元素不存在，就会报错**。为了避免这种情况，我们最好先判断元素是否存在。 同样 `remove() `也会修改原列表。
  ```python
    animals = ['11', '22', '33', '11'] 
    animals.remove('11')    # 存在两个 '11'，只会删除第一个匹配上的元素。
    print(animals)    # ['22', '33', '11']
  ```

#### 将列表中的所有元素连接成一个字符串 `join`
- **`str.join(list_obj)`** str 是一个连接符，它是可选参数，表示连接元素之间的符号。
    ```python
    alist = ['11', '22', '33'] 
    result1 = ''.join(alist)
    result2 = ','.join(alist)
    print(result1)  # 112233
    print(result2)  # 11,22,33
    ```

#### 合并列表:`extend()` 和 `+` 
- **`alist_ojb.extend(blist_obj)`** 表示将列表 blist_ojb 合并到列表 alist_obj 中，最终**会改变列表 alist_ojb 的值**。
    ```python
    nums1 = [1, 2, 3]
    nums2 = [4, 5, 6]
    nums1.extend(nums2)    # 将 nums2 合并到 nums1 中，最后 nums1 的值会改变
    print(nums1)  # [1, 2, 3, 4, 5, 6]
    ```
**`alist_obj + blist_ojb`** 列表相加 **` + `** **不会修改原列表**，如果想要得到合并后的列表，我们需要使用一个新的变量来保存。
    ```python
    nums1 = [1, 2, 3] 
    nums2 = [4, 5, 6] 
    result = nums1 + nums2 
    print(nums1)    # [1, 2, 3]
    print(result)   # [1, 2, 3, 4, 5, 6]
    ```

#### 乘法 `*`
- **`list_obj * n`**列表只能跟正整数n相乘，表示重复多次，但是不能跟另外一个列表相乘。
    ```python
    result1 = [1, 2] * 3
    print(result1)  # [1, 2, 1, 2, 1, 2]
    ```

#### 二维列表

```python
nums = [[10, 20, 30], [40, 50, 60], [70, 80, 90]]
print(nums[0][0])   # 10
print(nums[1][1])   # 50
print(nums[2][2])   # 90
```
|       |     |    |
|  ----   | ----  | ---- |
|  10     | 20    | 30   |
|  40     | 50    | 60   |
|  70     | 80    | 90   |


### 元组tuple
元组的元素不能修改，而列表的元素可以修改。可以把元组`tuple`看成是一种特殊的列表`list`
- 定义一个空元组 `t = ()`
- 只有**一个元素的元组**，必须在元素后加一个英文逗号 **`,`** 例如`t = ("aaa",)`
- 也可以去掉括号，提供以逗号分隔的多个对象， 如定义元组t： `t = 1, 2.5, 'data'`
- 因为元组是不可变的， 所以元组也不存在列表推导式这样的语法。


# lambda

```python
lambda arg1,arg2...argn: expression
```
`lambda` 可以使用**任意数量的参数**，但只能包含**一个表达式**的匿名函数。

貌似在下面这个例子里， 列表推导比使用lambda更简单。

```python
numbers = [1, 2, 3, 4, 5]
a = list(map(lambda n: n+1, numbers))  # 使用 lambda。  map(func, iterable, ...) func是一个函数,iterable表示可迭代序列。map()把iterable的每个元素作为参数逐个调用func
b = [x + 1 for x in numbers]         # 使用 列表推导

print(a)   # [2, 3, 4, 5, 6]
print(b)   # [2, 3, 4, 5, 6]
```

### 用lambda排序
例1： 在下面这个排序函数里， 貌似只能用lambda不能用 列表推导
```python
users = [
    {"name": "Yack", "age": 21},
    {"name": "Lucy", "age": 19},
    {"name": "Aony", "age": 20}
]
result = sorted(users, key=lambda user: user['age'])  # lambda表达式指定用 age 字段进行排序
print(result)
```

例2： 用lambda指定按平均分进行排序， 平均分(用//取整) = score[1][0]//len(score[1][1])
```python
# 字典 {  "11": [sum, [100,70,90]],     "22":[sum, [65,100,80]]   }  转成
# 列表 [ ("11", [sum, [100,70,90]),    ("22":[sum, [65,100,80])   ]
score_dict = {
    '0024': [620, [110, 135, 110, 60, 105, 100]],
    '5215': [495, [100, 110, 65, 80, 40, 100]],
    '2851': [520, [90, 115, 105, 60, 80, 70]],
    '8330': [280, [145, 135]]
}

score_list= list(score_dict.items())  # 字典是无序的，不能排序； 先把字典转成列表

 # 按平均分进行排序， 平均分 = score[1][0]//len(score[1][1])
sorted_score_list = sorted(score_list, key = lambda score: score[1][0]//len(score[1][1]), reverse=True)
print(sorted_score_list)

for index, row in enumerate(sorted_score_list):
    row[1][1].reverse()
    test_times = len(row[1][1])  # 考试次数
    print((index+1), "\t", row[0], "\t", row[1][0], "\t", row[1][0]//test_times, "\t", test_times, "\t", row[1][1])
```
输出：
```
[('8330', [280, [145, 135]]), ('0024', [620, [110, 135, 110, 60, 105, 100]]), ('2851', [520, [90, 115, 105, 60, 80, 70]]), ('5215', [495, [100, 110, 65, 80, 40, 100]])]

1        8330    280     140     2       [135, 145]
2        0024    620     103     6       [100, 105, 60, 110, 135, 110]
3        2851    520     86      6       [70, 80, 60, 105, 115, 90]
4        5215    495     82      6       [100, 40, 80, 65, 110, 100]
```

# json
**python没有直接的json类型**，而是通过用**字典`dict`** 或者 **列表`list`** 这两种类型来表示json。

**用字典表示：**
```python
jd = {
    "book": "Python tutorial",
    "author": "Jack",
    "price": 99
}

print(type(jd), "\n", jd)   # <class 'dict'>    ....
```

**用列表来表示**，那么列表的每一个元素一般要求是一个字典，比如:
```python
jl = [
    {"name": "Jack", "age": 21},
    {"name": "Lucy", "age": 19},
    {"name": "Tony", "age": 20}
]

print(type(jl), "\n", jl)   #  <class 'list'>   ....
```

### json的 load、loads 和 dump、dumps用法
- **`json.load(file)`** 用来读取**文件**，文件的内容是格式正确的json， 该函数**把json文件转成字典或者列表对象**；函数返回值是转换后的对象。
- **`json.loads(str)`** 用来读取**字符串**，字符串的内容是格式正确的json， 该函数**把json字符串转成字典或者列表对象**；函数返回值是转换后的对象。
- **`json.dump(json_obj, file)`** 将表示json的字典或者列表对象 **写入文件** ； **写入的文件内容一定是格式正确的json**。函数没有返回值。
- **`json.dumps(json_obj)`** 将表示json的字典或者列表对象**转化格式正确的json字符串**、函数的返回值是该字符串。 **<font color=red>把json转成格式正确的json字符串，一定要使用</font>: <font color=blue>json.dumps(json_obj)</font>**
  

例子： 用`json.load(f)` 读取json文件
```python
import json

""" 假设json文件text1.json的内容如下
{"姓名": "张三", "年龄": 18}
"""
file = "text1.json"
with open(file, encoding="utf-8") as f: 
    dic = json.load(f)

print(type(dic))
print(dic)
```

例子： 用`json.dump(obj, file)` 把json写入文件
```python
import json
file = "save1.json"
dic = {"姓名": "张三", "年龄": 18}
with open(file, "w") as fw:
    json.dump(dic, fw, ensure_ascii=False)  # 把json写入文件
```
> ensure_ascii: 默认值为True

### JSON字符串 只能使用双引号，格式非常严格，
1. json的字符串表示，说的是字符串，不是字典或列表；也就是说 **<font color=red>json字符串只能使用双引号</font>，不能使用单引号**;
2. 字典dict 或者 列表list， 可以根据需要自由使用单引号或者双引号。
3. json字符串最后一个元素或键值对的后面不允许有多余的逗号。

- `f"{json_obj}"`用f字符串拼接字典或者列表，输出用的是单引号， 不是有效的json字符串
- 用`print`打印josn的字典对象，输出用的是单引号。 不是有效的json字符串
- `json.dumps(json_obj)`的返回值，输出用的是双引号，才是格式正确的json字符串。

```python
import json

# 在字典里使用 '单引号 或者 "双引号 都是有效的
jd = {'姓名': "张三", "年龄": 18}   
f = f"{jd}"
print(f)                                   # 无效的json    {'姓名': '张三', '年龄': 18}
print(jd)                                  # 无效的json    {'姓名': '张三', '年龄': 18}

print(json.dumps(jd, ensure_ascii=False))  # 正确的josn格式  {"姓名": "张三", "年龄": 18}
```

### `indent`参数，使JSON具有可读性（pretty-printing）
在`json.dump(obj, file)` 或者 `json.dumps(str)`函数里使用 **`indent`** 参数可以对 JSON 字符串进行格式化，使其易于阅读。

```python
import json
json_dict = {
    'people': [
        {'name': '大军', 'website': 'stackabuse.com', 'from': 'Nebraska'}
    ]
}
print(json.dumps(json_dict, ensure_ascii=False, indent=4))

# 输出带缩进、格式化好的json字符串
"""
{
    "people": [
        {
            "name": "大军",
            "website": "stackabuse.com",
            "from": "Nebraska"
        }
    ]
}
"""

```


# 解包 unpacking

**解包unpacking**就是对一个**容器(可迭代对象)**进行结构拆解，从而获取该容器的元素值，然后**把这些元素值赋值给左边的变量**。
- 解包本质上就是一种匹配模式。只要等号两边的模式相同，**左边变量和容器元素的数量要一致**。
```python
# 列表解包
a, b, c = [1, 2, 3]
print(a, b, c)  # 1  2  3

# 字符串解包
s1, s2, s3, s4 = '你好中国'
print(s1, s2, s3, s4)  # 你 好 中 国
```

**字典解包**：如若不做特殊处理，只会把字典的**键(key)**取出来，而**值(value)** 则会丢失。


# with ... as ...
对于系统资源如：文件、数据库连接、socket 而言，打开这些资源并执行完业务逻辑之后，必须做的一件事就是要关闭（断开）该资源。很多时候我们经常忘记手动关闭。否则会出现什么情况呢？极端情况下会出现 "Too many open files" 的错误，因为系统允许你打开的最大文件数量是有限的。

**`with...as`** 语句，即上下文管理器，用于对资源进行访问的场合，确保**不管使用过程中是否发生异常**都会**自动执行清理操作，释放资源**，比如文件使用后自动关闭、线程中锁的自动获取和释放等。
```python
with EXPR as VAR:
    BLOCK
```
这里就是一个标准的上下文管理器的使用逻辑，稍微解释一下其中的运行逻辑：

1. 执行EXPR语句，获取上下文管理器（Context Manager）
2. 调用上下文管理器中的 **`__enter__`** 方法，该方法执行一些预处理工作。
3. 这里的`as VAR`可以省略，如果不省略，则将`__enter__`方法的返回值赋值给VAR。
4. 执行代码块BLOCK，这里的VAR可以当做普通变量使用。
5. 最后调用上下文管理器中的的 **`__exit__`** 方法。
6. `__exit__`方法有三个参数：exc_type, exc_val, exc_tb。如果代码块BLOCK发生异常并退出，那么分别对应异常的type、value 和 traceback。否则三个参数全为None。
7. `__exit__`方法的返回值可以为`True`或者`False`。如果为`True`，那么表示异常被忽视，相当于进行了try-except操作；如果为`False`，则该异常会被重新raise。

```python
#文件的读操作,  r 表示只读
with open('input_filename.txt','r') as f:  
   df=pd.read_csv(f)  
   print(f.read())
```

打开文件的其他模式：
**r** 以只读方式打开文件。
**rb** 以二进制格式打开一个文件用于只读。
**r+** 打开一个文件用于读写。文件指针将会放在文件的开头。
**rb+** 以二进制格式打开一个文件用于读写。

```python
#文件的写操作
with open('output_filename.csv', 'w') as f:
   f.write('hello world')  
```
写入文件的其它模式
**w**	打开一个文件只用于写入。如果该文件已存在则将其覆盖。如果该文件不存在，创建新文件。
**wb** 以二进制格式打开一个文件只用于写入。如果该文件已存在则将其覆盖。如果该文件不存在，创建新文件。
**w+** 打开一个文件用于读写。如果该文件已存在则将其覆盖。如果该文件不存在，创建新文件。
**wb+** 以二进制格式打开一个文件用于读写。如果该文件已存在则将其覆盖。如果该文件不存在，创建新文件。
**a** 打开一个文件用于追加。如果该文件已存在，文件指针将会放在文件的结尾。也就是说，新的内容将会被写入到已有内容之后。如果该文件不存在，创建新文件进行写入。
**ab** 以二进制格式打开一个文件用于追加。如果该文件已存在，文件指针将会放在文件的结尾。也就是说，新的内容将会被写入到已有内容之后。如果该文件不存在，创建新文件进行写入。
**a+** 打开一个文件用于读写。如果该文件已存在，文件指针将会放在文件的结尾。文件打开时会是追加模式。如果该文件不存在，创建新文件用于读写。
**ab+** 以二进制格式打开一个文件用于追加。如果该文件已存在，文件指针将会放在文件的结尾。如果该文件不存在，创建新文件用于读写。

### `with open("file_name") as f:` 逐行读取文件
```python
with open(file_name) as f:
    for row in f:
        print(row)
``` 

### with ... as VAR1, ... as VAR2 同时打开多个资源

例子，使用with结构同时打开3个文件
```python
with open(filename1, 'rb') as fp1, open(filename2, 'rb') as fp2, open(filename3, 'rb') as fp3:
    for i in fp1:
        j = fp2.readline()
        k = fp3.readline()
        print(i, j, k)
```


# python 的字符串

### 字符串在内存中是`Unicode`编码、在存储和传输时是`utf-8`编码

由于计算机只能处理二进制，字符串类型必须转为数字才能处理，所以字符串是一种特殊的数据类型，它需要编解码才能在计算机中进行处理。

- **ASCII**：最早计算机只处理英文字母，数字和一些符号，所以127个字符的ASCII编码就够了，**ASCII编码占用1个字节**。

- **Unicode**：随着计算机发展，全世界各国语言都需要显示，ASCII码不够用了。Unicode编码应用而生，范围从 0 - 0x10ffff，它把所有语言都统一编码，包含了世界上所有文字和符号，一百多万个字符。
  - 但值得注意的是unicode只是一个符号集，规定了如何编码但没规定如何存储，所以不能说unicode字符一定占用**2**个字节
  - 世界上的每个字符都编上号了, 怎么存储这些编号呢? 目前 Unicode 编码的最大值达 **0x10FFFF**, 需要 **21 位**二进制数; 然而每个字符的编码大小不一, 如果简单地将一个字符分配三字节的话, 未免太浪费空间了。`utf-8` 就是一种字符编码方案, 它采用变长编码, 能够有效节省空间.
- **`utf-8`、即可变长的Unicode编码**：英文字符明明1个字节就能搞定的事情，如果都统一使用UniCode，在空间上是一种浪费。所有又出现了UniCode的可变长编码形式utf-8编码。可以用1-4个字节来表示一个字符，具体的大小根据实际情况来，英文字母就是1个字节，**中文汉字通常是3个字节**。

在Python2中默认的编码是ASCII,不能识别中文字符，需要指定字符编码；

在Python3中默认的编码是Unicode，可以识别中文字符；
- 在计算机**内存中，统一使用Unicode编码**，主要是因为Unicode的编码长度是固定的。如果内存中的字符编码是不定长的，会给算法带来麻烦，比如你没法确定第2000个字符在哪个字节开始。
- 当需要**保存到硬盘或者需要传输的时候，就转换为`utf-8`编码**，目的是节省磁盘空间、和提高网络IO的传输效率。

### 字符串encode 和 decode 
计算机通信采用字节流（bytes）进行传输，人类认知世界采用字符串（str），因而这两种形式之间不可避免地经常需要相互转换。
- python的字符系列有两种：`str` 和 `bytes`（b 开头的）。str 是人类可读的文本，bytes 字节码就是计算机能识别的（0/1）。
- encode 编码为字节流`bytes`， decode解码为可读字符串`str`
```python
str.encode(encoding='utf-8', errors='strict') -> bytes

bytes.decode(encoding='utf-8', errors='strict') -> str
```

原来是str类型，encode后就变成了bytes类型。
```python
s = 'ab你==好'
g = s.encode('gbk')
u = s.encode('utf-8')
print(f"s type={type(s)}  {s}")   # s type=<class 'str'>  ab你==好
print(f"g type={type(g)}  {g}")   # g type=<class 'bytes'>  b'ab\xc4\xe3==\xba\xc3'
print(f"u type={type(u)}  {u}")   # u type=<class 'bytes'>  b'ab\xe4\xbd\xa0==\xe5\xa5\xbd'
```


decode()方法为bytes对象的方法，用于将二进制数据转换为字符串


# `global`全局变量关键字
全局变量是在函数外部定义的变量（没有定义在某一个函数内），所有函数内部都可以使用这个变量。

如果只是在函数中访问全局变量，不需要使用`global`声明； 只有对**全局变量修改时才需要先用`global`关键字进行声明**。 
```python
num = 1  # 全局变量

def update():
    global num  # 使用global声明num，在函数中就可以修改全局变量的值。 没有这行，下面修改全局变量会报错
    num += 1    # 修改全局变量的值
    return 0

print(num)  # 1
update()    # 修改全局变量
print(num)  # 2
```

# `sys.argv`、`argparse`命令行参数

#### 使用 `sys` 模块的 `sys.argv`属性获取命令行参数
**argv**即 **argument value** 是一个list列表对象，其中存储的是在命令行调用 python 脚本时提供的 **命令行参数**。
- `sys.argv[0]` 是被调用的脚本文件名或全路径。
- `sys.argv `属性返回的是命令行参数列表
- `len(sys.argv)` 获得命令行参数个数

例子： 下面脚本保存在 test.py 文件， 用 `python test.py -a "AA" -b` 执行
```python
# test.py  使用这个命令运行 python test.py -a "AA" -b
import sys

print("脚本名称:", sys.argv[0])      # 脚本名称: test.py
print('参数个数:', len(sys.argv))    # 参数个数: 4
print('参数列表:', sys.argv)         # 参数列表: ['test.py', '-a', 'AA', '-b']
```

#### `argparse`
内置的 argparse 模块能自动生成参数帮助使用手册，可以通过 **「 -h / --help 」** 命令参数查看帮助文档。在用户给程序传入无效参数时能抛出清晰的错误信息。

argparse使用需要三个步骤：

1. 创建一个解析器: 调用`ArgumentParser(description="***")`方法创建`argparse`对象。
2. 添加参数: 调用 `add_argument(...)` 方法添加参数。
3. 解析参数: 使用 `parse_args()` 解析添加的参数。

- 如果命令行参数后面不需要提供值，则可以把 action设为 **'store_true'**，  如果命令行指定了参数， 则值是 True, 否则就是False，例如下面的 -o 参数。
- `choices=['***', '***',...] `可以限定参数值只能是这些备选值中的一个。
- 位置参数（positional arguments）: 参数没有显式的使用 **--xxx** 或者 **-x**， 而是直接赋值，例如下面的例子中的 filename 参数

```python
import argparse

parser = argparse.ArgumentParser(description='参数说明...')        # 创建argparse实例

parser.add_argument('filename') # 位置参数，直接赋值，不需要使用 --xxx 或者 -x。 

parser.add_argument('--name', '-n', type=str, help='名字, 必须提供', required=True)  # 添加参数
parser.add_argument('--year', '-y', type=int, help='演示默认值 2017', default=2017)
parser.add_argument('--body', '-b', type=str, help='参数可以省略，不提供')

parser.add_argument('--out', '-o', action='store_true', help="参数不需要提供值")
parser.add_argument('--type', '-t', choices=['install','uninstall','start','stop'], default='stop') # 备选值

args = parser.parse_args()  # 解析参数

# 通过这个命令运行脚本 python test.py -n 大军 -y 1974 -b "are you ok" -o -t start aabb
if __name__ == '__main__':
    print(f"{args.name} | {args.year} | {args.body}")  # 大军 | 1974 | are you ok

    # 参数 -o 的 action='store_true'。 如果命令行指定了参数 -o， 则args.out的值是 True, 否则就是False
    print(args.out)     # True

    print(args.type)    # start

    print(args.filename)    # filename位置参数的值: aabb
```

# if __name__ == "__main__" 
Python使用缩进对齐组织代码的执行，所有没有缩进的代码（非函数定义和类定义），都会在载入时自动执行。为了区分文件是主动直接执行、还是被其它文件导入时执行，Python引入了一个变量`__name__`，当文件是被导入时执行，它的值为模块名(也就是去掉扩展名后的文件名)，**当文件是主动直接执行时**，它的值为`__main__`。
```python
PI = 3.14

def main():
    print("PI:", PI)

if __name__ == "__main__":
    main()
```

# 切片Slice
切片是对**序列型对象** `list`, `string`, `tuple`的一种高级索引方法。普通索引只取出序列中一个下标对应的元素，而切片取出序列中一个范围对应的元素。 而且切片操作的结果是返回一个**新的列表对象**
```python
>>> a = list(range(7))
>>> a
[0, 1, 2, 3, 4, 5, 6]
>>> b = a[:]
>>> b
[0, 1, 2, 3, 4, 5, 6]
>>> id(a), id(b)
(4302235904, 4302953280)     # a和b 虽然内容一样， 但他俩是不同的两个对象。
>>>
>>>
>>> c=a[::2]
>>> id(c), c
(4303013696, [0, 2, 4, 6])
```


# 一切皆对象
Python 中一切皆对象，是的，数字、列表、字典等等啥都是对象。除此之外，函数、类本身也是对象。变量充其量就是对象的一个引用，变量赋值操作 `=` 其实是**把一个名字绑定到对象**上name binding，通俗讲，变量就是一个标签，一个名字，仅此而已，不像 C 语言那样。

### `name binding`
**python中name是没有类型的**，而**name所指向的对象是有类型的**，比如name  x 可以指向对象int数1，你也可以让它指向一个list对象。
```python
x = 1
y = x          # x 和 y 指向同一个对象
print(y is x)  # True   is用来比较 y 与 x 所指向的对象是否为同一个，也就是id(x)与id(y)是不是一样的

print(id(x))   # 4300374256
x += 1         # 此时x的值为2,  x重新绑定到了对象int 2 上,  id(x)也会发生改变
print(id(x))   # 4300374288
```
- 例子中的 `x`, `y` **这些东西叫做name**，而**不是叫变量**，因为如果使用一个未定义的东西xx，python会报错 `NameError: name 'xx' is not` defined。

- `x = 1 `表示的是给对象int 1绑定了一个名字(name)叫做x，可以用名字 x来引用int 1 这个对象了。

### 可变对象：`list` `dict` `set`
  修改可变对象所包含元素的值，并不会改变**可变对象所指向的内存地址**，也就是说**对象还是原来的对象**，只是内容变了。 只有给整个可变对象重新赋值，才会指向另一个内存地址，一个新对象。
```python
# 修改可变对象所包含元素的值，并不会改变可变对象所指向的内存地址，也就是说对象还是原来的对象。
x = [1, 2, 3]
print(id(x))         # 输出：139644486420232
x.append(4)
print(id(x))         # 输出：139644486420232

# 只有给整个可变对象重新赋值，才会指向另一个内存地址。
x = [1, 2, 3, 4, 5]
print(id(x))         # 输出：139644486437576
```
我们先是让变量 x 指向了一个列表 `[1, 2, 3]`，然后我们通过 `append()` 方法改变了这个列表，使其变为了 `[1, 2, 3, 4]`。此时，x 所指向的对象并没有改变，但是对象自身发生了变化。然后，我们让 x 指向了一个新的列表 `[1, 2, 3, 4, 5]`。此时，x 所指向的对象改变了。

### 不可变对象：`tuple` `string` `int` `float` `bool`
基本类型的不可变对象，它的值不可改变，要想给它不同的值，只能重新赋一个新的对象。
```python
x = 3
print(id(x))  # 输出：4340384048

x = 4
print(id(x))  # 输出：4340384080
```
我们先让变量 x 指向了整数 3，然后又让 x 指向了整数 4, 通过id(x)的输出， 可以看到x已经被重新赋予一个新的对象。

### 不可变容器对象，包含的元素是可变对象
元组是容器类型的不可变对象，正常的元组我们是不可以修改它元素的值，但是，如果**元组的元素是一个可变对象**，比如列表， 那么修改这个列表的值是可以的，而且元组所指向的内存地址并没有改变，**对象还是原来的对象**。 **但这个不可变对象的内容已经变了**，毕竟所包含的可变对象元素已经被修改了。 只有给整个元组重新赋值，它的地址才会改变。
```python
a = ([1], 100)     # 定义一个不可变对象，这里是元组a
print(a, id(a))    # ([1], 100) 4306542976
a[0].append(2)     # a[0]是一个列表， 列表是可变对象，可以修改它的值
a[0].append(3)
print(a, id(a))    # ([1, 2, 3], 100) 4306542976  a的地址没变，还是原来的对象，内容变了
```
元组a的第一个元素`a[0]`是一个可变对象(列表)， 所以`a[0]`的值是可以改变的。 但对a[0]的改变，并没有导致a所指向的内存地址发生改变，a还是指向原来的内存地址，还是原来的对象 


# python参数传递：`形参是实参的别名`
python中，万物皆对象。python中不存在所谓的传值调用，一切传递的都是对象的引用，也可以认为是传址。 也就是说，函数内部的**形参是实参的别名**。

### 实参是：可变对象， 在函数中对其修改, 会影响实参
可变对象作为参数传入时，在函数中对其进行修改，是会影响到函数外的实参的，因为函数是对该对象所指向的内存地址进行了修改，所以**会影响函数外的实参**。

```python
def foo(b):
    b.append(4)   # 形参b 改变了 实参a的值

a = [1,2,3]
foo(a)
print(a)  #  [1,2,3,4]   这里可以看到 实参a的值变了
```

### 实参是：不可变对象，整个赋值不影响、局部修改影响实参
#### 1、不可变对象，整个赋值实参不受影响
  
基本类型的不可变对象，对它进行运算操作，或者说想改变它的值， 只能创建新的对象，然后将原先的变量名绑定到新的对象上，所以**函数外的实参不受影响**
```python
def bar(c):
    c = [0,0,0]   # 在函数里形参c重新绑定到一个新对象，这个变动不会反映到上一层，也就是实参a的值不会变
a = 100
bar(a)
print(a)  # 100
```

不可变容器对象(比如元组），在函数内**给整个元组重新赋值，函数外的`实参不受影响`**。
```python
def reassign_tuple(atuple):
    print("    ", atuple, id(atuple))
    atuple = [1000, 2000, 3000]  # 不是修改元组的莫个元素， 而是给整个元组重新赋值，函数外实参不受影响
    print("    ", atuple, id(atuple))

b = (10, 20, 30)
print(b, id(b))
reassign_tuple(b)
print(b, id(b))
```
程序输出：
```
[10, 20, 30] 4350728000
     [10, 20, 30] 4350728000
     [1000, 2000, 3000] 4350731648
[10, 20, 30] 4350728000
```
#### 2、不可变对象，局部修改影响实参
  
不可变容器对象，包含的元素是可变对象，在函数中对包含的可变对象元素进行修改（局部修改）, 虽然不可变对象所指向的内存地址并没有改变，**对象还是原来的对象**， 但**函数外的实参会受影响**，毕竟内容已经变了。

```python
def test_immutable_for_tuple(args):
    print("    ", cur, id(args))
    args[0].append(5)  # 形参args修改了不可变元组包含的可变的元素列表[0]， 改为[0,5]，会影响函数外的实参cur
    print("    ", cur, id(args))

if __name__ == '__main__':
    cur = ([0], 1)      # 不可变的元组里，含有可变的列表[0]
    print(cur, id(cur))
    test_immutable_for_tuple(cur)
    print(cur, id(cur)) # 实参地址没变， 但函数内，修改形参的值，函数外的实参也跟着变了。
```
输出如下：
```
([0], 1) 4386234240
        ([0], 1) 4386234240
        ([0, 5], 1) 4386234240
([0, 5], 1) 4386234240          # 对象还是原来的对象，但内容变了
```


# decimal十进制浮点数
标准库模块decimal提供了十进制浮点运算支持。我们在数据库处理金融数据的时候也会遇到 `Decimal` 对象。

# class 类相关

### self

无论是显式创建**类的构造方法**，还是向类中添加**实例方法**，`都要将 self 参数作为方法的第一个参数`。例如，定义一个 Person 类：
```python
class Person:
    def __init__(self):
        print("正在执行构造方法")
    # 定义一个study()实例方法
    def study(self):
        print(self,"正在学Python")
zhangsan = Person()
zhangsan.study()
```
输出：
<pre>
正在执行构造方法
<__main__.Person object at 0x10484a770> 正在学Python
</pre>

> 事实上，Python 只是规定，无论是构造方法还是实例方法，最少要包含一个参数，并没有规定该参数的具体名称。之所以将其命名为 **self**，只是程序员之间约定俗成的一种习惯，遵守这个约定，可以使我们编写的代码具有更好的可读性（大家一看到 self，就知道它的作用）。

### 类属性 & 类变量
- **类变量**: 类体中、所有**函数之外定义的变量**
  - 类变量的特点是，**所有的类实例都同时共享类变量**，也就是说，类变量在所有实例化对象中是作为公用资源存在的。
  - 类变量的读取或重新赋值都可以用 **`类名.类变量名`** （优先使用，歧义少）的方式访问，但 **`实例名.类变量名`** 这种方式仅能读取类变量的值，不能给类变量赋值，这是因为通过类实例名修改类变量的值，不是在给“类变量赋值”，而是在定义新的实例变量。
- **实例变量**: 类体中，所有**函数内部**以 **self.变量名** 的方式定义的变量。
  - 实例变量**只能通过实例的对象名访问**，无法通过类名访问。

#### 定义类变量
```python
class CLanguage :
    # 下面定义了2个类变量
    name = "C语言中文网"
    add = "http://c.biancheng.net"

    # 下面定义了一个say实例方法
    def say(self, content):
        print(content)

print(f"使用类名访问 类变量: {CLanguage.name} \t {CLanguage.add}\n")

print("修改前，用实例名称访问  类变量：")
clang1 = CLanguage()
print(f"{clang1.name} \t {clang1.add}")   # 用实例名称访问  类变量
clang2 = CLanguage()
print(f"{clang2.name} \t {clang2.add}\n")

print("修改后，因为类变量在所有的类实例中共享，通过类名修改类变量的值，会影响所有的类实例")
CLanguage.name = "Python教程"              # 给类变量赋值要用类名访问  类变量
CLanguage.add = "http://c.biancheng.net/python"
print(f"{clang1.name} \t {clang1.add}")
print(f"{clang2.name} \t {clang2.add}")
```
输出：
<pre>
使用类名访问 类变量: C语言中文网 	 http://c.biancheng.net

修改前，用实例名称访问  类变量：
C语言中文网 	 http://c.biancheng.net
C语言中文网 	 http://c.biancheng.net

修改后，因为类变量在所有的类实例中共享，通过类名修改类变量的值，会影响所有的类实例
Python教程 	 http://c.biancheng.net/python
Python教程 	 http://c.biancheng.net/python
</pre>

#### 动态添加 类变量 `类名.变量名 = 值`
值得一提的是，除了可以`通过类名访问类变量`之外，还可以**动态地为类添加类变量**: `类名.变量名 = 值` 例如，在上面 CLanguage 类的基础上，动态添加一个类变量`catalog`以下代码：
```python
clang = CLanguage()
CLanguage.catalog = 13
print(clang.catalog)    # 输出 13
```

#### 类属性
在此 AnthonerLanguage 类中，name、add 以及 catalog 都是实例变量。其中，由于 `__init__()` 函数在实例化类时会自动调用，而 `say() `方法需要通过类实例手动才会调用。因此，AnthonerLanguage 类的实例都会包含 name 和 add 这两个实例变量，而只有通过类对象手动调用了 say() 方法，才会包含 catalog 实例变量。
```python
class AnthonerLanguage :
    def __init__(self):
        # 定义2个实例变量
        self.name = "C语言中文网"
        self.add = "http://c.biancheng.net"
        
    # 下面定义了一个say实例方法
    def say(self):
        self.catalog = 13

clang = AnthonerLanguage()
print(f"{clang.name} \t {clang.add}")

#由于 clang 对象未调用 say() 方法，因此其没有 catalog 变量，下面这行代码会报错
# print(clang.catalog)

clang2 = AnthonerLanguage()
print(f"{clang2.name} \t {clang2.add}")
#只有调用 say()，才会拥有 catalog 实例变量
clang2.say()
print(clang2.catalog)
```
输出：
<pre>
C语言中文网 	 http://c.biancheng.net
C语言中文网 	 http://c.biancheng.net
13
</pre>

#### 动态添加 实例变量 `实例名.变量名 = 值`

通过类实例名修改类变量的值，不是在给“类变量赋值”，而是在定义新的实例变量。

### 实例方法
通常情况下，在类中定义的方法**默认都是实例方法**。类的构造方法理论上也属于实例方法，只不过它比较特殊。实例方法最大的特点就是，它**最少也要包含一个 self 参数**，用于绑定调用此方法的实例对象（Python 会自动完成绑定）。

当然，Python 也支持使用类名调用实例方法，但此方式需要手动给 `self` 参数传值。例如：

```python
clang = CLanguage()
CLanguage.say(clang)   #类名调用实例方法，需手动给 self 参数传值
```
### 类方法 `＠classmethod`
类方法就是用`＠classmethod`修饰， 定义在类内的函数，而且它的第一个参数是`cls`。Python 会自动将类本身绑定给 cls 参数（注意，绑定的是类，不是类的实例对象）。也就是说，我们在调用类方法时，无需显式为 cls 参数传参。
- 类方法推荐**使用类名直接调用**，当然也可以使用实例对象来调用（不推荐）
- 和 self 一样，cls 参数的命名也不是规定的（可以随意命名），只是 Python 程序员约定俗称的习惯而已。
```python
class CLanguage:
    #类构造方法，也属于实例方法
    def __init__(self):
        self.name = "C语言中文网"
        self.add = "http://c.biancheng.net"
        
    #下面定义了一个类方法
    @classmethod
    def info(cls):
        print("正在调用类方法",cls)

#使用类名直接调用类方法
CLanguage.info()    # 输出： 正在调用类方法 <class '__main__.CLanguage'>

#使用类对象调用类方法
clang = CLanguage()
clang.info()        # 输出： 正在调用类方法 <class '__main__.CLanguage'>
```

> 注意，如果没有 ＠classmethod，则 Python 解释器会将 fly() 方法认定为实例方法，而不是类方法。

### 类静态方法 `＠staticmethod`
静态方法就是用`＠staticmethod`修饰，定义在类内的函数， 它没有类似 `self`、`cls` 这样的特殊参数，因此 Python 解释器不会对它包含的参数做任何类或对象的绑定。也正因为如此，类的静态方法中**无法调用任何类属性和类方法**。
- 静态方法的调用，既可以使用类名，也可以使用类对象
```python
class CLanguage:
    @staticmethod
    def info(name,add):
        print(name,add)

#使用类名直接调用静态方法
CLanguage.info("C语言中文网","http://c.biancheng.net")   # C语言中文网 http://c.biancheng.net

#使用类对象调用静态方法
clang = CLanguage()
clang.info("Python教程","http://c.biancheng.net/python") # Python教程 http://c.biancheng.net/python
```

>在实际编程中，几乎不会用到类方法和静态方法，因为我们完全可以使用函数代替它们实现想要的功能，但在一些特殊的场景中（例如工厂模式中），使用类方法和静态方法也是很不错的选择。












