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
println! 对齐格式  **`>  ^ <`**
- **>** 右对齐，默认方式
- **^** 居中对齐
- **<** 左对齐
     
```rust
fn main() {
    // 右对齐，不足左边补空格
    println!("|{:6}|",  21);      // |    21|
    println!("|{:>6}|", 21);      // |    21|

    // > 右对齐，不足左边补0
    println!("{:06}",  21);      // 000021
    println!("{:>06}", 21);      // 000021
    println!("{:0>6}", 21);      // 000021

    // > 右对齐，左边补-
    println!("{:->6}",   21);    // ----21

    // ^ 居中对齐
    println!("|{:^6}|",  21);    // |  21  |

    // 左对齐，右边补-
    println!("|{:-<6}|", 21);    // |21----|
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
在debug模式 下编译器会自动插入整数溢出检查，一旦发生溢出，则会引发panic; 在release模式下，不检查整数溢出，而是采用自动舍弃高位的方式，程序不会报错。需要更精细地自主控制**整数溢出**的行为，可以调用标准库中的checked_、saturating_ 和wrapping_系列函数进行数学运算。推荐使用 checked_** 系列函数，结果更可控。
- checked_** 系列函数返回的类型是Option<\_>，当出现溢出的时候，返回值是None; 没溢出返回Some(v)
- saturating_** 饱和函数返回类型是整数，当运算溢出时，结果为该类型的最大值（上溢）或最小值（下溢）。
  >比如，对一个值为120的i8整数加10 ，发生了上溢，那么结果将为i8类型的最大整值127。 相反，如果对i8值的计算造成了下溢， 那么结果将被设置为i8的最小值 -128 。
- wrapping_**   回绕函数直接抛弃已经溢出的最高位，将剩下的部分返回
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
如果元组中只包含一个元素，必须在后面添加一个 **`,逗号`**。 以区分括号表达式和元组
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
一个元素都没有的元组叫**unit单元类型/空元组**, 如： **`let empty : () = ();`**。 **`空元组`** 和 **`空结构体struct Foo;`** 一样，不占用内存空间，也就是内存占用都是 0 。这与C++中的空类型不同，Rust中实打实的有内存空间占用是0的类型。
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

比如下面这个代码是合法的: 因为loop里面的代码一定会被执行，所以变量 x 在外面虽然没初始化，但在loop里，x在使用前进行了初始化。

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
相反，下面这个代码编译出错, 因为编译器会觉得while语句的执行跟条件表达式在运行阶段的值有关，不能保证while里面的语句一定会被执行，因此它不确定y是否一定会初始化，于是它决定给出一个错误: borrow of possibly-uninitialized variable: `y`
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
**fn item/function item 函数项**指的是`函数本身的类型`, 在Rust中，每个函数项都有一个自己唯一的类型，实际上函数项的类型是不可命名的，因为整个函数本身才是它真正的类型，但理解上可以考虑用函数的名字来表示函数项的类型名称, 因为编译器不允许有2个同名而且函数签名完全相同的函数存在，其实也就是说如果2个函数的签名相同，那么它的名字就要不同。
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
> Rust 要求if else 两个分支的返回值类型相同. Rust 之所以要求不能返回多种类型是因为, **需要在编译期确定返回值占用的内存大小**, 显然不同类型的返回值其内存大小不一定相同. 既然如此, 那能不能让函数返回多种类型呢? 把返回值装箱, 返回一个胖指针Box<T>, 这样我们的返回值大小可以确定了.

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
>- [ ] 这个部分的示例代码不是**rust**
>- [x] 在Rust中递归是可能的，但不保证尾递归优化，所以rust并不真正鼓励递归。相反，Rust 更喜欢称为迭代iterator的东西，也称为循环。

**尾调用tail call**是函数式编程的一个重要概念，简单来说就是在函数执行的最后一步调用另一个函数，举例说明，这段代码中，在x函数的最后一步调用了y函数，就是一个尾调用

```rust
function x () {
  return y()
}
```
**尾调用优化**: 函数调用会在内存中形成一个调用栈，保存着调用位置和内部变量等信息，在我们的示例中，在函数x中调用函数y，也就是说在调用栈中，函数X上面还会有函数Y，当函数Y执行完毕之后出栈，将结果给到函数X，如果函数Y还调用了函数Z，那么调用栈中还会有函数Z。当函数中存在尾调用时，事实上当前函数的内部变量和调用位置等信息其实已经没有用了，所以当前函数其实已经没有必要存在在栈中了，**直接使用被尾调用的函数的调用信息取代当前函数就可以了**，这就是尾调用优化。
> 每个递归在调用前都会在调用栈中保存一份当前函数的调佣信息，以便函数返回时可以继续往下运行；在一些需要很多层递归嵌套，或者递归实现的无限循环（例如事件循环）将消耗完我们的内存，最终导致内存溢出。 即使是尾调用，Rust也不保证尾递归优化，所以rust并不鼓励递归。相反，Rust 更喜欢称为迭代iterator的东西，也称为循环。


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


# trait
trait 的主要作用是用来抽象行为，类似于其他编程语言中的「接口」。Rust中Self(大写S)和self(小写s)都是关键字，大写S的是类型名，小写s的是变量名。 所有的trait都有一个隐含的类型**Self(大写S)**，代表当前实现了此trait的具体类型。
- 关联函数associated function： trait中定义的函数，也称作关联函数
- 方法method：关键是第一个参数的名称必须是**self(小写s)** 、而且是Self的某个类型， 这样的关联函数我们称为方法，要通过**实例变量**加小数点来调用。self参数只能用在第一个参数的位置
- 静态函数static function：第一个参数不是**self(小写s)** 的关联函数, 我们称为静态函数。要通过类型加**双冒号::** 的方式来调用

对于第一个名称是的self参数，Box指针类型**self: Box\<Self\>** 也是可以的.  对一些常用的self参数，Rust提供了简化写法。
<pre>
 self: Self        可简写为  self
 self: &Self       可简写为  &self
 self: &mut Self   可简写为  &mut self
</pre>

```rust
trait T {
    fn method1(self: Self);
    fn method2(self: &Self);
    fn method3(self: &mut Self);
}
// 上下两种写法是完全一样的 trait T {
    fn method1(self);
    fn method2(&self);
    fn method3(&mut self);
}
```
即便第一个参数是Self相关类型，只要变量名不是**self**，就不是方法，也就不能用小数点的语法调用。
```rust
struct T(i32);

