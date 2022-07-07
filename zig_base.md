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
>
> 多行字符串, 每行用两个反斜杠开头 \\\\, 而且里面的特殊字符不会转义
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
 
# 用户自定义类型：struct、enum、union
# struct
普通的结构体，Zig不保证结构体成员在内存中的顺序和整个结构体占用的内存大小，但保证字段是 ABI 对齐的。

**packed struct压缩结构体**的内存布局，zig会严格按照它的声明顺序， 而且成员之间不会填充。
>ABI(Application Binary Interface): 实际上是CPU如何执行API函数调用的一种约定，比如你的程序调用了一个第三方库， 那么参数在调用者和被调用者之间如何传递，返回值怎么提供给调用者; 库函数怎么被应用，以及库怎么被加载到内存。ABI 可以理解成是机器语言、也就是二进制层面上的 API。 举例来说，假设你的应用程序引用的一个库某天更新了，虽然 API 和调用方式基本没变，但你需要重新编译你的应用程序才能使用这个库，那么一般说这个库是 Source compatible；反之，如果不需要重新编译应用程序就能使用新版本的库，那么说这个库跟它之前的版本是二进制兼容的
```zig
const Point = struct {
    x: f31,
    y: f31,
};

// 实例化
const p = Point{
    .x = -1.12,
    .y = -1.34,
};

// 实例化时，不初始化的成员要明确赋值： undefined
var p1 = Point{
    .x = -1.12,
    .y = undefined,
};
```

结构体当命名空间来使用成员变量 
```zig
const expect = @import("std").testing.expect;

const Empty = struct {
    pub const PI = 3.14;
};
test "struct namespaced variable" {
    try expect(Empty.PI == 3.14);           // 结构体命名空间来使用成员变量  Empty.PI
    try expect(@sizeOf(Empty) == 0);

    // you can still instantiate an empty struct
    const does_nothing = Empty{};

    _ = does_nothing;
}
```

**结构体可以有方法**, 结构体的方法其实也没什么特殊的，也可以理解成只是把结构体当做命名空间namespace来使用。通过 **`.`** 来调用方法
```zig
const expect = @import("std").testing.expect;

const Vec3 = struct {
    x: f32,
    y: f32,
    z: f32,
    
    pub fn init(x: f32, y: f32, z: f32) Vec3 {
        return Vec3{
            .x = x,
            .y = y,
            .z = z,
        };
    }

    pub fn dot(self: Vec3, other: Vec3) f32 {
        return self.x * other.x + self.y * other.y + self.z * other.z;
    }
};

test "dot product" {
    const v1 = Vec3.init(1.0, 0.0, 0.0);
    const v2 = Vec3.init(0.0, 1.0, 0.0);

    try expect(v1.dot(v2) == 0.0);          // 函数调用, 通过 . 来调用
    try expect(Vec3.dot(v1, v2) == 0.0);    // 函数调用, 通过 . 来调用
}
```

**从函数返回一个结构体的定义**, zig使用这个方法来实现泛型generics
```zig
const expect = @import("std").testing.expect;

fn LinkedList(comptime T: type) type {   // 函数返回一个struct声明
    return struct {                      // 定义一个匿名struct
        pub const Node = struct {
            prev: ?*Node,
            next: ?*Node,
            data: T,
        };

        first: ?*Node,
        last: ?*Node,
        len: usize,
    };
}

test "linked list" {
    try expect(LinkedList(i32) == LinkedList(i32));

    var list = LinkedList(i32){
        .first = null,
        .last = null,
        .len = 0,
    };
    try expect(list.len == 0);

    const ListOfInts = LinkedList(i32);  //类型是一等公民，可以把类型赋值给变量或者函数参数，然后实例化
    try expect(ListOfInts == LinkedList(i32));

    var node = ListOfInts.Node{
        .prev = null,
        .next = null,
        .data = 1234,
    };
    var list2 = LinkedList(i32){
        .first = &node,
        .last = &node,
        .len = 1,
    };

    try expect(list2.first.?.data == 1234);     //指向结构体的指针，可以直接访问结构体成员 list2.first就是一个指向结构体的指针
}
```
### packed struct 压缩结构体
**packed struct压缩结构体**的内存布局，zig会严格按照它的声明顺序， 而且成员之间不会被填充，也就是说成员间不会为了字节对齐而填充。
```zig
const std = @import("std");
const native_endian = @import("builtin").target.cpu.arch.endian();
const expect = std.testing.expect;

const Full = packed struct {
    number: u16,
};
const Divided = packed struct {
    half1: u8,
    quarter3: u4,
    quarter4: u4,
};

test "@bitCast between packed structs" {
    try doTheTest();
    comptime try doTheTest();
}

fn doTheTest() !void {
    try expect(@sizeOf(Full) == 2);
    try expect(@sizeOf(Divided) == 2);  //结构体成员之间不会被填充。也就是成员间不会为了字节对齐而填充。
    var full = Full{ .number = 0x1234 };

    // 将结构体位转换为相同内存大小的类型会编译出错。但是，如果是压缩结构体packed strucrt，那么是可以的。
    var divided = @bitCast(Divided, full); 


    switch (native_endian) {
        .Big => {
            try expect(divided.half1 == 0x12);
            try expect(divided.quarter3 == 0x3);
            try expect(divided.quarter4 == 0x4);
        },
        .Little => {
            try expect(divided.half1 == 0x34);
            try expect(divided.quarter3 == 0x2);
            try expect(divided.quarter4 == 0x1);
        },
    }
}
```


