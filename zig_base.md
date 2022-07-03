# @import("std") 标准库
当导入**标准库std**的时候，其实导入的是这个文件 **zig/lib/std/std.zig**
```zig
const std = @import("std");
```
- 标准库std中简单的子模块，可以直接在一个和模块同名的文件中实现，例如子模块`std.ascii`，就在 **/lib/std/ascii.zig**这一个文件中实现。
- 标准库std中复杂的子模块，全部放在一个文件也可以实现，但稍显复杂或者结构不清晰。 
    - 这时通常会有一个**和模块同名的实现子目录**，在这个目录下放置所有和这个子模块实现有关的文件。这个**实现子目录里的内容一般不直接对外**，而是通过下面这个文件来导出对外需要的东东。例如 std.math子模块，就有自己的**实现子目录 /std/math/\*\***
    - 除了实现子目录，为了方便外部的使用，通常还有一个和模块同名、而且用来对外的文件，比如 **/std/math.zig文件**。实现子目录需要对外开放的接口&函数&变量或者类型等等，**一般都是通过这个文件对外导出**。 其实通过`@import`导入模块，导入的是和该模块同名的 **.zig** 文件。
      > 所以代码 `const math = @import("std").math;` 导入的是 **/lib/std/math.zig** 这个文件
```
$ lib/
  -- std/
     |-- ascii.zig             // 简单子模块， 在一个文件中实现
     |-- math/          // 复杂子模块std.math 在一个实现子目录中实现
     |   -- ceil.zig
     |   -- ****.zig
     |-- math.zig       // 复杂子模块std.math, 还有一个和实现子目录同名的文件, 重新导出对外开放的接口&函数&变量。。。
                        // 重新导出的目的，是方便外部的使用。
```

# 自动生成文档 /// 和  //!
**对结构体、函数或者变量进行说明的文档**: 直接在它们的上面**每行都用** **`///`** 开头的文字
> 注释用的是两个斜杠 **//**
```zig
/// A structure for storing a timestamp, with nanosecond precision (this is a
/// multiline doc comment).
const Timestamp = struct {
    /// The number of seconds since the epoch (this is also a doc comment).
    seconds: i64,  // signed so we can represent pre-1970 (not a doc comment)
    /// The number of nanoseconds past the second (doc comment again).
    nanos: u32,

    /// Returns a `Timestamp` struct representing the Unix epoch; that is, the
    /// moment of 1970 Jan 1 00:00:00 UTC (this is a doc comment too).
    pub fn unixEpoch() Timestamp {
        return Timestamp{
            .seconds = 0,
            .nanos = 0,
        };
    }
};
```
A top level doc comment：针对整个模块进行说明的文档，而不是针对某个方法和变量的文档， **每行文档都用** **`//!`** 开头
 ```zig
//! This module provides functions for retrieving the current date and
//! time with varying degrees of precision and accuracy. It does not
//! depend on libc, but will use functions from it if available.
 ```
 
# union联合体
联合体union的声明和结构体很相似，但是运行时只有一个成员生效
```zig
const Payload = union {
    member1: i64,
    member2: f64,
    member3: bool,
};
test "simple union" {
    var payload = Payload{ .member1 = 1234 };
    payload.member2 = 12.34;    //panic: access of inactive union field
}
```

# enum枚举
在zig语言中enum默认是用int作为内部表示的，所以可以转化为int比较

```zig
const expect = @import("std").testing.expect;

const Type = enum {
    ok,
    not_ok,
};


test "simple enum" {
    try expect(@enumToInt(Type.ok) == 0);   // enum默认是用int作为内部表示的，所以可以转化为int比较
    try expect(@enumToInt(Type.not_ok) == 1);
}
```

# String字符串
字符串以**空字符null结尾**

Zig字符串默认是UTF-8编码。但是，可以使用`\xNN`(用十六进制的2个数字)表示法将**单字节字符**嵌入到字符串文字中。
```zig
const mem = @import("std").mem; // will be used to compare bytes
pub fn main() !void{
    mem.eql(u8, "hello", "h\x65llo");   // \x65 是字母 e
}
```