impl T {
    fn func(this: &Self) { //第一个参数是Self相关类型，但变量名不是self，就不是方法，不能用小数点的语法调用
        println! {"value {}", this.0};
    }
}

fn main() {
    let x = T(42);
    // x.func();       // error:  小数点方式调用是不合法的
    T::func(&x);      // value 42
}
```
>在标准库中就有这样的例子。Box的一系列方法Box::into_raw(b:Self) Box::leak(b:Self)，以及Rc的一系列方法Rc::try_unwrap(this:Self) Rc::downgrade(this:&Self)，都是这种情况。这样设计的目的是强制用户用Rc::downgrade(&obj)的形式调用，而禁止obj.downgrade()形式的调用。这样源码表达出来的意思更清晰，不会因为Rc<T>里面的成员方法和T里面的成员方法重名而造成误解。

### impl trait | 实现trait
trait中可以包含方法的默认实现。如果这个方法在trait中已经有了方法体，那么在针对具体类型实现的时候，就可以选择不用重写。当然，如果需要针对特殊类型作特殊处理，也可以选择重新实现来**override**默认的实现方式。
```rust
trait Shape {
    fn area(self: Box<Self>) -> f63; // 只能通过Box的实例调用
}

struct Circle {
    radius: f63,
}

impl Shape for Circle {             // impl trait
    fn area(self: Box<Self>) -> f63 {
        std::f63::consts::PI * self.radius * self.radius
    }
}

fn main() {
    let c = Circle { radius: 1f64 };
    // c.area(); // 编译错误
    let b = Box::new(Circle { radius: 3f64 }); // 编译正确
    println!("{}", b.area()); // 49.26548245743669
}
```
### 内在方法|固有方法(inherent methods)
针对一个类型，也可以直接对它impl来增加成员方法，无须trait名字。比如这段代码看作是为Circle类型impl了一个匿名的trait。这种方式定义的方法叫作这个类型的“内在方法|固有方法”(inherent methods)。
```rust
struct Circle {
    radius: f63,
}

