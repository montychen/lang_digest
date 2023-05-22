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
- **llama-13b-hf** 文件大小: 25G,  实际占用空间：50G, 
<pre>
llama-13b-hf
    ├── [ 472]  config.json
    ├── [ 137]  generation_config.json
    ├── [9.3G]  pytorch_model-00001-of-00003.bin
    ├── [9.2G]  pytorch_model-00002-of-00003.bin
    ├── [6.1G]  pytorch_model-00003-of-00003.bin
    ├── [ 33K]  pytorch_model.bin.index.json
    ├── [8.6K]  README.md
    ├── [  72]  special_tokens_map.json
    ├── [ 207]  tokenizer_config.json
    └── [488K]  tokenizer.model
</pre>

# 二、下载 vicuna增量权重
Vicuna 仅发布了 **delta权重(增量权重)**，以符合 LLaMA 模型license授权。 
下载Vicuna的 delta 权重： 
```bash
# git lfs clone https://huggingface.co/lmsys/vicuna-7b-delta-v1.1
git lfs clone https://huggingface.co/lmsys/vicuna-13b-delta-v1.1
```
- **vicuna-13b-delta-v1.1**: 大小25G， 实际占用49G; 
<pre>
vicuna-13b-delta-v1.1
    ├── [ 578]  config.json
    ├── [ 137]  generation_config.json
    ├── [9.3G]  pytorch_model-00001-of-00003.bin
    ├── [9.2G]  pytorch_model-00002-of-00003.bin
    ├── [5.8G]  pytorch_model-00003-of-00003.bin
    ├── [ 33K]  pytorch_model.bin.index.json
    ├── [1.8K]  README.md
    ├── [ 411]  special_tokens_map.json
    ├── [ 727]  tokenizer_config.json
    └── [488K]  tokenizer.model
</pre>

# 三、vicuna增量权重 合并到 LLaMA 
因此，我们需要把**vicuna的增量权重**合并到**已经转成hf格式的LLaMA 权重**以获得**完整的Vicuna权重**。 通过调用fastchat的代码 **`fastchat.model.apply_delta`** 来完成增量权重合并。

下面的代码是居于这个目录结构
```
FastChat  llama-13b-hf  vicuna-13b-delta-v1.1
```

```bash
# 进入 FastChat 目录
cd FastChat

# 用fastchat的代码，执行增量权重合并
# llama-13b-hf 和 vicuna-13b-delta-v1.1 如果在不同的目录，下面的路径参数要调整
python3 -m fastchat.model.apply_delta \
    --base ../llama-13b-hf            \
    --delta ../vicuna-13b-delta-v1.1  \
    --target ../vicuna-13b-all-v1.1   
```

增量权重合并后， 完整的vicuna权重如下：
<pre>
vicuna-13b-all-v1.1
│   ├── [ 540]  config.json
│   ├── [ 132]  generation_config.json
│   ├── [9.3G]  pytorch_model-00001-of-00003.bin
│   ├── [9.2G]  pytorch_model-00002-of-00003.bin
│   ├── [6.1G]  pytorch_model-00003-of-00003.bin
│   ├── [ 33K]  pytorch_model.bin.index.json
│   ├── [ 411]  special_tokens_map.json
│   ├── [ 727]  tokenizer_config.json
│   └── [488K]  tokenizer.model
</pre>

# 四、运行 vicuna （推理 Inference）
#### 命令行 CLI 、单显卡
在单GPU上面进行模型推理， Vicuna-13B 需要 **28GB的GPU内存**

```bash
# 进入 FastChat 目录
cd FastChat

python3 -m fastchat.serve.cli --model-path ../vicuna-13b-all-v1.1 
```

#### 命令行 CLI 、多块显卡
如果有多个显卡，可以通过 **`--num-gpus`** 参数来指定显卡数量
```bash
# 进入 FastChat 目录
cd FastChat

# 有2块显卡，通过--num-gpus 参数来指定显卡数量
python3 -m fastchat.serve.cli --model-path ../vicuna-13b-all-v1.1 --num-gpus 2
```

#### OutOfMemoryError
如果没有足够的**显存**，可以通过向上述命令添加 **`--load-8bit`** 来启用 8 位压缩。这可以将内存使用量减少大约一半，同时略微降低模型质量。

```bash
# 进入 FastChat 目录
cd FastChat

python3 -m fastchat.serve.cli --model-path ../vicuna-13b-all-v1.1 --load-8bit
```

#### webui 运行



# 五、通过 api 访问 vicuna


# 六、自己微调 vicuna
自己喂数据训练 Vicuna的硬件要求， 不同模型大小，要求不一样。

- 显卡Tesla P40 上微调失败，此款显卡使用的SM_62架构，目前模型fine-tuning至少需要SM_75及以上架构。
- 看社区有在**4090**、**A100**或者**A80**显卡上fine-tuning成功的，所以fine-tuning只能后续再更高架构的显卡上进行了。


### 官方硬件要求
- Vicuna-7B:  
    - GPU显卡: 4卡 * A100(显存40G) 
    - CPU内存: 80G
- Vicuna-13:  
    - GPU显卡：8卡 * A100(显存40G)
    - CPU内存: 80G



# Inference推理/本地运行 vicuna的响应时间
- GPU： RTX 4090(显存24GB) * 1卡
- CPU： 15 vCPU Intel(R) Xeon(R) Platinum 8375C CPU @ 2.90GHz
- 内存：80GB
- 模型: 13B
  - **响应时间 40秒左右**
  - [vicuna官网](https://chat.lmsys.org/)的响应时间是12秒左右

