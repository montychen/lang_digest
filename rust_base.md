# std标准库& prelude
Rust有一个极简标准库，叫作**std**。用户不需要手动添加对标准库的依赖，编译器会自动引入对标准库的依赖。除此之外，标准库中的某些type、trait、function、macro等实在是太常用了。每次都写use语句确实非常无聊和冗长，因此标准库提供了一个`std::prelude`模块包含这些东东，编译器也会为自动引入:
```rust
use std::prelude::*;
```

# println!常用输出格式
Rust的宏macro是一种编译器扩展，它的调用方式为some_macro!(...)，宏调用后面都跟着一个 **`感叹号!`**。 println!是一个宏，用于向标准输出打印字符串，常用的格式有。
```rust
fn main() {
    println!("{}", 1);            // 默认用法,打印Display.   输出： 1
    println!("{:p}", &0);         // 指针地址                输出： 0x10049e7fc

    println!("{:?}", "test");                // 打印Debug                 输出："test" 
    println!("{:#?}", ("test1", "test2"));   // 带换行和缩进的Debug打印   输出：(
                                                                          //       "test1",
                                                                          //       "test2",
                                                                          //    )
    println!("{:x}", 255);  // 十六进制 小写    输出：ff 
    println!("{:X}", 255);  // 十六进制 大写    输出：FF
    println!("{:b}", 15);   // 二进制           输出：1111 

    println!("{a} {b} {b}", a = "x", b = "y"); // 命名参数    输出： x y y
}
```

# 变量遮蔽shadowing
Rust允许在同一个代码块中声明同样名字的变量。如果这样做，后面声明的变量会将前面声明的变量“遮蔽”(Shadowing)起来，前面声明的变量将不再可用。
```rust
fn main() {
       let x = "hello";
       println!("x is {}", x);

       let x = 5;     // x 重新声明，遮蔽了之前的声明，现在x的值是数字 5, 而不再是字符串"hello" 
       println!("x is {}", x);   // 输出：  x is 5
   }
```
变量遮蔽在某些情况下非常有用，比如，在同一个函数内部，需要修改一个变量的可变性。例如，我们对一个可变数组执行初始化，希望此时它是可读写的，但是初始化完成后，我们希望它是只读的。可以这样做:
```rust
// 注意:这段代码只是演示变量遮蔽功能,并不是Vec类型的最佳初始化方法 
fn main() {
    let mut v = Vec::new();  // v 必须是mut修饰,因为我们需要对它写入数据
    v.push(1);
    v.push(2);
    v.push(3);

    let v = v;               // 从这里往下,v成了只读变量,可读写变量v已经被遮蔽,无法再访问
    for i in &v {
        println!("{}", i);
    }
}
```
反过来，如果一个变量是不可变的，我们也可以通过变量遮蔽创建一个新的、可变的同名变量。
```rust
fn main() {
       let v = Vec::new();
       let mut v = v;
       v.push(1);
       println!("{:?}", v);
}
```

# char类型和ASCII字符
**char类型**的设计目的是描述任意一个unicode字符，因此它占据的内存空间不是1个字节，而是**4个字节**。单个的字符字面量用**单引号**包围
```rust
let good = '好';    // good的类型是 char
```

对于ASCII字符其实只需占用1个字节的空间，因此Rust提供了**单字节字符字面量**来表示ASCII字符。我们可以在字符或者字符串前面使用一个**字母b**，代表这个字面量存储在u8类型数组中，这样占用空间比char型数组要小一些。
```rust
let y :u8 = b'A';
let s :&[u8;5] = b"hello";
let r :&[u8;14] = br#"hello \n world"#;
```

# 整数溢出overflow
在debug模式 下编译器会自动插入整数溢出检查，一旦发生溢出，则会引发panic; 在release模式下，不检查整数溢出，而是采用自动舍弃高位的方式，程序不会报错。需要更精细地自主控制整数溢出的行为，可以调用标准库中的checked_、saturating_ 和wrapping_系列函数进行数学运算。推荐使用 checked_** 系列函数，结果更可控。
- checked_** 系列函数返回的类型是Option<\_>，当出现溢出的时候，返回值是None; 没溢出返回Some(v)
- saturating_** 系列函数返回类型是整数，如果溢出，则给出该类型的**最大/最小值**;
- wrapping_** 系列函数则是直接抛弃已经溢出的最高位，将剩下的部分返回
```rust
fn main() {
    println!("i8::MAX = {}\n", i8::MAX);         // i8::MAX = 127

    let i = 100_i8;
    println!("checked {:?}", i.checked_add(i));  // 溢出，输出：checked None
    if let Some(n) = i.checked_add(20) {         // 没溢出，返回Some（120）
        println!("{}", n);                       // 120
    }

    println!("saturating {:?}", i.saturating_add(i));  // 溢出，取最大值 saturating 127
    println!("wrapping {:?}", i.wrapping_add(i));      // 溢出, 抛弃已经溢出的最高位，将剩下的部分返回, 输出： wrapping -56
}
```

