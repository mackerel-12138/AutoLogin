# AutoLogin
自用自动签到脚本，使用青龙面板

## 98堂/色花堂
1. 青龙面板安装依赖
   - Python3:
      - webdriver_manager
      - selenium
      - retrying
      - requests
      - numpy
   - Linux:
      - chromium-chromedriver
      - chromium

2. 设置环境变量
    - sehua_username: 用户名
    - sehua_password: 密码
    - sehua_url: 98堂地址 www.sehuatang.org
    - proxy: 代理地址，比如 http://192.168.1.1:7890
    - sehua_reply: 每日回帖回复词，逗号分隔
    - ua: 浏览器ua

## FnOS飞牛论坛
### 在不常用的地址登录可能需要输验证码，暂不支持
1. 青龙面板安装依赖
   - Python3:
      - webdriver_manager
      - selenium
      - retrying
      - requests
      - numpy
   - Linux:
      - chromium-chromedriver
      - chromium

2. 设置环境变量
    - fnclub_username: 用户名
    - fnclub_password: 密码
    - fnclub_url: 论坛地址 club.fnnas.com
    - ua: 浏览器ua