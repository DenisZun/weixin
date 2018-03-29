# -*- coding:utf-8 -*-
import time
import xmltodict
from flask import Flask, request
import hashlib

WECHAT_TOKEN = 'denis'

app = Flask(__name__)


@app.route('/wechat8005', methods=['GET', 'POST'])
def index():
    # signature：微信加密签名
    signature = request.args.get('signature')
    # timestamp：时间戳
    timestamp = request.args.get('timestamp')
    # nonce：随机数
    nonce = request.args.get('nonce')
    # echostr：随机字符串
    echostr = request.args.get('echostr')

    # 1）将token、timestamp、nonce三个参数进行字典序排序
    tmp_list = [WECHAT_TOKEN, timestamp, nonce]
    tmp_list.sort()

    # 2）将三个参数字符串拼接成一个字符串进行sha1加密
    tmp_str = ''.join(tmp_list)
    sin_str = hashlib.sha1(tmp_str).hexdigest()

    print 'token是{}'.format(sin_str)
    print '加密签名是{}'.format(signature)

    # 3）开发者获得加密后的字符串可与signature对比，标识该请求来源于微信
    if sin_str == signature:
        # 进入这个判断说明对接成功
        print '服务器可用'

        if request.method == 'POST':
            print '接收到消息'
            # 处理消息
            # get请求做校验;post请求发消息

            xml_str = request.data  # data属性负责处理客户端发给服务器的字符串数据
            xml_dict = xmltodict.parse(xml_str)  # 得到一个字典{‘xml’:{'MsgType':12312}}
            request_dict = xml_dict.get('xml')

            # 获取类型
            msg_type = request_dict.get('MsgType')

            # 判断文本类型
            if msg_type == 'text':
                new_dict = {
                    'ToUserName': request_dict.get('FromUserName'),
                    'FromUserName': request_dict.get('ToUserName'),
                    'CreateTime': time.time(),
                    'MsgType': 'text',
                    'Content': u'你今天设了没？'
                }
                print request_dict.get('Content')

                # 封装响应字典
                response_dict = {'xml': new_dict}

                # 将响应字典转化为字符串类型
                response_xml_str = xmltodict.unparse(response_dict)

                # 将转化得到的字符串给威信服务器
                return response_xml_str

        else:
            return echostr

        """
        在此响应你想响应的数据！！！
        而不是echostr
        以XML的格式响应
        <xml>响应的内容</xml>

        发消息的消息体：
        <xml>
        <ToUserName>< ![CDATA[toUser] ]></ToUserName>
        <FromUserName>< ![CDATA[fromUser] ]></FromUserName>
        <CreateTime>1348831860</CreateTime>
        <MsgType>< ![CDATA[text] ]></MsgType>
        <Content>< ![CDATA[this is a test] ]></Content>
        <MsgId>1234567890123456</MsgId>
        </xml>


        参数	描述
        ToUserName	开发者微信号
        FromUserName	发送方帐号（一个OpenID）
        CreateTime	消息创建时间 （整型）
        MsgType	text
        Content	文本消息内容
        MsgId	消息id，64位整型

        xml是字符串的形式
        若要提取其中的消息应该字符串截取使用库xmltodict
        将xml字符串形式转化为python中的字典

        unparse将字典转化为字符串形式

        """

    return "" # 服务器不可用

if __name__ == '__main__':
    app.run(debug=True, port=8005)