# tuple元组
如果元组中只包含一个元素，应该在后面添加一个 **`,逗号`**。 以区分括号表达式和元组
```rust
let a = (0,);   // a是一个元组,只有一个元素， 注意后面一定有个逗号
let b = (0);    // b是一个括号表达式,它是i32类型
```
访问tuple元组内部元素有两种方法，一种是**模式匹配 pattern destructuring**，另外一种是**数字索引**
```rust
fn main(){
    let p = (1i32, 2i32);
    let (a, b) = p;         // 模式匹配
    
    let x = p.0;            // 数字索引
    let y = p.1;
    println!("{} {} {} {}", a, b, x, y);  // 输出：1  2  1  2
}
```
### unit 单元类型/空元组
一个元素都没有的元组叫**unit单元类型/空元组**, 如： **`let empty : () = ();`**。 `空元组`和`空结构体struct Foo;`一样，都是占用0内存空间。这与C++中的空类型不同，Rust中存在实打实的0大小的类型。
```rust
fn main() {
     println!("i8占用字节 {}" , std::mem::size_of::<i8>());         // i8占用字节 1
     println!("char占用字节 {}" , std::mem::size_of::<char>());     // char占用字节 4
     println!("空元组() 占用字节{}" , std::mem::size_of::<()>());   // 空元组() 占用字节 0
}
```


# struct结构体
Rust中除了常规的结构体之外，还有 tuple结构体，单元结构体。

**Unit结构体/空结构体**没有字段, 这种类型的值不占用内存，很像`单元类型()`，只是它有自己的类型名称，但它的值只能有一个。
```rust
struct Onesuch;       // 单元结构体
let o = Onesuch;      // 单元结构体的值只有一个
```

结构体默认只能在当前模块和子模块中使用，如果想要导出结构体需要使用**pub**标识，字段也是同样的道理

如果用同名的变量对struct进行初始化，那么可以用简写语法
```rust
struct Point {
    x: i32,
    y: i32,
}

fn main() {
    let x = 10;
    let y = 20;
    // 用同名的变量对struct进行初始化，那么可以用简写语法, 等同于 Point { x: x, y: y }
    let p = Point { x, y }; 
    println!("Point is at {} {}", p.x, p.y);
}
```

使用相同类型的结构变量去初始化另外一个，在末尾使用`.. 运算符`，自动填充未显示赋值的字段
```rust
#[derive(Debug)]
struct Person {
    name: String,
    age: i32,
    sex: char,
}

fn main() {
    let p1 = Person {
        name: "michael".to_string(),
        age: 28,
        sex: '男',
    };

    let p2 = Person {
        name: "skye".to_string(),
        ..p1            // .. 使用同类型的结构体变量去初始化 
    };

    println!("p1: {:?}, pw: {:?}", p1, p2);  
    // 输出 p1: Person { name: "michael", age: 28, sex: '男' }, pw: Person { name: "skye", age: 28, sex: '男' }
}
```

### tuple struct 元组结构体
有时候我们不需要特别关心结构体内部成员的名字，可以采用这种`tuple struct`它就像是tuple和struct的混合。区别在于，tuple struct有名字，而它们的成员没有名字。
```rust
struct Color(i32, i32, i32);
struct Point(i32, i32, i32);

// 它们可以被想象成这样的结构体
struct Color{
    0: i32,
    1: i32,
    2: i32,
}
struct Point {
    0: i32,
    1: i32,
    2: i32,
}
```
**什么是newtype？**  tuple struct有一个特别有用的场景，那就是当它只包含一个元素的时候，就是所谓的newtype idiom。因为它实际上让我们非常方便地在一个类型的基础上创建了一个新的类型，如： `struct Year(u32);` newtype的优点：
- 自定义类型可以让我们给出更有意义和可读性的类型名
- 某些场景，只有newtype可以很好的解决
- 隐藏内部类型的细节
```rust
fn main() {
    struct Year(u32);

    fn f1(value: Year) {}
    fn f2(value: u32) {}
    let v: u32 = 0;
    f1(v); // 编译不过, 类型不匹配 expected struct `Year`, found `u32`
    f2(v);
}
```
通过newtype自定义一个类型给出更有意义的命名
```rust
struct Years(i64);
struct Days(i64);

impl Years {
    pub fn to_days(&self) -> Days {
        Days(self.0 * 365)
    }
}

impl Days {
    pub fn to_years(&self) -> Years {
        Years(self.0 / 365)
    }
}
```


