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
