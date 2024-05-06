最常见的日志输出是使用` print() `，直接打印各种提示信息，常见于个人练习项目里，通常是懒得单独配置日志，而且项目太小不需要日志信息，不需要上线，不需要持续运行，完整的项目不推荐直接打印日志信息，现实中也几乎没有人这么做。


Python标准库自带的`logging`不推介使用，使用前它需要初始化配置，而且还有些费劲的，比如需要配置 Handler/Formatter 等，不太Pythonic，而开源的 [loguru](https://github.com/Delgan/loguru)成为众多工程师及项目中首选，loguru是一个可以 开箱即用 、无需配置 的日志记录模块

### 安装 `logure` 
```bash
pip install loguru
```

### loguru 定义了`7`个不同日志级别
1. TRACE
2. DEBUG
3. INFO
4. SUCCESS
5. WARNING
6. ERROR
7. CRITICAL


### loguru开箱即用， 它的主要概念只有一个 `logger`
```python
from loguru import logger

logger.info("This is log info!")
logger.warning("This is log warn!")
logger.error("This is log error!")
logger.debug("This is log debug!")
```
输出：
```bash
2024-05-06 14:34:05.118 | INFO     | __main__:<module>:3 - This is log info!
2024-05-06 14:34:05.118 | WARNING  | __main__:<module>:4 - This is log warn!
2024-05-06 14:34:05.118 | ERROR    | __main__:<module>:5 - This is log error!
2024-05-06 14:34:05.118 | DEBUG    | __main__:<module>:6 - This is log debug!
```
### loguru的默认输出足够漂亮， 必要时也可以使用 `f-string`格式化输出
```python
from loguru import logger

logger.debug('this is a debug {name} | {age}', name="你好，世界", age=88)
```


### 只要一个 `logger.add()`函数， 就可以自定义日志级别，日志格式，保存日志到文件

如果想自定义日志级别，自定义日志格式，保存日志到文件该怎么办？与 logging 模块不同，不需要 Handler，不需要 Formatter，只需要一个`logger.add()`函数就可以了。

例如把日志储存到文件、同时在终端输出：
```python
from loguru import logger

logger.add('test.log')
logger.debug('this is a debug')
```



# `add() `函数的参数说明


## `add() `函数的 `rotation`参数，控制日志文件分隔
下面例子中的 `{time}` 会自动使用当前时间，不需要自己额外定义。
#### 每天 0 点新创建一个 log 文件  
```python
`logger.add('runtime_{time}.log', rotation='00:00')`
```

#### 超过 500 MB 新创建一个 log 文件  
```python
logger.add('runtime_{time}.log', rotation="500 MB")
```

#### 每隔一个周新创建一个 log 文件
```python
logger.add('runtime_{time}.log', rotation='1 week')
```
## `add()` 函数的 `retention` 参数，设置日志的最长保留时间
#### 设置日志文件最长保留 15 天： 
```python
logger.add('runtime_{time}.log', retention='15 days')
```

#### 设置日志文件最多保留 10 个
```python
logger.add('runtime_{time}.log', retention=10)
```


# `@logger.catch`装饰器 可以直接用在函数上，自动捕获异常

```python
from loguru import logger

@logger.catch
def my_function(x, y, z):
    return 1 / (x + y + z)

my_function(0, 0, 0)   # 除以 0， 抛出异常
```
而且得到的日志是无比详细的, 输出：
```bash
2024-05-06 15:32:37.718 | ERROR    | __main__:<module>:9 - An error has been caught in function '<module>', process 'MainProcess' (75792), thread 'MainThread' (7990169600):
Traceback (most recent call last):

> File "/Users/dj/STUDY/python_study/b.py", line 9, in <module>
    my_function(0, 0, 0)
    └ <function my_function at 0x101267f60>

  File "/Users/dj/STUDY/python_study/b.py", line 6, in my_function
    return 1 / (x + y + z)
                │   │   └ 0
                │   └ 0
                └ 0

ZeroDivisionError: division by zero
```



