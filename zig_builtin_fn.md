zig内建的全局函数Builtin functions，都以 **`@`** 前缀开头。  函数形参前面的`comptime`表示该参数的值，在编译的时候必须是**已知**的

### @bitCast
```zig
@bitCast(comptime DestType: type, value: anytype) DestType
```
把一个类型的值value转换成另一个类型。

如果值在编译时已知，则该转换在编译时发生。由于结构体的内存布局是不确定的，因此将结构体bitCast位转换为相同内存大小的类型会编译出错。但是，如果是压缩结构体packed strucrt，那么是可以的。

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
返回包含该函数的结构体、枚举或联合类型，这对于需要引用自身的匿名结构很有用。
```zig
const std = @import("std");
const expect = std.testing.expect;

fn List(comptime T: type) type {
    return struct {
        const Self = @This(); // @This（）返回代表当前结构体的类型

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


如果`@This()`调用，没在结构体、枚举或者联合类型内， 那返回的就是表示当前文件结构体，和当前文件同名
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


