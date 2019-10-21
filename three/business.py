import boto3


class Business():
    def __init__(self):
        self.dbTobus_URL = 'https://sqs.us-east-1.amazonaws.com/604291830461/Myqueue'
        self.busTodb_URL = 'https://sqs.us-east-1.amazonaws.com/604291830461/busTodb'
        self.busToui_URL = 'https://sqs.us-east-1.amazonaws.com/604291830461/busToui'
        self.uiTobus_URL = 'https://sqs.us-east-1.amazonaws.com/604291830461/uiTobus'
        self.client = boto3.client('sqs')

    def recv_message(self, url):
        """
        接受消息
        :param url: SQS队列的URL，确定是接受数据连接层还是用户层的消息
        :return:
        """
        try:
            resp = self.client.receive_message(QueueUrl=url)
            self.client.delete_message(
                QueueUrl=url,
                ReceiptHandle=resp['Messages'][0]['ReceiptHandle'])
            print(resp['Messages'][0]['Body'])
            return resp['Messages'][0]['Body']
        except BaseException:
            return None

    def send_message(self, message, url):
        """
        向业务逻辑层发送消息
        :param message:
        :return:
        """
        self.client.send_message(
            QueueUrl=url, MessageBody=message)

    def business(self):
        """
        业务处理根据接收的消息，进行对应的处理
        :return:
        """
        while True:
            print('waitting ui--------------------------')
            num = self.recv_message(self.uiTobus_URL)
            if num:
                if num is "1":
                    print("查询差价")
                    self.send_message(
                        'select avg([开盘价(元)]), avg([收盘价(元)]) from pufa group by(datepart(yy,日期))',
                        self.busTodb_URL)
                    break
                elif num is "2":
                    print("查询转手率")
                    self.send_message(
                        'select avg([换手率(%)]) from pufa group by(datepart(yy,日期))',
                        self.busTodb_URL)
                    break
                elif num is "3":
                    print("查询涨跌")
                    self.send_message(
                        'select avg([涨跌幅(%)]) from pufa group by(datepart(yy,日期))',
                        self.busTodb_URL)
                    break
        while True:
            print('waitting db--------------------------')
            result = self.recv_message(self.dbTobus_URL)
            if result:
                result = result.strip('(').strip(')').split(')(')
                print(result)
                if num is "1":
                    data = self.handle_diff(result)
                if num is "2":
                    data = self.handle_rate(result)
                if num is "3":
                    data = self.handle_up_down(result)
                print(data)
                self.send_message(data, self.busToui_URL)
                break

    # 处理数据

    def handle_diff(self, result):
        """
        查询差价
        :param result:
        :return:
        """
        data = ""
        print(result)
        for i in range(len(result)):
            temp = result[i].split(',')
            print(temp)
            out = str(float(temp[0]) - float(temp[1]))
            data += out
            if i < len(result):
                data += ','
        return data

    def handle_rate(self, result):
        """
        查询转手率
        :param result:
        :return:
        """
        data = ""
        for i in range(len(result)):
            data += str(result[i])
            if i < len(result):
                data += ','
        return data

    def handle_up_down(self, result):
        """
        查询涨跌
        :param result:
        :return:
        """
        data = ""
        for i in range(len(result)):
            temp = result[i].split(',')
            data += str(temp[len(temp) - 1])
            if i < len(result):
                data += ','
        return data


if __name__ == '__main__':
    business = Business()
    while True:
        business.business()
