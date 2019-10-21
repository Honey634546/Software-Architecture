import boto3
import tkinter
from tkinter import scrolledtext
from tkinter import *
from threading import Thread
from threading import Timer



class recv_GUI(tkinter.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master.title("Recv")

        lable1 = Label(self.master, text="消息")
        lable1.pack()

        self.scr = scrolledtext.ScrolledText(
            self.master,
            width=30,
            height=10,
            wrap=WORD)
        self.scr.pack()
        self.client = boto3.client('sqs')

        t = Thread(target=self.show)
        t.start()


    def show(self):
        self.recv_message()
        t = Timer(0.5, self.show)
        t.start()

    def recv_message(self):
        URL = 'https://sqs.us-east-1.amazonaws.com/604291830461/Myqueue'

        try:
            resp = self.client.receive_message(QueueUrl=URL)
            date = resp['ResponseMetadata']['HTTPHeaders']['date']

            self.client.delete_message(
                QueueUrl=URL, ReceiptHandle=resp['Messages'][0]['ReceiptHandle'])

            self.scr.insert(END, date+'\r\n')
            self.scr.insert(END, resp['Messages'][0]['Body']+'\r\n')
            return resp['Messages'][0]['Body']
        except BaseException:
            return None


if __name__ == '__main__':
    root = tkinter.Tk()
    app = recv_GUI(root)
    root.mainloop()
    tmp = {
        'Messages': [
            {
                'MessageId': '1c3e8527-56a5-4aab-9a9c-a7d35f095f55',
                'ReceiptHandle': 'AQEBhoGlTrKpL+um84SzJsUi2iGp3pnlZ6POQNAUhwWiPPlJJBvBITFF3yg+YMRESlW3wcuqZOgKib11v+HaIC+6IDvbnkU1J7QLWB+eJ9Z2UXv1uABPSRihAQkq1loX5yJfTNEO9rlfDKNxab5IA2ev737EMl8HWc2Bkf/OUQ1cIwotdfWI2L7OCU5KzluW9QcpDfBbvE7OshEaF632nGpU4i8W3DCdUbcgFi5r0ThNn8mVV1aJLgrH7qGn+8QDAkyjl4/QmWLCLl9KQZXNzwfQp60phxHMKtuCUCleL2BNhgIp99jGuwbKnbvy3p1PMUFzMHNkA7F9/MPBQmHnDuwLlRvN9fyPU1CgBgC5zGQxOMuV4HE4A0YnoEJUmr0d1ZD3',
                'MD5OfBody': '5ca2aa845c8cd5ace6b016841f100d82',
                'Body': 'da'}],
        'ResponseMetadata': {
            'RequestId': '60bc276a-b6c1-5c15-94db-717f884e3ead',
            'HTTPStatusCode': 200,
            'HTTPHeaders': {
                'x-amzn-requestid': '60bc276a-b6c1-5c15-94db-717f884e3ead',
                'date': 'Mon, 07 Oct 2019 13:23:27 GMT',
                'content-type': 'text/xml',
                'content-length': '829'},
            'RetryAttempts': 0}}