impl Circle {     // 直接实现，没有通过trait
    fn get_radius(&self) -> f64 { self.radius }   // 内在方法
}
```
### trait特征定义与实现的位置(孤儿规则)
**孤儿规则Orphan Rule**： 如果你想要为类型 A 实现特征 T，那么 A 或者 T **至少有一个是在当前作用域中`定义`的**！ 目的是可以确保其它人编写的代码不会破坏你的代码，也确保了你不会莫名其妙就破坏了风马牛不相及的代码。

### 泛型
**多态Polymorphism**就好比坦克的炮管，既可以发射普通弹药，也可以发射制导炮弹，也可以发射贫铀穿甲弹，甚至发射子母弹，没有必要为每一种炮弹都在坦克上分别安装一个专用炮管，即使生产商愿意，炮手也不愿意，累死人啊。所以在编程开发中，我们也需要这样**通用的炮管**，这个“通用的炮管”就是多态。

>rust通过**trait object**来实现多态。

**泛型Generics**：实际上，泛型就是一种多态。泛型主要目的是为程序员提供编程的便利; 对那些逻辑功能完全相同，只是数据类型不同的方法，没必要每个类型都重复实现一遍，通过泛型可以极大减少代码的臃肿，为程序员提供了一个通用炮管。想想，一个函数，可以代替几十个，甚至数百个函数，是一件多么让人兴奋的事情
>rust通过trait来实现泛型。 泛型不是一种数据类型，它可被看作是数据类型的参数形式或抽象形式，在编译期间会被替换为具体的数据类型。
#### 泛型参数: 使用前要先对其进行声明
使用泛型参数，有一个先决条件，必需在使用前先对其进行声明，以及一些必要的**特征约束(trait bound)**，就是说明泛型参数要满足那些trait。 如下列所示，不是所有类型都能相加的，因此要对T进行限制，必须是那些实现了std::ops::Add这个trail的类型才行。
>如果同时有几个不同类型的泛型参数，泛型参数的声明顺序还要按照：生命周期（lifetime），类型（type），常量（const）。
```rust
// 在标准库中，std::ops::Add是一个trait，它的声明如下  
// pub trait Add<Rhs = Self> {
//     type Output;
//     fn add(self, rhs: Rhs) -> Self::Output;
// }

// 首先 add<T> 对泛型参数 T 进行了声明，然后才在函数参数中使用该泛型参数 (a: T, b: T)
fn add<T: std::ops::Add<Output = T>>(a: T, b: T) -> T {   // 不是所有类型都能相加，因此要对T进行特征约束
    a + b
}

fn main() {
    println!("add i8: {}", add(2i8, 3i8));
    println!("add i32: {}", add(20, 30));
    println!("add f64: {}", add(1.23, 1.23));
}
```
#### where 约束
当特征约束变得很多时，函数的签名将变得很复杂; 但是我们还是能通过**where**对其做一些形式上的改进
```rust
use std::fmt::Debug;
use std::fmt::Display;

fn main() {
    fn fn1<T: Display + Clone, U: Clone + Debug>(t: &T, u: &U) -> i32 {
        32
    }

    fn fn2<T, U>(t: &T, u: &U) -> i32
    where
        T: Display + Clone,
        U: Clone + Debug,
    {
        32
    }
}
```



跟泛型函数定义类似，在结构体中使用泛型参数，也要提前进行声明**Point\<T, U\>** ，接着就可以在结构体中使用T, U来替代具体的类型

在impl实现泛型的时候，结构体上的泛型参数依然也要提前声明：**impl\<T, U\>**，才能在**Point\<T, U\>** 中使用

除了结构体中的泛型参数，还能在该**结构体的方法中定义额外的泛型参数** ，就跟泛型函数一样
```rust
struct Point<T, U> { // T,U 是定义在结构体 Point 上的泛型参数
    x: T,
    y: U,
}

impl<T, U> Point<T, U> {  //在impl实现的时候，结构体上的泛型参数也要提前声明:impl<T, U>，才能在Point<T, U>中使用

    // 除了结构体中的泛型参数TU，还能在该结构体的方法中定义额外的泛型参数VW，就跟泛型函数一样
   fn mixup<V, W>(self, other: Point<V, W>) -> Point<T, W> { // V,W是单独定义在方法mixup上的泛型参数
       Point {
           x: self.x,
           y: other.y,
       }
   }
}

