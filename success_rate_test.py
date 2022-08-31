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

def callback(json):
  return json

def delect(time):
  response = requests.get('http://captcha.chaoxing.com/captcha/get/verification/image?callback=callback&captchaId=42sxgHoTPTKbt0uZxPJ7ssOvtXr3ZgZ1&type=slide&version=1.1.11&_=1661778542882')

  data = eval(response.text)
  token = data['token']

  img_data = base64.b64decode(data["imageVerificationVo"]["shadeImage"])
  img = Image.open(BytesIO(img_data))
  
  model_def_path = "chaoxing_slidecaptcha_verify.cfg"  # 模型定义文件
  weights_path   = "chaoxing_slidecaptcha_verify.pth"  # 保存点权重（非结果）

  conf_thres     = 0.9  # object confidence threshold （对象置信度）
  nms_thres      = 0.4  # iou thresshold for non-maximum suppression
  batch_size     = 1    # size of the batches
  n_cpu          = 0    # number of cpu threads to use during batch generation
  img_size       = 416  # size of each image dimension

  origin_img_width = 280
  origin_img_height = 171
  
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

  img_tensor = transforms.ToTensor()(img.convert('RGB'))           # 转 tensor 对象
  img_tensor_square, _ = pad_to_square(img_tensor, 0)              # Pad to square resolution
  img_tensor_resize    = resize(img_tensor_square, img_size)       # resize

  dataloader = DataLoader(
      [img_tensor_resize],
      batch_size=batch_size,
      shuffle=False,
      num_workers=n_cpu,
  )

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

      # Get result
      if detections[0] is not None:
          x1 = detections[0][0][0]
          y1 = detections[0][0][1]
          x2 = detections[0][0][2]
          y2 = detections[0][0][3]
          conf = detections[0][0][4]
          cls_conf = detections[0][0][5]
          cls_pred = detections[0][0][6]
      else:
          x1 = 0
          y1 = 0
          x2 = 0
          y2 = 0
          conf = 0
          cls_conf = 0
          cls_conf = 0
          cls_pred = 0

  # Draw bounding boxes and labels of detections
  orig_w = origin_img_width

  # The amount of padding that was added
  pad_x = 0 * (img_size / orig_w)

  # Image height and width after padding is removed
  unpad_w = img_size - pad_x

  x1 = ((x1 - pad_x // 2) / unpad_w) * orig_w

  x = int(x1)-5

  response = requests.get(
    "http://captcha.chaoxing.com/captcha/check/verification/result", 
    params = {
      "callback": "callback",
      "captchaId": "42sxgHoTPTKbt0uZxPJ7ssOvtXr3ZgZ1",
      "type": "slide",
      "token": token,
      "textClickArr": ('[{{\"x\":{x}}}]').format(x = x),
      "coordinate": "[]",
      "runEnv": "10",
      "version": "1.1.11",
      "_": "1661870661005"
    },
    headers = {
    "Referer": "http://office.chaoxing.com/",
   }
  )

  data = eval(response.text)
  #validate 有效凭证
  if data["result"]:
    validate = eval(data["extraData"])["validate"]
    print("验证成功")
    return True
  else:
    print("验证失败")
    return False
  return


true  = True
false = False

if __name__ == "__main__":
  sum = 0
  for i in range(100):
    sum += delect()

  print("成功率: %.4f%%"% (sum /100 *100))