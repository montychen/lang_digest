# `可变对象`当做函数的默认参数
```python
def bad_append(new_item, a_list=[]):
    print('address of a_list:', id(a_list))
    a_list.append(new_item)
    return a_list

print(bad_append('1'))  # 两次调用bad_append，默认参数a_list的地址是相同的。
print(bad_append('2'))
```
输出：
```
address of a_list: 4344363776
['1']
address of a_list: 4344363776
['1', '2']
```
可以这样简单理解： 一条def函数定义语句，函数头里的默认参数求值只会仅且执行一次，，**后续每次函数调用，使用的都是`同一个`默认参数对象**。 除非再次碰到def函数定义语句，函数头里的默认参数才会再次重新求值； 从上面的例子也可以看出，两次调用`bad_append`，默认参数`a_list`的地址是相同的，也就是说都是**同一对象**。
  
- 根源在于 Python 是动态语言，以关键字 `def` 开头的函数定义在 Python中也是个可执行语句。每碰到一条`def`定义的函数，这条语句就会被执行，而且就像定义其它普通变量一样，这条语句仅且执行一次；并且执行的是 **`函数头`里参数的赋值语句**和函数名称和这个函数对象的绑定，并将参数保存为函数对象的一部分（即其属性）。之后通过该函数名称进行函数调用的时候，只会执行函数体（通过 `__code__ `指向的代码片段）的语句， 函数头里的东西不会再次执行。
- 而在函数不是第一等公民静态语言中，函数定义是在编译阶段做的，不能在运行时多次重复绑定。在每次函数调用时，形参实参都会进行一次结合，默认参数会被重新进行赋值。

再看看下面这个例子
```python
import datetime as dt
from time import sleep

def log_time(msg, the_time=dt.datetime.now()):
    sleep(1)  # 线程暂停一秒
    print(the_time, msg)

log_time('msg 1')  # 2023-07-28 18:59:45.085270 msg 1
log_time('msg 2')  # 2023-07-28 18:59:45.085270 msg 2
log_time('msg 3')  # 2023-07-28 18:59:45.085270 msg 3
```
即使使用了sleep(1)让线程暂停一秒，排除了程序执行很快的因素。输出中三次调用打印出的时间还是相同的，即三次调用中默认参数the_time的值是相同的。
