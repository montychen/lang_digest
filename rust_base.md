# if let
```
if let Ok(length) = fields[1].parse::<f32>() {
     // 输出到标准输出
     println!("{}, {}cm", name, length);
}
```
if let 是一个匹配表达式，用来从 = 右边的结果中，匹配出 length 的值：
   
1. 当=右边的表达式执行成功，则会返回一个 Ok(f32) 的类型，若失败，则会返回一个 Err(e) 类型，if let 的作用就是仅匹配 Ok 也就是成功的情况，如果是错误，就直接忽略
2. 同时 if let 还会做一次解构匹配，通过 Ok(length) 去匹配右边的 Ok(f32)，最终把相应的 f32 值赋给 length
3. 当然你也可以忽略成功的情况，用 `if let Err(e) = fields[1].parse::<f32>() {...}` 匹配出错误，然后打印出来
