# dvadmin-sms

#### 介绍
一款适用于django-vue-admin基于阿里云、腾讯云、华为云等官方短信服务开发的短信发送插件，快速整合各端的短信服务插件。

## 功能及服务商
### 服务商
- [x] 阿里云短信服务
- [x] 腾讯云短信服务
- [ ] 京东云短信服务
- [ ] 华为云短信服务

### 功能
- [x] 通过手机号码限制短信发送频率
- [ ] 通过IP地址限制短信发送频率
- [x] 发送登录短信验证码
- [ ] 发送语音验证码
- [ ] 发送注册短信验证码
- [ ] 发送变更手机号短信验证码
- [ ] 发送重置密码短信验证码
- [ ] 发送更改密码短信验证码
- [ ] 短信发送记录保存
- [ ] 短信发送记录后台查看记录
- [ ] 后台中控制台卡片展示信息

## 优惠短信包推荐
### 阿里云
[200条/6.9元优惠 点我领取](https://www.aliyun.com/activity/2023caigouji/dysms?source=5176.11533457&userCode=jpef8a71)
[1000条/35元优惠 点我领取](https://www.aliyun.com/activity/2023caigouji/dysms?source=5176.11533457&userCode=jpef8a71)
### 腾讯云
[100条/3.5元优惠 点我领取](https://cloud.tencent.com/act/cps/redirect?redirect=10541&cps_key=b302a514a6688aa30823fac954464e5d)
[1000条/33.5元优惠 点我领取](https://cloud.tencent.com/act/cps/redirect?redirect=10541&cps_key=b302a514a6688aa30823fac954464e5d)

## 安装包

使用pip安装软件包：

~~~python
pip install dvadmin-sms
~~~
### 配置方式一: 一键导入注册配置
在 application / settings.py 插件配置中下导入默认配置
```python
...
from dvadmin_sms.settings import *
```
### 配置方式二: 手动配置
在INSTALLED_APPS 中注册app

~~~python
INSTALLED_APPS = [
    ...
    'dvadmin_sms',
]
~~~

在 application / urls.py 中注册url地址

~~~python
urlpatterns = [
    ...
    re_path(r'api/sms/', include('dvadmin_sms.urls')),
]
~~~

进行迁移及初始化
```python
python3 manage.py makemigrations 
python3 manage.py migrate 
# 注意备份初始化信息
python3 manage.py init -y 
```
