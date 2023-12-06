# 标量scalar、向量vector、矩阵matrix、张量Tensor
**深度学习**的表现之所以能够超过传统的机器学习算法离不开**神经网络**，然而神经网络最基本的数据结构就是**向量**和**矩阵**，神经网络的输入是向量，然后通过每个矩阵对向量进行线性变换，再经过**激活函数**的非线性变换，通过层层计算最终使得**损失函数的最小化**，完成模型的训练。所以要想学好深度学习，对这些基础的数据结构还是要非常了解。

- 点——标量（scalar）， 就是一个单独的数(0D张量)
- 线——向量（vector），一维数组(1D张量)
- 面——矩阵（matrix），二维数组(2D张量)
- 体——张量（tensor），超过二维的数组(多维数组)
> dimension维度， 也叫轴axis、或者阶rank；说的是同一个东西。

标量、向量、矩阵、张量的关系：Scalar - Vector - Matrix - Tensor其实就是数据维度逐渐上升的过程
![标量、向量、矩阵、张量的关系](./res/mojo_scalar_vector.jpg)

### scalar标量， 一个数(0D张量)
一个标量**就是一个单独的数**，可以是**数字**、**布尔值**、**字符**或 **null** 等。 标量张量有0个轴（0维）或者0阶。

标量也叫：标量张量、零维张量、0D张量
```python
x = np.array(12)

# 可以用 ndim 属性来查看一个 Numpy 张量的轴的个数。标量张量有 0 个轴（ ndim == 0 ）
print(x.ndim) 
```
### Vector（向量），一维数组(1D张量)
一个向量表示一组有序排列的**一维数组**，通过次序中的索引我们能够找到每个单独的数。向量也叫一维张量（1D 张量）。
```
np.array([12, 3, 6, 14, 7])  # 5D向量， 2D张量
```
这个向量有 5 个元素，所以被称为 5D**向量**。不要把 5D向量 和 5D**张量** 弄混！ 5D向量只有一个轴，沿着轴有 5 个维度，而 5D 张量有 5 个轴（沿着每个轴可能有任意个维度）
### 矩阵（matrix），二维数组(2D张量)
矩阵是一个二维数组，也叫二维张量(2D 张量)，其中的每一个元素由两个索引来决定。
```python
np.array([[5, 78, 2, 34, 0], [6, 79, 3, 35, 1], [7, 80, 4, 36, 2]])
```

### 张量（Tensor）：超过二维的数组(多维数组)
Tensor = multi-dimensional array of numbers **张量是一个多维数组**。张量的dimension**维度， 也叫轴axis、或者阶rank**；说的是同一个东西。

深度学习处理的一般是 0D 到 4D 的张量，但处理视频数据时可能会遇到 5D 张量。

下面是一个 Numpy 的 3D 张量(立方体)。
```python
np.array([[[5, 78, 2, 34, 0],
           [6, 79, 3, 35, 1],
           [7, 80, 4, 36, 2]],

          [[5, 78, 2, 34, 0],
           [6, 79, 3, 35, 1],
           [7, 80, 4, 36, 2]],

          [[5, 78, 2, 34, 0],
           [6, 79, 3, 35, 1],
           [7, 80, 4, 36, 2]]])

```
张量的三个关键属性：
- ndim轴的个数：例如，3D 张量有 3 个轴，矩阵有 2 个轴。
- shape形状: 一个整数元组，表示张量沿每个轴的维度大小。
- dtype: 张量的数据类型，例如float32、int64等。

### 标量、向量、矩阵、张量之间的联系
标量是**0维空间中的一个点**，向量是**一维空间中的一条线**，矩阵是**二维空间的一个面**，三维张量是**三维空间中的一个体**。也就是说，向量是由标量组成的，矩阵是向量组成的，张量是矩阵组成的。