fn main() {
    let p1 = Point { x: 5, y: 10.4 };
    let p2 = Point { x: "Hello", y: 'c' };

    let p3 = p1.mixup(p2);
    println!("p3.x = {}, p3.y = {}", p3.x, p3.y);    //  p3.x = 5, p3.y = c
}
```
>这个例子中，T,U 是定义在结构体 Point 上的泛型参数，V,W 是单独定义在方法 mixup 上的泛型参数，它们并不冲突，说白了，你可以理解为，一个是结构体泛型，一个是函数泛型。

#### 为具体的泛型类型实现方法
对于 Point\<T\> 类型，你不仅能定义基于T的方法，还能针对特定的具体类型，比如Point\<f32\>进行专门的方法定义。
```rust
struct Point<T> {
    x: T,
    y: T,
}
fn main() {
    impl Point<f32> {
        fn distance_from_origin(&self) -> f32 {
            (self.x.powi(2) + self.y.powi(2)).sqrt()
        }
    }
}
```
这段代码意味着 Point\<f32\> 类型会有一个方法 distance_from_origin，而其他 T 不是 f32 类型的 Point\<T\> 实例则没有定义此方法。这样我们就能针对特定的泛型类型实现某个特定的方法，对于其它泛型类型则没有定义该方法。

#### const generic|常量泛型（Rust 1.51 版本引入的重要特性）
**const N: usiz** 常量泛型/const 泛型，也就是用常量值而不是类型作为泛型的参数。
比如对于数组，很重要的一点：同一类型不同长度的数组也是不同的数组类型。**[i32; 2] 和 [i32; 3] 就是不同的数组类型**，下面的代码会报错。
```rust
fn display_array(arr: [i32; 3]) {
    println!("{:?}", arr);
}
fn main() {
    let arr: [i32; 3] = [1, 2, 3];
    display_array(arr);

    let arr: [i32;2] = [1,2];
    display_array(arr); //报错：expected an array with a fixed size of 3 elements, found one with 2 elements
}
```
让我们修改代码，引入**const泛型(const N: usize)**, 让display_array能打印任意长度的 i32 数组：
```rust
fn display_array<T: std::fmt::Debug, const N: usize>(arr: [T; N]) {
    println!("{:?}", arr);
}
fn main() {
    let arr: [i32; 3] = [1, 2, 3];
    display_array(arr);    // [1, 2, 3]

    let arr: [i32; 2] = [1, 2];
    display_array(arr);    // [1, 2]
}
```
如上所示，我们定义了一个类型为 [T; N] 的数组，其中 T 是一个基于类型的泛型参数，这个和之前讲的泛型没有区别，而重点在于 N 这个泛型参数，它是一个基于值的泛型参数！因为它用来替代的是数组的长度。

N 就是 const 泛型，定义的语法是 **const N: usize，表示 const 泛型 N** ，它基于的值类型是 usize。

#### const泛型参数的限制
- 目前唯一可以用作 const 泛型参数类型的类型是整数（即有符号和无符号整数，也包括isize和usize）以及char和bool的类型。
- const泛型参数中不能有复杂的泛型表达式。当前，只能通过以下形式的 const 参数实例化 const 参数：
    - 一个独立的常量参数。
    - 一个字面量。
    - 一个没有泛型参数的具体常量表达式（用{}括起来）。 示例
```rust
fn main() {
    fn foo<const N: usize>() {}

    fn bar<T, const M: usize>() {
        foo::<M>(); // ok: `M` 是常量参数
        foo::<2021>(); // ok: `2021` 是字面量
        foo::<{ 20 * 100 + 20 * 10 + 1 }>(); // ok: 常量表达式不包括泛型

        foo::<{ M + 1 }>(); // error: 常量表达式包括泛型参数 `M`
        foo::<{ std::mem::size_of::<T>() }>(); // error: 常量表达式包括泛型参数 `T`

        let _: [u8; M]; // ok: `M` 是常量参数
        let _: [u8; std::mem::size_of::<T>()]; // error: 常量表达式包括泛型参数 `T`
    }
}
```

### 静态分派static dispatch | 动态分派dynamic dispatch
impl trait 和 dyn trait 在Rust分别被称为静态分派和动态分派。
- **静态分派impl trait**: 指具体调用哪个函数，在编译阶段就确定了。Rust中的**静态分派靠泛型也就是impl trait**来完成。对于每个不同的泛型类型参数，编译器会生成一个不同版本的函数，在编译阶段就确定好了应该调用哪个函数。

- **动态分派dyn trait**: 指具体调用哪个函数，在运行的执行阶段才能确定。 Rust中的**动态分派靠Trait Object**来完成。**Trait Object本质上是指针**，它可以指向不同的类型；指向的具体类型不同，调用的方法也就不同。

**trait是一种DST动态大小类型Dynamic Sized Type**，因为trait不是一个具体类型，它占用的内存大小size无法在编译阶段确定，所以编译器是**不允许直接使用trait作为参数类型和返回值类型**的。这也是trait跟许多语言中的“interface”的一个区别。

所以下面这段代码，test函数直接使用trait来做参数和返回值的类型，编译不过
```rust
trait Bird {
    fn fly(&self);
}
struct Duck;
struct Swan;

