#!/usr/bin/python3
#coding=utf-8
import json
import requests
import datetime
class iciba:

    def get_weather(self,city):
        url = f'http://wthrcdn.etouch.cn/weather_mini?city={city}'
        response = requests.get(url).json()
        results = response['data']['forecast'][0]
        return f"\n\n\n亲爱的喵喵琪琪子(◍•ᴗ•◍)：\n今天{city}的天气是{results['type']}，最{results['high'][:-1]}度，最{results['low'][:-1]},Ծ‸Ծ,,"
        
    # 初始化
    def __init__(self, wechat_config):
        self.appid = wechat_config['appid']
        self.appsecret = wechat_config['appsecret']
        self.template_id = wechat_config['template_id']
        self.access_token = ''

    # 获取access_token
    def get_access_token(self, appid, appsecret):
        url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (str(appid), str(appsecret))
        r = requests.get(url)
        data = json.loads(r.text)
        access_token = data['access_token']
        self.access_token = access_token
        return self.access_token

    # 获取用户列表
    def get_user_list(self):
        if self.access_token == '':
            self.get_access_token(self.appid, self.appsecret)
        access_token = self.access_token
        url = 'https://api.weixin.qq.com/cgi-bin/user/get?access_token=%s&next_openid=' % str(access_token)
        
        r = requests.get(url)
        return json.loads(r.text)

    # 发送消息
    def send_msg(self, openid, template_id, everyday_words,weather,aday,bday):
        msg = {
            'touser': openid,
            'template_id': template_id,
            'url': 'vveg26.github.io',
            'data': {
                'everyday_words': {
                    'value': everyday_words,
                    'color': '#FFA500'
                    },
                'aday': {
                    'value': aday,
                    'color': '#C8E5ED'
                },
                'bday': {
                    'value': bday,
                    'color': '#feeeed'
                },               
                'weather': {
                    'value': weather,
                }
            }
        }
        json_data = json.dumps(msg)
        if self.access_token == '':
            self.get_access_token(self.appid, self.appsecret)
        access_token = self.access_token
        url = 'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=%s' % str(access_token)
        r = requests.post(url, json_data)
        return json.loads(r.text)


    def get_line(self):
        url = 'https://v2.jinrishici.com/one.json?client=browser-sdk/1.2&X-User-Token=BKN5S7uBsT1%2B1lHyscjY3CZh9rq5a1Dw'
        response = requests.get(url)
        return (f'每日一句：{response.json()["data"]["content"]}')
    # 为设置的用户列表发送消息
    def send_everyday_words(self, openids):
        #everyday_words = self.get_iciba_everyday()
        everyday_words = self.get_line()
        weather = self.get_weather('海宁')
        annor_days = '\n\n'+'殷琪琪破壳也已经'+str((datetime.datetime.today()-datetime.datetime(2020,11,3)).days)+'天了，哇哦，太牛啦鼓掌，鼓掌！ʕु•̫͡•ʔु ✧ '
        birth_days = '\n\n\n'+'你知道殷琪琪和峰峰子已经相恋了'+str((datetime.datetime.today()-datetime.datetime(2002,1,16)).days)+'日子了吗？'
        for openid in openids:
            result = self.send_msg(openid, self.template_id, everyday_words,weather,annor_days,birth_days)
            if result['errcode'] == 0:
                print (' [INFO] send to %s is success' % openid)
                #print(weather)
            else:
                print (' [ERROR] send to %s is error' % openid)

    # 执行
    def run(self, openids=[]):
        if openids == []:
            # 如果openids为空，则遍历用户列表
            result = self.get_user_list()
            openids = result['data']['openid']
        # 根据openids对用户进行群发
        self.send_everyday_words(openids)


if __name__ == '__main__':
    # 微信配置
    wechat_config = {
        'appid': 'xxxxxxxxxxx', #(No.1)此处填写你的appid
        'appsecret': 'xxxxxxxxxxxx', #(No.2)此处填写你的appsecret
        'template_id': 'xxxxxxxxxxxxxxxxxxxx' #(No.3)此处填写你的模板消息ID
    }
    
    # 用户列表
    openids = [
        'xxxxxxxxxx', #(No.4)此处填写你的微信号（微信公众平台上你的微信号）
        #'xxxxx', #如果有多个用户也可以
        #'xxxxx',
    ]

    
    # 执行
    icb = iciba(wechat_config)

    # run()方法可以传入openids列表，也可不传参数
    # 不传参数则对微信公众号的所有用户进行群发
    icb.run()


