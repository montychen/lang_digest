✅

❌

[Carbon](https://github.com/carbon-language/carbon-lang) 是2022年7月19日，在多伦多举行的CppNorth大会上，Google的**Chandler Carruth**在会上[对外正式发布](https://www.youtube.com/watch?v=omrY53kbVoA)的一门开放源码的语言，目标是可以和C++代码互相无缝调用，强调性能、简单和安全：**simple c++、safter c++**。
>Chandler Carruth 是Google在c++委员会的代表，他在委员会里的地位仅次于 C++ 之父 Bjarne Stroustrup 和 Herb Sutter

# 关键字
carbon的大多数语句前面都有一个介绍关键字，这是carbon 的精心设计。虽然对人类读者来说可能并不重要，但它对我们的工具很重要，因为代码更容易解析、而且没有歧义。例如：fn 表示函数，var 表示变量声明，let 表示常量声明 . . .

# 在线carbon编辑器
carbon目前还处于非常初期， 可以用 Carbon 在线 IDE 来试验代码。[ compiler-explorer.com](https://carbon.compiler-explorer.com/) 或者 [Carbon Godbolt](https://carbon.godbolt.org/) 

# Carbon代码编译的3种构建模式build model
- development build: 在开发构建中，优先级是方便诊断问题、缩短构建时间。
- performance build: 在性能构建中，优先级是代码有最快的执行速度、最低低的内存使用率。
- hardened build: 在强化构建中，首要任务是安全、其次才是性能。

# 命名
### 命名习惯
- **UpperCamelCase** 大驼峰命名，用于类型名、函数名称、常量	
- **lower_snake_case** 蛇形命名，用于变量名、关键字

### alias 定义别名
`alias`可以给一个类型、函数、变量定义别名。 不能给一个具体的值定义别名。
```carbon
alias MyInt = Int;                        // 给一个类型，创建一个别名MyInt
alias NewName = SomePackage.host_name;    // 给一个变量定义别名   

class ContactInfo {
  external impl as Printable;
  alias PrintToScreen = Printable.Print;  // 给一个函数定义别名
  ...
}

alias four = 4;      // ❌ 不能给一个具体的值定义别名。
 
```
### namespce 
`namespce`可以给后面声明的名称定义一个前缀，类似于命名空间。
```carbon
package P api;

fn F();

namespace N;       // 在当前包定义一个命名空间 N
private fn N.G();  // 使用命名空间 N 当前缀，定义一个函数 N.G()
fn Bad.H();        // ❌ 命名空间 Bad 没有定义， 不能用来做前缀


namespace M.L;  // 定义了2个命名空间，一个是 M  另一个是 M.L
fn M.Q();
fn M.L.R();


fn N.K() {
  F();             // 调用外包的全局函数 F()
  G();             // 在命名空间 N 的里面，调用 N.G()函数，可以省略前缀
}

```




# package & library
```carbon
package ExplorerTest api;

fn Main() -> i32 {
    var s: auto = "Hello world!";
    Print(s);
    return 0;
}
```
- package包含library， 编译后分发的二进制包是`package`, `import`导入的是library；
- 每个library只能有一个 **`api`接口文件**，可以理解成是这个库的对外接口声明文件，包含了这个库允许外部访问的所有public公共声明，实现可以放在这个`api`文件、或者其它的 **`impl`实现文件**。
    - 每个`impl`实现文件，都会自动导入它自己的`api`接口文件。
    - `api`里的声明默认是`public`。
    - 如果把`api`文件里的某个声明手动标记为`private`，那就是库范围内的私有，只在这个库的`api`和所有`impl`文件里可见。 其它库不可见。
    - `impl`里的声明默认是`private`，意思是只在自己的这个`impl`文件里可见。
- 每个package有自己的命名空间，同一个包内的库不能重名；在不同的包里，库可以同名。

#### 包声明： package  可选包名 可选`library`和库名   `api`或`impl`;
```carbon
//        包名      库关键字    库名
package  Geometry  library   "Shapes"  api;   // 在包Gemetry里定义一个名叫 “Shapes”的库
```
- 省略包名，则该文件属于默认包default package。默认包不能被其它包导入，也就是默认包里的东西不能被其它包复用。
- 省略`library`，这个文件属于默认库default library。 `import`导入包的时候，如果不明确指定库名，导入的就是这个包的默认库。
- 如果一个文件顶部完全没有包声明，那这个文件默认属于`api`文件，属于默认包和默认库，它还是可以通过 **`package impl`** 有多个`impl`实现文件。这种用法主要是为测试和小的程序提供便利。
#### 导入： import   包名    可选`library`和库名
```carbon
//       包名     库关键字    库名  
improt Geometry  library   "Shapes"   // 导入Geometry这个包里的“Shapes”库 
```
- `import`导入包时，省略关键字`library`和库名，导入的就是这个包的默认库。
- `import 包名...`, 导入的东西都当作`private`, 所以要导入当前包的库，要省略包名，用下面的方式导入。 
- `import library ...`导入时省略包名，这种情况，关键字`library`和库名不能省略；导入的是当前包的库。
    ```carbon
    import library "Vertex";   // 从当前包导入“Vertex”库
    import library default;    // 从当前包导入默认库
    ```
- `import library ...`把指定库的public公共声明导入,而且是作为`private`导入到当前文件。 
- 每个`impl`实现文件，都会自动导入它自己的`api`接口文件。

# 变量和常量
用var声明变量， let声明常量。
### auto
var或let在声明变量或常量的时候，同时进行初始化，如果没有指定类型，就要明确使用`auto`来让系统根据初始化值，自动推导出类型Type inference
```carbon
var x: i64 = 2;
let x: auto = x + 3;   // The type of `y` is inferred to be i64  
```


# 类型type
**carbon把类型type当作值**，而且是在**编译时已知的常量值**；而且作为**值**来说，值的类型都是明确的。
- Expression表达式是用来计算值的， 既然把type当作值看待，那么书写类型是按照表达式的语法习惯; 所以，Carbon 在类型中不使用尖括号`<`... `>`，因为`<` 和`>`在表达式中是比较的语义。

# 整型
下划线 `_` 可用作数字分隔符。数字常量区分大小写：
- 12_345 和 12345相等（十进制）
- 0x1FE（十六进制）表示十六进制的前缀`0x`必须小写，而后面表示10-15的字母A-F必须大写用。
- 0b1010（二进制）表示二进制的前缀`0b` 必须为小写

## 整数加减乘 + - * 溢出overflw
- development build: 在开发构建中，运行时发生overflow会立即被捕获。
- performance build: 在性能构建中，优化程序的前提是假定不会发生overflow；如果真的发生了overlow，程序该如何处理是没有预先定义的。
- hardened build: 在强化构建中，针对溢出的处理都是事先定义好的: 要么程序被中止，要么返回在数学上是不正确的结果。
  - 如果是无符号整数计算，溢出发生，结果会是**回绕运算wrapping**: 直接抛弃已经溢出的最高位，将剩下的部分返回   

# 字符串 String 和 StringView
- `String` UTF-8编码的字节序列
- `StringView` UTF-8 字节序列的只读引用。


单行和多行字符串字面量
- 单行字符串使用双引号 `"`。
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

# tuple 元组 ( ) ，用索引访问成员 x[1]
元组用括号声明`( )`, 使用索引访问元组的成员。
```carbon
package ExplorerTest api;

fn Main() -> i32 {
  var x: auto = (0, 1);     // 声明元组
  Print("{0}", x[1]);       // 用索引访问元组成员
  return x[0];
}
```

# struct 结构体 {...}，用名称访问成员`s.name1` 
用 **花括号{...}** 来声明struct，结构体可帮助我们用名称而不是索引来访问成员； 如：`var s: auto = {.name1 = value1, .name2 = value2, ... };`，然后就可以这样访问`s.name1`。
- [x] carbon的结构体struct和元组tuple一样，都很轻量，可以**就地直接使用**，不需要预先定义。 

#### 就地直接使用struct作为变量类型，不需要提前定义struct
```carbon
package ExplorerTest api;

fn Main() -> i32 {
  var point: auto = {.x_axis = 0, .y_axis = 1};  // 就地直接使用struct 结构体
  point = {.x_axis = 5, .y_axis = 10};           // 修改struct结构体成员值

  var result: i32 = point.x_axis * point.x_axis + point.y_axis * point.y_axis;  // 使用名称来访问结构体成员
  Print("Result : {0}", result);
  return 0;
}
```
#### 就地直接使用struct作为函数返回类型，不需要提前定义struct
> 函数可以使用元组或者结构体来返回多个值
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
Carbon的指针不支持算术运算，也就是不能通过对指针执行加加减减等这些算术操作，来先前或先后来移动指针所指向的地址。
- `T*` 声明指针,  如： `var y: i32* = &x;` 
- `&var` 获取变量var的地址
- `*ptr` 解引用Dereference，访问指针ptr所指向地址的内容， 如： `*y = 100;` 
   > **`ptr->m`** 是`(*ptr).m`的语法糖
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
### Optional
Carbon不支持空指针，如果想表示不存在，使用Optional(T*)。

# 数组 [T, N]
- `[T; N]` 声明具备N个元素的T类型数组。 `var a: [i32; 4] = (1, 2, 3, 4);`
- 在初始化赋值的时候，数组的大小N可以推导出来，可以省略。
```carbon
// `[i32;]` equivalent to `[i32; 3]` here.
var a: [i32;] = (1, 2, 3);
```
`

# 循环语句 while for
- `while( condition ){ ... }` 一般的循环，条件为True就继续执行： `while (not (x == 0)) { ... } `
- `for (var name: String in names) { ... }`  用于在容器内循环



# match 匹配语句
```carbon
match(condition) {
  case (condition) => {...}   // 可以包含if条件帮助过滤,  要同时满足该case语句和if条件，才会执行该case。
  default => {...}    // default 可选，不是必须的
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

match 的case语句可以包含if条件来帮助过滤: 要同时满足该case语句和if条件，才会执行该case。
```carbon
fn Bar() -> (i32, (f32, f32));

fn Foo() -> f32 {
  match (Bar()) {
    case (42, (x: f32, y: f32)) => {
      return x - y;
    }
    case (p: i32, (x: f32, _: f32)) if (p < 13) => {   // 包含if条件帮助过滤
      return p * x;
    }
    case (p: i32, _: auto) if (p > 3) => {             // 包含if条件帮助过滤
      return p * Pi;
    }
    default => {
      return Pi;
    }
  }
}
```

# class 类
Carbon用 **`Self`** 表示当前类的类型。 类成员声明的顺序，决定了它在内存布局中的顺序。
- **类成员默认`public`**：Carbon中类中成员访问控制权限默认都是public，如果需要声明成私有则需要单独加private关键字。这个行为和C/C++的struct相同，但是和主流语言的class都不同。
- **`[me: Self]`只读方法**：表示当前对象的成员变量在函数中是只读、不能进行任何修改。**me**在函数体中表示对当前对象的引用，类似C++的this。
- **`[addr me: Self*]`可修改方法**： 表示当前对象的成员变量在函数中是可以修改的。 **addr**意思是先获取参数的地址。
- **类函数**：如果类中的函数没有`[me: Self]` 或 `[addr me: Self*]`，则表示是一个和对象无关的函数也叫**类函数**, 等价于C++中的static成员函数。**carbon没有构造函数constructor**，创建类实例习惯用以`Make`来命名的 **类方法**实现。
    ```carbon
    class NewsAriticle {
      // 类函数
      fn Make(headline: String, body_html: String) -> NewsAritcle(); // 创建类实例习惯用类方法来实现。
    }
    ```
- **析构函数**： Carbon有析构函数，不是抽象类abstract class都可以有析构函数。 抽象类不能生产实例，所以也就不需要析构。用`destructor [me: Self] {...}`或`destructor [addr me: Self*] {...}`定义。
  - 如果一个非抽象类没有定义析构函数，系统默认会生成一个空的析构函数：`destructor [me: Self] { }`
  - 析构函数也可以用**virtual**定义成虚函数，如果是这样，那它子类的析构函数都必须是 impl

      ```carbon
      base class MyBaseClass {
          virtual destructor [addr me: Self*] { ... }
      }

      class MyDerivedClass extends MyBaseClass {
          impl destructor [addr me: Self*] { ... }
      }
      ```

    > 类的析构函数在其数据成员的析构函数之前运行。数据成员按声明的相反顺序销毁。派生类在其基类之前被销毁, 也就是：
      1. 派生类的析构函数运行， 派生类的数据成员按声明的相反顺序销毁
      2. 直接基类的析构函数运行，直接基类的数据成员按声明的相反顺序销毁


```carbon
class NewsAriticle {
  // 类函数
  fn Make(headline: String, body_html: String) -> NewsAritcle(); // 创建类实例习惯用类方法来实现。

  // 只读方法
  fn AsHtml[me: Self]() -> String;

  // 可修改方法, 这里me是指针类型， me->published 是 (*m).published 的语法糖，
  fn Publish[addr me: Self*]() { me->published = DateTime.Now(); } // 在类内直接实现方法或函数

  private var headline: String;
  private var body_html: String;
  private var published: Optional(Datetime);
}

// 类外实现成员函数 fn ClassName.MethodName(...){...}
fn NewsAriticle.AsHtml[me: Self]() -> String{ ... }
```

### single inheritance: 类不支持多继承，只有单继承
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

- **abstract fn** 必须被子类重写，只能在抽象类abstract class里定义、但**不能有默认实现**。 这个对应c++的纯虚函数。

### virtual methods 虚函数
默认情况下，方法是普通正常的函数，不是虚函数的， **不是虚函数不能重写覆盖** override：
- 普通正常的函数，不是虚函数，那么在定义它的类中就要有实现; 可以在类内实现，也可以在类外实现。
- 不是虚函数，就不能被覆盖重写，包括不能被子类覆盖重写override。


虚函数可以在子类或者子子类中多次重写覆盖。虚函数必须明确用下面2个关键字声明：
- **virtual fn** 可以被子类重写。只能在base或abstract的类里定义、**一定有默认实现**，哪怕是仅有一对大括号的空方法。
    - 情况1：基类中定义了virtual方法，但在派生类中没有重写该虚方法。那么在对派生类实例的调用中，该虚方法使用的是基类定义的方法。
    - 情况2：基类中定义了virtual方法，然后在派生类中重写该方法。那么在对派生类实例的调用中，该虚方法使用的是派生重写的方法。

- **abstract fn** 必须被子类重写。只能在抽象类abstract class里定义、**不能有默认实现**。 对应c++的纯虚函数。

    -
- 虚函数只能在类里面定义，不能在接口中定义。而且只能在 base class 或者 abstract class类里定义，**final class** 里不能定义虚函数，但可以`impl`父类的虚函数。 
- 类函数不能定义成虚函数，类函数就是类中那些没有[me: Self] 或 [addr me: Self*]的函数
> **impl fn**用来重写或实现父类的虚函数（用virtual 或者 abstract标记的函数）。  后续子类还可以继续用`impl`覆盖重写这个虚函数。


### 多态&方法动态派发
多态：同一操作作用于不同的对象，可以不同的执行结果。一个指向子类的指针，可以转换成父类指针，此时用父类指针调用虚函数，实际调用的是子类指针所指向的类型重写的方法。

### partial Self 和 `.base`


### public private protected 访问控制权限
- **类成员默认`public`**：Carbon类成员默认是public, 可以被任意实例访问。这个行为和C/C++的struct相同，但是和主流语言的class都不同。
- **private** 只能在自己的类内和`友元freend`内访问，不能被派生类访问。
  > 私有虚函数`private virtual fn`或`private abstract fn`可以在子类中实现，但还是不能在子类中被调用。

- **procteted** 除了可以在自己的类内访问，也可以被子类访问。

### friend 友元

### 结构体和类
在carbon里，**struct结构体本质其实是只有数据成员的类** (data class)。具有相同数据成员的struct结构体和类class之间， carbon定义了隐式转换。这样就很方便了，可以用stuct结构体，给具有相同数据成员的类class赋值，如：
```carbon
class Widget {
  var x: i32;
  var y: i32;
  var payload: String;
}

// 用stuct结构体，给具有相同数据成员的类class赋值
var w1: Widget = {.x = 3, .y = 4, .payload = "Sproing"};  
w1 = {.x = 2, .y = 1, .payload = "Bounce"};  

// w2 的类型是struct 
var w2: Auto =  {.x = 3, .y = 4, .payload = "Sproing"}; 

//用as把w3转换成Widget类型；他们具有相同的数据成员，可以相互转换 
var w3: Auto =  {.x = 3, .y = 4, .payload = "Sproing"} as Widget; 
```


# Choice type 选项类型
**Choice type选项类型** 类似`tagged union`，可以在容纳最大项的数据存储空间中存储不同类型的数据。每一项有个名称和一个可选参数，每次只能有一项生效。
```carbon
choice IntResult {
    Success(value: i32),
    Failure(error: String),
    Cancelled
}
...
// 生成选项类型的实例
if (not IsDigit(c)) {
   return .Failure("Invalid character");  // 也可以写成 IntResult.Failure("Invalid character")
}
...
```
用`match`匹配选项类型
```carbon
match (ParseAsInt(s)) {
  case .Success(value: i32) => {
    return value;
  }
  case .Failure(error: String) => {
    Display(error);
  }
  case .Cancelled => {
    Terminate();
  }
}
```


# generic 泛型 T:!
**泛型**即通过参数化类型来实现在同一份代码上操作多种数据类型。**`T:!`** 表示 **T** 是一个泛型的类型参数, 简称泛型参数。carbon的泛型参数**T**有两种：`checked` 和 `template`。
- 在`[]` **方括号里提前声明的泛型参数，调用时不要也不能手动指定**，它会根据实参自动推断。
- 没有在方括号`[]`里提前声明，而是在参数列表里用 **`:!`** **直接声明直接用的泛型函数，调用时要明确指定**。这样想想，正常参数列表里的参数，调用时本来就要提供值，估计就好理解了。
- **`checked`** 这是泛型参数的**默认方式**，如：**`[T:! Printable & Ordered]`**  **编译时**就对泛型参数T的实参进行类型检查，要满足约束条件。约束条件一般是某个具体的接口，多个约束条件可以用 **&** 连接， 
     ```carbon
     fn Min[T:! Printable & Ordered](x: T, y: T) -> T {
         x.Print();
         y.Print();
         return if x <= y then x else y;
     }
     
     var a: i32 = 1;
     var b: i32 = 2;
     Assert(Min(a, b) == 1);
     Assert(Min("abc", "xyz") == "abc");
     ```
- **`template`** 在泛型参数前加一个前缀**template**，如：**`[template T:! Type]`**, 类型**Type**表示可以传递任何类型， 当然也可以添加约束。这种泛型参数是在**运行时的实际调用**才触发实例化，所以类型检查、鸭子类型绑定都延后了。
    ```carbon
    fn Min[template T:! Ordered](x: T, y: T) -> T {   // 给template泛型参数添加约束
        return if x <= y then x else y;
    }
    ```
    > 当约束只是`Type`时，这将提供类似于C++模板的语义。当然随后可以持续添加更具体的约束，直到添加完所有的约束后，此时删除`template`以切换到泛型参数默认的`checked`方式下，是安全的。尽管检查泛型参数通常是首选，但模板泛型参数可以在C++和 Carbon 之间转换代码，并解决泛型类型检查过于严格导致的一些问题。

    > 也可以不用提前声明，而是**直接在函数参数前加`template`**，并改用`:!`来声明，这种**不提前声明的泛型函数，调用的时候要手动明确指定**。

    ```carbon
    fn Convert[template T:! Type](source: T, template U:! Type) -> U {    // 泛型参数U没有提前定义 
        var converted: U = source;
        return converted;
    }
        
     fn Foo(i: i32) -> f32 {
        return Convert(i, f32);      // 泛型参数T自动推导；泛型参数U没有提前定义，要明确指定为f32
    }
    ```
### 泛型类
类也可以有参数，而且只能用泛型做类的参数；可以根据需要在泛型参数前加`template`
```carbon
class Stack(T:! Type) {           // 泛型参数 T ，没有在方括号[]里提前声明
  fn Push[addr me: Self*](value: T);
  fn Pop[addr me: Self*]() -> T;

  var storage: Array(T);
}

var int_stack: Stack(i32);       // 直接声明直接用的泛型函数 T，调用时明确指定为 i32

// 下面这个例子，稍显复杂，但有点意思
fn PeekTopOfStack[T:! Type](s: Stack(T)*) -> T {
  var top: T = s->Pop();
  s->Push(top);
  return top;
}

PeekTopOfStack(&int_stack);
```

### generic Choice type 泛型选项类型
选项类型可以有泛型参数；可以根据需要在泛型参数前加template
```carbon
choice Result(T:! Type, Error:! Type) {
  Success(value: T),
  Failure(error: Error)
}
```


# interface 接口
接口定义了一组要求或约束；carbon通过要求某个类型实现一些接口来表达约束；满足约束后，就可以说类型具备某种能力。
- 接口里定义的方法，可以有`Self`参数，如：`[me: Self]` 或者 `[addr me: Self*]`， **Self** 指代最终实现这个接口的类。

### `impl as` *Interface* 在类里实现接口，接口方法直接成为类的方法
```carbon
interface Summary {                       // 接口
  fn Summarize[me: Self]() -> String;     // Self 表示实现这个接口的类型
}

fn PrintSummary[T:! Summary](x: T) {  // 泛型函数用接口来约束泛型参数
  Console.Print(x.Summarize());
}

class NewsArticle {
  ...
  impl as Summary {                               // 在类里面实现接口
    fn Summarize[me: Self]() -> String { ... }    // 接口方法 Summarize() 成为类的方法
  }
}

// n 是 NewsArticle类型。
PrintSummary(n);       // 调用泛型函数 
n.Summarize();         // 用类实例调用类的方法  
```

### `external impl` *Class* `as` *Interface* 给外部类实现接口
```carbon
import OtherPackage;   

interface Summary {
  fn Summarize[me: Self]() -> String;
}

// 给外部类 OtherPackege.Tweet 实现接口
external impl OtherPackege.Tweet as Summary {
  fn Summarize[me: Self]() -> String { ... }
}
```
## 接口里的 Associated types 关联类型
关联类型有什么用？比如，一个栈stack通常可以存储不同类型的数据，那么描述这个栈的接口就可以用`关联类型`来表示栈中将要存储的的数据类型；在具体实现接口的时候，再明确指定具体的类型；这样，**接口就统一**了，而存储不同数据类型的**实现可以有多种**。

- 关联类型是**接口里声明的一个类型占位符**，用**let**和泛型语法 **`:!`** 声明，如：`let ElementType:! Movable`; 没有初始值。
- 关联类型可以**像一个真正的类型**一样，在这个接口里自由使用，它的最终取值在具体实现这个接口时才会明确指定，而且是**编译时已知**的值;

#### `let` ElementType`:!` Movable; 在接口里声明关联类型
例如，定义一个栈stack接口，在这个接口里有一个关联类型用来表示将要存储的数据类型，而它的具体的类型，在实现这个栈stack接口时，再明确指定。
```carbon
interface StackInterface {
  let ElementType:! Movable;      // ElementType 是关联类型，可以看做是一个类型占位符
  fn Push[addr me: Self*](value: ElementType);   // 可以像真实类型一样，使用关联类型ElementType
  fn Pop[addr me: Self*]() -> ElementType;
  fn IsEmpty[addr me: Self*]() -> bool;
}
```
#### `impl as` StackInterface `where` .ElementType = i32 `{...}`实现接口时指定关联类型
例子：在类里面用`impl as`实现上面定义的栈接口StackInterface，用**where**指定关联类型的具体取值。同样的接口，下面提供了2种不同的实现。
```carbon
class IntStack {
  impl as StackInterface where .ElementType = i32 {
    fn Push[addr me: Self*](value: i32);
    ...
  }
}

class FruitStack {
  impl as StackInterface where .ElementType = Fruit {
    fn Push[addr me: Self*](value: Fruit);
    ...
  }
}
```

### 泛型接口 generic interface
接口常用的参数是`Self` 指代最终实现这个接口的类。接口也可以有泛型参数；可以根据需要在泛型参数前加template。接口的泛型参数和Associated type关联类型不同。

```carbon
interface AddWith(U:! Type);
```
一个没有参数的接口，只能被一个类实现一次。但带参数(泛型参数)的接口，可以被一个类实现多次，只要每次提供不同的类型作为泛型参数的实参。比如，一个类可以实现AddWith(i32)同时也可以实现 AddWith(BigInt)。

# CommonType 公共类型
`CommonType`公共类型想解决的问题是：比如，在传统if...else..语句中，两个分支的返回值，有时是不同的两个类型； 

- **`if` c `then` A `else` B** 返回值A和B要求是公共类型。A 和 B 的公共类型是`A as CommonType(B))`。
- **`impl` A `as CommonTypeWith(`B`) where .Result =` C {...}**，类型A和B通过实现`CommonTypeWith`接口成为公共类型。
- `CommonType`: A 和 B 的公共类型始终与 B 和A 的公共类型相同。

还有一种情况情况是

# 函数
函数参数
- 参数默认只读: 默认是通过`let`语义传递参数，所以参数是只读值的。
- var参数： 先把`var参数`内容copy到函数内的一个局部变量，实参其实就是这个局部变量，所以在函数内可以修改参数，但这种修改外部不可见。
- ptr指针参数：指针参数可以被修改，而且这种修改外部可见。一般是通过`&var`获取变量地址来传递参数，在函数内通过`*ptr`来访问或者修改内容。 

函数返回值
- 返回多个值： 函数可以使用元组或者结构体来返回多个值.
- 返回值类型是`auto`：通过返回值，自动推导出返回类型. 

### return var    
避免函数返回变量时发生复制，可以把 **`returned`** 加到返回变量的声明中，并在要返回的地方用 **`return var`** 直接返回，注意这里没有写具体变量的名称，而是用**var**；因为当变量被标记为`returned`时，它就是函数内唯一必须返回的值。
```carbon
fn MakeCircle(radius: i32) -> Circle {
  returned var c: Circle;
  c.radius = radius;
  return var;    // `return c` 是无效的语句， 因为在声明变量c的时候，使用了returned。这里要用 return var
}
```
如果被`returned`的变量，在函数正常返回前已经离开它的作用域，失效了。所以后面就不能用 return var 返回，而是要写出具体的变量名或者表达式.
```carbon
fn MakePointInArea(area: Area, preferred_x: i32, preferred_y: i32) -> Point {
  if (preferred_x >= 0 && preferred_y >= 0) {
    returned var p: Point = { .x = preferred_x, .y = preferred_y };  // 变量p 标记为 returned
    if (area.Contains(p)) {
      return var;
    }
  }   // 标记为returned的变量 p，已经离开它的作用域，所以后面就不能用 return var 返回，而是要写出具体的变量名。

  return area.RandomPoint();
}
```

# Operator overloading 运算符重载





