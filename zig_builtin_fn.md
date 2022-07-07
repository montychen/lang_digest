zig内建的全局函数Builtin functions，都以 **`@`** 前缀开头。  函数形参前面的`comptime`表示该参数的值，在编译的时候必须是**已知**的

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

### @This
