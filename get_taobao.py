import os
import asyncio
from pyppeteer import launch
import datetime
import time
import random
# from exe_js import js1, js2, js3, js4, js5
# from alifunc import mouse_slide, input_time_random

width, height = 1366, 768

# ==== 设定账号密码 （修改此处，指定账号密码）====
USERNAME = '888'
PASSWORD = '8888'

# ==== 设定抢购时间 （修改此处，指定抢购时间点）====
BUY_TIME = '2020-02-28 22:10:30'
buy_time_object = datetime.datetime.strptime(BUY_TIME, '%Y-%m-%d %H:%M:%S')

now_time = datetime.datetime.now()
if now_time > buy_time_object:
    print("当前已过抢购时间，请确认抢购时间是否填错...")
    exit(0)

async def main():
    url = 'https://login.taobao.com/member/login.jhtml'
    browser = await launch(
        headless=False,  #设置pyppeteer为有头模式
        args=[f'--window-size={width},{height}', '--disable-infobars']  #设置网页大小，无监控头
    )
    #在浏览器上创建新页面
    page = await browser.newPage()
    await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36')
    await page.setViewport({'width': width, 'height': height})
    await page.goto(url)
    await page.evaluate(
        '''() =>{ Object.defineProperties(navigator,{ webdriver:{ get: () => false } }) }'''
    )
    # await page.evaluate(js2)
    # await page.evaluate(js3)
    # await page.evaluate(js4)
    # await page.evaluate(js5)
    time.sleep(1)

    await page.click('i#J_Quick2Static')
    #username =
    await page.type('input#TPL_username_1', USERNAME)
    #password =
    await page.type('input#TPL_password_1', PASSWORD)
    time.sleep(2)

    await page.click('button#J_SubmitStatic')
    await asyncio.sleep(2)
    await wait(page)
    await asyncio.sleep(2)
    await buy(page)
    await asyncio.sleep(100)

async def buy(page):
    await page.goto('https://cart.taobao.com/cart.htm')
    await asyncio.sleep(1)

    if await page.J("div#J_SelectAll1"):
        all = await page.J("div#J_SelectAll1")
        await all.click()
        print("已经选中购物车中全部商品 ...")

    await asyncio.sleep(1)

    submit_succ = False
    retry_submit_time = 1
    while True:
        now = datetime.datetime.now()
        if now >= buy_time_object:
            print('到达抢购时间，开始执行抢购...尝试次数' + str(retry_submit_time))
            if submit_succ:
                print('订单提交成功...')
                break
            if retry_submit_time > 50:
                print('超过次数，放弃尝试...')
                break

            retry_submit_time += 1

            try:
                if await page.J('a#J_Go'):
                    a = await page.J('a#J_Go')
                    await a.click()
                    print('点击结算按钮')
                    await asyncio.sleep(1)

                    click_submit_time = 1
                    while True:
                        try:
                            if click_submit_time < 10:
                                b = await page.J('a.go-btn')
                                await b.click()
                                print('已经点击提交订单按钮')
                                await asyncio.sleep(1)
                                submit_succ = True
                                break
                            else:
                                print('提交订单失败')
                        except Exception as ee:
                            print('未发现提交订单按钮，重试')
                            click_submit_time += 1
                            time.sleep(0.1)
            except Exception as e:
                print(e)
                print('挂了，提交订单失败')
        await asyncio.sleep(0.1)

async def wait(page):
    print("当前距离抢购时间点还有较长时间，开始定时刷新防止登录超时...")
    while True:
            currenTime = datetime.datetime.now()
            if (buy_time_object - currenTime).seconds > 180:
                await page.goto('https://cart.taobao.com/cart.htm')
                print((buy_time_object - currenTime).seconds)
                print("刷新购物车界面，防止登录超时...")
                await asyncio.sleep(60)
            else:
                print((buy_time_object - currenTime).seconds)
                break

asyncio.get_event_loop().run_until_complete(main())


