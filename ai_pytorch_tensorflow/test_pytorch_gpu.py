import torch

# 测试pytorch 是否启用 gpu
print("\n【pytorch 的 gpu 是否能用】")
use_cuda = torch.cuda.is_available()
print("\tcuda.is_available: ", use_cuda)

device = torch.device("cuda:0" if use_cuda else "cpu")
print('\tcuda设备名：',device)
print('\tgpu名称：',torch.cuda.get_device_name(0))
print('\tpytorch版本：',torch.__version__)
print('\tcuda版本：',torch.version.cuda)
print('\tcudnn版本号：',torch.backends.cudnn.version())
print('\t定义一个torch格式的3*3的矩阵：\n\t',torch.rand(3,3).cuda())