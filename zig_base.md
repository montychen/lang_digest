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

# var & const
用var声明变量， const声明常量。 

**identifier标识符**, 必须以字母或下划线开头，后面可以有任何数量的字母数字字符或下划线。如果需要一个不符合这些要求的名称，例如与外部库的链接，可以使用 **`@"..."`** 把它包裹起来。
 ```zig
const @"identifier with spaces in it" = 0xff;   // 标识符含有空格
const @"1SmallStep4Man" = 112358;               // 标识符以数字1开头

const c = @import("std").c;
pub extern "c" fn @"error"() void;              // 标识符和关键字冲突
 ```
### 变量 undefined
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


**整数字面量的类型是`comptime_int`**、 **小数字面量的类型是`comptime_float`**； 所以数字字面量只能赋值给**const常量**或者值在编译时已知的变量, 也就是**comptime变量**。
```zig
const print = @import("std").debug.print;

pub fn main() void {
    var x = 47;     // error: variable of type 'comptime_int' must be const or comptime

    // comptime var x = 47;    // 改成这样就没问题了, x 的类型是编译时已知的类型 comptime_int
    // var x: i32 = 47;        // 如果非要用var声明，那么指定明确的类型i32， 这样也是可以的
    print("x={}; x type is = {s}\n", .{ x, @typeName(@TypeOf(x)) });
}
```

**变量遮蔽shadowing**: zig不允许重复声明同名的变量或常量，也就是说不允许变量遮蔽。 
```zig
const x: i32 = 47;

pub fn main() void {
    var x: i32 = 42;  // 报错: redefinition of 'x'
}   
```

# block 块
block块就是用**大括号{...}** 定义的一个作用域。
```zig
test "access variable after block scope" {
    {                   // 定义了一个块, 也就定义了一个作用域
        var x: i32 = 1;
        _ = x;
    }
    x += 1;             // 出错， x 已经离开了它的作用域，所以这里不能再用
}
```

块其实是一个表达式，是表达式就有值；还可以给块用标签命名，例如通过`break :blk value;`携带值退出指定的块。
```zig
const std = @import("std");
const expect = std.testing.expect;

test "labeled break from labeled block expression" {
    var y: i32 = 123;

    const x = blk: {        // 给块命名 blk
        y += 1;
        break :blk y;       // 用y作为块的值返回, 并赋值给x
    };
    try expect(x == 124);
    try expect(y == 124);
}
```


# option: orelse unreachable  .?
orelse 和 .? 都是用来处理option类型

**`a orelse b`** a有值返回解包后的值， 如果a 是null 那么返回 b;

**`a.?`** a有值返回解包后的值，如果a是null那么执行unreachable，程序崩溃报错。 `a.?`是这句的语法糖 `a orelse unreachable`
```zig
const expect = @import("std").testing.expect;

test "orelse .? " {
    var a: ?i32 = null;
    var b = a orelse 100;
    try expect(b == 100);

    const value: ?i32 = 200;
    try expect(value.? == 200);
}
```

# error: catch 和 try
error其实是一个特殊的union联合类型。 catch 和 try 都是用来处理和error有关的类型。

- **`a catch b`** a没错(不是error)就返回解包后的值； a是error就返回b
```zig
const value: anyerror!u32 = error.Broken;
const unwrapped = value catch 1234;     // unwrapped 的结果是 1234
```

- **`a catch |err| {...}`** 有错就捕获并处理; 没错，继续往下执行 
- **`try`** 出错就抛出错误并返回， 它是这句的语法糖`catch | err | {return err}`。 没错，继续往下执行 

