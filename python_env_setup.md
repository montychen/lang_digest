OpenAI的python接口版本要求： `python >= 3.9`, `openai的版本至少是0.27`

# 一、 创建虚拟环境 
venv 和 [anaconda](https://anaconda.org) 二选一，推荐**anaconda**
### 1、通过 venv 操作虚拟环境
 **venv** 是python3.3标准库自带的虚拟环境库
#### 创建虚拟环境
 ```bash
 python -m venv your_env_name  # -m 把模块当作脚本运行
 ```
#### 激活虚拟环境
```bash
source <环境名称>/bin/activate
````
```bash
deactivate
```

### 2、通过anaconda 创建虚拟环境
需要先安装 [anaconda](https://anaconda.org)
#### 创建虚拟环境，同时指定python使用3.8版本
```bash
conda create -n my_python3.10_env python=3.10
```
#### 激活 anaconda 虚拟环境
```bash
source activate my_python3.10_env 
# 或者
conda activate my_python3.10_env 
```
#### 修改虚拟环境的安装目录
1、查看conda配置文件`.condarc`的路径（user config file属性）
```bash
conda info
```
<pre>
     active environment : my_python3.10_env
    active env location : /Users/dj/opt/anaconda3/envs/my_python3.10_env
            shell level : 2
       user config file : /Users/dj/.condarc     <--- 这个就是配置文件路径
 populated config files :
          conda version : 23.1.0
    conda-build version : 3.23.3
         python version : 3.10.9.final.0
       virtual packages : __archspec=1=arm64
                          __osx=13.2.1=0
                          __unix=0=0
       base environment : /Users/dj/opt/anaconda3  (writable)
      conda av data dir : /Users/dj/opt/anaconda3/etc/conda
  conda av metadata url : None
           channel URLs : https://repo.anaconda.com/pkgs/main/osx-arm64
                          https://repo.anaconda.com/pkgs/main/noarch
                          https://repo.anaconda.com/pkgs/r/osx-arm64
                          https://repo.anaconda.com/pkgs/r/noarch
          package cache : /Users/dj/opt/anaconda3/pkgs
                          /Users/dj/.conda/pkgs
       envs directories : /Users/dj/opt/anaconda3/envs    <--- 这个就是虚拟环境安装的目录
                          /Users/dj/.conda/envs
               platform : osx-arm64
             user-agent : conda/23.1.0 requests/2.28.1 CPython/3.10.9 Darwin/22.3.0 OSX/13.2.1
                UID:GID : 501:20
             netrc file : None
           offline mode : False
</pre>

2. 编辑 `.condarc` 配置文件， 修改虚拟环境的路径
   
`conda info`输出的信息中有两个路径：

- **package cache** ：缓存路径
- **envs directories** ：环境路径
  
它们按顺序将第一个路径作为虚拟环境的默认存储路径

编辑 `.condarc` 配置文件, 在文件末尾加入下面几行， 就把虚拟环境的目录改成了 /root/autodl-tmp/my_python_env
```bash
envs_dirs:
  - /root/autodl-tmp/my_python_env

pkgs_dirs:
  - /root/autodl-tmp/my_python_env
```


#### 关闭虚拟环境
```bash
conda deactivate
```
#### 列出有那些环境，及安装目录
```bash
conda env list
```
输出如下， 星号 **`*`** 表示当前激活的环境 
<pre>
# conda environments:
#
base                     /Users/dj/opt/anaconda3
my_python3.10_env     *  /Users/dj/opt/anaconda3/envs/my_python3.10_env
</pre>

#### 删除虚拟环境
```bash
conda env remove -n env_name -all
```


#### 更新 conda
```bash
conda update -n base conda
```

#### 彻底删除 anaconda
1. 运行 `anaconda-clean`
    ```bash
    conda install anaconda-clean
    anaconda-clean
    ```
2. 删除Anaconda目录，Anaconda的安装文件都包含在一个目录中，所以直接将该目录删除即可。 `conda info` 可以查看到当初 anaconda 安装所在目录
3. 删除 `~/.bash_profile`中anaconda的环境变量，使用vim打开删除；Anaconda在安装的时候，会**自动**在`~/.bash_profile` 加入一些环境变量。


[参考这篇文章](https://blog.csdn.net/weixin_45277161/article/details/127817700)


# PyPI 镜像使用帮助(例子：使用清华的镜像)
临时使用pip镜像
```bash
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple some-package
```

修改pip默认镜像
```bash
python -m pip install --upgrade pip
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```
如果您当前 pip 默认源的网络连接较差，临时使用本镜像站来升级 `pip`
```bash
python -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --upgrade pip

```

# faq

### error: metadata-generation-failed
````
error: subprocess-exited-with-error

  × python setup.py egg_info did not run successfully.
  │ exit code: 1
  ╰─> [1 lines of output]
      ERROR: Can not execute `setup.py` since setuptools is not available in the build environment.
      [end of output]

  note: This error originates from a subprocess, and is likely not a problem with pip.
error: metadata-generation-failed

× Encountered error while generating package metadata.
╰─> See above for output.
````
By running `pip install setuptools --upgrade` fixed the version with Successfully installed setuptools-67.2.0


### Your shell has not been properly configured to use 'conda activate'.
用`conda activate my_python3.10_env`激活 虚拟环境报下面的错误

``` bash
CommandNotFoundError: Your shell has not been properly configured to use 'conda activate'.
To initialize your shell, run

    $ conda init <SHELL_NAME>

Currently supported shells are:
  - bash
  - fish
  - tcsh
  - xonsh
  - zsh
  - powershell
```
解决办法，是先运行下面的命令先激活 anaconda 环境
```bash
# 激活 anaconda 环境
source activate
```