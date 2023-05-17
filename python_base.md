# 命名习惯
- **常量** 全大写，如多个单词，用下划线隔开, 如： `MAX_CONNECTION=100`
- **类名** 大驼峰命名，全部单词的首字母都大写，如： `class ClassName():`
- **函数、变量** 蛇形命名，单词全部小写，用下划线连接。 如： `max_value`

# 双下划线开头和结尾 的魔法方法Magic Methods
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
    for row in open(file_name, "r"):
        yield row       # 通过遍历，加载一行、处理一行，从而避免了内存溢出。
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
- 因为元组是不可变的， 所以元组也不存在列表推导式这样的语法。


# lambda

```python
lambda arg1,arg2...argn: expression
```
`lambda` 可以使用任意数量的参数，但只能包含**一个表达式**的匿名函数。

貌似在下面这个例子里， 列表推导比使用lambda更简单。

```python
numbers = [1, 2, 3, 4, 5]
a = list(map(lambda n: n+1, numbers))  # 使用 lambda
b = [x + 1 for x in numbers]         # 使用 列表推导

print(a)   # [2, 3, 4, 5, 6]
print(b)   # [2, 3, 4, 5, 6]
```

不过在下面这个排序函数里， 貌似只能用lambda不能用 列表推导
```python
users = [
    {"name": "Yack", "age": 21},
    {"name": "Lucy", "age": 19},
    {"name": "Aony", "age": 20}
]
result = sorted(users, key=lambda user: user['age'])  # lambda表达式指定用 age 字段进行排序
print(result)
```

# json
JSON 有两种表示方式:一种是使用**字典**来表示，另一种是使用**列表**来表示。

**用字典表示：**
```python
{
    "book": "Python tutorial",
    "author": "Jack",
    "price": 99
}
```

**用列表来表示**，那么列表的每一个元素一般要求是一个字典，比如:
```python
[
    {"name": "Jack", "age": 21},
    {"name": "Lucy", "age": 19},
    {"name": "Tony", "age": 20}
]
```
JSON 格式要求非常严格，特别注意这两点:
1. 只能使用双引号，不能使 用单引号;
2. 最后一个元素或键值对的后面不允许有多余的逗号。