# enum枚举
在zig语中enum默认是用int作为内部表示的，所以可以转化为int比较

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


# String字符串
字符串是以**空字符null结尾**的`字节byte数组`，字符串字面量的类型其实是一个指向字节数组的常量指针 **`*const [N:0]u8 `** ，N是字符串的字节长度，没包括结尾的null字符。**:0** 表示以空null字符结尾。
>如果一个字符串含有非ASCII的字符，那么默认都会采用UTF-8编码，把它放进字节数组中，一个UTF-8字符占用3个字节
```zig
const print = @import("std").debug.print;

pub fn main() void {
    const bytes = "hello";
    const ubs = "hello你";      // 包含一个UTF-8字符， 占用3个字节

    print("{s}\n", .{@typeName(@TypeOf(bytes))});  // *const [5:0]u8
    print("{s}\n", .{@typeName(@TypeOf(ubs))});    // *const [8:0]u8    

    print("{d}\n", .{bytes.len}); // 5  字符串长度没包括结尾的null字符。
    print("{c}\n", .{bytes[1]}); // 'e'
}
```

#### 字符转义编码
**\xNN** 用十六进制的2个数字，表示**可单字节表示的字符**, 比如ASCII码。

**\u{NNNNNN}** 用十六进制的1到6个数字，表示utf-8的字符, 占用3个字节。 比如 **\\u{1f4a9}就代表💩**

```zig
const print = @import("std").debug.print;
const mem = @import("std").mem; // will be used to compare bytes
pub fn main() !void {
    print("{}\n", .{'e' == '\x65'});                    // true     \x65 是ASCII字母 e
    print("{}\n", .{mem.eql(u8, "hello", "h\x65llo")}); // true

    print("={u}=\n", .{'\u{1f4a9}'}); // 输出\u{NNNNNN}编码的utf-8字符   =💩=
    print("{u}\n", .{'💩'});          // 直接输出一个utf-8字符 💩

    print("{d}\n", .{'💩'});          //十进制输出    128169  
    print("{x}\n", .{'💩'});          //十六进制输出 0x1f4a9
}
```

#### 多行字符串 \\\\
跨越多行的字符串，每行都要用 **\\\\** 开头， 里面的特殊字符不会转义，也就是说\n 不会输出换行，输出的还是\n
```zig
const hello_world_in_c = \\#include <stdio.h>
    \\
    \\int main(int argc, char **argv) {
    \\    printf("hello world\n");
    \\    return 0;
    \\}
;
```

# 变量 undefined
用`var`声明变量的时候必须要初始化， 如果不初始化就要明确赋值**undefined**， `undefined`表示这是一个没有意义的值， 它可以强制转换成任何类型。
> 用const声明常量， 如：`const constant: i32 = 5;  `
```zig
const print = @import("std").debug.print;

pub fn main() void {
    var x: i32 = undefined;     
    // var x: i32;             // 如果声明变量没初始化，会报错.
    x = 1;
    print("{d}", .{x});
}
```



# test
**test**测试函数不需要声明返回类型， 默认都是而且只能是 **`anyerror!void`** 这个错误联合类型Error Union Type。 如果zig的码源文件不是通过`zig test ***`命令来运行， 那里面的**test**函数都会被自动忽略，比如`zig build/run ***`的时候。
> 在命令行通过`zig test file_name.zig` 来运行测试
```zig
const std = @import("std");

test "expect addOne adds one to 41" {
    try std.testing.expect(addOne(41) == 42);
}

fn addOne(number: i32) i32 {
    return number + 1;
}
```