# enum枚举
Rust的enum与C/C++的enum和union都不一样。它是一种更安全的类型，可以被称为“tagged union”。 Rust里面也支持union类型，这个类型与C语言中的union完全一致。 但在Rust里面，读取它内部的值被认为是unsafe行为，一般情况下我们 不使用这种类型。它存在的主要目的是为了方便与C语言进行交互。

在Rust中，enum和struct为内部成员创建了新的名字空间。如果要访问内部成员，使用`::符号`

# Rust三种循环loop、while和for循环
```rust
// loop里面的代码一定会被执行， 直到遇到break语句才会跳出循环
loop {
  code
}

// while循环每次执行循环体代码之前都会先判断一次条件，当条件成立时才执行循环体代码
while expression {
  code
}

// for用于遍历一个迭代器
for var in iterator {
  code
}

// for当然也可以返回元素的索引，只需要一个.enumerate()函数，比如
for (i,v) in (1..=3).enumerate() {
    println!("索引为{}的元素是{}", i, v);
}
```

### loop & while true 区别
**loop{ }** 和 **while true{ }** 循环有什么区别，为什么Rust专门设计了一个死循环，loop语句难道不是完全多余的吗? 实际上不是。主要原因在于，相比于其他的许多语言，Rust语言要做更多的静态分析。loop和while true语句在运行时没有什么区别，它们主要是会影响编译器内部的静态分析结果。

比如下面这个代码是合法的:
```rust
fn main() {
    let x;
    loop {
        x = 1;
        break;
    }
    println!("{}", x);
}
```
相反，下面这个代码编译出错, 因为编译器会觉得while语句的执行跟条件表达式在运行阶段的值有关，因此它不确定y是否一定会初始化，于是它决定给出一个错误: borrow of possibly-uninitialized variable: `y`
```rust
fn main() {
    let y;
    while true {
        y = 1;
        break;
    }

    println!("{}", y);
}
```



### break & continue
break语句和continue语句还可以在多重循环中选择跳出到哪一层:  先在**loop、 while、 for**循环前面加上以 **单引号'** 开头的生命周期标识符， 然后在内部的循环中可以使用break/continue语句选择跳出到指定的那一层。
```rust
fn main() {
    // A counter variable
    let mut m = 1;
    let n = 1;
    'a: loop {             // 以单引号开头，定义了生命周期标识符a
        if m < 100 {
            m += 1;
        } else {
            'b: loop {     // 以单引号开头，定义了生命周期标识符b
                if m + n > 50 {
                    println!("break");
                    break 'a;      // 跳出指定的循环
                } else {
                    continue 'a;
                }
            }
        }
    }
}
```


# 函数
### fn item 函数项 & 函数指针function pointer 
**fn item/function item 函数项**指的是`函数本身的类型`, 在Rust中，每个函数项都有一个自己唯一的类型，实际上函数项的类型是不可命名的，因为整个函数本身才是它真正的类型，但理解上可以考虑用函数的名字来表示函数项的类型名称, 即使两个函数的签名完全相同，毕竟这是2个不同名的函数。
- 函数项不会占用内存空间，也就是说它的内存占用是0。
- 编译器把函数项类型显示为类似 `fn((_, _)) -> _ {add1}` 的内容 (函数名称在 {} 中)。
- 尽可能地使用函数项类型，不到万不得已不要使用函数指针类型，这样有助于享受零大小类型的优化。
<pre>different `fn` items always have unique types, even if the ir signatures are the same</pre>
如下例所示，虽然add1和add2有同样的签名（参数类型和返回值类型都一样），但它们是不同的**函数项**，所以报错了
```rust
fn add1(t: (i32, i32)) -> i32 {
    t.0 + t.1
}

fn add2(t: (i32, i32)) -> i32 {
    t.0 + t.1
}

fn main() {
    let mut ef = add1;    // ef 的类型是函数项 Fn item， 类型名就是函数名add1 
    assert_eq!(std::mem::size_of_val(&ef), 0);   // 函数项不会占用内存空间，也就是说它的内存占用是0。 
    ef = add2;            // 这句会报错：重新赋值, 让ef指向另一函数项 add2, 毕竟是2个函数，类型不同编译不过

    let mut of = add1 as fn((i32,i32)) -> i32;   // 通过显式指定函数类型转换为一个函数指针类型, of的类型是函数指针
    println!("{:p}", of);                        // 0x104fe4e54 ，指针可以通过{:p}格式打印地址，而非指针不行
    of = add2;

    let p = (1, 3);
    println!("{}", of(p));
}
```
<pre>
error[E0308]: mismatched types
  --> src/main.rs:12:10
   |
