#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import argparse
import configparser
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(config, args):
    """
    根据配置和命令行参数发送邮件
    """
    # 创建一个multipart/alternative子类型的MIME邮件对象
    msg = MIMEMultipart("alternative")
    msg["Subject"] = args.title
    msg["From"] = config['account']['email']
    msg["To"] = args.receiver
    # 创建邮件正文
    text = MIMEText(args.content, "plain")
    msg.attach(text)
    # 连接到SMTP服务器
    server = smtplib.SMTP(config['server']['server'], config['server']['port'])
    server.starttls()  # 启动安全传输模式
    server.login(config['account']['email'], config['account']['password'])  # 登录SMTP服务器
    # 发送邮件
    server.sendmail(config['account']['email'], args.receiver, msg.as_string())
    # 关闭服务器连接
    server.quit()

def new_config():
    """
    新建配置文件
    """
    # 输入配置
    config = configparser.ConfigParser()
    config['server'] = {
        'server': input("请输入邮件SMTP服务器地址："),
        'port': input("请输入邮件SMTP服务器端口号：")
    }
    config['account'] = {
        'email': input("请输入SMTP账户："),
        'password': input("请输入SMTP密码：")
    }
    # 保存配置
    with open("config.ini", "w") as f:
        config.write(f)

def main():
    # 是否无配置文件
    if not os.path.isfile("config.ini"):
        print("\033[1;32;40m")
        print("=== 检测到首次运行，请先完成配置！ ===")
        new_config()
        print("=== 配置完成！自动退出，下次运行生效 ===")
        print("如果后续运行配置有问题，可以删掉ini文件或手动修改其内容")
        print("\033[0m")
        exit()

    # 读取命令行参数
    p = argparse.ArgumentParser()
    p.add_argument("-r", "--receiver", type=str, help="收件人邮箱地址", required=True)
    p.add_argument("-t", "--title", type=str, help="邮件标题", required=True)
    p.add_argument("-c", "--content", type=str, help="邮件内容", required=True)
    args = p.parse_args()

    # 读取配置文件
    config = configparser.ConfigParser()
    config.read("config.ini")

    # 发送邮件
    try:
        send_email(config, args)
        print("\033[1;32;40m")
        print(f"成功发送邮件《{args.title}》到 {args.receiver}")
        print("\033[0m")
    except Exception as e:
        print("\033[1;31;40m")
        print(f"发生了错误：{e}")
        print("\033[0m")

if __name__ == "__main__":
    main()