```zig
const print = @import("std").debug.print;
const MyError = error{GenericError};

fn foo(v: i32) !i32 {
    if (v == 42) return MyError.GenericError;
    return v;
}

fn wrap_foo(v: i32) void {    
    if (foo(v)) | value | {                 // |...|捕获值
        print("value: {}\n", .{value});
    } else | err | {                        // |...| 捕获错误
        print("error: {}\n", .{err});
    }
} 

pub fn main() !void {
    _ = foo(42) catch |err| {               // 捕获错误
        print("error: {}\n", .{err});
    };

    print("foo: {}\n\n", .{try foo(47)});   // 没有出错，继续往下执行 

    // _ = try foo(42);  //编译没问题。 运行会出错，因为try会捕获并重新往上抛出错误
    wrap_foo(42);        // 输出error: error.GenericError
    wrap_foo(47);        // 输出 value: 47
}
```


# function 函数
函数的返回值， 如果不用，必须明确把它赋值给 **`下划线_`**，表示明确丢弃该返回值的意思， 否则编译会出错；
```zig
fn foo() i32 {    return 47;    }

pub fn main() void {
    foo();       // error: expression value is ignored
    _ = foo();   //  如果不用，必须明确把返回值赋值给 下划线_
}
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
>有一个语法糖，如果结构体 **方法的第一个参数是本struct结构体的指针or对象(这时习惯用self来命名这个参数)**，那么在调用该方法的时候，就可以使用 struct_obj.method(...) 的方式调用该方法， 有点类似oop语言中的方法调用。
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

    try expect(v1.dot(v2) == 0.0); // 第一个参数是本struct结构体的指针or对象，使用struct_obj.method(…) 的方式调用
    try expect(Vec3.dot(v1, v2) == 0.0);    // 函数调用, 通过 . 来调用
}
```

**从函数返回一个结构体的定义**, zig使用这个方法来实现泛型generics
> 指向结构体的指针，可以直接访问结构体成员，不需要解引用dereference
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
在zig语中enum默认是用int作为内部表示的，所以可以转化为int比较，但它不会自动强制转换，您必须使用 `@enumToInt` 或 `@intToEnum` 进行转换。

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

# 指针pointer
**`星号 *`** 放在类型的前面用来声明指针, 如` var ptr: *i32 = null`。  指针表示的是一个内存地址。
- **`*T`** 指向一个元素的指针，比如 *u8
    - **`ptr.*`** 用来解引用dereferenced，也就是访问指针指向的内容。
    - **`&x`** 用来获取变量x的地址，然后可以把它赋给指针，如` ptr = &x;`
- **`[*]T`** 指向多个元素的指针，没有长度信息，与C中指向数组的指针类似。对类型T的要求是：具体占用多少空间必须是确定的；不能是opaque类型
    - 支持索引访问：`ptr[i]`
    - 支持切片语法：`ptr[start .. end]`
    - 指针可以加减来前后移动：`ptr + x`,  `ptr - x`
- **`*[N]T`** 指向 N 个元素数组的指针
    - 长度信息可以通过 `array_ptr.len` 获取
    - 支持索引访问：`array_ptr.[i]`
    - 支持切片语法：`array_ptr.[start .. end]`

对于指向结构体struct的指针， 可以直接使用点 **`.`** 来访问结构体**第一层级的成员变量**，第二、第三...等更深层级的变量，就要先解引用才能访问。
```zig
const print = @import("std").debug.print;

const MyStruct = struct {
    value: i32
};

pub fn printer(s: *MyStruct) void {      // s是指向结构体的指针
    print("value: {}\n", .{s.value});    // 即使s是指针，通过 . 也可以直接访问结构体第一层级的成员
}

pub fn main() void {
    const c = 1234;
    const c_prt = &c;   // 获取常量c的地址， 并赋值给指针 c_ptr

    var value = MyStruct{ .value = c_prt.* };  //c_ptr.* 访问指针c_ptr指向的内容，这里是1234
    printer(&value);    // value: 1234
}
```



# 数组 和 切片[ ]T
**数组`[N]T`的长度是在编译时已知**的连续内存。可以使用数组的`len`字段访问长度。如`[3]u32`有明确的长度。

