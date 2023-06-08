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