10 |     let mut ef = add1; // ef 的类型是函数项 Fn item， 类型名就是函数名add1
   |                  ---- expected due to this value
11 |     assert_eq!(std::mem::size_of_val(&ef), 0); // 函数项不会占用内存空间，也就是说它的内存占用是0。
12 |     ef = add2; // 这句会报错：重新赋值, 让ef指向另一函数项 add2, 毕竟是2个函数，类型不同编译不过
   |          ^^^^ expected fn item, found a different fn item
   |
   = note: expected fn item `fn((_, _)) -> _ {add1}`
              found fn item `fn((_, _)) -> _ {add2}`
   = note: different `fn` items always have unique types, even if their signatures are the same
   = help: change the expected type to be function pointer `fn((i32, i32)) -> i32`
</pre>
    

**函数指针**: 看起来像 `fn((i32, i32)) -> i32`这样的类型。函数指针不能包含数据，顾名思义，它们是指针, **不是零大小的**；一个函数指针可以指向一个函数项，也可以指向一个不捕获任何东西的闭包，但它不能为空。
 
- 函数项可以通过显式指定函数指针类型转换为函数指针类型。如:`let of = add1 as fn((i32,i32)) ->i32`
- 函数项和闭包会在可能的情况下自动强制转换为相关的函数指针类型，这就是 `let f: fn(i32) = |_| ();` 合法的原因。因为闭包不捕获任何内容，因此可以将其强制转换为函数指针。 


### 发散函数diverging function
**发散函数diverging function**永远不会被返回，它们的返回值被标记 **感叹号!** 。当程序调用发散函数时，该进程将直接进入崩溃（一般上来讲是发生程序员无法处理的错误时调用）。需要注意的是，函数中不返回的函数有很多，但只有发散函数这种不返回，也不会向下执行，或者说当前线程就崩溃了，退出了。而其它不返回的函数，程序仍然会继续向下执行。最简单的例子就是在loop循环中调用一些不返回的函数来反复监听或者执行某项任务。
```rust
fn foo() -> ! {
    panic!("This call never returns.");
}
```
在发散函数后面，如果仍然有一些其它的代码，编译器会报类似下面的警告“warning: unreachable statement --> src\main.rs:4:5”。
所以说，发散函数可以作为一种意外的条件让线程终止的方式。一般来说它都是在panic！宏调用时使用或者其它发散函数的再调用。

**发散类型的最大特点就是，它和任意类型兼容、可以被转换为任意类型**, 我们为什么需要这样的一种返回类型呢?先看下面的例子: 包含一个if-else分支结构的表达式。我们知道，对于分支结构的表达式，它的每条分支的类型必须一致。那么这条panic! 宏应该生成一个什么类型呢? 这就是!类型的作用了。因为它可以与任意类型相容，所以编译器的类型检查才能通过。
```rust
let p = if x {
    panic!("error");
} else {
    100
};
```


### const fn
函数可以用const关键字修饰，这样的函数可以在编译阶段被编译器执行，返回值也被视为编译期常量。
```rust
const fn cube(num: usize) -> usize {
    num * num * num
}
fn main() {
    const DIM : usize = cube(2);
    const ARR : [i32; DIM] = [0; DIM];
    println!("{:?}", ARR);      //  [0, 0, 0, 0, 0, 0, 0, 0]
}
```

### 尾递归tail call/tail recursive
**尾调用tail call**是函数式编程的一个重要概念，简单来说就是在函数执行的最后一步调用另一个函数，举例说明，这段代码中，在x函数的最后一步调用了y函数，就是一个尾调用

```rust
function x () {
  return y()
}
```
**尾调用优化**函数调用会在内存中形成一个调用栈，保存着调用位置和内部变量等信息，在我们的示例中，在函数x中调用函数y，也就是说在调用栈中，函数X上面还会有函数Y，当函数Y执行完毕之后出栈，将结果给到函数X，如果函数Y还调用了函数Z，那么调用栈中还会有函数Z。当函数中存在尾调用时，事实上当前函数的内部变量和调用位置等信息其实已经没有用了，所以当前函数其实已经没有必要存在在栈中了，**直接使用被尾调用的函数的调用信息取代当前函数就可以了**，这就是尾调用优化。

