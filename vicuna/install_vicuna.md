安装 vicuna
```bash
git clone https://github.com/lm-sys/FastChat.git
cd FastChat

pip3 install --upgrade pip  # enable PEP 660 support
pip3 install -e .
```

# 下载 LLaMA 权重
vicuna是从Meta的**LLaMA**微调而来，因此需要先下载LLaMA模型权重，这里是通过[pyllama](https://github.com/juncongmoo/pyllama) 来下载。 

默认情况下，pyllama的下载程序llama.download会在当前目录下新建一个文件夹 **`pyllama_data`**，并把下载的文件保存在这个目录里。**支持断点续传，下载没速度后，ctrl+c停掉重新打开。**


```bash
# 安装 pyllama
pip install pyllama -U

# 下载 LLaMA 模型， 该方式支持断点续传。下载没速度后，ctrl+c停掉重新打开。
python -m llama.download --model_size 13B
# python -m llama.download --model_size 7B   
```

下载后的文件列表如下（7B大小13G，13B大小25G）

# LLaMA权重 转成 Hugging Face 格式

使用huggingface的格式转换程序[convert_llama_weights_to_hf.py](https://github.com/huggingface/transformers/blob/main/src/transformers/models/llama/convert_llama_weights_to_hf.py) 把上面下载的 LLaMA模型权重 转换成 Hugging Face 的格式。

手动下载这个格式转换程序，并放在 **`pyllama_data`**这个上面保存LLaMA权重的文件的目录下。
```
git clone git@github.com:huggingface/transformers.git

cp 
```