用一个比较通俗的例子可以概括为：假设你手中拿着一根棍子，**标量**就是我们只知道棍子的长度，但是不知道棍子指向的方向。**向量**就是我们除了知道棍子的长度之外还知道棍子指向的是左边还是右边，**矩阵**就是除了知道向量知道的信息外还知道棍子是朝上还是朝下，**张量**就是除了知道矩阵知道的信息外还知道棍子是朝前还是朝后。
 

 # SIMD 单指令流多数据流

## `SIMD`一个由硬件支持的向量
SIMD（Single Instruction, Multiple Data）是一种并行计算技术，基本思想是在单一操作中同时对多个数据元素执行相同的指令。



**`SIMD是一个向量vector`， 而且是由硬件支持的向量（ backed by a hardware vector element）**，注意，**它是vector向量**，现在的CPU和GPU都内置专门的`SIMD向量寄存器（属于硬件）`，所以SIMD的速度非常快。 **一个SIMD向量寄存器可以可以存储多个数据元素**， 不同型号的cpu或gpu，它们内置的simd向量寄存器长度不同，例如，一个 128 位的 SIMD 寄存器可以存储 4 个 32 位的浮点数。 **一个指令可以同时对同一个SIMD内的`多个`数据`进行操作`** ， 而不是逐个执行。
- **单一指令** ：这意味着在给定的时钟周期内，执行的是同一条指令，而不是多条不同的指令。
- **多个数据** ：这意味着上述指令可以同时对同一个SIMD寄存器内的多个数据进行操作，而不是逐个地执行。

- **指令集扩展** ：许多现代处理器提供 SIMD 指令集扩展，如 Intel 的 SSE 和 AVX，以及 ARM 的 NEON。这些扩展增加了专门的指令来支持向量化的操作。



### SIMD示例
我们可以使用一个简单的向量加法操作来解释 SIMD 的工作原理。假设我们需要将两个浮点数向量相加。每个向量都包含了四个元素。

**场景：向量加法**
假设我们有两个浮点数向量 A 和 B：
```python
A = [a1, a2, a3, a4]
B = [b1, b2, b3, b4]
```
我们的任务是计算它们的和，即 $C=A+B$。

**1、传统的逐元素加法（没有使用 SIMD）**
如果我们使用传统的方法（例如，在一个没有 SIMD 支持的老旧处理器上），我们会逐个元素地进行加法操作：
```
c1 = a1 + b1
c2 = a2 + b2
c3 = a3 + b3
c4 = a4 + b4
```
**这四个操作是串行的**，意味着每次只能执行一个加法操作。

**2、 使用 SIMD 的向量加法**
现在，假设我们的处理器支持 4 个元素的 SIMD 加法操作。这意味着它有特殊的寄存器（通常称为**向量寄存器**），可以同时存储四个浮点数。

1. **数据加载**：首先，我们将向量 A 和 B 的元素加载到两个 SIMD 寄存器中。
2. **单一指令加法**：接着，我们使用单一的 SIMD 加法指令，同时对两个SIMD寄存器中的所有元素执行加法操作。
3. **数据存储**：最后，我们**将结果从 SIMD 向量寄存器存储回内存中**，得到向量 C。

在这个 SIMD 示例中，四个加法操作几乎同时完成，而不是逐个进行，从而大大提高了性能。


## Mojo内置SIMD类型

SIMD类型有2个参数：
- type(DType): 一个SIMD寄存器可以存储多个数据元素，type指定数据元素的类型。
- size(Int): SIMD向量的**长度**（要求是2的幂， 如：1, 2, 4, 8...）, 代表**可以存储 多少个类型是type的数据元素**。