也有几种类似的情况，但它们不属于尾调用
```rust
//情况一
function x() {
  let y = g();
  return y;  //函数调用之后还有赋值操作，不属于尾调用
}

//情况二
function x() {
 return y() +1;  //函数调用后还有运算，不属于尾调用
}

// 情况三
function x() {
  y();    //函数调用之后还有一行隐式的return语句，也不属于尾调用
}
```
**尾递归tail recursive**函数尾调用的函数是自身，那就是尾递归了。举一个递归的写法来说明
```rust
function factorial(n) {
  if (n === 1) return 1;
  return n * factorial(n - 1);   // 不是尾调用，因此它也不是尾递归
}

factorial(5);
```
在上面这个递归函数写法中，最后一行递归执行不是尾调用，因此它也不是尾递归，这样的话也不会适用于尾调用优化，也就是说每一次调用都会在栈中叠加一个本身函数的调用信息。如果调用n次，则需要保存n个调用记录，如果改造成尾递归，则只会保存一个函数的调用信息
```rust
function factorial(n, total) {
  if (n === 1) return total;
  return factorial(n - 1, n * total);     // 这是尾递归
}

factorial(5, 1) // 120
```
尾调用优化能对递归调用起到很大的优化作用。再举一个例子，斐波那契数列
```rust
function Fibonacci (n) {
  if ( n <= 1 ) {return 1};

  return Fibonacci(n - 1) + Fibonacci(n - 2);   // 这不是尾调用
}

Fibonacci(10) // 89
Fibonacci(100) // 超时
Fibonacci(500) // 超时


// 改写为尾递归之后
function Fibonacci2 (n , ac1 = 1 , ac2 = 1) {
  if( n <= 1 ) {return ac2};

  return Fibonacci2 (n - 1, ac2, ac1 + ac2);  // 这是尾递归
}

Fibonacci2(100) // 573147844013817200000
Fibonacci2(1000) // 7.0330367711422765e+208
Fibonacci2(10000) // Infinity
```



# 内存
并非所有的内存都是平等的:

**栈stack:** 栈是一个内存段，用于程序中函数调用的暂存空间。每次调用函数时，都会在栈顶分配一个称为帧（frame）的连续内存块。靠近栈底部的是主函数的帧，当函数调用其他函数时，额外的帧被压入栈。函数的帧包含该函数中包含的所有变量，以及该函数接受的任何参数。当函数返回时，它的栈帧被回收。 所以如果函数调用时需要的空间超出了stack栈总空间的大小，就会发生**stack overflow错误**， 这种情况容易在函数递归调用时容易发生。
- **栈stack空间的大小**：当您编译和链接代码时，会生成一个可执行文件，可执行文件也包含了默认需要多少栈内存stack memory的信息。虽然在链接时可以手动指定栈内存的大小，但链接器有一个默认值，它通常是 8MB，但在 Windows 上可能只有 1MB。

- **stack空间的使用**：当程序启动，操作系统会根据app里指定的stack栈空间大小，预先给app分配那么多内存空间，并设置一个特殊寄存器来指向该内存的开头。现在，每当您在程序中定义局部变量时，它都会存储在栈stack中。此外，当您调用某个函数时，返回地址和所有或部分参数也存储在那里。例如，如果在某个函数中，您将一个局部变量定义为一个由 100 个整数组成的数组，并且如果一个整数占用 4 个字节，那么您只需从堆栈内存中分配 400 个字节。那么现在如何释放内存呢？好吧，因为当您从该函数返回时，再也不能使用每个局部变量和函数参数，所以该函数的所有内存都会自动释放。因此，每当程序进入一个新函数并声明新的局部变量时，我们说栈会增长，并且无论何时我们从一个函数返回，我们说栈缩小。

- **Stack Overflow 错误**：如果你用尽了为程序保留的所有栈内存并且您尝试进行另一个函数调用，程序将因栈溢出错误而失败。需要注意的是，编译器通常以这样一种方式编译代码，即一旦输入函数，所有局部变量的空间就会立即被保留。即使某些变量仅在某些条件块中使用，也会在函数开始时为其保留空间。这就是为什么只有在输入新函数时才会发生 **Stack Overflow 错误**。

这通常是您可以从操作系统请求的额外内存，这是您实际需要管理并在不再需要时正确释放的内存。当函数返回时，您还想保存某些值供后续使用，亦或某些东西需要太大的存储空间而无法放入stack栈中

