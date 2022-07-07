zig内建的全局函数Builtin functions，都以 **@** 前缀开头。  函数形参前面的`comptime`表示该参数的值，在编译的时候必须是**已知**的

### @fieldParentPtr 
```zig
@fieldParentPtr(comptime ParentType: type, comptime field_name: []const u8,
    field_ptr: *T) *ParentType
```
给定一个结构体的类型、一个结构体成员的名字、和指向这个结构体成员的指针， 就可以获得指向该结构体的指针
```zig
const expect = @import("std").testing.expect;

const Point = struct {
    x: f32,
    y: f32,
};

fn setYBasedOnX(x: *f32, y: f32) void {
    const point = @fieldParentPtr(Point, "x", x);   // 获得结构体的指针
    point.y = y;
}
test "field parent pointer" {
    var point = Point{
        .x = 0.1234,
        .y = 0.5678,
    };
    setYBasedOnX(&point.x, 0.9);
    try expect(point.y == 0.9);
}
```

### @This
