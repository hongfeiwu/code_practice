# -*- coding: UTF-8 -*-
"""
SMTP（Simple Mail Transfer Protocol）即简单邮件传输协议,它是一组用于由源地址到目的地址传送邮件的规则，由它来控制信件的中转方式。
smtplib.SMTP( [host [, port [, local_hostname]]] )
    host: SMTP 服务器主机。 你可以指定主机的ip地址或者域名如: runoob.com，这个是可选参数。
    port: 如果你提供了 host 参数, 你需要指定 SMTP 服务使用的端口号，一般情况下 SMTP 端口号为25。
    local_hostname: 如果 SMTP 在你的本机上，你只需要指定服务器地址为 localhost 即可。


错误1：smtplib.SMTPAuthenticationError: (550, b‘User has no permission‘)
    我们使用python发送邮件时相当于自定义客户端根据用户名和密码登录，然后使用SMTP服务发送邮件，
    新注册的163邮箱是默认不开启客户端授权的（对指定的邮箱大师客户端默认开启），因此登录总是被拒绝，
    解决办法（以163邮箱为例）：进入163邮箱-设置-客户端授权密码-开启（授权码是用于登录第三方邮件客户端的专用密码）
错误2：smtplib.SMTPAuthenticationError: (535, b‘Error: authentication failed‘)
　　以163邮箱为例，在开启POP3/SMTP服务，并开启客户端授权密码时会设置授权码，
    将这个授权码代替smtplib.SMTP().login(user,password)方法中的password即可。


"""
import smtplib
from email.mime.text import MIMEText

# 第三方 SMTP 服务
mail_host = "smtp.163.com"  # SMTP服务器
mail_user = "wwwuhongfei@163.com"  # 用户名
mail_pass = "whf0602"  # 密码

sender = 'wwwuhongfei@163.com'  # 发件人邮箱(最好写全, 不然会失败)
receivers = ['455767036@qq.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

content = '只是测试一下下!'
title = 'Python SMTP Mail Test'  # 邮件主题
message = MIMEText(content, 'plain', 'utf-8')  # 内容, 格式, 编码
message['From'] = "{}".format(sender)
message['To'] = ",".join(receivers)
message['Subject'] = title

try:
    smtpObj = smtplib.SMTP_SSL(mail_host, 465)  # 启用SSL发信, 端口一般是465
    smtpObj.login(mail_user, mail_pass)  # 登录验证
    smtpObj.sendmail(sender, receivers, message.as_string())  # 发送
    print("mail has been send successfully.")
except smtplib.SMTPException as e:
    print(e)
