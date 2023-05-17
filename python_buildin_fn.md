# dir(obj)
可以通过**`dir(obj)`**方法来查看某个对象的所有方法和属性。
```python
>>> dir("hello")
['__add__', '__class__', '__contains__', '__delattr__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', 
'__getattribute__', '__getitem__', '__getnewargs__', '__gt__', '__hash__', '__init__', '__init_subclass__', 
'__iter__', '__le__', '__len__', '__lt__', '__mod__', '__mul__', '__ne__', '__new__', '__reduce__', 
'__reduce_ex__', '__repr__', '__rmod__', '__rmul__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', 
'capitalize', 'casefold', 'center', 'count', 'encode', 'endswith', 'expandtabs', 'find', 'format', 'format_map', 
'index', 'isalnum', 'isalpha', 'isascii', 'isdecimal', 'isdigit', 'isidentifier', 'islower', 'isnumeric', 
'isprintable', 'isspace', 'istitle', 'isupper', 'join', 'ljust', 'lower', 'lstrip', 'maketrans', 'partition', 
'removeprefix', 'removesuffix', 'replace', 'rfind', 'rindex', 'rjust', 'rpartition', 'rsplit', 'rstrip', 
'split', 'splitlines', 'startswith', 'strip', 'swapcase', 'title', 'translate', 'upper', 'zfill']
```

# enumerate(iterable, start=0)
 `enumerate()`函数将一个可迭代对象组合成一个**带索引的序列**。 在实际开发中，一般放在 `for` 循环中使用。
 ```python
colors = ['red', 'green', 'blue']
for index, color in enumerate(colors): 
    print(color, index)   # red 0       green 1        blue 2
 ```

 enumerate()函数返回的是一个**包含所有 “元素下标和元素值” 的可迭代对象**，因此可以使用 `list()` 函数将其转换为列表。
```python
colors = ['red', 'green', 'blue']
result = enumerate(colors)
print(list(result))    # [(0, 'red'), (1, 'green'), (2, 'blue')]

```



# hasattr(obj, attr_name)
该实参是一个对象和一个字符串。如果字符串是对象的属性之一的名称，则返回 True，否则返回 False。（此功能是通过调用 `getattr(object, name)` 看是否有 `AttributeError` 异常来实现的。）


# sorted(iterable, key=None , reverse=False)
`sorted()`函数并不会影响原列表，而是会返回一个新列表。

key的值是一个只有参数的函数，返回一个用于排序的键(key值)， 也就是用于比较的键。该函数只需要调用一次，所以排序速度很快。默认值为 None (直接比较元素)。

reverse 表示排序方式，reverse=True 是降序，reverse=False 是升序(默认)。

例子： 下面代码user[0] 表示这 个 lambda 表达式最终返回的是元组的第 1 个元素。也就是说，此时用于排序的是每一个用户的 姓名。
```python
users = [('Tony', 20), ('Ack', 21), ('Yucy', 19)] 
result = sorted(users, key=lambda user: user[0]) 
print(result)       # [('Ack', 21), ('Tony', 20), ('Yucy', 19)]
```