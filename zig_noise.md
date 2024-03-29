# `const` 习惯不加类型
```zig
const foo = 1234;   
const bar = 12.34;
```

# `var` 要加类型或者加`comptime`
整数字面量的类型是`comptime_int`、 小数字面量的类型是`comptime_float`

数字字面量赋值给var变量， 一定要指明类型。 
- 报错： `var x = 47;`  因为**var默认是运行时求值**，和编译时的类型`comptime_int`47不兼容。
- `var x: i32 = 47;`  这样没问题，明确指定类型i32， 这样会强制把 47的类型转换成 i32
- `comptime var x = 47;`  这样也没问题, 加了`comptime`后，强制要求`var x` 在编译时求值，x的类型转换成`comptime_int`

```zig
pub fn main() void {
    var x1 = 47; // 报错

    comptime var x = 47;
    var y: i32 = 20;
    print("x={}; x type = {s}\n", .{ x, @typeName(@TypeOf(x)) }); // x=47; x type = comptime_int
    print("y={}; y type = {s}\n", .{ y, @typeName(@TypeOf(y)) }); // y=20; y type = i32
}
```
# std.testing.expectEqual 两个参数类型不一致
```zig
pub fn expectEqual(expected: anytype, actual: @TypeOf(expected)) !void
```
从上面`std.testing.expectEqual`函数的签名可以看出，参数`actual`的类型要被强制为`expected`类型。 实际调用的时候，如果参数`actual`的类型和`expected`不一致就会编译出错，而且在实际编码过程中确实很容易出现不一致。 

### `i64`类型不能转换成`comptime_int`的问题
比如下面这个例子，出错的原因是actual的类型`i64`不能转换成expected的类型`comptime_int`，所以导致类型不一致，编译出错。
```zig
const std = @import("std");

fn add(a: i64, b: i64) i64 {
    return a + b;
}

test "add" {
    try std.testing.expectEqual(5, add(2, 3)); // 报错。add(2,3)返回值的类型i64不能转换成5的类型comptime_int
    try std.testing.expectEqual(add(2, 3), 5); // 这样可以。因为5的类型comptime_int 可以转换成add(2,3)返回值的类型 i64
    try std.testing.expectEqual(@as(i64, 5), add(2, 3)); // 这样也可以。两个参数的类型都是i64
}
```

### `?[]const u8`类型不能转换成 `null`的问题
其它函数也会有类似的问题, 比如`std.StringHashMap`的方法`fn get(self: Self, key: K) ?V`

下面例子出错的原因是： 函数`m.get("teg")`的返回类型`?[]const u8` 不能转换成 `null`类型，所以报错。 解决办法是我们可以先把 `null`类型转换成`?[]const u8`类型。
```zig
const std = @import("std");

test "hashmap: get" {
  var m = std.StringHashMap([]const u8).init(std.testing.allocator);
  defer m.deinit();

  try std.testing.expectEqual(null, m.get("teg"));   // 报错，`m.get("teg")`的返回类型 ?[]const u8 不能转换成 null 类型，
  try std.testing.expectEqual(@as(?[]const u8, null), m.get("teg")); // 这样可以。 可以先把 `null`类型转换成`?[]const u8`类型。
}
```