# Rust 中的所有权
- 一个值只能有一个所有者
- 您可以对一个值有多个共享的不可变引用
- 一个值只能有一个可变引用

与其处理生命周期，不如使用Arc或Arc<Mutex<...>>. 这也是为什么我在这个博客上的第一篇文章是关于Arc和Mutex- 我认为Arc 当你需要在线程之间共享东西时应该是你尝试的第一件事，而不是最后一个。大多数时候它会足够快，不用担心。那么只有当你需要更高的性能或者你认为你可以提供更好的 API 时，你才能尝试更高级的东西，

Arc是一个智能指针，可让您在多个线程之间安全地共享值。Mutex是另一种类型的包装器，它允许跨线程的安全可变性

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
对于集合X中的所有元素（假设只有a,b,c三个元素），都存在 a<b 或 a>b 或者 a==b，三者必居其一， 称为完全性。 如果集合X中的元素只具备上述前两条特征，则称X是 **偏序**。同时具备以上所有特征，则称X是 **全序**。

**NaN**: 对于数学上未定义的结果，例如对负数取平方根 -42.1.sqrt() ，会产生一个特殊的结果：Rust 的浮点数类型使用 NaN (not a number)来处理这些情况。
- 而且任意一个不是NaN的数和NaN之间做比较，无法分出先后关系, 即使是2个NaN之间也是不相等的 `NaN != NaN`。
- Rust浮点类型f32/f64只实现了PartialEq而不是Eq; 浮点数不具备“全序”特征，因为 **NaN != NaN**， 所以浮点数不满足全序。
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
pub trait PartialEq<Rhs = Self> where Rhs: ?Sized, {
    fn eq(&self, other: &Rhs) -> bool;
    fn ne(&self, other: &Rhs) -> bool { ... }
}

pub trait PartialOrd<Rhs = Self>: PartialEq<Rhs> where  Rhs: ?Sized, {
    fn partial_cmp(&self, other: &Rhs) -> Option<Ordering>;
    fn lt(&self, other: &Rhs) -> bool { ... }
    fn le(&self, other: &Rhs) -> bool { ... }
    fn gt(&self, other: &Rhs) -> bool { ... }
    fn ge(&self, other: &Rhs) -> bool { ... }
}

pub trait Ord: Eq + PartialOrd<Self> {
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