impl Bird for Duck {
    fn fly(&self) {
        println!("duck duck");
    }
}
impl Bird for Swan {
    fn fly(&self) {
        println!("swan swan");
    }
}

fn test(arg: Bird) {}   //不允许直接使用trait作为参数类型和返回类型
fn test() -> Bird {}
```
这时可以用**impl trait泛型**来解决: **`fn test<T: Bird>(arg: T) {..}`** 或者 `fn test(arg: impl Bird) {..}`, 这两种写法是一样的。这样，test函数的实参既可以是Duck类型，也可以是Swan类型。实际上，编译器会根据实际调用参数的类型，直接生成不同的函数版本，类似C++中的template. 
>所以，通过泛型函数实现的“多态”，是在编译阶段就已经确定好了 调用哪个版本的函数，因此被称为“静态分派”。
```rust
trait Bird {
    fn fly(&self);
}
struct Duck;
struct Swan;

impl Bird for Duck {
    fn fly(&self) {
        println!("duck duck");
    }
}
impl Bird for Swan {
    fn fly(&self) {
        println!("swan swan");
    }
}

fn test<T: Bird>(arg: T) {   // 或者写成下面这样，也是可以的  
// fn test(arg: impl Bird) { 
    arg.fly();
}

fn main() {
    let d = Duck {};
    let s = Swan {};
    test(d);
    test(s);
}
```
我们还有另外一种办法来实现“多态”，那就是通过指针。虽然trait是DST类型，但是指向trait的指针不是DST。如果我们把trait隐藏到指针的后面，那它就是一个**trait object，而它是可以作为参数和返回类型的**。

### trait object 
什么是trait object呢? **指向trait的指针就是trait object**，它是一个胖指针，这个指针的名字就叫trait object。虽然trait是DST类型，但是指向trait的指针不是DST的，因为指针的大小是固定的，所以**trait object是可以作为参数和返回类型的**。
>trait对象是一个胖指针，包含两个常规指针: 数据指针和vtable指针. vtable是一个包含析构函数指针、所有trait方法指针以及数据大小和对齐方式的 struct.

**dyn是trait对象类型的前缀**：那么具体的trait object是什么样的呢？假如Bird是一 个trait的名称，那么dyn Bird就是一个DST动态大小类型。 而&dyn Bird、 &mut dyn Bird、Box\<dyn Bird\>、*const dyn Bird、*mut dyn Bird以及 Rc\<dyn Bird\>等等都是Trait Object。


Trait Object本质上是指针，它可以指向不同的类型；指向的具体类型不同，调用的方法也就不同，也就可以用来实现多态。Rust的动态分派和C++的动态分派， 内存布局有所不同。在C++里，如果一个类型里面有虚函数，那么每一个这种类型的变量内部都包含一个指向虚函数表的地址。而在Rust里面，对象本身不包含指向虚函数表的指针，这个指针是存在于trait object指针里面的。如果一个类型实现了多个trait，那么不同的trait object指向的虚函数表也不一样。

#### 在集合中存储多个实现了相同trait但类型不同的对象，可以使用Trait对象。
例如，类型Square和类型Rectangle都实现了Trait Area以及方法get_area，现在要创建一个vec，这个vec中包含了任意能够调用get_area方法的类型实例。这种需求建议采用Trait Object方式：
```rust
fn main() {
    let mut sharps: Vec<&dyn Area> = vec![];    // &dny Area  是trait object
    sharps.push(&Square(3.0));
    sharps.push(&Rectangle(3.0, 2.0));

    println!("{}", sharps[0].get_area());   // 9
    println!("{}", sharps[1].get_area());   // 6
}

