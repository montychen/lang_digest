import tensorflow as tf

# 测试 tensorflow 是启用 gpu
gpus = tf.config.list_physical_devices('GPU')
cpus = tf.config.list_physical_devices('CPU')
print("\n【tensorflow 的 gpu 是否能用】")
print("\ttensorflow_version: ",  tf.__version__)
print(f"\tgpu={gpus} \n\tcpu={cpus}\n")