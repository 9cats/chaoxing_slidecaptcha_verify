## 本地
> 注意要清理

```PowerShell
Remove-Item .\__pycache__\ -Recurse
Remove-Item .\utils\__pycache__\ -Recurse
docker rmi      9cats/chaoxing_slidecaptcha_verify   #删除镜像
docker build -t 9cats/chaoxing_slidecaptcha_verify . #构建镜像
docker push     9cats/chaoxing_slidecaptcha_verify
```

## 远程
> 注意切换到对应文件夹

```bash
docker stop caviar
docker rm caviar
docker rmi 9cats/caviar
docker stop      chaoxing_slidecaptcha_verify
docker rm        chaoxing_slidecaptcha_verify
docker rmi 9cats/chaoxing_slidecaptcha_verify
docker-compose up -d
```