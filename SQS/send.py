# （1）基于AWS SQS（Amazon Simple Queue Service，亚马逊简单队列服务）或阿里云等消息队列服务，使用Java，C
# 或者其他语言分别编写一个发送程序和接收程序（构建两个进程或者程序，一个用于发送消息--发到云端队列，一个用于接
# 收消息--从云端队列订阅下来），实现“点对点”的进程间通信功能。
# 提示与思考：
# 1) 本次实验用到的AWS 相关操作，参见文档《AWS使用简明教程》，里面有如何获取AWS key，以及如何建立AWS连接等介绍。
# 2) 前端页面应简洁明了，用户体验较好，重点在后台通信机制。
# 3) 这种消息队列服务是基础性的，AWS 作为商业云平台提供了针对SQS的高可用性解决方案。如果你基于Kafka构建消息队列服务，如何确保其高可用性？
# 4) 相关链接：
# AWS .NET API,你可以在该链接找到你想要的类及相关方法：
# https://docs.aws.amazon.com/sdkfornet/v3/apidocs/Index.html
# Java API:
# https://docs.aws.amazon.com/zh_cn/AWSJavaSDK/latest/javadoc/index.html
# SQS官方文档链接：
# https://docs.aws.amazon.com/sqs/index.html#lang/zh_cn


import tkinter
from tkinter import *

import boto3


class send_GUI(tkinter.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master.title("Sender")

        lable1 = Label(self.master, text="消息")
        lable1.pack()

        self.entry1 = Entry(self.master)
        self.entry1.pack()

        button1 = Button(
            self.master,
            text='发送',
            command=lambda: self.send_message(
                self.entry1.get()))
        button1.pack()
        self.client = boto3.client('sqs')

    def send_message(self, message):

        URL = 'https://sqs.us-east-1.amazonaws.com/604291830461/Myqueue'
        # body = 'hello world'
        response = self.client.send_message(QueueUrl=URL, MessageBody=message)
        print(response)
        self.entry1.delete(0, END)


if __name__ == '__main__':
    root = tkinter.Tk()
    app = send_GUI(root)
    root.mainloop()