**堆heap:** 堆是一个内存池，与当前程序的调用stack栈无关。它的生存期和程序运行时一样长，在堆内存中的值会一直存在，直到它们被明确地释放。
- 堆heap通常是您可以从操作系统请求的额外内存，这是您实际需要管理并在不再需要时正确释放的内存。当在函数返回后，你还想保存某些值供后续使用；又或者某些东西需要的存储空间太大而无法放入stack栈中，这时候就需要堆heap。
- Rust 中与堆交互的主要机制是 **`Box`** 类型。当你写`Box::new(value)`时，该值被放到堆上，而你得到的结果 `Box<T>` 是堆上该值的一个指针。当 Box 最终被`析构Drop`时，该内存被释放。如果你忘记释放堆内存，它会永远存在，而你的应用程序最终会吃掉机器上的所有内存。

**静态内存Static memory :**
静态内存是已经编译好的执行文件中的几个密切相关区域的总称。当程序被执行时，这些区域会自动加载到内存中。静态内存中的值在程序整个执行过程中一直存在, 在整个程序结束前都不会被释放。静态内存里的内容通常都是只读的，如：程序的二进制代码，静态关键字`static`声明的静态变量，代码中的字面量常量。

**const**用来声明全局可用的**常量**, 值不可修改、一定不允许用mut关键字来修饰、声明时一般需要大写、而且要指定类型。const常量并没有固定的内存地址，因为在编译阶段它们会被**内联**到用到它们的地方, 无运行时开销。如： `const N: i32 = 5;`

**static** 用来声明**静态变量/static变量**，而且它的生存期贯穿整个程序，static 变量的生命周期永远是'static，它占用的内存空间也不会在执行过程中回收。这也是Rust中唯一的声明全局变量的方法。所以也叫**全局变量**。声明时一般需要大写、而且要指定类型, 不过静态变量在使用时并不内联。这意味着对每一个值只有一个实例，并且位于静态内存区域。和常量不同，全局变量可以定义为可变的mut, 也就是`可变全局变量`，那就会出现被多个线程同时访问的情况，因而引发内存不安全的问题，所以对于全局可变(static mut)变量的访问和修改代码就必须在unsafe块中。
```rust
static mut NUM:i32 = 100;   // 可变全局变量

unsafe {
    NUM += 1;
    println!("NUM: {}", NUM);
}
```



内存安全memory safety的3个主要问题
1. 内存的不正确访问引发的内存安全问题
    1. 使用未初始化的内存
    2. 对空指针解引用(dereference)
    3. 悬垂指针(使用已经被释放的内存)
    4. 缓冲区溢出
    5. 非法释放内存(释放未分配的指针或重复释放指针)

2. 由于多个变量指向同一块内存区域导致的数据一致性问题
3. 由于变量在多个线程中传递，导致的数据竞争data race的问题

比如下面这个C/C++代码是有严重内存问题的，但还是可以编译通过，当然，编译器还是会给出警告信息。这段代码也是可以运行的，也会输出信息
```c++
#include <iostream>
struct Point {
	int x;
	int y;
};

Point* newPoint(int x,int y) {
	Point p { .x=x, .y=y };
	return &p; //悬垂指针
}

int main() {
	int values[3]= { 1,2,3 };
	std::cout<<values[0]<<","<<values[3]<<std::endl; //缓冲区溢出

	Point *p1 = (Point*)malloc(sizeof(Point));
	std::cout<<p1->x<<","<<p1->y<<std::endl; //使用未初始化内存

	Point *p2 = newPoint(10,10); //悬垂指针
	delete p2; //非法释放内存

	p1 = NULL;
	std::cout<<p1->x<<std::endl; //对空指针解引用
	return 0;
}
```

**为什么要转移所有权？** 我们知道，C/C++/Rust 的变量关联了某个内存区域，但变量总会在表达式中进行操作再赋值给另一个变量，或者在函数间传递。实际上期望被传递的是变量绑定的内存区域的内容，如果这块内存区域比较大，复制内存数据到给新的变量就是开销很大的操作。所以需要把所有权转移给新的变量，同时当前变量放弃所有权。所以归根结底，转移所有权还是为了性能。


# 所有权、生命周期、借用
- 一个值只能有一个所有者owner
- 您可以对一个值有多个共享的不可变引用 immutable reference
- 一个值只能有一个可变引用 mutable reference

# Copy
Rust 中大多数原生类型，比如整数和浮点类型，都是 复制（Copy）类型。要成为复制类型，必须能够做到简单地通过复制它们的比特位来复制该类型的值。这就排除了所有包含非复制类型的类型，以及任何拥有资源的类型。因为当值被析构时，它必须被释放。

# Arc 和 Mutex
Arc: 当你需要在线程之间共享东西时，`Arc`应该是你尝试的第一件事，而不是最后一个。大多数时候它会足够快，不用担心。那么只有当你需要更高的性能或者你认为你可以提供更好的 API 时，你才能尝试更高级的东西，


