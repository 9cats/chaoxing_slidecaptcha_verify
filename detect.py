# 导入依赖库
import urllib3
import requests
import os, base64
import matplotlib.pyplot as plt
from io import BytesIO
from PIL import Image

from torch.utils.data import DataLoader

from models import *

from utils.datasets import *
from utils.utils import *

# 检测
import time
import datetime

# YoloV3 配置
model_def_path = "chaoxing_slidecaptcha_verify.cfg"  # 模型定义文件
weights_path   = "chaoxing_slidecaptcha_verify.pth"  # 保存点权重（非结果）

conf_thres     = 0.9  # object confidence threshold （对象置信度）
nms_thres      = 0.4  # iou thresshold for non-maximum suppression
batch_size     = 1    # size of the batches
n_cpu          = 0    # number of cpu threads to use during batch generation
img_size       = 416  # size of each image dimension

origin_img_width = 280
origin_img_height = 171

def base64ImgData_covert_TensorImg(images):
  tersonImages = []
  for image in images:
    image_data             = base64.b64decode(image)
    image_obj              = Image.open(BytesIO(image_data))
    image_tensor           = transforms.ToTensor()(image_obj.convert('RGB'))
    image_tensor_square, _ = pad_to_square(image_tensor, 0)
    image_tensor_resize    = resize(image_tensor_square, img_size)
    tersonImages.append(image_tensor_resize)
  return tersonImages

def delect(images):
  # 初始化
  device = torch.device("cpu") # 选择使用 cpu
  # Set up model
  model = Darknet(model_def_path, img_size=img_size).to(device)
  # Load checkpoint weights
  model.load_state_dict(torch.load(weights_path, map_location="cpu"))
  # Set in evaluation mode
  model.eval()
  # Select FloatTensor
  Tensor = torch.FloatTensor

  # Get Terson Image
  tersonImages = base64ImgData_covert_TensorImg(images)

  dataloader = DataLoader(
    tersonImages,
    batch_size=batch_size,
    shuffle=False,
    num_workers=n_cpu,
  )

  result = []

  prev_time = time.time()
  for batch_i, img_tensor in enumerate(dataloader):
    # Configure input
    input_img = Variable(img_tensor.type(Tensor))

    # Get detections
    with torch.no_grad():
        detections = model(input_img)
        detections = non_max_suppression(detections, conf_thres, nms_thres)
        
    # Log progress
    current_time = time.time()
    inference_time = datetime.timedelta(seconds=current_time - prev_time)
    prev_time = current_time
    print("\t+ Batch %d, Inference Time: %s" % (batch_i, inference_time))

    # Get result
    if detections[0] is not None:
        x1 = detections[0][0][0]
        cls_conf = detections[0][0][5]
    else:
        x1 = 0
        cls_conf = 0
    x1 = x1 / img_size * origin_img_width

    x = int(x1) - 6
    
    print(detections)
    print("\t+ Label: %s, Conf: %.5f" % ("target", cls_conf))

    result.append(x)

  return result