import smtplib
import email
import re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email.mime.application import MIMEApplication
from email.header import Header


class webEmail:
    def __init__(self):
        self.username = 'cug@cugtianxin.top'
        self.password = 'ABCDabcd123'
        self.replyto = None
        self.rcptto = None
        self.receivers = []
        self.msg = None

    def sendEmail(self, url, title, payload, file):
        """
        向一个人发送电子邮件
        :param url: 邮件地址
        :param title: 邮件标题
        :param payload: 内容
        :return: 发送成功则返回Y，发送失败则返回N
        """
        if self.validateEmailAddress(url) == 'N':
            print('邮件地址格式错误，请检查邮件地址')
            return 'N', '邮件地址格式错误，请检查邮件地址'
        self.rcptto = url
        self.msg = self.structure_msg(title, payload, file)
        try:
            client = smtplib.SMTP()
            # python 2.7以上版本，若需要使用SSL，可以这样创建client
            # client = smtplib.SMTP_SSL()
            # SMTP普通端口为25或80
            client.connect('smtpdm.aliyun.com', 25)
            # 开启DEBUG模式
            # client.set_debuglevel(0)
            client.login(self.username, self.password)
            # 发件人和认证地址必须一致
            # 备注：若想取到DATA命令返回值,可参考smtplib的sendmaili封装方法:
            #      使用SMTP.mail/SMTP.rcpt/SMTP.data方法
            client.sendmail(self.username, self.rcptto, self.msg.as_string())
            # 支持多个收件人
            # client.sendmail(self.username, self.receivers, self.msg.as_string())
            client.quit()
            print('邮件发送成功！')
            return 'Y', '邮件发送成功！'
        except smtplib.SMTPConnectError as e:
            print('邮件发送失败，连接失败:', e.smtp_code, e.smtp_error)
        except smtplib.SMTPAuthenticationError as e:
            print('邮件发送失败，认证错误:', e.smtp_code, e.smtp_error)
        except smtplib.SMTPSenderRefused as e:
            print('邮件发送失败，发件人被拒绝:', e.smtp_code, e.smtp_error)
        except smtplib.SMTPRecipientsRefused as e:
            print('邮件发送失败，收件人被拒绝:', e.smtp_code, e.smtp_error)
        except smtplib.SMTPDataError as e:
            print('邮件发送失败，数据接收拒绝:', e.smtp_code, e.smtp_error)
        except smtplib.SMTPException as e:
            print('邮件发送失败, ', e.message)
        except Exception as e:
            print('邮件发送异常, ', str(e))

    def structure_msg(self, title, payload, file):
        """
        构建邮件主体
        :param title: 标题
        :param payload: 内容
        :param file: 附件
        :return:
        """
        msg = MIMEMultipart('mixed')
        msg['Subject'] = Header(title).encode()
        msg['From'] = '%s <%s>' % (
            Header('honey').encode(), self.username)
        msg['To'] = self.rcptto
        msg['Reply-to'] = self.replyto
        msg['Message-id'] = email.utils.make_msgid()
        msg['Date'] = email.utils.formatdate()

        # 构建 multipart/alternative 的 text/plain 部分
        alternative = MIMEMultipart('alternative')
        textplain = MIMEText('纯文本部分', _subtype='plain', _charset='UTF-8')
        alternative.attach(textplain)

        # 构建 multipart/alternative 的 text/html 部分
        texthtml = MIMEText(payload, _subtype='html', _charset='UTF-8')
        alternative.attach(texthtml)

        # 将 alternative 加入 mixed 的内部
        msg.attach(alternative)

        if file:
            filepart = MIMEApplication(file.read())
            filepart.add_header(
                'Content-Disposition',
                'attachment',
                filename=(
                    'utf-8',
                    '',
                    file.filename))
            msg.attach(filepart)
        return msg

    def validateEmailAddress(self, url):
        """
        验证是否为有效的邮件地址
        :param url: 邮件地址
        :return: 是邮件地址则Y，不是邮件地址则N
        """
        pat = r'^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}$'
        matched = re.match(pat, url)
        if matched:
            return 'Y'
        else:
            return 'N'

    def sendEmailBatch(self, urls, title, payload, file):
        """
        向一群人发送邮件
        :param urls: 多份邮件地址
        :param title: 标题
        :param payload: 内容
        :param file: 附件
        :return:
        """
        for url in urls:
            if self.validateEmailAddress(url) == 'N':
                print('邮件地址格式错误，请检查邮件地址')
                return 'N', '邮件地址格式错误，请检查邮件地址'
        # self.rcptto = url
        self.receivers = ','.join(urls)
        self.msg = self.structure_msg(title, payload, file)
        try:
            client = smtplib.SMTP()
            # python 2.7以上版本，若需要使用SSL，可以这样创建client
            # client = smtplib.SMTP_SSL()
            # SMTP普通端口为25或80
            client.connect('smtpdm.aliyun.com', 25)
            # 开启DEBUG模式
            # client.set_debuglevel(0)
            client.login(self.username, self.password)
            # 发件人和认证地址必须一致
            # 备注：若想取到DATA命令返回值,可参考smtplib的sendmaili封装方法:
            #      使用SMTP.mail/SMTP.rcpt/SMTP.data方法
            # client.sendmail(self.username, self.rcptto, self.msg.as_string())
            # 支持多个收件人
            client.sendmail(
                self.username,
                self.receivers,
                self.msg.as_string())
            client.quit()
            print('邮件发送成功！')
            return 'Y', None

        except smtplib.SMTPConnectError as e:
            print('邮件发送失败，连接失败:', e.smtp_code, e.smtp_error)
        except smtplib.SMTPAuthenticationError as e:
            print('邮件发送失败，认证错误:', e.smtp_code, e.smtp_error)
        except smtplib.SMTPSenderRefused as e:
            print('邮件发送失败，发件人被拒绝:', e.smtp_code, e.smtp_error)
        except smtplib.SMTPRecipientsRefused as e:
            print('邮件发送失败，收件人被拒绝:', e.smtp_code, e.smtp_error)
        except smtplib.SMTPDataError as e:
            print('邮件发送失败，数据接收拒绝:', e.smtp_code, e.smtp_error)
        except smtplib.SMTPException as e:
            print('邮件发送失败, ', e.message)
        except Exception as e:
            print('邮件发送异常, ', str(e))


if __name__ == '__main__':
    myemail = webEmail()
    url = '462194914@qq.com'
    s = myemail.validateEmailAddress(url)
    print(s)
    # myemail.sendEmail('1227993492@qq.com', '听课')
