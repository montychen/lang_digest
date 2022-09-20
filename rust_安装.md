 强烈建议使用 **rustup** 来安装 Rust
# mac或Linux 安装Rust
```bash
curl --proto '=https' --tlsv1.2 https://sh.rustup.rs -sSf | sh
```
运行完成后，Rust开发需要的所有工具链(rustup、rustc、cargo)都会安装在 **`~/.cargo/bin`** 目录中。而且在安装过程中，会尝试把这个目录加到环境变量PATH里
- 注意部分机器curl版本可能导致命令执行失败，比如自带的curl提示ssl 443错误，如果遇到的话，尝试重新安装curl

### 安装 C 语言编译器：（非必需）
Rust 对运行环境的依赖和 Go 语言很像，几乎所有环境都可以无需安装任何依赖直接运行。但是，Rust 会依赖 libc 和链接器 linker。所以如果遇到了提示链接器无法执行的错误，你需要再手动安装一个 C 语言编译器：
#### macOS 下：
```
xcode-select --install
```

#### Linux 下：
Linux 用户一般应按照相应发行版的文档来安装 GCC 或 Clang。
 
例如，如果你使用 Ubuntu，则可安装 `build-essential`

### 检查安装是否成功
```
$ rustc -V
rustc 1.61.0 (fe5b13d68 2022-05-18)

$ cargo -V
cargo 1.61.0 (a028ae42f 2022-04-29)
```

# cargo 构建or运行慢的问题
`cargo build`一直出现 **Blocking waiting for file lock on package cache**

如果确定没有多个程序占用，可以删除 `rm -rf ~/.cargo/.package-cache`，然后再执行

# rustup设置toolchain工具链常用命令 
升级Rust及工具链到最新稳定版: `rustup update stable`

设置默认工具链为beta版本: `rustup default beta`

设置默认工具链为nightly版本: `rustup default nightly`


# 依赖下载 [crates.io](https://crates.io)很慢
crates.io是Rust官方搭建的仓库镜像下载和管理服务, 导地址在国外，致了某些时候国内会下载缓慢
#### 1、使用[crm](https://github.com/wtklbm/crm)命令行工具，运行`crm best`自动选择国内最快的镜像
安装  `cargo install crm`

```bash
$ crm

  crm best       评估网络延迟并自动切换到最优的镜像
  crm current    获取当前所使用的镜像
  crm default    恢复为官方默认镜像
  crm publish    用官方源执行cargo publish（对于crate贡献者很有用，在开着镜像的时候不能publish）
  ...
```

#### 2、覆盖默认的镜像地址
在 `$HOME/.cargo/config.toml` 中添加以下内容：
```toml
[source.crates-io]
replace-with = 'ustc'

[source.ustc]
# 中科大的Rust Crates源
registry = "git://mirrors.ustc.edu.cn/crates.io-index"
```
首先，创建一个新的镜像源 [source.ustc]，地址使用中科大的[Rust Crates源](https://mirrors.ustc.edu.cn/help/crates.io-index.html)。

然后将默认的 crates-io 替换成新的镜像源: replace-with = 'ustc'

只要这样配置后，以后需要去 crates.io 下载的包，会全部从科大的镜像地址下载

# 卸载rust 
```
rustup self uninstall
```

# 本地文档
官方自带的英文文档

安装 Rust 的同时也会在本地安装一个文档服务，方便我们离线阅读, 运行 `rustup doc` 让浏览器打开本地文档。

中文翻译的API文档 [gitee地址](https://gitee.com/wtklbm/rust-library-chinese) 或者 [github地址](https://github.com/wtklbm/rust-library-i18n)