内置的 `Scalar、Int8、UInt8、Int16、UInt16...Int64、UInt64 、Float16、 Float32、Float64` 都是 SIMD子类型的 **别名Aliase**。
- `Scalar = SIMD[?, 1]` 表示标量数据类型。
- `Int8 = SIMD[si8, 1]` 表示8位有符号标量整数。
- `UInt8 = SIMD[ui8, 1]` 表示8位无符号标量整数。
- `Int16 = SIMD[si16, 1]` 表示 16 位有符号标量整数。
- `UInt16 = SIMD[ui16, 1]` 表示16位无符号标量整数。
- `Int32 = SIMD[si32, 1]` 表示 32 位有符号标量整数。
- `UInt32 = SIMD[ui32, 1]` 表示32位无符号标量整数。
- `Int64 = SIMD[si64, 1]` 表示 64 位有符号标量整数。
- `UInt64 = SIMD[ui64, 1]` 表示64位无符号标量整数。
- `Float16 = SIMD[f16, 1]` 代表16位浮点值。
- `Float32 = SIMD[f32, 1]` 表示32位浮点值。
- `Float64 = SIMD[f64, 1]` 表示64位浮点值。



# CPU 的 L1 L2 L3 Cache 缓存 & RAM memory 内存
通常每个CPU内部都**内置**有一个L1和L2缓存，L3缓存是多个CPU共用一个。

CPU查找数据的时候首先在L1，然后看L2，如果还没有，就到L3和内存查找。 L1缓存的访问速度最快，所以很快需要的东西都保存在那里。然而，它是从L2缓存填充的，L2缓存本身是从L3缓存填充的，L3缓存是从内存填充的。这让我们想到了优化代码的第一个想法：使用已经在更近的缓存中的东西可以帮助代码运行得更快，因为它不必被查询和移动到这个链上

L1/L2/L3 Cache 和 memory 速度差别

- L1 cache: 3 cycles， L1缓存的容量通常在32—256KB。

- L2 cache: 11 cycles，L2缓存大小通常在 1-32MB

- L3 cache: 25 cycles，高端消费类 CPU的L3缓存通常32MB-128MB

- RAM Memory: 100 cycles


# Stack（栈） & Heap（堆）

# 模块 module & 包 package

**Module模块**：其实就是一个单独的Mojo源文件，里面包含了其它文件在导入它时可以使用的代码。**文件名就是模块名**(不包含.mojo扩展名)，**module可独自存在**，不用归属莫个包package，当然 module 也可以归入某个包下。
- 模块通常只是包含API，以便被导入并在其他Mojo程序中使用。所以一般模块的代码文件里不定义`main()`函数。

**包package**：其实是一个目录，目录下是一个个定义**module模块**的.mojo文件，这个目录下有一个特殊的文件 **`__init__.mojo`** ，即使是空文件也一定要有，用于把这个目录识别为一个包。 把模块文件放入包目录，这个模块就属于这个包。  默认**目录名就是包名**
- 可选地，你还可以使用`mojo package`命令将该包编译成一个更易于共享的`.mojopkg`或`.📦`文件。可以使用`-o`参数指定包名，可以与目录名不同。

- **导入包**：可以直接**从源文件** 或 **编译后的 .mojopkg** / .📦 文件导入。这两种导入方式对Mojo没有真实的区别。
  - 当从源文件导入时，目录名用作包名
  - 当从编译的包导入时，文件名是包名（使用 mojo package 命令指定，它可以与目录名不同）

> **访问模块成员的完整路径**: 如果有包，就先包名、然后是模块名、最后才是模块成员的名称  **包名.模块名.module_member_name**
> 
## module 模块
### 定义一个模块
例如，您可以创建一个定义结构体的模块，文件名是`mymodule.mojo`，如下所示：

文件`mymodule.mojo`
```mojo
struct MyPair：
    var first: Int
    var second: Int

    fn __init__(inout self, first: Int, second: Int)：
        self.first = first
        self.second = second

    fn dump(self)：
        print(self.first, self.second)
```

### 使用模块

#### 1、从模块里直接导入所需内容 `from 模块名 import 所需内容`
以下是如何在与mymodule.mojo位于同一目录的名为main.mojo的文件中导入MyPair：

文件`main.mojo`
```mojo
from mymodule import MyPair

fn main()：
    let mine = MyPair(2, 4)
    mine.dump()
```
在终端命令行下运行： `mojo main.mojo`