trait Area {
    fn get_area(&self) -> f64;
}

struct Square(f64);
struct Rectangle(f64, f64);

impl Area for Square {
    fn get_area(&self) -> f64 {
        self.0 * self.0
    }
}
impl Area for Rectangle {
    fn get_area(&self) -> f64 {
        self.0 * self.1
    }
}
```



### 数组[T; n]
数组类型的表示方式为[T; n]。其中T代表元素类型; n代表元素个数;


# 内存
并非所有的内存都是平等的:

**栈stack:** 栈是一个内存段，用于程序中函数调用的暂存空间。每次调用函数时，都会在栈顶分配一个称为帧（frame）的连续内存块。靠近栈底部的是主函数的帧，当函数调用其他函数时，额外的帧被压入栈。函数的帧包含该函数中包含的所有变量，以及该函数接受的任何参数。当函数返回时，它的栈帧被回收。 所以如果函数调用时需要的空间超出了stack栈总空间的大小，就会发生**stack overflow错误**， 这种情况容易在函数递归调用时容易发生。
- **栈stack空间的大小**：当您编译和链接代码时，会生成一个可执行文件，可执行文件也包含了默认需要多少栈内存stack memory的信息。虽然在链接时可以手动指定栈内存的大小，但链接器有一个默认值，它通常是 8MB，但在 Windows 上可能只有 1MB。

- **栈stack空间的使用**：当程序启动，操作系统会根据app里指定的stack栈空间大小，预先给app分配那么多内存空间，并设置一个特殊寄存器来指向该内存的开头。现在，每当您在程序中定义局部变量时，它都会存储在栈stack中。此外，当您调用某个函数时，返回地址和所有或部分参数也存储在那里。例如，如果在某个函数中，您将一个局部变量定义为一个由 100 个整数组成的数组，并且如果一个整数占用 4 个字节，那么您只需从堆栈内存中分配 400 个字节。那么现在如何释放内存呢？好吧，因为当您从该函数返回时，再也不能使用每个局部变量和函数参数，所以该函数的所有内存都会自动释放。因此，每当程序进入一个新函数并声明新的局部变量时，我们说栈会增长，并且无论何时我们从一个函数返回，我们说栈缩小。

- **Stack Overflow 栈溢出**：如果你用尽了为程序保留的所有栈内存并且您尝试进行另一个函数调用，程序将因栈溢出错误而失败。需要注意的是，编译器通常以这样一种方式编译代码，即一旦输入函数，所有局部变量的空间就会立即被保留。即使某些变量仅在某些条件块中使用，也会在函数开始时为其保留空间。这就是为什么只有在输入新函数时才会发生 **Stack Overflow 错误**。

这通常是您可以从操作系统请求的额外内存，这是您实际需要管理并在不再需要时正确释放的内存。当函数返回时，您还想保存某些值供后续使用，亦或某些东西需要太大的存储空间而无法放入stack栈中

**堆heap:** 堆是一个内存池，与当前程序的调用stack栈无关。它的生存期和程序运行时一样长，在堆内存中的值会一直存在，直到它们被明确地释放。
- 堆heap通常是您可以从操作系统请求的额外内存，这是您实际需要管理并在不再需要时正确释放的内存。当在函数返回后，你还想保存某些值供后续使用；又或者某些东西需要的存储空间太大而无法放入stack栈中，这时候就需要堆heap。
- Rust 中与堆交互的主要机制是 **`Box`** 类型。当你写`Box::new(value)`时，该值被放到堆上，而你得到的结果 `Box<T>` 是堆上该值的一个指针。当 Box最终被`析构Drop`时，该内存被释放。如果你忘记释放堆内存，它会永远存在，而你的应用程序最终会吃掉机器上的所有内存。

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

## 内存安全

内存安全memory safety的3个主要问题
1. 内存的不正确访问引发的内存安全问题
    1. 使用未初始化的内存
    2. 对空指针解引用(dereference)
    3. 悬垂指针(使用已经被释放的内存)
    4. 缓冲区溢出
    5. 非法释放内存(释放未分配的指针或重复释放指针)
    6. 迭代器失效：在迭代的过程中，迭代器被修改而引发的问题

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

## rust并不能解决所有内存安全问题
**心脏出血Heartbleed**: 是2014年在OpenSSL中新发现的安全漏洞，简单来说就是往缓冲区写入内容前，没有先清空缓冲区，所以缓冲区本身就是不干净的，导致写入的数据，有可能包含上次遗留的**脏数据**，因此在下次读取缓冲区的内容的时候，有可能包含了这部分脏数据。Rust并不能避免此类**逻辑错误**
>心脏出血这个问题出现在openSSL处理TLS心跳的过程中：A向B发送维持链接的心跳请求包，B收到后读取这个包的内容data，并返回一个包含有请求包内容的响应包。请求包的内容(data)中包含有包的类型(type)和数据长度等信息。
 
>**当B收到A的请求包后，并没有的验证A包的实际长度**，而是简单的把请求包data中说明的长度当作data的实际长度，于是当请求包中说明的长度与请求包数据实际长度不同时，问题就产生了。假设A构造一个请求包，它的实际内容长度只有1，而却告诉B的它的长度是65535，那么B接受到这个包后就会把A的内容完全当作65535来处理，其实到这里，问题还并不严重，最严重的问题出在，心跳的响应包还需要附带请求包的全部内容，这就需要程序做一次将请求包的数据从它所在的内存拷贝到响应包的内存里的操作，这下就出大问题了，当拷贝的时候，程序认为A包的内容长度是65535个字节，结果A包在内存里面实际只有1个字节，于是程序不仅拷贝出了A包的内容，还“傻傻”地将A包数据在内存中位置后额外的65534个字节拷贝进了响应包里，并将这个响应包发还给了A，于是A便轻易地获得了B内存中这65534个字节的数据。想象一下，如果这65534个字节数据中包括一些敏感信息，那么后果将非常严重。而且A还可以简单地通过连续的发送心跳包，获取B机器内存中n个65534字节的数据，这个漏洞不愧是2014年“最佳漏洞”。
```rust
let buffer = &mut[0u8; 1024]; //将一个可变数组的引用（&）绑定到变量buffer，该数组包含1024个无符号8位整数，并初始化为0。
read_secrets(&user1, buffer); // 使用user1对象的字节数据去填充buffer。
store_secrets(buffer);

