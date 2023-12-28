Mojo是第一个专门为MLIR设计的语言，它不仅要成为**Python的超集**，而且是一门**追求极致性能的系统编程语言（Focused on performance & system programming)**。 Mojo寻求尽可能高的性能，以消除两个世界的问题（Python为了提高性能，很多性能敏感的库只能使用C或C++来编写）；Mojo直接编译为原生机器代码，没有用C作为中间代码。

- Python是动态、强类型的**解释型语言**。内存管理机制是：引入计数、**垃圾回收**、内存池机制。
- **Mojo**是静态、强类型、**内存安全memory safety**的**编译型**语言。 它没有使用引用计数和垃圾收集器来管理内存。而是像Rust一样，通过**定义`对象的生命周期`，使用`借用检查器`来`自动管理内存`**。

为什么Mojo成为Python的超集可以实现？ Chris Lattner 是LLVM、Clang、Swift、MLIR的作者。
- Clang编译器（C、C++、Objective-C、CUDA、OpenCL等编译器）是GCC、MSVC和其他现有编译器的“兼容替代品”。Clang编译器要兼容这些的复杂性比实现Mojo兼容Python大一个数量级。

- Swift拥抱了Objective-C运行时和语言生态系统， 通过Swift，Chris Lattner 具备保持“运行时兼容”以及如何与遗留运行时合作的丰富经验。

期待有这么一天：CPython团队最终用Mojo语言而不是C语言实现解释器 🔥 。 （Python官方的解释器实现用C语言实现的，所以也叫**CPython**，它是最广泛使用的Python解释器）

