[facechain](https://github.com/modelscope/facechain) 制作数字分身

# ubuntu下安装`facechain`
阿里云gpu服务器，OS版本、GPU驱动选择
- ubuntu 20.04
- 安装GPU驱动：CUDA Version: **11.4** （CUDA 12.0.1 版本不行）

服务器启动后
1. 使用conda 创建 `python 3.10` 的虚拟环境
2. pytorch 要指定是 2.0版本，不然在安装`mim install mmcv-full==1.7.0` 时会报错：
<pre>
ERROR: Could not build wheels for mmcv, which is required to install pyproject.toml-based projects
</pre>
3. 在文件`facechain/requirements.txt`中，加入一行指定pytorch版本是**2.0**
```bash
torch==2.0
```
4. 然后再安装facechain的依赖 
```bash
pip3 install -r requirements.txt
```


5. 核实torch安装的版本
```bash
python -c 'import torch;print(torch.__version__)'
```

 # 命令行运行

 ## 多用户，使用各自上传的照片进行训练
 训练脚本`train_lora.sh`里的参数 **`--dataset_name`** 就是指定包含用来训练的原始照片的目录。 可以通过 **命令行的第四个参数传递**。例如，下面指定用来包含训练的原始照片的目录是`./imgs`
 ```bash
PYTHONPATH=. sh train_lora.sh "ly261666/cv_portrait_model" "v2.0" "film/film" "./imgs" "./processed" "./train_model_output/dj"
```

 ## 多用户，指定各自训练后模型的名称，以及在推理过程中使用
1. 训练脚本`train_lora.sh`里的参数 **`--output_dir`** 就是指定训练后模型的名称。 可以通过 **命令行的第六个参数传递**。
2. 推理脚本`run_inference.py`里的参数 **`train_output_dir`** 的值要和上面`--output_dir`参数的值保持一致。

训练脚本`train_lora.sh`通过命令行传递的第六个参数`./output` 会赋值给训练脚本`train_lora.sh`里的变量 **`--output_dir`**, 它保存了用户上传照片后，训练好的模型的名称。 所以如果要区别不同用户的模型，可以传不同的值， 比如，给大军的模型传递`./output/dj`, 给星辰的模型传递`./output/xc`作为第六个参数的值.

一、例如大军的训练脚本的执行命令：

```bash
PYTHONPATH=. sh train_lora.sh "ly261666/cv_portrait_model" "v2.0" "film/film" "./imgs" "./processed" "./train_model_output/dj"
```
二、推理脚本`run_inference.py`里的参数 **`train_output_dir`**保持一致，进行相应的修改，例如：
```python
...
# 如果是大军的模型，对应上面训练脚本，改成如下
50 train_output_dir = './train_model_output/dj'

# 或者
# 如果是星辰的模型，对应上面训练脚本，改成如下
50 train_output_dir = './train_model_output/xc'
...
```


# gradio 部署（nginx）
facechain的web界面使用[gradio](https://github.com/gradio-app/gradio/)进行开发, 而gradio的运行的服务只能部署在内网地址上，所以外网访问，需要通过**nginx**进行转发， 下面是`nginx.conf`的配置文件：



```
user www-data;
worker_processes auto;
pid /run/nginx.pid;
# include /etc/nginx/modules-enabled/*.conf;

events {
        worker_connections 768;
        # multi_accept on;
}


http {
    default_type  application/octet-stream;
    sendfile        on;
    keepalive_timeout  65;

    client_max_body_size 10m;   # 设置允许上传附件的大小


    server {      # 将 http 重定向 https
        listen 80;
        server_name chat.ouj.com;
        index index.html index.htm;

    location / {
            proxy_pass http://127.0.0.1:7860/;   # 转发到 gradio监听的 内网地址
            proxy_redirect off;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_set_header Host $host;
        }
    }

}
```