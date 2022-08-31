from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import requests
import json

from detect import *

host = ('0.0.0.0', 8888)

true  = True
false = False
# 回调
def callback(json):
  return json

# 获取
def getSlideCaptcha(num):
  tokens = []
  images = []

  for i in range(num):
    try:
      # 获取滑动条验证码 及 token
      response = requests.get(
        "http://captcha.chaoxing.com/captcha/get/verification/image", 
        params = {
          "callback": "callback",
          "captchaId": "42sxgHoTPTKbt0uZxPJ7ssOvtXr3ZgZ1",
        },
        headers = {
        "Referer": "http://office.chaoxing.com/",
       }
      )

      data = eval(response.text)
      tokens.append(data['token'])
      images.append(data["imageVerificationVo"]["shadeImage"])
    except:
      print("get image error")
      pass
  return tokens, images

# 验证
def verifySlideCaptcha(tokens, result):
  # validates = []
  for token,x in zip(tokens,result):
    response = requests.get(
      "http://captcha.chaoxing.com/captcha/check/verification/result", 
      params = {
        "callback": "callback",
        "captchaId": "42sxgHoTPTKbt0uZxPJ7ssOvtXr3ZgZ1",
        "token": token,
        "textClickArr": ('[{{\"x\":{x}}}]').format(x = x),
        "coordinate": "[]",
        "runEnv": "10"
      },
      headers = {
      "Referer": "http://office.chaoxing.com/",
     }
    )
    
    data = eval(response.text)
    print(data)

  # validates



class RequestHandler(BaseHTTPRequestHandler):
  def do_GET(self):
    self.send_response(200)
    self.send_header('Content-type', 'application/json')
    self.end_headers()
    
    # 获取路径
    path = self.path.split('?')[0]
    
    # 前端获取一个 validate
    if path == "/validate/pop":
      data = {
        'success': True,
        'msg': 'null',
        'token': '123',
        'validate': '123'  
      }
      self.wfile.write(json.dumps(data).encode())
    
    # 后端储存 n 个 validate
    elif path == "/validate/get":
      query = parse_qs(urlparse(self.path).query)
      num = eval(query['num'][0])

      # 获取
      tokens,images = getSlideCaptcha(num)
      # 检测
      result = delect(images)
      # 验证
      verifySlideCaptcha(tokens, result)
      # validates = verifySlideCaptcha(tokens, result)
      #print(validates)

      data = {
        'success': True,
        'msg': 'null',
      }
      self.wfile.write(json.dumps(data).encode())

    # page not find
    else:
      data = {
        'success': False,
        'msg': 'Page Not Find',
      }
      self.wfile.write(json.dumps(data).encode())      


    return

if __name__ == '__main__':
  server = HTTPServer(host, RequestHandler)
  server.serve_forever()