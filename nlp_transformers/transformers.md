# [Hugging Face的Transformers](https://github.com/huggingface/transformers) 

书籍 **Natural_Language_Processing_with_Transformers**  [gihut社区中文版](https://github.com/hellotransformers/Natural_Language_Processing_with_Transformers) | [amazon](https://www.amazon.com/Natural-Language-Processing-Transformers-Revised/dp/1098136799/ref=sr_1_1?keywords=Natural+Language_Processing+with+Transformers&qid=1684824571&s=books&sr=1-1)

自2017年推出以来，Transformers已经成为处理学术界和工业界广泛的自然语言处理（NLP）任务的事实标准。

- **Transformers**是2017年由谷歌研究团队发表的一篇名为 "Attention Is All You Need "的开创性论文中提出的神经网络架构。 在短短几年内，它席卷了整个领域，**粉碎了以前通常基于递归神经网络（RNN）的架构**。 Transformer架构在捕捉长序列数据的模式和处理巨大的数据集方面非常出色--以至于它的用途现在已经远远超出了NLP的范围，比如说图像处理任务。

- 在大多数项目中，你**无法获得一个巨大的数据集来从头训练一个模型**。 幸运的是，通常可以下载一个在通用数据集上预训练过的模型。 那么你需要做的就是在**你自己的（更小的）数据集上进行微调。** 自2010年代初以来，预训练已成为图像处理的主流，但在NLP中，它仅限于上下文无关的词嵌入（即单个词的密集矢量表示）。 例如，"熊 "这个词在 "泰迪熊 "和 "to bear "中有相同的预训练嵌入。 然后，在2018年，几篇论文提出了完整的语言模型，可以为各种NLP任务进行预训练和微调。 这完全改变了游戏规则。

- 像[Hugging Face](https://huggingface.co)这样的模型中心也是一个游戏规则的改变者。 在早期，预训练的模型只是被放置在零散的位置，所以要找到你需要的东西并不容易。 墨菲定律保证PyTorch用户只能找到TensorFlow模型，反之亦然。 而当你找到一个模型时，弄清楚如何对其进行微调并不总是容易。 这就是[Hugging Face的Transformers](https://github.com/huggingface/transformers) 库的作用。 它是开源的，它同时支持TensorFlow和PyTorch，**它使你很容易从Hugging Face Hub下载一个最先进的预训练模型，为你的任务配置它，在你的数据集上微调它，并评估它**。 本程序库的使用正在迅速增长。 在2021年第四季度，它被五千多个组织使用，每月使用pip方式安装超过四百万次。 此外，Transformer程序库及其生态系统正在扩展到NLP之外，图像处理模型也是可用的。 你也可以从hub下载许多数据集来训练或评估你的模型。