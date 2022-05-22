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
