# [Llama2](https://ai.meta.com/llama/) Meta开源的大模型、Hugging Face[下载地址](https://huggingface.co/meta-llama)

Llama2开源模型目前有**7B**、**13B**、**70B**三种尺寸，预训练阶段使用了2万亿Token，SFT阶段使用了超过10w数据，人类偏好数据超过100w。 虽然Llama 2对第一版的LlaMA模型做了升级，但是其仍然对中文没有太好的支持，中文占比只有0.13%。

为了遵循相应的许可，一般都不会发布完整的模型权重，只发布LoRA权重，其与Meta的LlaMA2权重合并就可以得到完整的模型权重

hugging face的[开放大模型排行榜](https://huggingface.co/spaces/HuggingFaceH4/open_llm_leaderboard)