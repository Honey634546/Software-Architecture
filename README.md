# Software-Architecture

软件体系结构的课程实习
Course Practice of Software Architecture

## SQS 第一次实习：消息队列
>基于AWS SQS（Amazon Simple Queue Service，亚马逊简单队列服务）或阿里云等消息队列服务，使用Java，C#或者其他语言分别编写一个发送程序和接收程序（构建两个进程或者程序，一个用于发送消息--发到云端队列，一个用于接收消息--从云端队列订阅下来），实现“点对点”的进程间通信功能。

## three 第二次实习：三层架构

>结合相当规模数据集，使用Java设计实现一个三层架构的业务数据分析系统。各逻辑层的功能如下：

>表现层：包含输入、查询相关的控件以及数据图表的展示（如百分图，折线图）；

>业务逻辑层：数据处理、数据分析（不少于三项统计分析功能）、数据查询；

>数据访问层：负责数据库的访问，主要职责为打开、关闭数据库、构建SQL查询、返回查询结果。

>修改程序以适应三个逻辑层的分布式部署，要求三个逻辑分层分别部署于客户机（本机或手机）、AWS EC2应用服务器和AWC RDS数据库服务器上（即多层C/S架构），部署完成后能通过公网IP访问该系统。

## webmail 第三次实习：邮件推送

>结合 SOA 风格，基于阿里云的邮件服务，实现一个发送电 子邮件消息的WebService服务，包括如下三个具体服务（提供基于SOAP 协议和 REST 风格的两种接口）：
>1. sendEmail(String_url,String_payload) //邮件地址为_url，内容为_payload
>2. sendEmailBatch(String[]_url,String_payload) //批量发送邮件
>3. validateEmailAddress(String_url) //验证是否为有效的邮件地址
