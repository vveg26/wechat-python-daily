#!/usr/bin/python3
#coding=utf-8
import json
import os
import requests
import datetime
import time
import schedule
class iciba:




    #获取两个日期的时间
    def get_days(self,date):
        date_old=datetime.datetime.strptime(date[0:10],"%Y-%m-%d")
    
        date_today=datetime.datetime.today()
        num=(date_today-date_old).days
        return num
#计算还有多少天生日(生日\今天\生日月\生日天)
    def how_long(self,str1):
        try:
    #获取当前年月日(单个)
    #将年月日连接起来，使其成为完整的时间(例：2022 - 03 -27)
            todaynow = time.strftime("%Y-%m-%d",time.localtime())
            toyear = time.strftime('%Y',time.localtime(time.time()))    #"%Y"将被无世纪的年份锁代替
            tomon = time.strftime('%m',time.localtime(time.time()))
            today = time.strftime('%d',time.localtime(time.time()))
            toyear = int(toyear)
            tomon = int(tomon)
            today = int(today)

            #明年的今天
            mon = str1.split('-', 3)[1]
            day = str1.split('-', 3)[2]
            next_year = int(toyear) + 1
            str3 = str(next_year) + "-" + str(mon) + "-" + str(day)
            str4 = str(int(toyear)) + "-" + str(mon) + "-" + str(day)
            date2 = datetime.datetime.strptime(todaynow[0:10], "%Y-%m-%d")  #今天
            date3 = datetime.datetime.strptime(str3[0:10], "%Y-%m-%d")     #明年生日=今年年份+1 +生日的月日
            date4 = datetime.datetime.strptime(str4[0:10], "%Y-%m-%d")    #今年的年+生日的月日
            num = 0
            mon = int(mon)
            day = int(day)
            #明年
            #今天过生日:月日相等
            if mon == tomon:
                if day == today:
                    #print("今天过生日，祝你生日快乐")
                    num = 0
                if day > today:
                    #print("这个月过生日")
                    num = (date4 - date2).days
    
                if day < today:
                    #print("生日这个月已过")
                    num = (date3 - date2).days
            #已经过了的生日:明年生日-今天
            elif mon < tomon:
                #print("今年生日已经过了")
                num = (date3 - date2).days
            #还没过生日:今年的年+生日的月日 - 今天的年月日
            else:
                #print("今年的生日还没到")
                num = (date4 - date2).days                      #返回的全部是非0的整数
        except ValueError as e:
            #print("请输入正确的日期，一个月只有适合的天数 " + e)
            print("程序结束...")
        return num


    def get_weather(self,city):
        url = f'http://wthrcdn.etouch.cn/weather_mini?city={city}'
        response = requests.get(url).json()
        results = response['data']['forecast'][0]
       
        return results

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
    def send_msg(self, openid, template_id, datas):
        msg = {
            'touser': openid,
            'template_id': template_id,
            'url': 'vveg26.github.io',
            'data': {
                'words': {
                    'value': datas['words'],
                    'color': '#FFA500'
                    },
                'aday': {
                    'value': datas['annor_days'],
                    'color': '#C8E5ED'
                },
                'bday': {
                    'value': datas['birth_days'],
                    'color': '#feeeed'
                },
                'taday': {
                    'value': datas['to_annordays'],
                    'color': '#C8E5ED'
                },
                'tbday': {
                    'value': datas['to_birthdays'],
                    'color': '#feeeed'
                },               
                'weather': {
                    'value': datas['weather']['type'],
                    'color' : '#99cc33'
                },
                'high_temp': {
                    'value': datas['weather']['high'],
                    'color' : '#69AB5'
                },
                'low_temp': {
                    'value': datas['weather']['low'],
                    'color' : '#0197d2'
                },
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
        return (f'{response.json()["data"]["content"]}')
    # 为设置的用户列表发送消息
    def send_everyday_words(self, openids):
        city = info['city']
        datas = {
            'name' : info['name'],
            'city' : info['city'],
            'words' : self.get_line(),
            'weather' : self.get_weather(city),
            'annor_days' : self.get_days(info['annorday']),
            'birth_days' : self.get_days(info['birthday']),
            'to_annordays' : self.how_long(info['annorday']),
            'to_birthdays' : self.how_long(info['birthday'])
        }


        for openid in openids:
            result = self.send_msg(openid, self.template_id, datas)
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
        # 系统变量
    APPID = os.environ['APPID']
    APPSECRET = os.environ['APPSECRET']
    TEMPLATEID = os.environ['TEMPLATEID']
    OPENID = os.environ['OPENID']
    CITY = os.environ['CITY']
    NAME = os.environ['NAME']
    ANNORDAY = os.environ['ANNORDAY']
    BIRTHDAT = os.environ['BIRTHDAT']
    wechat_config = {
        'appid': APPID, #(No.1)此处填写你的appid
        'appsecret': APPSECRET, #(No.2)此处填写你的appsecret
        'template_id': TEMPLATEID #(No.3)此处填写你的模板消息ID
        
    }
    

    # 用户列表
    openids = [
        OPENID, #(No.4)此处填写你的微信号（微信公众平台上你的微信号）
        #'xxxxx', #如果有多个用户也可以
        #'xxxxx',
    ]

    # Info
    info = {
        'city' : CITY, #城市
        'name' : NAME,    #姓名
        'annorday': ANNORDAY, #恋爱纪念日
        'birthday':BIRTHDAT #生日
    }
    #主方法
    def main():
        # 执行
        icb = iciba(wechat_config)

        # run()方法可以传入openids列表，也可不传参数
        # 不传参数则对微信公众号的所有用户进行群发
        icb.run()
    
    #首次运行直接执行一次，次日九点半执行
    main()

    # schedule.every().day.at("09:30").do(main)
    # #schedule.every(10).seconds.do(main)
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)



