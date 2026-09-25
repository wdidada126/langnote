# EECS498-007 配套项目计划

> 严格对齐课程 6 个 Assignment + Mini-Project；全部 Python (PyTorch)，以 Handout 为蓝本重做"裸实现"。本轮只写不编译。

| 章节 | 建议语言 | 小项目 | 编译/运行方式 |
| --- | --- | --- | --- |
| L1-L4（A1-A2 对应） | Python (numpy+PyTorch) | 裸写两层 MLP 与线性分类器训练 MNIST | `python a2_mlp/train.py --model linear/mlp` |
| L5-L8（A3） | Python (PyTorch) | 手写卷积/池化反向 + mini-CNN CIFAR-10 + BN 消融 | `pytest a3_cnn/test_conv_backward.py` |
| L9-L10 | Python (PyTorch) | U-Net 语义分割小数据集（CamVid 子集） | `python seg/unet.py --data camvid` |
| L11-L12（A4） | Python (PyTorch) | 实现 SSD 与 Faster R-CNN 推理+训练骨架，算 mAP | `python detect/train.py --arch ssd` |
| L13-L16（A5） | Python (PyTorch) | LSTM Captioning + Transformer Captioning 对比（COCO 子集） | `python caption/train.py --model rnn/transformer` |
| L17 | Python (PyTorch) | ViT-mini 与 CNN 参数量/精度曲线对比 | `bash vit/ablate.sh` |
| L18-L19 | Python (PyTorch) | PixelCNN 玩具版 + PointNet 分类 | `python pointnet/main.py` |
| L20-L21（A6） | Python (PyTorch) | MNIST 上 VAE 与 DCGAN 并跑，FID/插值对比 | `python gen/train.py --model vae/gan` |
| L22 | Python (PyTorch) | Gatys 风格迁移 + 特征可视化（Deep Dream） | `python style_transfer/main.py` |
| Mini-Project | Python | 自选完整 pipeline（如证件照属性识别）：数据→训练→评估→部署 | `bash mini_project/run_all.sh` |