// 再次写入缓冲区前，没有先清空缓冲区buffer；
// 导致buffer有可能被user2全覆盖，也有可能没有全部覆盖，还保留user1的部分数据。
read_secrets(&user2, buffer); 
store_secrets(buffer);        // 有可能读到user1的脏数据， 这就是隐患的根源
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
### ==  !=   PartialEq 比较相等or不等
- 如果想比较某个类型的两值x and y是否相等，或者不等， 如：x == y and x != y， 那么必须为类型实现 **`PartialEq部分相等`** Trait
- 注意 **`Eq完全相等`** Trait的定义是空的，没有方法，它是一种标记性的Trait, 表示全等 使类型可用作hashmaps中的键。
### >   <   PartialOrd 比较大小
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

# Rust调用C代码
Rust调用C函数时，需要注意：
- 需要extern "C"{}的方式引入C的APIs.
- Rust不支持原生的C类型，需要引入std::os::raw库下的类型。
- 对于C的结构体类型和其他自定义类型，Rust必须使用#[repr(C)]重新定义该类型，才能在Rust中使用。
- Rust调用非标准库时，需要使用#[link(name = "xxx")], 并且需要在链接时指定库。
- Rust调用C函数时，编译器没办法进行严格的检查，所以需要使用unsafe关键字标注。

Rust调用C标准库函数的例子：
```rust
use std::ffi::CStr;
use std::ffi::CString;
use std::os::raw::c_char;

extern "C" {        //  需要extern "C"{}的方式引入C的APIs.
    fn strlen(s: *const c_char) -> usize;
}

fn main() {
    let rs = "hello你";
    let cs = CString::new(rs).unwrap();

    unsafe {        // 调用C函数时，要用unsafe关键字标注
        let len = strlen(cs.as_ptr());
        println!("len: {}", len);   // len: 8
    }

    unsafe {
        let nrs = CStr::from_ptr(cs.as_ptr());
        println!("new rust string: {}", nrs.to_string_lossy()); //new rust string: hello你
    }
}
```
# Rust 调用c++代码
由于Rust只对C-ABI有稳定版本，我们不得不把C++函数的接口改为C版本