**切片`[]T`的长度在运行的时候才确定**。可以使用切片操作从数组或其他切片构造切片, 切片也有`len` 字段来返回它的长度。如`[]u32
`没有具体的长度，它的长度在运行的时候才确定。 或者这样 **`*[2]u32 `** 一个指向数组的指针。
>数组和切片如果越界访问index out of bounds，程序将会panic崩溃
```zig
const print = @import("std").debug.print;

pub fn main() void {
    var array = [_]u32{ 1, 2, 3 };   // array是数组， 类型是 [3]u32 
    var aslice: []u32 = array[0..2]; // aslice是切片，类型是 []u32
    var bslice = array[0..2];        // bslice是切片，类型是 *[2]u32  指向数组的指针

    var slice_ptoa = &array;         // slice_ptoa是切片，类型是 *[3]u32  指向数组的指针

    print("array type: {s}\n",         .{ @typeName( @TypeOf(array) ) });
    print("aslice type: {s}\n",        .{ @typeName( @TypeOf(aslice) ) });
    print("bslice type: {s}\n\n",      .{ @typeName( @TypeOf(bslice) ) });

    print("slice_ptoa type: {s}\n\n",  .{ @typeName( @TypeOf(slice_ptoa) ) });

    print("aslice[0]: {}\n",        .{aslice[0]});
    print("bslice[0]: {}\n",        .{bslice[0]});
    print("aslice length: {}\n",    .{aslice.len});
    print("bslice length: {}\n",    .{bslice.len});
}
```




# String字符串 [ ]const u8
zig字符串是以**空字符null结尾**的`字节byte数组`。如果一个字符串含有非ASCII的字符，那么默认都会采用UTF-8编码，把它放进字节数组中，一个UTF-8字符占用3个字节

字符串字面量的类型其实是一个指向字节数组的常量指针 **`*const [N:0]u8 `** ，N是字符串的字节长度，没包括结尾的null空终止符。**:0** 表示以空字符结尾。 字符串长度len虽然不包括结尾的null空字符（官方称为“哨兵终止符”）,  但**通过索引访问结尾的空终止符是安全的**。
```zig
const print = @import("std").debug.print;

pub fn main() void {
    const bytes = "hello";
    const ubs = "hello你";           // 包含一个UTF-8字符， 占用3个字节

    print("{s}\n", .{@typeName(@TypeOf(bytes))});  // 字符串字面量类似是 *const [5:0]u8
    print("{s}\n", .{@typeName(@TypeOf(ubs))});    // *const [8:0]u8  一个UTF-8字符占用3个字节
    

    print("{d}\n", .{bytes.len});            // 5  字符串长度没包括结尾的null字符。
    print("空终止符: {c}\n", .{bytes[5]});   // 通过索引访问结尾的空终止符是安全的。
    print("{c}\n", .{bytes[1]});             // 'e'
}
```
`const数组`可以强制转换为`const切片`。

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


# 控制语句if switch for while

### |var| 或者 |*var| 变量捕获
**`|*var|`** 是变量捕获。如果只想捕获一个不需要修改的值，可以写成|val|。在某些情况下可以简化条件内容块中的语句。
```zig
const std = @import("std");

pub fn main() !void {
    var arg: ?u32 = null;
    std.log.info("arg is {}", .{arg});      // info: arg is null

    arg = 10;
    if (arg) |*val| {   // 变量捕获，这里是可以修改
        val.* += 2;     // val* 是访问指针val的内容（deref syntax)
    }
    std.log.info("arg is {}", .{arg});      // info: arg is 12
}
```




