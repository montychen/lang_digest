# zig 安装

### 方法一：直接下载二进制包进行安装

macbook 笔记本现在用的是苹果自己的m1 pro芯片，这个芯片属于arm64架构|aarch64, 所以要选择 **aarch64**文件进行下载。

1. 直接从[zig官网](https://ziglang.org/download/)下 **aarch64**结构的二进制包

2. 解压下载的 *.tar.xz 文件, 解压后，目录里有一个名叫**zig**的可执行文件

3. 编辑`~/.bash_profile`文件，把**zig可执行文件**的路径加到`PATH`环境变量里。
```bash
ZIG_LANG_HOME=~/.dj_soft/zig_lang
export PATH=$ZIG_LANG_HOME/:$PATH
```    