Mutex: 当你需要修改在线程间共享的数据时，你还需要使用Mutex。当你想要修改线程间共享的数据，并且无法通过使用引用来共享一个Mutex时，你应该使用`Arc<Mutex<...>>`


# 字符串String 和 &str 
rust字符串是unicode字符序列，但内存表示并不是字符数组，它们以UTF-8格式存储，一种变宽编码，ASCII字符以1个字节存储，其他的以多个字节存储。
- 字符串可以直接换行，**折行**前面的空格也包含在内，假如换行的上一行以 **反斜杠\\** 结尾，则折行前面的空格不包含在内。
- 字符串前面加**b**，叫**字节字符串**，表示u8类型的切片，而不是字符串。
- 在字符串前面加r表示raw字符串


&str只读、无所有权，适合切片、字面量等不可变的情形；String可变、持所有权，适合字符串字段类型存储等情形。

**String**
- String是标准库的一个类型：std::string::String，是一个基于UTF-8的可增长的字符串，在堆上动态分配空间，对其保存的字符串内容有所有权。
- String通常用来创建一个可以修改的字符串。

**&str是什么？**
- &str是对String的一种借用形式，被称为字符串切片。使用&'static str代表对一个静态字符串的引用。`let hello: &'static str = "Hello, world!";`
- &str是字符串字面量的类型，它有点特殊，它是引用自“预分配文本(preallocated text)”的字符串切片，这个预分配文本存储在可执行程序的只读内存中。换句话说，这是装载我们程序的内存并且不依赖于在堆上分配的缓冲区。

**函数传参**
- 一般使用&str来传递一个只读的字符串引用变量。如果想获取字符串所有权，或者修改字符串，需要传递一个String。

**为什么Rust中的String不能用整数下标进行切片？**

&str、String 在底层是通过 Vec<u8> 实现的：字符串数据以字节数组的形式存在堆上，但在使用时，它们都是 UTF-8 编码的, 每次UTF-8 解析实际上是相当昂贵的。
- UTF-8是变长编码，如果你按照char的方式分割，性能低下
- 如果按照byte的方式分割，有可能拿到的不是合法的 `char boundary`
```rust
fn main() {
    let s: &str = "中国人";
    for c in s.chars() {
        println!("{}", c) // 依次输出：中 、 国 、 人
    }

    let c = &s[0..3]; // 1. "中" 在 UTF-8 中占用 3 个字节 2. Rust 不支持字符串索引，因此只能通过切片的方式获取 "中"
    assert_eq!(c, "中");
}
```

# if let

```
if let Ok(length) = fields[1].parse::<f32>() {
     // 输出到标准输出
     println!("{}, {}cm", name, length);
}
```

if let 是一个匹配表达式，用来从 = 右边的结果中，匹配出 length 的值：

1. 当=右边的表达式执行成功，则会返回一个 Ok(f32) 的类型，若失败，则会返回一个 Err(e) 类型，if let 的作用就是仅匹配 Ok 也就是成功的情况，如果是错误，就直接忽略
2. 同时 if let 还会做一次解构匹配，通过 Ok(length) 去匹配右边的 Ok(f32)，最终把相应的 f32 值赋给 length
3. 当然你也可以忽略成功的情况，用 `if let Err(e) = fields[1].parse::<f32>() {...}` 匹配出错误，然后打印出来
4. 类型标注，通过 `::<f32>` 的使用，告诉编译器 length 是f32 类型的浮点数。这种类型标注不常用，但是在编译器无法推断出你的数据类型时，就很有用了。

# 条件编译 `#[cfg(...)]`属性 和 `cfg!(...)`宏

`#[cfg(...)]`属性: 一般用在函数定义的开头，条件为假 false的代码不会编译而且也不会包含在最终生成的二进制代码中，所以 `#[cfg(...)]`可以用在 **同名函数中**

```rust
// 在MacOS系统下才编译
#[cfg(target_os = "macos")]
fn cross_platform() {
}

// 在windows系统下才编译
#[cfg(target_os = "windows")]
fn cross_platform() {
}

// 若条件`foo`或`bar`任意一个成立，则编译以下的Item
#[cfg(any(foo, bar))]
fn need_foo_or_bar() {
}

// 针对32位的Unix系统
#[cfg(all(unix, target_pointer_width = "32"))]
fn on_32bit_unix() {
}

// 若`foo`不成立时编译
#[cfg(not(foo))]
fn needs_not_foo() {
}
```

