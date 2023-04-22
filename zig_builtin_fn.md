zig内建的全局函数Builtin functions，都以 **`@`** 前缀开头。  函数形参前面的`comptime`表示该参数的值，在编译的时候必须是**已知**的

### @as
```zig
@as(comptime T: type, expression) T
```
把表达式expression的值，强制转换成T指定的类型；这是**执行强制类型转换的首选**方式。当转换的结果是明确且安全的，才允许执行转换，不然会报错。 


### @bitCast
```zig
@bitCast(comptime DestType: type, value: anytype) DestType
```
把值value转换成DestType指定的类型。

如果值在编译时已知，则该转换在编译时发生。由于结构体的内存布局是不确定的，因此将结构体bitCast位转换为相同内存大小的类型会编译出错。但是，如果是压缩结构体packed strucrt，那么是可以的。

### @compileError
```zig
@compileError(comptime msg: []u8) noreturn
```
人为调用，在编译阶段，用来输出编译时的错误信息。

例子：switch有返回数值，我们用参数 T 的类型做开关，如果 T 符合数字类型，那么 switch 条件语句返回 true
```zig
fn assertNumber(comptime T: type) void { // 参数前加上comptime，告诉编译器这是要在编译时必须已知的参数。
    const is_num = switch (T) {
        i8, i16, i32, i64 => true,
        u8, u16, u32, u64 => true,
        comptime_int, comptime_float => true,
        f16, f32, f64 => true,
        else => false,
    };

    if (!is_num) {
        @compileError("Inputs must be numbers");
    }
}

pub fn main() !void {
    assertNumber(bool);
}
```

### @fieldParentPtr 
```zig
@fieldParentPtr(comptime ParentType: type, comptime field_name: []const u8,
    field_ptr: *T) *ParentType
```
给定一个结构体的类型、一个结构体成员的名称、和指向这个结构体成员的指针， 就可以获得指向该结构体的指针
> 指向结构体的指针，可以直接访问结构体成员，不需要解引用dereferencing。比如下面的代码， point是指向结构体Point的指针，这个指针就可以直接访问结构体成员x， 如： `point.y`
```zig
const expect = @import("std").testing.expect;

const Point = struct {
    x: f32,
    y: f32,
};

fn setYBasedOnX(x: *f32, y: f32) void {
    // Point 结构体类型
    // "x"   结构体成员名称
    //  x    指向结构体成员x的指针
    const point = @fieldParentPtr(Point, "x", x); // 获得指向结构体的指针point
    point.y = y;                                  // 指向结构体的指针，可以直接访问结构体成员point.y
}
test "field parent pointer" {
    var point = Point{
        .x = 0.1234,
        .y = 0.5678,
    };
    setYBasedOnX(&point.x, 0.9);            // &point.x 是指向结构体成员x的指针
    try expect(point.y == 0.9);
}
```


### @sizeOf 
```zig
@sizeOf(comptime T: type) comptime_int
```
在**运行时runtime**测量类型T在内存中占用多少字节byte。对于运行时不允许的类型，例如 comptime_int 和 type，@sizeOf的返回值为 0。


### @This
```zig
@This() type
```
返回包含该函数调用的结构体、枚举或联合类型。方便我们对匿名结构的引用。
```zig
const std = @import("std");
const expect = std.testing.expect;

fn List(comptime T: type) type {
    return struct {
        const Self = @This(); // @This（）返回代表当前结构的类型

        items: []T,

        fn length(self: Self) usize {
            std.debug.print("{s}", .{@typeName(Self)});
            return self.items.len;
        }
    };
}

pub fn main() !void {
    var items = [_]i32{ 1, 2, 3, 4 };
    const list = List(i32){ .items = items[0..] };
    try expect(list.length() == 4);
}
```


如果`@This()`调用，没在结构体、枚举或者联合类型内， 那返回的是表示当前文件的隐式结构体，和当前文件同名
```zig
const print = @import("std").debug.print;

fn test_this() void {
    const Self = @This();
    print("{s}\n", .{@typeName(Self)}); //没在结构体、枚举或联合类型内调用，返回当前文件的文件名
}

pub fn main() !void {
    test_this();
}
```

### @Type @typeInfo @typeNmae  @TypeOf

- `@Type(comptime info: std.builtin.Type) type`
- `@typeInfo(comptime T: type) std.builtin.Type`

- `@typeName(T: type) *const [N:0]u8`
- `@TypeOf(...) type`