#### 2、导入整个模块 `import 模块名`
```mojo
import mymodule
let mine = mymodule.MyPair(2, 4)
```
#### 3、 as 为导入的成员创建别名 `import 模块名 as 别名`
```mojo
import mymodule as my
let mine = my.MyPair(2, 4)
```

## package 包
### 1、通过目录定义一个包
例如，考虑包含以下目录结构的项目：
<pre>
main.mojo
mypackage/
    __init__.mojo
    mymodule.mojo
</pre>
`__init__.mojo` 是空文件， 用于标识目录mypackage是一个 **包**

文件`mymodule.mojo`，定义一个模块
```mojo
struct MyPair：
    var first: Int
    var second: Int

    fn __init__(inout self, first: Int, second: Int)：
        self.first = first
        self.second = second

    fn dump(self)：
        print(self.first, self.second)
```

### 2、通过包的源文件导入包、包名是包的目录名
在这种情况下， main.mojo 文件现在可以**通过包名导入** MyPair ， 这里的导入方式是**通过包的源文件导入**， 所以**包名是包的目录名**，下如下所示：

文件main.mojo
> 正常**访问模块成员**的完整路径是： **包名.模块名.module_member_name** 先包名、然后是模块名、最后才是模块成员的名称。
```python
from mypackage.mymodule import MyPair  

fn main():
    let mine = MyPair(2, 4)
    mine.dump()
```


在终端命令行下运行： `mojo main.mojo`

### 3、从编译后的`.mojopkg`导入包、包名由 `mojo package` 命令指定，可以与源代码的目录名不同

#### 3.1 `mojo package` 编译包
把上面的包（也就是目录mypackage）编译成`.mojopkg`， 通过 `-o` 参数指定了生成的包名是` mypack`
```bash
mojo package mypackage -o mypack.mojopkg  # 通过 -o 指定了生成的包名是 mypack
```
注意：如果你想重命包名，你不能简单地编辑 .mojopkg 或 .📦 的文件名，因为**包的名称是在.mojopkg文件中编码的**。您必须再次运行 mojo package 以指定新名称。

#### 3.2 把生成的`.mojopkg`包放在main.mojo目录下
<pre>
main.mojo
mypack.mojopkg
</pre>

文件main.mojo, 导入包，调用
```mojo
from mypack.mymodule import MyPair  # 导入包

fn main():
    let me = MyPair(100, 200)
    me.dump()
```

### `__init__.mojo`预先导入模块成员 
目前，.mojo 文件中不支持顶级代码(top-level code)，因此与 Python 不同，你不能在 `__init__.mojo` 中编写在导入时执行的代码。

但是你可以在`__init__.mojo`里**预先导入模块成员**，后续使用导入这个包的时候，就可以**省略模块名**，直接通过 **`包名.module_member_name`** 来访问这些预先导入的模块成员， 

- 正常**访问模块成员**的完整路径是： **包名.模块名.module_member_name** 先包名、然后是模块名、最后才是模块成员的名称。
- 这个特性解释了为什么Mojo标准库中的一些成员可以从它们的包名导入

例如还是上面的 mypackage包， 我们在 `__init__.mojo` 中**预先导入模块成员**：

文件`__init__.mojo`
```mojo
from .mymodule import MyPair
```

现在文件main.mojo里就可以省略模块名`mymodule`，直接通过包名`mypackage` 访问被预先导入的模块成员`MyPair`

```mojo
from mypackage import MyPair

fn main():
    let me = MyPair(100, 200)
    me.dump()
```

# trait

struct 实现trait
```mojo
struct SomeStruct(SomeTrait):
```

trait 可以继承
```mojo
trait Parent:
    fn parent_func(self): ...

trait Child(Parent):
    fn child_func(self): ...
```

# AnyType

# raises

# Parametric & Argument

### Parametric & partially bound

Parametric types 支持部分绑定partially bound， 例如，添加了一个新的 Scalar 类型别名，定义为：
```mojo
alias Scalar = SIMD[size=1]
```
# Tensor