`cfg!(...)`宏：一般用在条件语句上

- cargo build 和 cargo run 默认是 debug模式
  
- release模式要明确指定 cargo build --release 或者 cargo run --release
  

```rust
// 在debug模式下才编译该语句 
 if cfg!(debug_assertions) { 
     // 输出到标准错误输出
     eprintln!("debug: {:?} -> {:?}",  record, fields);
 }
```

具体可以判断那些条件属性，在终端中运行 `rustc --print=cfg` 进行查询。当然也可以指定查询某个平台的属性 `rustc --print=cfg --target=x86_64-pc-windows-msvc`，该命令将对 64bit 的 Windows 进行查询。

```
$ rustc --print=cfg

    debug_assertions
    panic="unwind"
    target_arch="x86_64"
    target_endian="little"
    target_env=""
    target_family="unix"
    target_feature="fxsr"
    target_feature="sse"
    target_feature="sse2"
    target_feature="sse3"
    target_feature="ssse3"
    target_has_atomic="128"
    target_has_atomic="16"
    target_has_atomic="32"
    target_has_atomic="64"
    target_has_atomic="8"
    target_has_atomic="ptr"
    target_os="macos"
    target_pointer_width="64"
    target_vendor="apple"
    unix
```


# PartialEq、 Eq、  Hash、 PartialOrd、Ord 
对于集合X中的所有元素(假设只有a,b,c三个元素)，都存在 a<b 或 a>b 或者 a==b，三者必居其一， 称为完全性。 如果集合X中的元素只具备上述前两条特征，则称X是 **偏序**。同时具备以上所有特征，则称X是 **全序**。

**NaN**: 对于数学上未定义的结果，例如对负数取平方根 -42.1.sqrt() ，会产生一个特殊的结果：Rust 的浮点数类型使用 NaN (not a number)来处理这些情况。
- 而且任意一个不是NaN的数和NaN之间做比较，无法分出先后关系, 即使是2个NaN之间也是不相等的 `NaN != NaN`。
- Rust浮点类型f32/f64只实现了PartialEq而不是Eq; 浮点数不具备“全序”特征，因为 **NaN != NaN**， 所以**浮点数不满足全序**
```rust
fn main() {
    let nan = std::f32::NAN;
    let x = 1.0f32;
    println!("{}", nan < x);        // 输出 false
    println!("{}", nan > x);        // 输出 false
    println!("{}", nan == x);       // 输出 false
    println!("{}", nan == nan);     // 输出 false
}
```

- 如果想比较某个类型的两值x and y是否相等，或者不等， 如：x == y and x != y， 那么必须为类型实现 **`PartialEq部分相等`** Trait
- 注意 **`Eq完全相等`** Trait的定义是空的，没有方法，它是一种标记性的Trait, 表示全等 使类型可用作hashmaps中的键。
- 使用运算符<、<=、>=和>可以计算值的相对顺序(**排序**)，为此必须为该自定义类型实现`PartialOrd`
- 在为自定义类型实现 **`PartialOrd偏序`** Tait之前，必须首先为其实现`PartialEq` Trait。
- 在你实现 **`Ord全序`** Trait 之前， 你首先必须实现PartialOrd, Eq, PartialEq Trait。
- Ord Trait比较特殊， 它要求比较的两者必须类型相同

```rust
pub trait PartialEq<Rhs = Self> where Rhs: ?Sized, {  // ==  !=
    fn eq(&self, other: &Rhs) -> bool;
    fn ne(&self, other: &Rhs) -> bool { ... }
}

pub trait PartialOrd<Rhs = Self>: PartialEq<Rhs> where  Rhs: ?Sized, { //   <  <=    >  >=
    fn partial_cmp(&self, other: &Rhs) -> Option<Ordering>;
    fn lt(&self, other: &Rhs) -> bool { ... }
    fn le(&self, other: &Rhs) -> bool { ... }
    fn gt(&self, other: &Rhs) -> bool { ... }
    fn ge(&self, other: &Rhs) -> bool { ... }
}

pub trait Ord: Eq + PartialOrd<Self> {          // 
    fn cmp(&self, other: &Self) -> Ordering;
    fn max(self, other: Self) -> Self { ... }
    fn min(self, other: Self) -> Self { ... }
    fn clamp(self, min: Self, max: Self) -> Self { ... }
}

pub trait Hash {
    fn hash<H>(&self, state: &mut H) where H: Hasher;
    fn hash_slice<H>(data: &[Self], state: &mut H) where  H: Hasher,  { ... }
}
```

[参考这篇文章](https://zhuanlan.zhihu.com/p/136883035)
