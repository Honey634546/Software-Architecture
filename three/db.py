import pymssql
import boto3


class db():
    def __init__(self):
        self.dbTobus_URL = 'https://sqs.us-east-1.amazonaws.com/604291830461/Myqueue'
        self.busTodb_URL = 'https://sqs.us-east-1.amazonaws.com/604291830461/busTodb'
        self.client = boto3.client('sqs')

    def connect(self):
        """
        链接数据库
        :return: 游标
        """
        self.conn = pymssql.connect(
            host='localhost',
            user='sa',
            password='123',
            database='SAW')
        cursor = self.conn.cursor()
        if not cursor:
            print('数据库连接失败')
        else:
            return cursor

    def send_message(self, message):
        """
        向业务逻辑层发送消息
        :param message: 发送的消息
        :return:
        """
        print('send ', message)
        self.client.send_message(
            QueueUrl=self.dbTobus_URL, MessageBody=message)

    def recv_message(self):
        """
        接受业务逻辑层发来的消息
        :return: 有消息则返回消息 无消息返回None
        """
        try:
            resp = self.client.receive_message(QueueUrl=self.busTodb_URL)
            self.client.delete_message(
                QueueUrl=self.busTodb_URL,
                ReceiptHandle=resp['Messages'][0]['ReceiptHandle'])
            print(resp['Messages'][0]['Body'])
            return resp['Messages'][0]['Body']
        except BaseException:
            return None

    def ExecQuery(self, sql):
        """
        执行数据库语句
        :param sql: sql语句
        :return: 操作结果
        """
        cursor = self.connect()
        cursor.execute(sql)
        result = cursor.fetchall()
        self.conn.close()
        return result

    def send_format(self, result):
        """
        修改游标查询的信息格式
        :param result:
        :return:
        """
        data = ""
        for i in range(len(result)):
            temp = "("
            for j in range(len(result[i])):
                temp += str(result[i][j])
                if j < len(result[i]) - 1:
                    temp += ","
            temp += ")"
            data += temp
        return data


if __name__ == '__main__':
    db = db()
    while True:
        print('waitting--------------------------')
        message = db.recv_message()
        if message:
            result = db.ExecQuery(message)
            data = db.send_format(result)
            db.send_message(str(data))
