# vicuna 工作目录准备
下面所有操作都在 **DJ_vicuna** 这个目录下操作
```bash
# 在合适的地方创建目录
mkdir DJ_vicuna
```

按照如下指令走完后， DJ_vicuna目录最终可能会包含的目录说明（不需要手动创建，都会跟随命令自动创建）
```
FastChat  fine_tuning_output  llama-13b-hf  llama-7b-hf  pyllama_data  transformers  vicuna-13b-all-v1.1 vicuna-13b-delta-v1.1  vicuna-7b-delta-v1.1
```
- **FastChat**: git 克隆FastChat生成的目录
- **fine_tuning_output**: 自己**微调**后生成的模型
- **llama-13b-hf**: 已经转成hf格式的LLaMA 13B 模型权重
- **llama-7b-hf**: 已经转成hf格式的LLaMA 7B 模型权重
- **pyllama_data**:  LLaMA原始模型权重，里面有7B和13模型；通过pyllama的方式获得
- **transformers**:  git 克隆 hugging face的 transformers生成的目录
- **vicuna-13b-all-v1.1**: 把vicuna的13B增量权重 合并到已经转成hf格式的LLaMA权重后所获得 **完整的Vicuna 13B权重**
- **vicuna-13b-delta-v1.1**: Vicuna 仅发布了 delta权重(增量权重)， 这个是Vicuna对应13B的增量权重
- **vicuna-7b-delta-v1.1**: Vicuna 仅发布了 delta权重(增量权重)， 这个是Vicuna对应7B的增量权重


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

### 升级pip
```bash
# enable PEP 660 support
pip3 install --upgrade pip  
```



### 安装 vicuna
```bash
# 进入 DJ_vicuna
cd DJ_vicuna

git clone https://github.com/lm-sys/FastChat.git
cd FastChat
pip3 install -e .
```

# 一、获得 hf格式的LLaMA 权重

