- **cuda**: 是显卡厂商 NVIDIA 推出的运算平台。作为一种通用并行计算架构，CUDA 使 GPU 能够解决复杂的计算问题。它包含了 CUDA 指令集架构（ISA）以及GPU内部的并行计算引擎。 
- **cuDNN**: 是一个用于深度神经网络DNN的GPU加速库，可以在GPU上实现并行计算，显著提高性能。


# Nvidia显卡驱动

列出可支持的所有驱动以及推荐驱动， 然后使用 `apt-get install` 安装推荐的驱动
```bash
ubuntu-drivers devices 
```

执行以下命令，查看GPU驱动是否安装成功。 如果有输出，表明显卡驱动安装成功。 
```bash
nvidia-smi 
```

# 安装 cuda
2023年6月，实测在ununtu 22.0.4 通过 `pip3 install tensorflow` 安装的 tensorflow 不能正常使用 **CUDA 12**, 运行 `python test_tensorflow_gpu.py` 会报错：

**Could not find cuda drivers on your machine, GPU will not be used.**

所以在[安装 cuda](https://docs.nvidia.com/cuda/cuda-installation-guide-linux/index.html#ubuntu) 的时候，要强制回退到 **CUDA 11**
```bash
sudo apt install cuda-11-8
```



# 测试 tensorflow 是启用 gpu 
```python
import tensorflow as tf

gpus = tf.config.list_physical_devices('GPU')
cpus = tf.config.list_physical_devices('CPU')

print("\n【tensorflow 的 gpu 是否能用】")
print("\ttensorflow_version: ",  tf.__version__)
print(f"\tgpu= {gpus} \n\tcpu= {cpus}\n")
```


# 测试pytorch 是否启用 gpu
检查是否有权访问**GPU**的最简单方法，是调用`torch.cuda.is_available()`，如果结果为 `True`，则表明系统已正确安装Nvidia驱动，使用的是GPU版本的torch

```python
import torch

print("\n【pytorch 的 gpu 是否能用】")

# True使用的是GPU版本的torch； False则为CPU版本
print("\tcuda.is_available: ", torch.cuda.is_available())

# 如果CUDA可用，将设备设为GPU；如果CUDA不可用，将设备设为CPU
print('\tcuda device：', torch.device("cuda:0" if torch.cuda.is_available() else "cpu"))

print('\tgpu名称：', torch.cuda.get_device_name(0))
print("\tgpu数量:", torch.cuda.device_count())
print('\tpytorch版本：', torch.__version__)
print('\tcuda版本：', torch.version.cuda)
print('\tcudnn版本号：', torch.backends.cudnn.version())

# 将张量放在GPU上使用的话，可调用 .cuda()
print('\n\t定义一个torch格式的3*3的矩阵：\n\t', torch.rand(3, 3).cuda())

```