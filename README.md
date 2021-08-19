# 使用摄像头拍照并发往邮箱(纯属娱乐)

## 打包exe,app  使用摄像头拍摄照片发送到指定邮箱

## 打包方式 
   - pyinstaller,py2app,py2exe
   - pyinstaller --console --onefile get_cap_img.py

## pyinstaller打包参数配置

   - pyinstaller -F -wsetup.py   

      -F:覆盖打包
      -w:不显示命令窗口
      -i:更改应用程序图标 - pay.ico
      
## 查看图片
   - 收件人邮箱附件下载，后缀改为.jpeg就可以查看了
