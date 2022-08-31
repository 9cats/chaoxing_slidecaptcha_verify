## 本地
> 注意要清理

```PowerShell
Remove-Item .\__pycache__\ -Recurse
Remove-Item .\utils\__pycache__\ -Recurse
docker rmi 9cats/chaoxing_slidecaptcha_verify #删除镜像
docker build -t 9cats/chaoxing_slidecaptcha_verify .
```