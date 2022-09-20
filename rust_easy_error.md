### 只有一个元素的元组 tuple
如果元组tuple只包含一个元素，必须在后面添加一个 **`,逗号`**。 以区分括号表达式和元组
```rust
let a = (0,);   // a是一个元组,只有一个元素， 注意后面一定有个逗号
let b = (0);    // b是一个括号表达式,它是i32类型
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



