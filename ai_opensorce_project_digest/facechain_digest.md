[facechain](https://github.com/modelscope/facechain) 制作数字分身

 ### 命令行运行
 ```bash
 PYTHONPATH=. sh train_lora.sh "ly261666/cv_portrait_model" "v2.0" "film/film" "./imgs" "./processed" "./output"
 ```
 - 训练脚本`train_lora.sh`通过命令行传递的第六个参数`./output` 会赋值给训练脚本`train_lora.sh`里的变量 **`--output_dir`**, 它保存了用户上传照片后，训练好的模型的名称。 所以如果要区别不同用户的模型，可以传不同的值， 比如，给大军的模型传递`./output/dj`, 给星辰的模型传递`./output/xc`作为第六个参数的值.例如：
    ```bash
    PYTHONPATH=. sh train_lora.sh "ly261666/cv_portrait_model" "v2.0" "film/film" "./imgs" "./processed" "./train_model_output/dj"`
    ```
- 推理脚本`run_inference.py`里的参数 **`train_output_dir`** 的值要和这个参数保持一致，进行相应的修改，例如：
```python
...
50 train_output_dir = './train_model_output/dj'
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