# defer 和 errdefer
**`defer`** : 无论正常、还是出错退出，只要离开当前作用域**defer语句一定会执行**。如果当前作用域有多个defer语句，那么后面的先执行。
>如果一个作用域从没进入，也就不会发生离开该作用域，那么该作用域里面的**defer**就不会被执行。
```zig
const std = @import("std");
const print = std.debug.print;

pub fn main() !void {
    defer print("**3\n", .{});  // 这句最后执行

    defer {
        print("..2 ", .{});
    }
    defer {                 // 这句先执行
        print("..1 ", .{});
    }
    if (false) {            // 这个作用域从没进入，所以里面的defer不会执行
        defer print("从没进入 if 的作用域，所以这句不会被执行 ", .{});
    }
}
// 程序输出  ..1 ..2 **3
```
**`errdefer`** : 正常离开当前作用域不会执行，只有**出错退出return error**的情况下，errdefer语句才会执行。 下面这种情况下就特别有用：正常情况下不需要清理释放资源，只有在发生错误的时候需要释放资源。
```zig
const print = @import("std").debug.print;

fn deferError(is_error: bool) !void {
    defer print("无论正常、还是出错退出当前作用域， 这句都会执行\n", .{});

    errdefer print("\n======= 只有return error退出，这句才会执行\n", .{});

    if (is_error) {
        return error.DeferError;
    }
}

pub fn main() !void {
    try deferError(false);
    try deferError(true);
}
```

# Type、type、anytype 以及 void 和 error、 anyerror 

**type**: 是类型的类型，可以用来表示任何类型，具体是哪个类型，在实际调用的时候才确定，可以通过`type`来动态实例化它代表的类型。比如用在泛型函数声明中。

**std.builtin.Type**: 包含了某个具体类型的实现信息。 全局函数`@typeInfo(comptime T: type) Type` 可以返回**Type**

**`anytype`**: 只能用作函数参数的类型，当函数参数的类型是 anytype，那么该参数的实际类型会根据实参自动推断出来。
```zig
const expect = @import("std").testing.expect;

fn addFortyTwo(x: anytype) @TypeOf(x) {
    return x + 42;
}

test "fn type inference" {
    try expect(addFortyTwo(1) == 43);
    try expect(@TypeOf(addFortyTwo(1)) == comptime_int);
    var y: i64 = 2;
    try expect(addFortyTwo(y) == 44);
    try expect(@TypeOf(addFortyTwo(y)) == i64);
}
```

### void anyopaque
**void**：不占用内存空间。

**anyopaque**:  会占用一些内存空间，但具体多少不确定。和c语言的void交互，要用`anyopaque`。

# test
**test**测试函数不需要声明返回类型， 默认都是而且只能是 **`anyerror!void`** 这个错误联合类型Error Union Type。 如果zig的码源文件不是通过`zig test ***`命令来运行， 那里面的**test**测试函数都会被自动忽略，也就是说测试函数的代码不会包含在`zig build/run ***`等正常构建的二进制文件里。
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
默认情况下， `zig test` 只会解析运行那些在zig源文件顶层声明的test测试函数，不在顶层声明的测试函数会被忽略掉，除非它们被顶层的测试函数引用。


# compile 编译
**编译变量Compile variable**通过导入`@import("builtin")`包来获得，编译器为每个Zig源文件默认都导入了这个包。编译变量包含编译期间可能用到的信息，比如当前是什么平台架构、什么操作系统、那个release mode等等


# zig调用c代码
使用`@cImport`导入C的.h头文件或者一些预定义的宏或者常量。 下面这3个全局函数，只能在 **@cImport**里使用
- @cInclude 包含`.h`头文件， 比如 `@cInclude("stdio.h");`
- @cDefine  定义c使用的宏或者常量， 比如`@cDefine("_NO_CRT_STDIO_INLINE", "1");`
- @cUndef   取消某个宏或者常量的定义
>这几个全局函数都是在编译时执行
```zig
const std = @import("std");

const c = @cImport({
    @cDefine("_NO_CRT_STDIO_INLINE", "1");
    @cInclude("stdio.h");
});
pub fn main() void {
    _ = c.printf("hello你\n");//调用c函数printf

    var ch = c.getchar();   //调用c函数getchar
    std.debug.print("get char:{d}\n", .{ch});
}
```
