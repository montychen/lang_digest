[Carbon](https://github.com/carbon-language/carbon-lang) 是2022年7月19日，在多伦多举行的CppNorth大会上，Google的**Chandler Carruth**在会上[对外正式发布](https://www.youtube.com/watch?v=omrY53kbVoA)的一门开放源码的语言，目标是可以和C++代码互相无缝调用，强调性能、简单和安全：**simple c++、safter c++**。
>Chandler Carruth 是Google在c++委员会的代表，他在委员会里的地位仅次于 C++ 之父 Bjarne Stroustrup 和 Herb Sutter

# 关键字
carbon的大多数语句前面都有一个介绍关键字，这是carbon 的精心设计。虽然对人类读者来说可能并不重要，但它对我们的工具很重要，因为代码更容易解析、而且没有歧义。例如：fn 表示函数，var 表示变量声明，let 表示常量声明 . . .

# 在线carbon编辑器
carbon目前还处于非常初期， 可以用 Carbon 在线 IDE 来试验代码。[ compiler-explorer.com](https://carbon.compiler-explorer.com/) 或者 [Carbon Godbolt](https://carbon.godbolt.org/) 

# 变量和常量
用var声明变量， let声明常量。


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
用 **花括号{...}** 来声明struct，结构体可帮助我们用名称而不是索引来访问成员； 如：`var s: auto = {.name1 = value1, .name2 = value2, ... };`，然后就可以这样访问`s.name1`。
- [x] carbon的结构体struct和元组tuple一样，都很轻量，可以**就地直接使用**，不需要预先定义。 

#### 就地直接使用struct作为变量类型，不需要提前定义struct
```carbon
package ExplorerTest api;

fn Main() -> i32 {
  var point: auto = {.x_axis = 0, .y_axis = 1};  // 就地直接使用struct 结构体
  point = {.x_axis = 5, .y_axis = 10};           // 修改struct结构体成员值

  var result: i32 = point.x_axis * point.x_axis + point.y_axis * point.y_axis;
  Print("Result : {0}", result);
  return 0;
}
```
#### 就地直接使用struct作为函数返回类型，不需要提前定义struct
```carbon
// 返回值类型 {.factor: i32, .prime: bool} 是一个就地直接使用的struct
fn SmallestFactor(n: i32) -> {.factor: i32, .prime: bool} {  
  ...
    if (remainder == 0) {
      return {.factor = i, .prime = false};     // 返回一个结构体的值
    }
  ...
  return {.factor = n, .prime = true};          // 返回一个结构体的值
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

## Optional
Carbon不支持空指针，如果想表示不存在，使用Optional。
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
类的成员和函数
- **类成员默认`public`**：Carbon中类中成员访问控制权限默认都是public，如果需要声明成私有则需要单独加private关键字。这个行为和C/C++的struct相同，但是和主流语言的class都不同。
- **`[me: Self]`只读方法**：表示当前对象的成员变量在函数中是只读、不能进行任何修改。**me**在函数体中表示对当前对象的引用，类似C++的this。
- **`[addr me: Self*]`可修改方法**： 表示当前对象的成员变量在函数中是可以修改的。
- **类函数**：如果类中的函数没有`[me: Self]` 或 `[addr me: Self*]`，则表示是一个和对象无关的函数也叫**类函数**, 等价于C++中的static成员函数。
```carbon
class NewsAriticle {
  // 类函数
  fn Make(headline: String, body_html: String) -> NewsAritcle();

  // 只读方法
  fn AsHtml[me: Self]() -> String;

  // 可修改方法
  fn Publish[addr me: Self*]() { me->published = DateTime.Now(); }

  private var headline: String;
  private var body_html: String;
  private var published: Optional(Datetime);
}

// 类外实现成员函数
fn NewsAriticle.AsHtml[me: Self]() -> String{ ... }
```

继承和抽象
- **类默认是`final`** 的，即不能被继承生成子类（俗称『绝育』）。
- `abstrct class` 和 `base class`可以有子类，也就是可以被继承
    - `abstract class`抽象类不能被实例化，因为其中可能包含抽象方法。抽象方法等同于C++中的纯虚函数.
    - `base class` 可以有子类、也可以实例化。因为它里面不会有抽象方法，如果有继承而来的抽象方法都要被实现。
```carbon
// 抽象类（abstract class）不能被实例化，因为其中可能包含抽象方法
abstract class UIWidget {
  // 抽象方法(abstract fn)没有实现
  abstract fn Draw[me: Self](s: Screen);
  abstract fn Click[addr me: Self*](x: i32, y: i32);
}

// base class 允许扩展和实例化 
base class Button extends UIWidget {
  // 实现抽象方法
  impl fn Draw[me: Self](s: Screen) { ... }
  impl fn Click[addr me: Self*];

  // 新增了一个虚函数（virtual fn）
  virtual fn MoveTo[addr me: Self*](x: i32, y: i32);
}

// 类外实现方法
fn Button.Click[addr me: Self*](x: i32, y: i32) { ... }
fn Button.MoveTo[addr me: Self*](x: i32, y: i32) { ... }

class ImageButton extends Button {
  ...
}
```

# generic 泛型 T:!
**type编译时常量值**：carbon把类型type当作值、而且type的值在编译时必须是已知的值。

可以在类里面直接实现泛型接口，可以使用泛型函数来调用实现了泛型接口的类对象
```carbon
interface Summary {                   // 泛型接口
  fn Summarize[me: Self]() -> String;
}

fn PrintSummary[T:! Summary](x: T) {  // 泛型函数
  Console.Print(x.Summarize());
}

class NewsArticle {
  ...
  impl as Summary {                   // 在类里面实现泛型接口
    fn Summarize[me: Self]() -> String { ... }
  }
}

// n 是 NewsArticle类型。使用泛型函数来调用实现了泛型接口的类对象
PrintSummary(n);   
n.Summarize();        
```

## external impl 给外部已有的类实现新的接口
```carbon
import OtherPackage;   

interface Summary {
  fn Summarize[me: Self]() -> String;
}


// 给外部已有的类 OtherPackege.Tweet 实现新接口
external impl OtherPackege.Tweet as Summary {
  fn Summarize[me: Self]() -> String { ... }
}
```


# 函数
- 函数输入参数(实参)是只读值






