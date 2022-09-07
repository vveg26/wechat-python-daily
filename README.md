# wechat-python-daily
给女友的每日推送
## 利用GitHubAction实现每日定时发送微信推送
## 使用教程
每天九点定时发送
1. Fork我的仓库
2. 按如下操作填写相应内容
![step1](https://raw.githubusercontent.com/vveg26/ImageHosting/master/BlogImg/202209071709248.png)
![step2](https://raw.githubusercontent.com/vveg26/ImageHosting/master/BlogImg/202209071712529.png)
3. 依次如下添加各个字段

| Name | Value | 说明 |
| ---- | ---- | ---- |
| APPID | xxxxxxxx | vx测试号中获取 |
| APPSECRET | xxxxxxxx | vx测试号中获取 |
| TEMPLATEID | xxxxxxx | vx测试号中获取|
| OPENID | xxxxxxxxx | vx测试号中获取 |
| CITY | 上海 | 自己的地区 |
| NAME | 琪琪 | 名字 |
| ANNORDAY | 2020-11-3 | 纪念日 |
| BIRTHDAT | 2002-01-16 | 生日 |


4. 点击Action，之后开启Action
![](https://raw.githubusercontent.com/vveg26/ImageHosting/master/BlogImg/202209071720479.png)
5. 可以修改.github/workflow/main.yaml中的文件自己修改高级内容，第一次运行可以随意修改一下,即可发送一次
## 也可实现邮件发送（联系我）