> MLIR多级中间表示（Multi-Level Intermediate Representation ）是编程语言(如mojo）或者库（如 TensorFlow）和机器代码之间的中间语言，允许不同语言的不同编译器堆栈之间的代码重用以及其他性能和可用性优势。 

# Python 和 Mojo 的区别
- 在Python中，引用无处不在（名称就是引用，列表/元组中的元素都是引用，函数参数作为引用传递）
<br>
- **Python对象的可不可变`在于它们的类型`**：list列表可变， 元组tuple不可变。
```python
tup1 = ('physics', 'chemistry', 1997, 2000)  # 元组不可变
list1 = [3,7,'Mar','Feb','Jan']              # 列表可变
```
- 类似于其他静态语言，**Mojo对象的可不可变不在于类型，而在于是用`let`还是`var`来声明的**。例如，即使Mojo 的字符串本质上是可改动的, 也可以用像 `let s = String("Mojo")` 这样的语法声明一个不可改动的字符串。

# Mojo 常识

**`AnyType`**: 可以**表示任何Mojo的类型** 

**`AnyRegType`**: 表示可以再`机器寄存器`中传递的数据类型

### `alias` 定义`编译时常量`
```mojo
alias PI = 3.141592653589793
alias TAU = 2 * PI
```
### `let` 和 `var` 声明的变量可以`延迟初始化`
用`let` 和 `var` 声明的变量可以`延迟初始化`，例如：
```mojo
fn my_function(x: Int):
    let z: Float32      # 声明
    if x == 0:
        z = 1.0         # 延迟初始化
    else:
        z = foo()       # 延迟初始化
    print(z)

fn foo() -> Float32:
    return 3.14

fn main():
    let a = my_function(0)    # 1.0
    let b = my_function(1)    # 3.1400001049041748
```



# 内存管理
所有现代编程语言都将数据存储在两个地方之一：`call stack调用栈`和 `heap堆`，有时也用`CPU registers寄存器`存取数据。然而，每种语言读取和写入数据的方式略有不同-有时非常不同

### stack栈 & 存储空间固定的局部变量
一般来说，所有编程语言都以相同的方式使用`call stack调用栈`：当调用函数时，编译器在栈上分配一个内存块，该内存块的大小正好可以存储`执行逻辑` 和所有 **`存储空间固定的局部变量(fixed-size local values)`**。当另一个函数被调用时，它的数据同样被添加到栈的顶部。当一个函数完成时，它在栈中的所有数据都将被销毁，以便内存可用于其他代码。


### heap堆 & 动态改变存储空间的值
请注意，我们说只有 **存储空间固定的局部变量(fixed-size local values)** 才会存储在栈stack中。任何在运行时可以 **`动态改变存储空间的值(dynamically-sized values)`** 会存储在堆heap中，堆是一个更大的内存区域，允许在运行时进行动态内存访问。

此外，需要在函数的生存期之外生存的值，也存储在heap堆中。即使创建它的函数运行结束，从堆栈中移除之后，这些head堆上分配的值，也还在，这是发生大多数内存错误的地方，也是不同编程语言之间内存管理策略差异最大的地方。因为内存是有限的，所以程序尽快从heap堆中删除未使用的数据（“释放”内存）是很重要的。

### 垃圾收集器 GC & 手动内存管理
一些编程语言试图通过使用**垃圾收集器**来隐藏内存管理的复杂性，**该进程跟踪所有内存使用情况并定期释放未使用的堆内存**（也称为自动内存管理）。好处是，它减轻了开发人员手动内存管理的负担，可以避免错误，提高开发效率。但是，**GC会影响性能**，因为垃圾收集器会中断程序的执行，造成程序卡顿，并且可能不会很快回收内存，导致内存用量增加。

其他语言要求您**手动释放在堆上分配的数据**。然而，这种方法很**容易出错**，特别是当程序的多个部分需要访问同一块内存时，很难知道程序的哪个部分拥有该数据，并负责释放数据。程序员可能会在程序完成之前意外地释放数据，导致**释放后使用 use-after-free**的错误，或者它们可能释放它两次，导致**双重释放double free**错误，或者它们可能永远没释放，导致**泄漏内存leaked memory**错误。这样的错误会给程序带来灾难性的后果，而这些错误通常很难追踪。

### ownership 所有权 & 自动内存管理
Mojo没有引用计数器，也没有垃圾收集器，而是使用了第三种称为**所有权ownership**的方法，它依赖于**程序员在传递值时必须遵循一些规则**，核心规则就是 **`每个值同一时间只有一个所有者`，所有者在`生命周期结束时， Mojo会销毁该值`**。[详细的规则查看](#mojo的-ownership-所有权规则)
通过这种方式，Mojo会`自动为您分配和释放堆heap内存`，但它是以一种确定性和安全的方式进行的，不会出现诸如释放后使用，双重释放和内存泄漏等错误。此外，它以**非常低的性能开销**做到了这一点。






## Parametric 编译时参数 Fully-bound Partially-bound 
`完全绑定Fully-bound`：指定了所有`编译时参数`
`部分绑定Partially bound`：只指定了部分编译时参数，其中未绑定参数可在以后提供。

例如，添加了一个新的 Scalar 类型别名，定义为：
```mojo
alias Scalar = SIMD[size=1]    # 部分绑定
```


# `fn` & `def` 定义函数

**值语义value semantics**：复制（赋值or传参）以后，两个数据对象拥有的存储空间是**相互独立、互不影响**。

**引用语义reference semantics**：复制（赋值or传参）以后，两个数据对象**相互之间互为别名**。操作其中任意一个数据对象，则会影响到另一个。
  - `object` 是Mojo提供的唯一具有`引用语义`的类型， 而且使用的是**Python参数引用语义**：形参整个重新赋值不影响实参，局部修改影响实参，[下面有专门的描述](#python参数引用语义形参整个重新赋值不影响实参局部修改影响实参)

Mojo不强制使用**值语义**或**引用语义**，。每个类型的作者自己决定新建的类型是值语义还是引用语义，亦或两者兼而有之，然后再实现相应的`创建create`、`复制copy`和`移动move`方法即可。

### `Parametric编译时参数 []`不存在内存管理
**Parametric编译时参数** 要求放在**方夸号里`[ ]`**，它的值要求是**编译时是已知的、是编译时常量，不存在内存管理**。 后续所说参数的**所有权、以及内存管理都是针对`Argument运行时参数`**
**Argument 运行是参数** 要求放在**括号里`( )`**，它的值要求是在运行时是已知的，所以也叫**运行时参数**。

### `fn` 参数默认 `不可变引用 borrowed ` 强类型

`fn`定义函数要求是**强类型**的，无论参数、函数返回值还是函数体内的变量，都**要明确声明的类型**，而且编译时会进行检查，确保`实参`和`形参`的类型是一致的，包括函数的返回值和声明的类型也是一致的。 
- **fn的参数默认是`不可变引用 borrowed `**。这是一个内存优化，以避免不必要的副本拷贝；因为反正是不可变，如果还按照默认参数的`值语义`传递，效率差。
- `fn`函数体内的变量， 通过`let` 或者 `var`来标明变量是否可变
- 如果没有明确声明返回值类型，则默认为`None`，表示没有返回值。
- 如果函数可能会引发异常，则必须用 `raises` 关键字显式声明(def函数不需要声明异常)。

### `def`参数默认 `owned`、类型是`object`
虽然从Mojo的内部实现来看，`def`其实是`fn`的语法糖。 但是`fn`还是比`def`有2个优势：
1. `fn`的强制类型，有助于避免各种运行时错误。
2. `def`默认的类型是`object`，实际的类型会在运行时再自动推断，增加了开销，而`fn`的类型在编译时是固定的，所以性能更高。

`def`定义的函数提供了 **Python style的动态性** ：无论参数、函数返回值还是函数体内的变量，都**可以不用指定类型**。 由于没类型约定，如果在函数内用`形参`执行了某些操作，而实际传递的`实参`并没有实现这些操作， def函数会报错。
- **def的参数默认` owned `、类型是`object`**
- def函数如果没有明确声明**返回值类型**，**默认为`object`**。
- def函数体内的 **变量默认是`var` 可变的**。 在def函数里，也可以明确用`let`声明变量，那它就是不可变的。

- def定义函数**可以不用指定类型**，但是，如果一旦指定了类型，就要严格遵守，不然编译不过，会报错。比如：
  - 如果定义了`String`作为返回值， 那么就一定要有返回值，而且类型要是`String`
  - 如果注明参数的类型是`Int`, 如果传一个小数过去，是不行的。


#### `def` 没注明类型的都是`object`对象、而且是`引用语义`
- **关键字`object`用来表示一个`没有明确注明类型的对象`。使用def定义函数，如果它的`参数`、`函数体内的变量`、`甚至没有声明返回值类型`，那它们的类型都是`object`** 对象。 

- 任何类型的值都可以传给`object`， 这个值会自动构建出一个`object`对象，它可以动态表示Mojo标准库中的任何类型， 实际的类型会在运行时再自动推断。

- **为了和Python兼容， `object`是mojo提供的唯一一个`引用语义`的类型(而且使用的是Python参数传递的引用语义，简称：`Python参数引用语义`)，其它类型都是`值语义`**。所以，如果在`def`里明确声明了类型，那就不是`object对象`了，而是明确声明的那个类型，所以是`值语义`。 因此，这两类值在一起使用时要小心，毕竟`引用语义`和`值语义`在复制时（赋值or传参）它们的行为不一致。 
    - **Python参数引用语义**：形参整个重新赋值不影响实参，局部修改影响实参，[下面有专门的描述](#python参数引用语义形参整个重新赋值不影响实参局部修改影响实参)

例如：下面def定义的函数， 
- **参数x** 和 **函数体内的变量a**， 没有明确声明类型，所以类型都是 `object`属于`Python参数引用语义`。 
- **参数n** 明确声明了类型，所以是`值语义`
- 没有声明返回值类型， 所以系统会自动指明返回值类型是`object`。
```mojo
def f(x, n: Int):   # x 没有声明类型，所以类型是 `object`
    a = 100         # a 没有声明类型，所以类型是`object`
    print(x)
    print(n)
    print(a)
```



## `运行时参数argument`默认是`值语义`
**`运行时参数argument`默认是`值语义`**。 唯一特殊的是**def中没注明类型的都是`object对象`**, 它始终是`Python参数引用语义`。

例如，即使Mojo Tensor 类型是在堆上分配值，但def中第一的参数`t: Tensor[DType.uint8]`明确声明了类型，那就不是`object对象`了，而是所声明的类型`Tensor[DType.uint8]`, 是`值语义`。所以，在函数中修改参数t的值，原始值不变：
```mojo
def update_tensor(t: Tensor[DType.uint8]):
    t[1] = 3
    print(t)   # Tensor([[1, 3]], dtype=uint8, shape=2)

fn main() raises:
    var t = Tensor[DType.uint8](2) # Tensor 是在heap堆上分配空间
    t[0] = 1
    t[1] = 2
    _ = update_tensor(t)  # 忽略返回值 
    print(t)    # Tensor([[1, 2]], dtype=uint8, shape=2)
```
> 注意：如果上面这段是Python代码，则函数update_tensor对参数t的修改，将会传到到外面，因为Python参数的传递是`引用语义`。


## Python参数引用语义：`形参整个重新赋值`不影响实参，`局部修改`影响实参

**Python参数引用语义**: Python语言对参数传递的约定是**通过对象引用传递** pass by object reference，这意味着当你将一个变量传递给一个Python参数是，你实际上是**把对象的引用`作为一个值`进行传递**（所以它不是严格的引用语义 it’s not strictly reference semantics)

将对象引用`作为一个值`进行传递意味着**形参是实参的别名**。所以在函数内部**形参`整个重新赋值`不影响实参、`局部修改`影响实参**(例如在列表上调用 `append()` ) 。
- 形参局部修改：形参和实参所指向的内存地址是一样的，如果形参进行了修改，所以会影响函数外的实参。
- 形参整个重新赋值：重新赋值后，形参就指向了另外的对象，形参和实参指向的内存地址自然就不同了，此时对形参的修改就不会影响到实参。

#### python 形参整个重新赋值，不影响实参
注意下面是一段python代码
```python
def change_list(l):
    l = [3, 4]            # 形参整个重新赋值，不影响实参
    print("func:", l)     # func: [3, 4]

ar = [1, 2]     
change_list(ar)
print("orig:", ar)        # orig: [1, 2]
```

#### python 形参局部修改，会影响实参
注意下面是一段python代码
```python
def modify_list(l):
    l.append(3)         # 形参局部修改 会影响实参
    print("func:", l)   # func: [1, 2, 3]

ar = [1, 2]
modify_list(ar)
print("orig:", ar)      # orig: [1, 2, 3]
```



# Ownership 所有权 & `每个值同一时间只有一个所有者 owned`
在所有编程语言中，代码质量和性能在很大程度上取决于函数如何处理**参数**值。也就是说，函数接收的值是唯一值还是引用，是可变的还是不可变的，都有一系列的后果，这些后果定义了语言的可读性，性能和安全性。

Mojo希望提供完整的`值语义`，因为`值语义`提供了一致和可预测的行为。但是作为一种系统编程语言，每次传递值都进行拷贝，成本太高，为了提升效率，通常需要借助`引用语义`。

**Mojo的 Ownership 所有权规则**：编译器实现了一个借用检查器，可以跟踪每个值的`生存期`并在正确的时间销毁每个值（并且只销毁一次）。对于每一个值，Mojo不强制`独占访问`。只是强调：
1. 每个值 **`同一时间只有一个所有者owned`，所有者在`生命周期结束时， Mojo会销毁该值`**。
2. 每个值`同一时间只能有一个可变引用inout`， 可以有`多个不可变引用 borrowed`；
3. `可变引用inout` 和 `不可变引用borrowed` **不能同时存在**。


#### owned 所有者 & 可变引用 可以共存吗？？？？？， 同时都具备修改权限？？？？？
#### owned 所有者 可以被借用：不可变引用borrowed， 可变引用inout`吗？？？？？？


 

### `owned` 和 `^` 触发 `__moveinit__()` 或者 `__takeinit__()`
要支持移动，类型就要实现`__moveinit__()` 或者 `__takeinit__()`。

**`^`转移操作符** transfer operator： 是一个后缀操作符， 用在变量名称后面。**`^`** 的作用是把变量的所有权转移给接收者，**接收者要注明是`owned`**(这一点很重要)。有2种情况：
   1. 如果实参的类型实现了**破坏 移动构造函数`__moveinit__()`**，**`^`** 就会优先触发调用这个方法来执行转移所有权的具体操作，同时会让**原来的变量生命周期结束，失效**。
   2. 如果实参的类型没有实现**破坏 移动构造函数`__moveinit__()`**，而是实现了**窃取 移动构造函数`__takeinit__()`**，那 **`^`** 就会触发调用`__takeinit__()`方法来执行转移所有权的具体操作。**原来的变量继续维持有效**，可以正常使用。
   3. **`__moveinit__()`** 和 **`__takeinit__()`** stealing move基本一样，实现它们的代码都是**直接转移值的所有权，没有申请分配新的堆空间**、也没拷贝数据。 唯一的不同就是`__takeinit__()`不会结束原来变量的生命周期，虽然**原来的变量依然有效**，但在`__takeinit__()`的实现中，一定要 **`人为手动`把它的值变成`null`**。
   - 如果实参类型既没有实现`破坏 移动构造函数__moveinit__()`也没有实现 `窃取 移动构造函数 __takeinit__()` ，Mojo通过简单的把`caller’s stack调用者堆栈中值的引用`转移给对方，来实现所有权转移。**（。。。。。这一点，还没看到具体的例子，说法有待验证。。。）**


#### 破坏 移动构造函数`__moveinit__()`： 转移所有权、原变量失效 Rust的风格

Mojo强调**值语义**，不过复制有时会对性能造成重大影响。 所以Mojo提供 **`__moveinit__()`**，它**直接转移值的所有权**，没有发生重新分配新的堆空间、也没拷贝数据，所以效率很高。 

**`^`** 会优先触发调用这个方法来执行转移所有权的具体操作，同时会**让原来的变量生命周期结束**。所以叫**破坏性移动**，Rust的风格的移动也是这种方式。

```mojo
fn __moveinit__(inout self, owned existing: Self):  # 关键：形参要标记为 owned
```
`__moveinit__()` 的关键是existing**形参要标记为` owned`**，因为它将获得实参的唯一所有权。

例子： 演示有或没有 **`^`** 触发不同的调用:

1. `let b = a ^`  转移操作符 **`^`** 触发调用`__moveinit__`, a生命周期结束。
2. `let b = a`  没有调用__copyinit__; 还是调用`__moveint__` [因为在本例中，用a来赋值是最后一次使用它，编译器会把对a的复制变成移动](#用来赋值的变量是最后一次被使用编译器会把复制变成移动而不是copy--del)

```mojo
from memory.unsafe import Pointer


struct HeapArray:
    var data: Pointer[Int]
    var size: Int

    fn __init__(inout self, size: Int, val: Int):
        self.size = size
        self.data = Pointer[Int].alloc(self.size)
        for i in range(self.size):
            self.data.store(i, val)

    fn __copyinit__(inout self, existing: Self):  #  深度复制
        print("copy---")
        self.size = existing.size
        self.data = Pointer[Int].alloc(self.size)  # 手动分配新的堆内存空间
        for i in range(self.size):
            self.data.store(i, existing.data.load(i))

    fn __moveinit__(inout self, owned existing: Self):  # existing是owned
        print("move")
        # Shallow copy the existing value 可以理解是在转移所有权
        self.size = existing.size
        self.data = existing.data
        # Then the lifetime of `existing` ends here, but
        # Mojo does NOT call its destructor

    fn __del__(owned self):
        self.data.free()  # Pointer 手动分配的堆空间head， 也要手动负责释放

    fn dump(self):
        print_no_newline("[")
        for i in range(self.size):
            if i > 0:
                print_no_newline(", ")
            print_no_newline(self.data.load(i))
        print("]")


fn main():
    let a = HeapArray(3, 1)
    a.dump()  # Prints [1, 1, 1]

    # let b = a^ # Prints "move"; the lifetime of `a` ends here
    let b = a  # 打印的也是"move", 没调用__copyinit__; 因为用a来赋值是最后一次使用它，编译器会把对a的复制变成移动

    b.dump()  # Prints [1, 1, 1]
```

#### 窃取 移动构造函数`__takeinit__()`: 转移所有权、原变量依然有效 要人为把值变成null  C++风格
窃取移动构造函数`__takeinit__()` stealing move和 破坏移动构造函数`__moveinit__()`基本一样，都是**直接转移值的所有权**，没有发生重新分配新的堆空间、也没拷贝数据。 

唯一的不同就是, 如果实参的类型没有实现破坏 移动构造函数`__moveinit__()`， **`^`** 才会触发调用`__takeinit__()`，而且 **不会结束原来变量的生命周期**，虽然**原来的变量依然有效**，但在`__takeinit__()`的实现中，一定要 **`人为手动`把它的值变成`null`**，目的是让这个变量依然是有效的，**保证它的析构函数仍可正常运行**，同时可以避免双重释放和释放后使用。所以叫**窃取移动**， C++风格的移动也是这种方式。
```mojo
fn __takeinit__(inout self, inout existing: Self):  # 关键是 existing形参要标记为inout，实参要可变
```
1. `__takeinit__()` 关键是existing**形参要标记为`inout`**。
2. `__takeinit__()`里面的实现，要人为手动把existing的值变成null，所以传递的实参必须是可变的。

#### `__takeinit__()`的一个使用场景
假设创建了一个包含 HeapArray 值的数组。如果使用 `__moveinit__()` **仅转移该数组中一项的所有权**，则以后使用该数组时可能会遇到问题，因为该数组将包含无法读取的无效变量。为了解决这个问题，你可能想实现 `__takeinit__()` 而不是 `__moveinit__()` ，这样所有的数组项都是有效的。

- [ ] 🔥 没有输出 take running...，待验证。。。

```mojo
struct HeapArray:
    var data: Pointer[Int]
    var size: Int

    fn __init__(inout self, size: Int, val: Int):
        self.size = size
        self.data = Pointer[Int].alloc(self.size)
        for i in range(self.size):
            self.data.store(i, val)

    fn __takeinit__(inout self, inout existing: Self):
        print("take running...")
        # Shallow-copy the existing value 可以理解是在转移所有权
        self.size = existing.size
        self.data = existing.data

        # existing的生命周期没有结束，所以要人为手动把它的值会变成null，让这个变量依然有效，保证它的析构函数可正常运行，同时可以避免双重释放和释放后使用。
        existing.size = 0
        existing.data = Pointer[Int].get_null()  # 这一句 会释放内存吗？

    fn __del__(owned self):
        # Free the data only if the Pointer is not null
        if self.data:      # 上面 data设为null， 它的堆内存在哪里释放
            self.data.free()

    fn dump(self):
        print_no_newline("[")
        for i in range(self.size):
            if i > 0:
                print_no_newline(", ")
            print_no_newline(self.data.load(i))
        print("]")

fn test_take(owned aheaparray: HeapArray):
    print("call take")
    aheaparray.dump()

fn main():
    var a = HeapArray(3,1)
    a.dump()            # [1, 1, 1]
    test_take(a^)       # take running...
                        # [1, 1, 1]
```

### 参数 `borrowed` `inout` `owned`
- **`borrowed 不可变引用`**: 形参接收到的是一个`不可变的引用  immutable reference`，这意味着**可以读取值，但不能修改**。
- **`inout 可变引用`** ：形参接收到的是一个`可变引用mutable reference`，这意味着**可以读取和改变值**。 在函数内**对形参的修改，是会影响外面的实参**的。 声明为`inout`的参数不能有默认值。
- **`owned`**： 形参标记了`owned`，并**不能保证`形参`获得的是`对实参的可变引用`**，只保证 **形参一定会拥有和`实参一样的值`**，而且是这个值的唯一所有者。 形参有2种获得实参的值的方式: 通过`^`转移所有权获得、或者通过深度复制获得。
   - **实参使用了后缀`^`** ，[按照`^`的规则](#owned-和--触发-__moveinit__-或者-__takeinit__)， **实参`通过转让所有权`，`不是拷贝`，让形参完全拥有了原来的的数据**。
    -  **实参没有使用后缀`^`** 传递参数给`owned形参`，触发的是深度复制`__copyinit__()`，这是 **`值语义`**，就是单纯的把**实参的值深度复制一份给形参**，复制后的值和原来的值彼此独立的。 实参没有结束自己的生命周期，**也没有转让所有权**，实参继续是原来值的唯一所有者，仍然可以访问；而形参是复制后的值的唯一所有者。 这个过程会涉及复制、堆内存的申请和分配。
       - 当值类型用作`owned参数`，为了确保实参在没有使用`^` 的情况下也能正常按照值语义拷贝给形参，值类型必须确保是可深度复制的（通过实现 `__copyinit__()`来做到）。 

在处理大的或复制开销大的值时，传递一个`不可变引用`要有效得多，因为复制构造函数和析构函数不会被调用。例如下例，def的参数`tensor: Tensor[DType.float32]`，明确声明了类型，那就是`值语义`, 所以这里在参数前，明确加了`borrowed`， 把它变成`不可变引用`。
```mojo
from tensor import Tensor, TensorShape

def print_shape(borrowed tensor: Tensor[DType.float32]):  # 明确把def的参数声明成`不可变引用`
    shape = tensor.shape()
    print(shape.__str__())

fn main() raises:
    let tensor = Tensor[DType.float32](256, 256)
    _ = print_shape(tensor)         # 256x256
```

#### 例子，形参是owned， 实参后面 没有or有 后缀` ^`
```mojo
fn take_text(owned text: String):
    text += "!"
    print(text)          # Hello!

fn main():
    let message = "Hello"
    # take_text(message)  # 实参没有用后缀 ^，所以实参只是深度把值复制给形参， 实参继续是原来值的唯一所有者，仍然可以访问。
    take_text(message^) # 实参后面用了 ^，实参先结束自己的生命周期，再把所有权转给形参。实参已经无效，下面print语句报错。

    print(message)       # Hello
```





# `值的`生命周期方法 value lifecycle method

值的`生命周期lifecycle`由结构体struct中的各种双下划线的dunder方法定义。生命周期的不同事件由不同的方法处理，例如`初始化构造函数__init__()` ，`析构函数__del__()`，`复制构造函数__copyinit__()` 、`破坏 移动构造函数__moveinit__()`和`窃取 移动构造函数__takeinit__()` 。这些方法定义了值如何被创建和销毁。

> 构造函数的方法名里都带有`init`

值的生命周期从初始化时开始 The life of a value begins when it is initialized，到销毁时结束，通常（但不总是）从 `__init__()` 到 `__del__()` 。Mojo采用的是 **`尽快ASAP(as soon as possible)`销毁策略**，如果能够确定值后面不会再用，就会立即马上销毁值，不会等到代码块的结尾，甚至不会等到表达式的结尾，来销毁未使用的值。

### Mojo不会自动添加任何`生命周期方法`的默认实现。
Mojo中的所有数据类型-包括标准库中的基本类型（如 Bool 、 Int 和 String ），以及复杂类型（如 SIMD 和 object ）都是用`结构struct`实现的。这意味着任何数据的创建和销毁都遵循相同的生命周期规则。

当我们用struct实现自己的类型，如果没有手动实现`构造函数`、`复制构造函数`、`移动构造函数`和`析构函数`等生命周期方法。 **Mojo不会自动为我们添加任何`生命周期方法`的默认实现**。
- 结构体struct如果**没有手动实现构造函数，就不能被实例化**，没有实例，也就没有生命周期。
- **结构体的字段field声明的时候不能有默认值**， 字段必须要在构造器才能进行初始化（赋值）。
  
### 没有`构造函数`，不能被实例化
例如：创建一个没有构造函数的结构体，所以不能被实例化，`state`也没有被初始化，因为结构体的字段field要在构造函数里才能初始化。这个结构体唯一的作用就是作为**静态方法的命名空间**, 像这样调用静态方法 `NoInstances.print_hello()`
```mojo
struct NoInstances:
    var state: Int

    @staticmethod
    fn print_hello():
        print("Hello world!")

fn main():
    NoInstances.print_hello()  # 静态方法的命名空间。
```

### 有构造函数 `__init()__`才能创建实例
```mojo
 fn __init__(inout self, ... ) :
```
`__init__()`构造函数，只有手动实现了，才能创建实例，它的主要职责是初始化所有字段。
- 构造函数的第一个参数要是 `self`，而且要声明为`inout`。 注意：`Self`（大写S）表示的是当前类型名称的别名
- 每个构造函数结束时，都必须完成对**所有`结构体字段`的初始化**。这是硬性要求。
- 构造函数可以`重载overload`, 就是有不同数量或者类型的参数。 函数的返回值类型，不是判断重载函数的条件。

例如，MyPet有构造函数，所以可以实例化。 它的实例也可以被借用和销毁，但还不能被复制或移动，因为还没实现`复制构造函数__copyinit__()` 和`移动构造函数__moveinit__()`。
```mojo
struct MyPet:
    var name: String            # 定义2个结构体 字段
    var age: Int

    fn __init__(inout self):
        self.name = ""
        self.age = 0

    fn __init__(inout self, name: String):
        self = Self()          # 调用另一个 构造函数。 Self（大写S）是当前类型名称的别名
        self.name = name

fn main():
    let mine = MyPet("Loki")    # 有构造函数, 可以创建实例
```
#### 所有`结构体字段`都初始化了，`self`对象就视为完成了初始化
事实上，只要所有**结构体的字段都初始化**了， 即使在构造函数完成之前，也会将**self对象视为完成了初始化**，也就是说，这时**可以传递`self`调用其它函数**了。

例如，这个构造函数可以在所有字段初始化后立即传递 `self`调用其它函数。
```mojo
fn use(arg: MyPet):
    pass

struct MyPet:
    var name: String
    var age: Int

    fn __init__(inout self, name: String, age: Int, cond: Bool):
        self.name = name
        if cond:
            self.age = age  # 执行到这里，所有结构体的字段都初始化了
            use(self)   # 可以传递 self 调用其它函数

        self.age = age
        use(self)       # 可以传递 self 调用其它函数

fn main():
    let mine = MyPet("dj", 50, True)
```

### 单一参数的`__init__`，`= 赋值语句`是调用它的`语法糖`
如果初始化构造函数`__init__`只有一个参数（单一参数），可以直接用`=`赋值的方式触发调用这个初始化构造器；或者说 **`= 赋值语句`是调用`单一参数初始化构造器`的语法糖**。

比如String 有一个类型是Int的单一参数的初始化构造函数
```mojo
__init__(inout self, num: Int)
```
那么下面2种方法都可以初始化它。 
```mojo
var name1: String = 100      # 调用初始构造函数 __init__(inout self, num: Int)
var name2 = String(100)
```
#### 单一参数的`__init__` 和 `隐式类型转换`
只要是**单一参数初始化构造器**支持的类型的值，都可以直接作为实参，传递给函数。因为会触发调用这个单一参数初始化构造器， 这就是Mojo的**隐式类型转换**。 



例如：String有一个类型是Int的单一初始化构造器`__init__(inout self, num: Int)`，那么，就可以直接使用Int类型的值，传递给需要String的形参。

```mojo
fn take_string(version: String):  # 参数类型是 String
    print(version)

fn main():
    # 直接传递整数 100，会隐式触发调用String的__init__(inout self, num: Int)，把100转成String类型
    take_string(100)
```




### 复制构造函数 `__copyinit__()` & 同类型赋值 `=` 
```mojo
 fn __copyinit__(inout self, existing: Self):   # existing 使用fn参数的默认设定（不可变引用），因为不应修改被复制的值的内容
```
只有实现了 `复制构造函数__copyinit__()`，它的实例才支持在**同类型间进行复制**。 复制其实就是使用已经存在的值，构造出另一个**全新的对象**。 所以才叫**复制构造函数**。

>注意：赋值操作 `=` 触发`__copyinit__()`的条件： 是同类型的值，赋给另一个同类型的变量的时候，触发。 上面**单一参数的`__init__`** 的赋值操作 `=`, 是不同类型的值，触发。

主要有2种方式触发复制
- 赋值操作`=` 
- 实参没有使用后缀 **`^`**, 传递参数给`owned形参`，触发的也是复制操作



如果不想自己的类型被复制，就不要实现`__copyinit__()`。

```mojo
struct MyPet:
    var name: String
    var age: Int

    fn __init__(inout self, name: String, age: Int):
        self.name = name
        self.age = age

    fn __copyinit__(inout self, existing: Self):  # existing使用默认的不可变引用规则，因为不应修改被复制的值的内容
        self.name = existing.name
        self.age = existing.age


fn main():
    let mine = MyPet("Loki", 50)
    let second = mine       # 实现了 拷贝构造函数 ， 可以复制
```



#### 确保`__copyinit__()`执行`深度复制` & 满足`值语义`
Mojo强调`值语义value semantic`，默认情况下，赋值操作符`=`执行的是复制操作。 然而，Mojo编译器并不强制`复制构造函数__copyinit__()`满足**深度复制Deep Copy**， 而是交由自定义struct类型的作者自己来保证这一点。 也就是说类型的作者在实现`__copyinit__()`的时候，一定要确保执行的是深度复制，这样才能满足`值语义`。

```mojo
from memory.unsafe import Pointer

struct HeapArray:
    var data: Pointer[Int]
    var size: Int
    var cap: Int

    fn __init__(inout self, size: Int, val: Int):
        self.size = size
        self.cap = size * 2
        self.data = Pointer[Int].alloc(self.cap)
        for i in range(self.size):
            self.data.store(i, val)

    fn __copyinit__(inout self, existing: Self): # Deep-copy 深度复制 existing 的值
        self.size = existing.size
        self.cap = existing.cap
        self.data = Pointer[Int].alloc(self.size)   # 手动分配一块新的内存空间 heap
        for i in range(self.size):
            self.data.store(i, existing.data.load(i))

    fn __del__(owned self):
        self.data.free()        # Pointer 手动分配的堆空间head， 也要手动负责释放

    fn append(inout self, val: Int):
        if self.size < self.cap:
            self.data.store(self.size, val)
            self.size += 1
        else:
            print("Out of bounds")

    fn dump(self):
        print_no_newline("[")
        for i in range(self.size):
            if i > 0:
                print_no_newline(", ")
            print_no_newline(self.data.load(i))
        print("]")

fn main():
    let a = HeapArray(2, 1)
    var b = a    # 触发调用 复制构造函数
    a.dump()     # Prints [1, 1]
    b.dump()     # Prints [1, 1]

    b.append(2)  # Changes the copied data
    b.dump()     # Prints [1, 1, 2]
    a.dump()     # Prints [1, 1] (the original did not change)
```

请注意， 本例中`__copyinit__()` 不会复制 Pointer 值，这样做会使复制后的值和原来的值共享 data的 内存地址，这是一个浅复制。相反，我们先手动分配一块新的内存空间， 让data指向这个新的堆内存块heap，然后再逐个把原来的值，一个个复制到新分配的堆中（这是一个深拷贝）。

因此，当复制 HeapArray 的实例后，每个副本在堆上都有自己的值，修改其中一个的值，并不会影响另一个。

# `@value` 和 `__init__` 、`__copyinit__`、`__moveinit__` 

从执行效率来说， 如果自己定义的类型，**没有手动使用`Pointer`** 在堆heap上分配内存，那么**移动构造函数** `__moveinit__()`或者`__takeinit__()`的`移动语义`并不会给你带来实质的好处。因为在stack栈上复制 `Int`、`Float` 、`Bool`和 `SIMD`这些简单类型的数据效率是很高的。

而且，如果一个类型是允许被复制的，通常没有理由不允许移动，移动的效率比复制高；反过来说就不一定合适，假如一个类型的复制成本很高，那么可以只提供移动构造函数来支持移动，但不提供`__copyinit__()`来禁止昂贵的复制操作。所以：
1. 如果自定义的结构体，**没有手动使用`Pointer`** 在堆heap上分配内存，
2. 而且**所有`结构体的字段`使用的都是`小数据类型`或者`可自销毁的数据类型`**（例如 Int 、 Bool 、 String 等）。  后面的`@register_passable("trivial")`要求，字段只能是`小数据类型`
   - String不是小数据类型，可以用在`@value`, 但是不能用在`@register_passable("trivial")`

那么可以给自定义结构体添加 **`@value` 装饰器**，让Mojo帮你生成 **`__init__()`**(结构体的字段field都作为参数)、 **`__copyinit__()`** 和 **`__moveinit__()`** 。 **助记：一棵木**
   - 上述的3个生命周期方法，自定义的结构体如果有自己的实现，仍然可以使用`@value`。 有自己实现的，编译器就用你自己定义的，没有的，才会使用`@value`装饰器帮你生成的。
   - 生成的构造函数`__init__()`会使用结构体的**每个字段field都作为参数，而且是`owned`**，因为构造函数必须获得所有权来存储每个值。并允许使用**仅移动类型**作为它的实参。
   - 如果结构体声明了**只移动的**类型做字段field(这个类型实现了`__moveinit__`，没有实现`__copyinit__`)，哪怕只有一个，`@value`将不会为你生成`__copyinit__`，因为它不能复制这些字段。
   - 如果结构体声明了**既不可复制也不可移动**的类型做字段(比如：`Atomic`)，则 `@value` 装饰器根本无法工作。



### 用来赋值的`变量是最后一次被使用`，编译器会`把复制变成移动`，而不是`copy + del`
如果Mojo能判断出是**用来赋值的`变量是最后一次被使用`**，编译器就会很聪明的把**原本对变量执行的复制操作`__copyint__()`替换成移动操作`__moveinit__()`**，而不是**copy + del**。因为既然是最后一次使用该变量，执行完复制`__copyint__()`后，再也没有使用该变量，它的生命周期就会结束，也会触发调用析构函数释放`__del__`，所以直接把复制改成移动`__moveinit__()`，效率更高。[官方文档这里有说明](https://docs.modular.com/mojo/manual/lifecycle/life.html#value-decorator).


下面是使用`@value`的例子：
```mojo
@value
struct MyPet:
    var name: String
    var age: Int

# 使用了 @value的MyPet，结果就像你实际上写了下面这个：
struct MyPet:
    var name: String
    var age: Int

    fn __init__(inout self, owned name: String, age: Int):  # age是小数据类型，可以省略 owned
        self.name = name^  # 用来赋值的变量name是最后一次被使用，^不用也可以。
        self.age = age     # age的Int类型是小数据类型，可以省略 ^

    fn __copyinit__(inout self, existing: Self):
        self.name = existing.name
        self.age = existing.age

    fn __moveinit__(inout self, owned existing: Self):
        self.name = existing.name^
        self.age = existing.age
```

- 注意： 这里是自己手动添加了`@value` 装饰器， Mojo才会帮你生成了这些生命周期的方法，并没有违背mojo默认不会自动帮你生成任何生命周期的方法。




# Trivial types `小数据类型`的`owned`和`^`可以省略
`Int`、`Float`、`Bool`、`SIMD` 这样的Trivial types**小数据类型**，所有权对它们没有任何意义。
- **小数据类型的`复制、移动和销毁`不需要调用`生命周期方法`**。
- 小数据类型的值**直接在`机器寄存器`中以值的方式传递**，不通过内存，也不通过引用传递。效率明显高很多，和C++和Rust等语言相比，这是一个显着的性能增强。 
- 只要是小数据类型，原本要声明为`owned`的地方，或者在转移时要用`^`的地方，Mojo允许省略`owned`和`^`。

[小数据类型其实就是用`@register_passable("trivial")`实现的结构体](#register_passabletrivial--小数据类型-trivial-types)。


#### Trivial types 小数据类型包括：
- Int
- Float、Float64
- Bool
- SIMD
- 由小数据类型构成的数组。
- Pointer(指针其实是一个内存地址，所以也是小数据类型。)
- 。。。还有那些列出来

#### 不是 小数据类型的
- String，含有指针，需要构造函数分配和释放内存空间，所以不是

# `@register_passable` 直接在`机器寄存器`中`以值的方式`传递
可以在结构体上添加 `@register_passable` 装饰器来告诉Mojo，该结构体的值**直接在`机器寄存器`中以值的方式传递**，不通过内存，也不通过引用传递。

满足下面要求的结构体，才能使用`@register_passable`:
- `@register_passable`的字段只能是`AnyRegType`，例如**小数据类型**肯定可以。 `String`不是小数据类型，所以`String`不能用在`@register_passable`。
- 结构体**不能有 `__moveinit__()`**，因为@register_passable类型要**在机器寄存器中直接传递值**，不能通过引用传递。 

其它生命周期方法`__init__`, `__copyint__`,`__del__`可以根据需要定义。


## `@register_passable("trivial")` & 小数据类型 Trivial types
上面所说的**Trivial types小数据类型**(Int、Float、Bool、SIMD...)就是用`@register_passable("trivial")`实现的。

[`@register_passable("trivial")`标注的结构体就是小数据类型](#trivial-types-小数据类型的owned和可以省略)，不需要任何自定义任何生命周期方法，它们就可以复制、移动和销毁。它们的值**直接在`机器寄存器`中以值的方式传递**，不通过内存，也不通过引用传递。

添加 **`@register_passable("trivial")`** 后，对结构体的一些要求：
- **唯一可以定义`__init__`这个生命周期方法**，不定义也可以。不过这里定义的`__init__`有点不同，它的参数不用`inout self`，它是静态的、新创建的实例作为函数的返回值。
- **其它的生命周期方法都不能定义**，比如：析构函数`__del__()`，复制构造函数`__copyinit__()` 、破坏 移动构造函数`__moveinit__()`和窃取 移动构造函数`__takeinit__()`。

```mojo
@register_passable("trivial")
struct Pair(Stringable):
    var a: Int
    var b: Int

    fn __init__(one: Int, two: Int) -> Self:  # 参数没有inout self，新创建的实例作为函数的返回值
        return Self {a: one, b: two}    # 初始化结构体

    fn __str__(self: Self) -> String:
        return str(self.a) + str(", ") + str(self.b)


fn main():
    let x = Pair(5, 10)
    let y = x
    print(x)

```

# 销毁对象 - 尽快ASAP销毁策略
与其他语言类似，Mojo遵循对象在构造函数`__init__()`中获取资源，在析构函数`__del__()`中释放资源的原则。

Mojo采用的是 **`尽快ASAP(as soon as possible)`销毁策略**，如果能够确定值后面不会再用，就会立即马上销毁值，不会等到代码块的结尾，甚至不会等到表达式的结尾。这比基于作用域的销毁有一些优势，例如C++ RAII模式，要等到代码块的末尾，作用域结束时才销毁。
- 尽快ASAP销毁策略，可以优化：如果用来赋值的变量是最后一次被使用，编译器会把复制变成移动，而不是copy + del。
- 尽快ASAP销毁策略，可以避免**尾调用tail call**，或者说**尾递归tail recursive**的问题。因为Mojo采用的是尽快释放策略，析构函数调用总是发生在尾调用之前，避免了调用栈嵌套。

> **尾调用tail call**是函数式编程的一个重要概念，简单来说就是函数的return返回语句不是直接返回某个值， 而是通过调用另一个函数来获得返回值。例如： x函数的return调用了y函数，这就是一个尾调用。
```mojo
function x () {    # 这不是mojo代码， 是一段伪代码。
  return y()
} 
```
> **尾调用的嵌套问题：** 函数调用会在内存中形成一个调用栈，保存着调用位置和内部变量等信息，在上面的示例中，在函数x中调用函数y，也就是说在调用栈中，函数X上面还会有函数Y，当函数Y执行完毕之后出栈，将结果给到函数X，如果函数Y还调用了函数Z，那么调用栈中还会有函数Z...如果嵌套很多层，比如一些递归调用，或者递归实现的无限循环（例如事件循环），这将消耗完我们的内存，最终导致内存溢出。 


### `小数据`和`自销毁`字段组成的结构体，不需要析构函数，就可消耗
对于`小数据类型`和`自销毁类型`，Mojo知道如何销毁它们。 所以如果**结构体是由`小数据类型`和`自销毁类型`的字段组成**的，**不需要自定义实现析构函数`__del()__`**，就可以销毁。
- Mojo标准库中定义的所有的类型，除了指针`Pointer`，都是可以**自销毁的destructible**。


### `__del__` 属于 额外清理
```mojo
    fn __del__(owned self):
```

Mojo使用静态编译器来分析查找值最后一次使用的位置，然后，在该位置结束值的生存期，并调用 `__del__()` 析构函数来执行必要的资源清理。

- `__del__()` 方法是一个**额外的清理事件**，并且您的实现不会覆盖任何默认的销毁行为。**额外的意思**就是用来释放那些自己手动分配的内存，或者手动打开的文件句柄。 像`小数据`和`自销毁`，Mojo知道如何销毁它们，所以就不需要额外的`__del__()`
- 在析构函数`__del__()`返回之前， `self`的值仍然是完整的可用。

下面这个例子：因为String 和Int 都是可以自销毁的，Mojo知道如何销毁它们，并没有其它需要额外清理的。所以即使定义的是一个**空的`__del__()`**， 这个结构体也是可以正常销毁。
```mojo
struct MyPet:
    var name: String
    var age: Int

    fn __init__(inout self, name: String, age: Int):
        self.name = name
        self.age = age

    fn __del__(owned self):
        pass
```


如果自定义结构体含有其它不是`小数据`和`自销毁`组成的字段，比如手动使用`Pointer`在堆上heap分配了内存空间，或者手动打开了文件句柄。那么就要实现 `__del__()` 方法来执行必要的额外清理。
```mojo
struct HeapArray:
    var data: Pointer[Int]
    var size: Int

    fn __init__(inout self, size: Int, val: Int):
        self.size = size
        self.data = Pointer[Int].alloc(self.size)   # 手动分配的堆空间heap
        for i in range(self.size):
            self.data.store(i, val)

    fn __del__(owned self):
        self.data.free()    # 释放手动分配的堆空间heap
```


### 结构体的字段`可以临时转移`，结构体对象要`整体有效`才能作为一个整体使用。

结构体字段的所有权可以临时转移。 当结构体对象要作为一个整体使用时，必须确保是**整体有效**的，如果是**部分初始化**状态，会报错。 

例如，下面的结构体对象pet，它的字段name的所有权被转移了`pet.name^`，name变成无效，pet成了“部分初始化”状态，不再是**整体有效**， 所以调用`__del__`销毁的时候，报错。 解决办法就是重新初始化 `pet.name = String("Jasper") `，让pet对象整体重新有效。
```mojo
@value
struct MyPet:
    var name: String    # 定义了2个结构体字段 name 和 age
    var age: Int

fn consume(owned arg: String):
    pass

fn use(arg: MyPet):
    print(arg.name)

fn main():
    var pet = MyPet("Selma", 5)
    consume(pet.name^)  # 结构体字段name的所有权转移了，name变成无效，pet成了“部分初始化”状态（整体无效）

    # use(pet)  # 调用这句会出错， 因为 pet.name是无效的

    # pet.name = String("Jasper")  # 重新初始化pet.name， pet对象整体又有效了。
    # use(pet)                     
    # 这里会隐式触发调用 pet.__del__() 如果 pet是“部分初始化”状态，会报错。
```



# `struct` 编译时绑定、不允许动态分派和运行时更改
Mojo的 `struct` 类似于Python中的 class，它们都支持方法，字段，运算符重载，元编程的装饰器等等。然而，M**ojo的结构struct是完全静态的**，它们在**编译时绑定**，因此它们**不允许动态分派**或**对结构进行任何运行时更改**。

Mojo语言没有内置数据类型。所有数据类型，包括标准库中的基本类型，如 Bool 、 Int 和 String；以及复杂类型，如 SIMD 和 object 等都是用结构struct实现的。
- Mojo结构体不支持静态数据成员(字段)。
- Mojo结构体不支持继承，但结构体可以实现trait。

### 结构体 字段field `var`声明、不能有初始值
- 结构体的 **字段用`var`声明，不能有初始值**。 字段只能在`初始化构造器__init__()`中完成初始化， 而且 **所有字段都必须完成初始化**。目前，结构体不支持用 `let `声明字段

### 结构体 实例方法 第一个参数是`self`
结构体 `实例方法`必须通过结构体的实例来访问，它的 **第一个参数是 `self`**（只是一个约定、用其它的名称也可以) 用来代表当前的结构体对象，而且**可以省略类型**，Mojo会自动把当前的结构体实例传给它。可以**通过`self`访问`结构体的字段`**。
- 实例方法第一个参数的更准确的意思是：不管第一个参数的名称是什么，Mojo都会自动把当前的结构体实例传给它，只是大家习惯用`self`。

```mojo
struct MyPair:
    var first: Int      # 用 var 声明2个字段 first 和 second
    var second: Int     # 没有初始值

    fn __init__(inout self, first: Int, second: Int):  # 在初始化构造器 完全对所有字段的初始化
        self.first = first
        self.second = second

    fn get_sum(self) -> Int:            # 实例方法， 第一个参数是 self
        return self.first + self.second

fn main():
    let mine = MyPair(6, 8)
    print(mine.get_sum())       # 通过实例调用 实例方法
```

### 结构体 静态方法 `@staticmethod` 没有`self`
**声明`静态方法`要用 `@staticmethod`** 装饰器，第一个参数不是`self`(核心要表达的是：第一个参数不会隐式接收结构体实例），因此静态方法**不能访问`结构体的字段`**，而且第一个参数一定要指定类型。
- 静态方法第一个参数更准确的意思是：静态方法的第一个参数的名称无论叫什么，即使第一个参数命名为self，都不会隐式接收结构体实例。因为即使是实例方法的第一个参数，也不是强制一定要命名为`self`，用其它名称也可以。

可以 **`用类型`调用静态方法**，也可以 **`用实例`来调用**。

```mojo
struct Logger:
    fn __init__(inout self):
        pass

    @staticmethod                   #  用 @staticmethod 什么静态方法
    fn log_info(message: String):   # 
        print("Info: ", message)

fn main():
    Logger.log_info("Static method called.")   # 用类型 调用静态方法
    let l = Logger()
    l.log_info("Static method called from instance.")       # 用实例来调用 静态方法


```

### dunder方法 | 魔术方法 magic methods | 特殊方法 Special methods

Mojo支持一长串dunder方法，它们通常与Python的所有dunder方法匹配，分成2种类型：
1. **运算符重载Operator overloading**，很多dunder方法都是为了`重载操作符`而设计的。 例如 Int的`__lt__()`，用来执行整数 **小于比较**，例如 `if num1 < num2 :` 
2. 和实例生命周期有关的[生命周期方法](#值的生命周期方法-value-lifecycle-method) 



# `trait` & generic 泛型
**使用`trait`作为函数的参数类型**，**可以让你编写泛型函数**，它可以接受任何实现了该trait的类型，而不仅仅是某个特定的类型。

目前，`trait`里唯一可以定义的是方法的签名，而且方法签名后面必须跟三个点 `...` 表示该方法未实现。 
- 目前`trait`定义的方法**不能有默认实现**。在未来，计划支持在trait中**定义字段**和**默认方法实现**。
- `trait`可以定义`静态方法 @staticmethod`
- `trait`可以定义所需的生命周期方法，比如`初始化构造函数__init__()`, `移动构造函数__moveinit__()`等等。


#### 定义`trait` 方法后面有三个点 `...` 表示未实现
```mojo
trait Shape:
    fn area(self) -> Float64: ...   # 方法签名后面必须跟三个点 `...` 表示该方法未实现
```

#### 实现`trait` 放在括号里`( )`，多个用逗号`,`分隔
```mojo
@value
struct Circle(Shape):
    var radius: Float64

    fn area(self) -> Float64:
        return 3.141592653589793 * self.radius ** 2

```

#### 使用`trait`
使用`trait`Shape来约束编译时参数`T`
```mojo
fn print_area[T: Shape](shape: T):
    print(shape.area())


let circle = Circle(radius=1.5)  
print_area(circle)          # 不需要传递方括号[]里的编译时参数T，可以从实参推断出来，如果要传也是可以的。
print_area[Circle](circle)   # 传递方括号[]里的编译时参数T

```

#### trait 可以继承 放在括号里`( )`，多个用逗号`,`分隔
```mojo
trait Parent:
    fn parent_func(self): ...

trait Child(Parent):
    fn child_func(self): ...
```

#### `trait`定义`静态方法 @staticmethod`
```mojo
trait HasStaticMethod:
    @staticmethod           # 定义静态方法
    fn do_stuff(): ...

fn fun_with_traits[T: HasStaticMethod]():
    T.do_stuff()            # 用类型名调用 静态方法
```

#### `trait`定义所需的生命周期方法
```mojo
trait DefaultConstructible:
    fn __init__(inout self): ...

trait MassProducible(DefaultConstructible, Movable):  # Moveable 定义了 移动构造函数 __moveinit__ 
    pass

struct Thing(MassProducible):
    var id: Int

    fn __init__(inout self):
        self.id = 0

    fn __moveinit__(inout self, owned existing: Self):
        self.id = existing.id

fn factory[T: MassProducible]() -> T:
    return T()
    
fn main():
    let thing = factory[Thing]()
```


# 内置装饰器 `@unroll`

### **`@unroll` 编译时展开循环**
**`@unroll` 编译时展开循环**，用在`for`、`while`上面，要求： 
- **循环次数**必须是**编译时确定、运行时保持不变**
- **循环没有提前或中途退出**，因为这将使循环次数在运行时是可变。

```mojo
@unroll
for i in range(3):
    print(i)

# 相当于下面的语句

print(0)
print(1)
print(2)
```

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
- size(Int): SIMD向量的**长度**（**要求是2的幂**， 如：1, 2, 4, 8...）, 代表**可以存储 多少个类型是type的数据元素**。

**内置的** `Scalar、Int8、UInt8、Int16、UInt16...Int64、UInt64 、Float16、 Float32、Float64` 都是 SIMD子类型的 **别名Aliase**。
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

### Mojo SIMD的例子
```mojo
fn main():
    let a = SIMD[DType.int64, 4](1,  2, 3, 4)
    let b = SIMD[DType.int64, 4](10, 20, 30, 40)
    let c = a + b
    for i in range(4):
        print_no_newline(c[i], " ")  # 11  22  33  44
```

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



# raises


# Tensor



# docstrings API 文档
API 文档 `docstrings` 就是在函数名字的下面，用**3对双引号**`""" ... """`括起来的内容，一般按照下面这样的格式：
```mojo
fn print(x: String):
    """Prints a string.

    Args:
        x: The string to print.
    """
    ...
```

可以使用 `mojo doc` 命令从这些`docstrings`生成API说明文档。

# Python 集成
可以直接在Mojo中导入和运行Python代码，Mojo底层通过使用CPython来直接运行，因此在Mojo中执行Python并不比使用CPython快！

### 1. 从python包导入Mojo的`Python`模块 
```mojo
from python import Python
```

### 2. 用`Python.import_module("模块名")`导入需要的Python库。 
比如，这里导入numpy
```mojo
let np = Python.import_module("numpy")
```

完整实例如下：
```mojo
from python import Python

fn use_numpy() raises:
    let np = Python.import_module("numpy")
    let ar = np.arange(15).reshape(3, 5)
    print(ar)
    print(ar.shape)
```
