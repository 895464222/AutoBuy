# AutoBuy
淘宝等网站抢购脚本
==
两个版本：

        _pyppeteer_是用的pyppeteer异步渲染的方式写的，可以绕过淘宝webdriver检测，指定账号密码进行模拟登录，然后输入时间可以到时间抢购
----------------

        _selenium_使用selenium的，试了一下用扫码登录的方式，减少webdriver检测的风险，也是定时抢购
-------------------

_pyppeteer_
          --get_taobao.py 主程序：
          ==== 设定账号密码 （修改此处，指定账号密码）====
                                 
                                 USERNAME = '888'
                                 
                                 PASSWORD = '8888'
                                 
                                 BUY_TIME = '2020-02-28 22:10:30'
                                 
            wait（）方法的功能是定时刷新防止登陆超时，当当前时间-抢购时间>180时每60s刷新一次
                                 
            buy（）方法是跳到购物车界面，用click事件点击全选，然后开始循环结算，待页面跳转点击提交失败就会重试，上限50次
                                 
            main（）作用是运行js，修改webdriver的值为false，从而避开检测，之后模拟登入后先调用wait（page），判断时间，再
                                 
           调用buy（page）进行购买

_selenium_
          --sele——taobao.py 主程序：原理与上面差不多
                                 