## 1.1 用pyllama下载LLaMA权重 & 转成hf格式
vicuna是从Meta的**LLaMA**微调而来，因此需要先下载LLaMA模型权重，这里是通过[pyllama](https://github.com/juncongmoo/pyllama) 来下载。 

默认情况下，pyllama的下载程序llama.download会在当前目录下新建一个文件夹 **`pyllama_data`**，并把下载的文件保存在这个目录里。**支持断点续传，下载没速度后，ctrl+c停掉重新打开。**

#### 1.1.1 安装 pyllama & 下载 LLaMA权重
```bash
# 安装 pyllama
pip install pyllama -U

# 下载 LLaMA 模型， 该方式支持断点续传。下载没速度后，ctrl+c停掉重新打开。
# 进入 DJ_vicuna
cd DJ_vicuna

python -m llama.download --model_size 13B
# python -m llama.download --model_size 7B   
```

下载后的文件列表如下（**7B大小13G**，**13B大小25G**）
<pre>
pyllama_data
    ├──13B
    │   ├── [ 154]  checklist.chk
    │   ├── [ 12G]  consolidated.00.pth
    │   ├── [ 12G]  consolidated.01.pth
    │   └── [ 101]  params.json
    ├──7B
    │   ├── [ 100]  checklist.chk
    │   ├── [ 13G]  consolidated.00.pth
    │   └── [ 101]  params.json
    ├── [  50]  tokenizer_checklist.chk
    └── [488K]  tokenizer.model
</pre>

#### 1.1.2 LLaMA权重 转成 hf 格式

使用[huggingface transformers](https://github.com/huggingface/transformers) 提供的格式转换程序[convert_llama_weights_to_hf.py](https://github.com/huggingface/transformers/blob/main/src/transformers/models/llama/convert_llama_weights_to_hf.py) 把上面下载的 LLaMA模型权重 转换成 Hugging Face 的格式。

手动下载这个格式转换程序，并放在 **`pyllama_data`** 这个上面保存LLaMA权重的文件的目录下。
```
# 克隆 transformers
cd DJ_vicuna
git clone git@github.com:huggingface/transformers.git

# 把 convert_llama_weights_to_hf.py 拷贝到 pyllama_data 目录下
cp transformers/src/transformers/models/llama/convert_llama_weights_to_hf.py pyllama_data/
```
convert_llama_weights_to_hf.py 格式转换程序的位置如图所示：
<pre>
pyllama_data
    ├──13B
    │   ├── [ 154]  checklist.chk
    │   ├── [ 12G]  consolidated.00.pth
    │   ├── [ 12G]  consolidated.01.pth
    │   └── [ 101]  params.json
    ├──7B
    │   ├── [ 100]  checklist.chk
    │   ├── [ 13G]  consolidated.00.pth
    │   └── [ 101]  params.json
    ├── [ 10K]  convert_llama_weights_to_hf.py  格式转换程序
    ├── [  50]  tokenizer_checklist.chk
    └── [488K]  tokenizer.model
</pre>

执行格式转换在 **2卡A100(80G)** 上转换 **13B格式** , CPU内存消耗30G, **耗时 6分钟**
```bash
cd pyllama_data

# 转换 7B模型
python convert_llama_weights_to_hf.py \
    --input_dir ./ --model_size 7B \
    --output_dir ../llama-7b-hf

# 转换 13B模型
python convert_llama_weights_to_hf.py \
    --input_dir ./ --model_size 13B \
    --output_dir ../llama-13b-hf
```
现在 **DJ_vicuna** 下的目录结构如下：
```bash
FastChat  llama-13b-hf  llama-7b-hf  pyllama_data  transformers
```
已经转成hf格式的LLaMA模型 **llama-13b-hf** 目录结构:
```
llama-13b-hf
    ├── [ 502]  config.json
    ├── [ 132]  generation_config.json
    ├── [9.3G]  pytorch_model-00001-of-00003.bin
    ├── [9.2G]  pytorch_model-00002-of-00003.bin
    ├── [6.1G]  pytorch_model-00003-of-00003.bin
    ├── [ 33K]  pytorch_model.bin.index.json
    ├── [ 411]  special_tokens_map.json
    ├── [ 727]  tokenizer_config.json
    ├── [1.8M]  tokenizer.json
    └── [488K]  tokenizer.model
```

已经转成hf格式的LLaMA模型 **llama-7b-hf** 目录结构:
```
llama-7b-hf
    ├── [ 502]  config.json
    ├── [ 132]  generation_config.json
    ├── [9.3G]  pytorch_model-00001-of-00002.bin
    ├── [3.3G]  pytorch_model-00002-of-00002.bin
    ├── [ 26K]  pytorch_model.bin.index.json
    ├── [ 411]  special_tokens_map.json
    ├── [ 727]  tokenizer_config.json
    ├── [1.8M]  tokenizer.json
    └── [488K]  tokenizer.model
```



## 1.2 直接下载 已经转成hf格式的LLaMA模型
如果不想自己从原始的LLaMA转换成HF的格式， 可以直接从Hugging Face下载转换好的模型，下面就是一个已经转成hf格式的LLaMA模型 [yahma/llama-13b-hf](https://huggingface.co/yahma/llama-13b-hf)
```bash
# 进入 DJ_vicuna
cd DJ_vicuna

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
# 进入 DJ_vicuna
cd DJ_vicuna

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

下面的代码基于如下**DJ_vicuna**的目录
```
FastChat  llama-13b-hf  vicuna-13b-delta-v1.1
```

```bash
# 进入 FastChat 目录
cd FastChat

# 13B增量权重合并, 用fastchat的代码执行，
# llama-13b-hf 和 vicuna-13b-delta-v1.1 如果在不同的目录，下面的路径参数要调整
python3 -m fastchat.model.apply_delta \
    --base ../llama-13b-hf            \
    --delta ../vicuna-13b-delta-v1.1  \
    --target ../vicuna-13b-all-v1.1   

# 7B增量权重合并, 用fastchat的代码执行，
python3 -m fastchat.model.apply_delta \
    --base ../llama-7b-hf            \
    --delta ../vicuna-7b-delta-v1.1  \
    --target ../vicuna-7b-all-v1.1   
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

# 13B
python3 -m fastchat.serve.cli --model-path ../vicuna-13b-all-v1.1 

# 7B
python3 -m fastchat.serve.cli --model-path ../vicuna-7b-all-v1.1 

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



### Vicuna-7B 微调硬件
官方推荐: 4 * A100(**40G**); CPU内存: 80G

DJ 实测 **2 x A100 (80GB) + CPU 28核 80G内存** 
  - 微调成功 耗时： 17 分钟
   
### Vicuna-13B 微调硬件
官方推荐: 8 * A100(**80G**); CPU内存 200G内存

DJ 实测 **2 x A100 (80GB) + CPU 28核 200G内存** 微调代码
  - ❌报错： **内存溢出** OutOfMemoryError: CUDA out of memory. Tried to allocate 606.00 MiB
  
DJ 实测 **8 x 4090 (24GB) + CPU 28核 200G内存** 微调代码
  - ❌报错：**RuntimeError**: FlashAttention backward for head dim > 64 requires **A100** or **H100** GPUs as the implementation needs a large amount of shared memory


## 微调代码
**DJ实测是可以直接在vicuna已有的完整模型基础上进行微调**， 格式要求就是模型的格式要求是已经转成hf格式的。 
> 下面的微调代码是在 vicuna已有的模型基础上进行微调， 而不是直接从原始的LLaMA上进行微调。
> 
微调程序 **torchrun** 的参数
- `--nproc_per_node` 指定GPU的个数


### 在vicuna完整7B模型vicuna-7b-all-v1.1上进行微调
使用官方提供的 dummy.json 数据
```bash
cd FastChat

# --nproc_per_node 指定GPU的个数
torchrun --nproc_per_node=2 --master_port=20001 fastchat/train/train_mem.py \
    --model_name_or_path ../vicuna-7b-all-v1.1  \
    --data_path playground/data/dummy.json \
    --bf16 True \
    --output_dir ../fine_tuning_output/base-vicuna-7b-all-v1.1-dummy \
    --num_train_epochs 2 \
    --per_device_train_batch_size 1 \
    --per_device_eval_batch_size 1 \
    --gradient_accumulation_steps 8 \
    --evaluation_strategy "no" \
    --save_strategy "steps" \
    --save_steps 300 \
    --save_total_limit 10 \
    --learning_rate 2e-5 \
    --weight_decay 0. \
    --warmup_ratio 0.03 \
    --lr_scheduler_type "cosine" \
    --logging_steps 1 \
    --report_to "tensorboard" \
    --fsdp "full_shard auto_wrap" \
    --fsdp_transformer_layer_cls_to_wrap 'LlamaDecoderLayer' \
    --tf32 True \
    --model_max_length 2048 \
    --gradient_checkpointing True \
    --lazy_preprocess True
```

### 在vicuna完整13B模型 vicuna-13b-all-v1.1 上进行微调
使用官方提供的 dummy.json 数据
```bash
cd FastChat

# --nproc_per_node 指定GPU的个数
torchrun --nproc_per_node=2 --master_port=20001 fastchat/train/train_mem.py \
    --model_name_or_path ../vicuna-13b-all-v1.1  \
    --data_path playground/data/dummy.json \
    --bf16 True \
    --output_dir ../fine_tuning_output/base-vicuna-13b-all-v1.1-dummy \
    --num_train_epochs 2 \
    --per_device_train_batch_size 1 \
    --per_device_eval_batch_size 1 \
    --gradient_accumulation_steps 8 \
    --evaluation_strategy "no" \
    --save_strategy "steps" \
    --save_steps 300 \
    --save_total_limit 10 \
    --learning_rate 2e-5 \
    --weight_decay 0. \
    --warmup_ratio 0.03 \
    --lr_scheduler_type "cosine" \
    --logging_steps 1 \
    --report_to "tensorboard" \
    --fsdp "full_shard auto_wrap" \
    --fsdp_transformer_layer_cls_to_wrap 'LlamaDecoderLayer' \
    --tf32 True \
    --model_max_length 2048 \
    --gradient_checkpointing True \
    --lazy_preprocess True
```

#### 运行自己微调好的模型(推理 Inference)
如果有多个显卡，可以通过 `--num-gpus` 参数来指定显卡数量
```bash
cd FastChat

python3 -m fastchat.serve.cli --model-path ../fine_tuning_output/base-vicuna-7b-all-v1.1-dummy
```

#### 从原始的LLaMA 模型上进行微调。
```bash
cd FastChat

# 13B 微调 这个是从原始的LLaMA 13B模型上进行微调。
torchrun --nproc_per_node=2 --master_port=20001 fastchat/train/train_mem.py \
    --model_name_or_path ../llama-13b-hf  \
    --data_path playground/data/dummy.json \
    --bf16 True \
    --output_dir ../fine_tuning_output/base-llama-13b-hf-dummy \
    --num_train_epochs 2 \
    --per_device_train_batch_size 1 \
    --per_device_eval_batch_size 1 \
    --gradient_accumulation_steps 8 \
    --evaluation_strategy "no" \
    --save_strategy "steps" \
    --save_steps 300 \
    --save_total_limit 10 \
    --learning_rate 2e-5 \
    --weight_decay 0. \
    --warmup_ratio 0.03 \
    --lr_scheduler_type "cosine" \
    --logging_steps 1 \
    --report_to "tensorboard" \
    --fsdp "full_shard auto_wrap" \
    --fsdp_transformer_layer_cls_to_wrap 'LlamaDecoderLayer' \
    --tf32 True \
    --model_max_length 2048 \
    --gradient_checkpointing True \
    --lazy_preprocess True


# 7B 微调 这个是从原始的LLaMA 7B模型上进行微调。
torchrun --nproc_per_node=2 --master_port=20001 fastchat/train/train_mem.py \
    --model_name_or_path ../llama-7b-hf  \
    --data_path playground/data/dummy.json \
    --bf16 True \
    --output_dir ../fine_tuning_output/base-llama-7b-hf-dummy \
    --num_train_epochs 2 \
    --per_device_train_batch_size 1 \
    --per_device_eval_batch_size 1 \
    --gradient_accumulation_steps 8 \
    --evaluation_strategy "no" \
    --save_strategy "steps" \
    --save_steps 300 \
    --save_total_limit 10 \
    --learning_rate 2e-5 \
    --weight_decay 0. \
    --warmup_ratio 0.03 \
    --lr_scheduler_type "cosine" \
    --logging_steps 1 \
    --report_to "tensorboard" \
    --fsdp "full_shard auto_wrap" \
    --fsdp_transformer_layer_cls_to_wrap 'LlamaDecoderLayer' \
    --tf32 True \
    --model_max_length 2048 \
    --gradient_checkpointing True \
    --lazy_preprocess True
```




# 本地运行 vicuna的响应时间
### 1卡 * RTX 4090(显存24GB) 
- CPU： 15 vCPU Intel(R) Xeon(R) Platinum 8375C CPU @ 2.90GHz
- 内存：80GB
- 模型: 13B
  - **响应时间 40秒左右**
  - [vicuna官网](https://chat.lmsys.org/)的响应时间是12秒左右
  - 报错: **内存溢出 OutOfMemoryError**: CUDA out of memory. 
    - 解决办法： 添加 **`--load-8bit`** 参数来启用 8 位压缩，这样才正常运行
    ```bash
    # 进入 FastChat 目录
    cd FastChat

    python3 -m fastchat.serve.cli --model-path ../vicuna-13b-all-v1.1 --load-8bit
    ```


### GPU： 2卡 * A100(80G)
- CPU： 28 vCPU Intel(R) Xeon(R) Platinum 8352M CPU @ 2.30GHz
- 内存：456GB
- 模型: 13B
  - GPU内存消耗 40G, 内存消耗 20G
  - **响应时间 10秒左右**
  - [vicuna官网](https://chat.lmsys.org/)的响应时间是12秒左右
