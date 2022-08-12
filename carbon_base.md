[Carbon](https://github.com/carbon-language/carbon-lang) 是2022年7月19日，在多伦多举行的CppNorth大会上，Google的**Chandler Carruth**在会上[对外正式发布](https://www.youtube.com/watch?v=omrY53kbVoA)的一门开放源码的语言，目标是可以和C++代码互相无缝调用，强调性能、简单和安全：**simple c++、safter c++**。
>Chandler Carruth 是Google在c++委员会的代表，他在委员会里的地位仅次于 C++ 之父 Bjarne Stroustrup 和 Herb Sutter

# 关键字
carbon的大多数语句前面都有一个介绍关键字，这是carbon 的精心设计。虽然对人类读者来说可能并不重要，但它对我们的工具很重要，因为代码更容易解析、而且没有歧义。例如：fn 表示函数，var 表示变量声明，let 表示常量声明 . . .

# 在线carbon编辑器
carbon目前还处于非常初期， 可以用 Carbon 在线 IDE 来试验代码。[ compiler-explorer.com](https://carbon.compiler-explorer.com/) 或者 [Carbon Godbolt](https://carbon.godbolt.org/) 


# 字符串 String 和 StringView
- `String`对于字节序列
- `StringView`作为 utf-8 字节序列的只读参考。


单行和多行字符串字面量
- 单行使用双引号 `"`。
- 多行字符串使用3个双引号 `"""`，具体缩进多少，以字符串相对结尾`"""`的位置来作参考。
```carbon
package ExplorerTest api;

fn Main() -> i32 {
  var singleLine: String = "Hello world!";
  var multiLine: String = """
        TipSeason demo line 1
        TipSeason demo line 2    
        """;                 // 多行字符串字面量结束。 字符串和结尾的"""对齐，所以输出时，多行字符串没有缩进
  return 0;
}
```

# tuple 元组 ( )
元组用括号声明`( )`, 使用索引访问元组的成员。
```carbon
package ExplorerTest api;

fn Main() -> i32 {
  var x: auto = (0, 1);     // 声明元组
  Print("{0}", x[1]);       // 用索引访问元组成员
  return x[0];
}
```

# struct 结构体
用 **花括号{...}** 来声明struct，结构体可帮助我们用名称而不是索引来访问成员； 如：`var s: auto = {.name1 = value1, .name2 = value2, ... };`，然后就可以这样访问`s.name1`
```carbon
package ExplorerTest api;

fn Main() -> i32 {
  var point: auto = {.x_axis = 0, .y_axis = 1};  // struct 结构体
  point = {.x_axis = 5, .y_axis = 10};           // 修改struct结构体成员值

  var result: i32 = point.x_axis * point.x_axis + point.y_axis * point.y_axis;
  Print("Result : {0}", result);
  return 0;
}
```


# 指针 T*
- `T*` 声明指针,  如： `var y: i32* = &x;` 
- `&var` 获取变量var的地址
- `*ptr` 访问指针ptr的内容， 如： `*y = 100;`
- `b_ptr = &*a_ptr` 指针a_ptr和b_ptr都指向同一个变量，也就是a_ptr指向的变量 
```carbon
package ExplorerTest api;

fn Main() -> i32 {
  var x: i32 = 5;
  var y: i32* = &x;      // y 是指针，指向x
  *y = 10; 
  Print("---");
  Print("x = {0}", x);  // x = 10
  Print("y = {0}", *y); // y = 10

  var z: i32* = &*y;   // z也指向指针y指向的变量； 也就是说指针z和y都指向同一个变量x
  *z = 20;            
  Print("=====");
  Print("x = {0}", x);   // x = 20
  Print("y = {0}", *y);  // y = 20
  Print("z = {0}", *z);  // z = 20

  return 0;
}
```

# 数组[T, N]
- `[T; N]` 声明具备N个元素的T类型数组。 如：`var a: [i32; 4] = (1, 2, 3, 4);`

# 循环语句 while for
- `while( condition ){ ... }`, 如： `while (not (x == 0)) { ... } `
- `for ( loop conditions ) { ... }`, 如： `for (var name: String in names) { ... }`



# match 匹配语句
```carbon
match(condition) {
  case (condition) => {...}
  default => {...}
}
```
```carbon
package ExplorerTest api;

fn Matcher(var num: i32) -> i32 {
  var number: auto = 10;
  match (number) {
    case 5 => {
      Print("Got 5");
      return number;
    }
    default => {
      Print("Default");
      return number;
    }
  }
}

fn Main() -> i32 {
    Matcher(5);
    Matcher(10);
    return 0;
}
```

# class 类



# generic 泛型 T:!
**type类型是编译时常量值**：carbon把类型type当作值、而且type的值在编译时必须是已知的值。

# 函数
- 函数输入参数(实参)是只读值





