# 安装依赖
### 安装 git lfs
LFS是Large File Storage的缩写，专门用于帮助git管理大型文件[git lfs](https://github.com/git-lfs/git-lfs)
```bash
# linux(unbuntu)下安装：
curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | sudo bash
apt-get install git-lfs

# 安装完成后，首先先初始化；如果有反馈，一般表示初始化成功
git lfs install
```



### 安装 vicuna
```bash
git clone https://github.com/lm-sys/FastChat.git
cd FastChat

pip3 install --upgrade pip  # enable PEP 660 support
pip3 install -e .
```

# 一、获得 hf格式的LLaMA 权重

## 1.1 用pyllama下载LLaMA权重 & 转成hf格式
vicuna是从Meta的**LLaMA**微调而来，因此需要先下载LLaMA模型权重，这里是通过[pyllama](https://github.com/juncongmoo/pyllama) 来下载。 

默认情况下，pyllama的下载程序llama.download会在当前目录下新建一个文件夹 **`pyllama_data`**，并把下载的文件保存在这个目录里。**支持断点续传，下载没速度后，ctrl+c停掉重新打开。**

#### 安装 pyllama & 下载 LLaMA权重
```bash
# 安装 pyllama
pip install pyllama -U

# 下载 LLaMA 模型， 该方式支持断点续传。下载没速度后，ctrl+c停掉重新打开。
python -m llama.download --model_size 13B
# python -m llama.download --model_size 7B   
```

下载后的文件列表如下（7B大小13G，13B大小25G）

#### LLaMA权重 转成 hf 格式

使用huggingface的格式转换程序[convert_llama_weights_to_hf.py](https://github.com/huggingface/transformers/blob/main/src/transformers/models/llama/convert_llama_weights_to_hf.py) 把上面下载的 LLaMA模型权重 转换成 Hugging Face 的格式。

手动下载这个格式转换程序，并放在 **`pyllama_data`**这个上面保存LLaMA权重的文件的目录下。
```
git clone git@github.com:huggingface/transformers.git

cp 
```

## 1.2 直接下载 已经转成hf格式的LLaMA模型
如果不想自己从原始的LLaMA转换成HF的格式， 可以直接从Hugging Face下载转换好的模型，下面就是一个已经转成hf格式的LLaMA模型 [yahma/llama-13b-hf](https://huggingface.co/yahma/llama-13b-hf)
```bash
git lfs clone https://huggingface.co/yahma/llama-13b-hf
# git lfs clone https://huggingface.co/yahma/llama-7b-hf
```
# 二、下载 vicuna增量权重
Vicuna 仅发布了 **delta权重(增量权重)**，以符合 LLaMA 模型license授权。 
下载Vicuna的 delta 权重：
```bash
# git clone https://huggingface.co/lmsys/vicuna-7b-delta-v1.1
git clone https://huggingface.co/lmsys/vicuna-13b-delta-v1.1
```

# 三、vicuna增量权重 合并到 LLaMA 
因此，我们需要把**vicuna的增量权重**合并到**已经转成hf格式的LLaMA 权重**以获得**整个Vicuna 的权重**。


