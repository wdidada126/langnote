# yolo

深度学习培训班
就说一个，图像领域的目标检测，就是用yolo

YOLO（You Only Look Once）是一种非常流行的实时目标检测系统，它能够快速准确地识别图像中的多个物体。YOLO将目标检测问题转化为一个回归问题，直接从图像像素到边界框坐标和类别概率的映射。这种方法相较于传统的目标检测方法，如先生成候选区域再分类的R-CNN系列，速度有了大幅提升。


### 使用场景
YOLO目标检测广泛应用于以下场景：
1. 视频监控：实时监控视频中的异常行为或特定物体。
2. 自动驾驶：识别道路上的行人、车辆和其他障碍物。
3. 工业自动化：在生产线上检测和分类零件。
4. 零售业：货架管理，统计不同商品的数量。
5. 无人机：导航和避开障碍物。
6. 医疗图像分析：在医学图像中检测病变或器官。
7. 体育分析：追踪运动员和球的位置。


### API Demo 例子
为了使用YOLO进行目标检测，你需要安装包含预训练模型的YOLO库，比如`darknet`或基于Python的封装库如`tensorflow-yolov3`。以下是一个简单的API使用例子，假设你已经有了一个安装了所需库的环境：
```python
import cv2
import numpy as np
# 加载YOLO模型
net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
# 加载类别名称
with open("coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]
# 给定一个图像路径
image = cv2.imread("image.jpg")
# 图像尺寸
(H, W) = image.shape[:2]
# 构建blob，设置网络输入
blob = cv2.dnn.blobFromImage(image, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
net.setInput(blob)
# 运行前向传播
outs = net.forward(output_layers)
# 初始化列表以存储检测结果
class_ids = []
confidences = []
boxes = []
# 循环遍历输出层
for out in outs:
    # 遍历检测对象
    for detection in out:
        # 提取当前物体检测的类别ID和置信度
        scores = detection[5:]
        class_id = np.argmax(scores)
        confidence = scores[class_id]
        # 过滤掉那些置信度较小的物体检测
        if confidence > 0.5:
            # 将边界框的坐标还原至与原图相匹配，YOLO返回的是边界框的中心点坐标以及边界框的宽度和高度
            box = detection[0:4] * np.array([W, H, W, H])
            (center_x, center_y, width, height) = box.astype("int")
            # 用中心点坐标来表示边界框
            x = int(center_x - (width / 2))
            y = int(center_y - (height / 2))
            # 更新边界框坐标，置信度和类别ID
            boxes.append([x, y, int(width), int(height)])
            confidences.append(float(confidence))
            class_ids.append(class_id)
# 应用非极大值抑制来抑制弱、重叠边界框
indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
# 绘制边界框
for i in range(len(boxes)):
    if i in indexes:
        x, y, w, h = boxes[i]
        label = str(classes[class_ids[i]])
        confidence = confidences[i]
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(image, label +
```

比如有些不要求实时性的场景，可以选其他更慢但精度更高的模型，但不会用，因为yolo开源的代码最完善，网上各种教程也都是yolo，手把手教你
像瑞芯微的rk系列的芯片，带npu跑神经网络模型，他们适配了每一个版本的yolo，给出完整的c++部署demo代码，而且持续更新，出新的他们就适配

介绍 UltralyticsYOLOv8YOLOv8 

基于深度学习和计算机视觉领域的尖端技术，在速度和准确性方面具有无与伦比的性能。其流线型设计使其适用于各种应用，并可轻松适应从边缘设备到云 API 等不同硬件平台。
探索YOLOv8 文档，这是一个旨在帮助您了解和利用其特性和功能的综合资源。无论您是经验丰富的机器学习实践者还是该领域的新手，该中心都旨在最大限度地发挥YOLOv8 在您的项目中的潜力。

yolo 源代码仓库

YOLO (You Only Look Once) 是一种用于目标检测的深度学习算法。源代码可以在 GitHub 上找到。
YOLO v1 的源代码仓库：https://github.com/pjreddie/darknet
YOLO v2 的源代码仓库：https://github.com/pjreddie/darknet
YOLO v3 的源代码仓库：https://github.com/pjreddie/darknet
YOLO v4 的源代码仓库：https://github.com/AlexeyAB/darknet
注意：YOLO v1 到 v3 都是使用 Darknet 框架实现的，而 YOLO v4 则是使用更加现代化的框架，如 Keras 和 TensorFlow。


YOLO:简史
YOLO(You Only Look Once）是一种流行的物体检测和图像分割模型，由华盛顿大学的约瑟夫-雷德蒙（Joseph Redmon）和阿里-法哈迪（Ali Farhadi）开发。YOLO 于 2015 年推出，因其高速度和高精确度而迅速受到欢迎。

2016 年发布的YOLOv2 通过纳入批量归一化、锚框和维度集群改进了原始模型。
2018 年推出的YOLOv3 使用更高效的骨干网络、多锚和空间金字塔池进一步增强了模型的性能。
YOLOv4于 2020 年发布，引入了 Mosaic 数据增强、新的无锚检测头和新的损失函数等创新技术。
YOLOv5进一步提高了模型的性能，并增加了超参数优化、集成实验跟踪和自动导出为常用导出格式等新功能。
YOLOv6于 2022 年由美团开源，目前已用于该公司的许多自主配送机器人。
YOLOv7增加了额外的任务，如 COCO 关键点数据集的姿势估计。
YOLOv8是YOLO 的最新版本，由Ultralytics 提供。YOLOv8 YOLOv8 支持全方位的视觉 AI 任务，包括检测、分割、姿态估计、跟踪和分类。这种多功能性使用户能够在各种应用和领域中利用YOLOv8 的功能。
YOLOv9引入了可编程梯度信息 (PGI) 和通用高效层聚合网络 (GELAN) 等创新方法。

版本：

https://github.com/ultralytics/ultralytics/releases/tag/v8.2.0

real-time object detection and image segmentation model

https://docs.ultralytics.com/
https://docs.ultralytics.com/zh

github源仓库地址：
https://github.com/ultralytics/ultralytics
https://github.com/ultralytics/yolov5
https://github.com/ultralytics/yolov3


比如有些不要求实时性的场景，可以选其他更慢但精度更高的模型，但不会用，因为yolo开源的代码最完善，网上各种教程也都是yolo，手把手教你
像瑞芯微的rk系列的芯片，带npu跑神经网络模型，他们适配了每一个版本的yolo，给出完整的c++部署demo代码，而且持续更新，出新的他们就适配

实时性
精度

YOLO（You Only Look Once）是一种非常流行的实时目标检测系统，它能够快速准确地识别图像中的多个物体。YOLO将目标检测问题转化为一个回归问题，直接从图像像素到边界框坐标和类别概率的映射。这种方法相较于传统的目标检测方法，如先生成候选区域再分类的R-CNN系列，速度有了大幅提升。
### 使用场景
YOLO目标检测广泛应用于以下场景：
1. 视频监控：实时监控视频中的异常行为或特定物体。
2. 自动驾驶：识别道路上的行人、车辆和其他障碍物。
3. 工业自动化：在生产线上检测和分类零件。
4. 零售业：货架管理，统计不同商品的数量。
5. 无人机：导航和避开障碍物。
6. 医疗图像分析：在医学图像中检测病变或器官。
7. 体育分析：追踪运动员和球的位置。
