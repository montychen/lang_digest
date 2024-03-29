# print
```
print(*, sep: StringLiteral, end: StringLiteral, flush: Bool)
```
- `sep`: 打印出来的东西，用`sep`来指定每项间的 **分隔符** , 默认是**空字符串**
- `end`: 打印完成后，需要额外输出的，默认是回车`\n`。 打印完成后不想换行，可以指定end为空，如：`end=""`

```mojo
def main():
    print("Hello", "Mojo", sep="__", end="") # 输出： Hello__Mojo    而且打印完成后不换行
```