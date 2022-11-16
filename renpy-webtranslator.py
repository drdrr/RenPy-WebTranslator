import time
import re
import random
import time
from selenium.common.exceptions import SessionNotCreatedException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from sys import argv, exit
import atexit

def caiyun(fileName):
    browser.get('https://fanyi.caiyunapp.com/')
    print('等待网页加载...')
    time.sleep(5)
    ActionChains(browser).move_by_offset(0, 0).click().perform()
    inputArea = browser.find_element_by_class_name('textinput')
    #fileName = 'Translate-' + time.strftime("%Y-%m-%d_%H.%M.%S", time.localtime()) + '.rpy'
    result = open(fileName, 'w', encoding='utf-8')
    lines = 0

    for line in open('trans.txt', encoding='utf-8', errors='ignore'):
        lines += 1
        if not ('old "' in line or 'translate ' in line or '# ' in line or line == '\n'):  #识别需要翻译的内容
            rawtext = re.search(r'"(.*)"', line).group().strip('"') #提取需要翻译的内容
            #rawtext = re.search(r'"(.*?)(?<![^\\\\]\\\\)"', line).group().strip('"')  #提取需要翻译的内容
            if not rawtext == '': #如果这一句有内容则翻译
                inputArea.send_keys(rawtext)
                xpath = '//*[@id="texttarget"]/div/span'
                try:
                    WebDriverWait(browser, 15).until(lambda broswer: browser.find_element_by_xpath(xpath))  #等待翻译结果，超时15秒
                    text = browser.find_element_by_xpath(xpath)
                    line = line.replace(rawtext, text.text)
                except Exception as e: #如果超时则不替换，直接写入原句
                    print(e)
                time.sleep(random.uniform(0,1))  #设置随机等待时间，防止触发反bot机制

            try:
                #browser.find_element_by_class_name('text-delete').click()  #试图通过叉键清空
                inputArea.click()
                inputArea.send_keys(Keys.CONTROL, 'a')
                inputArea.send_keys(Keys.BACKSPACE)
            except:
                inputArea.clear()  #否则直接清空输入框
            time.sleep(2)  #等待清空延迟

        print(str(lines)+"   "+line, end='')
        result.write(line)
        result.flush()

def youdao(fileName):
    browser.get('https://fanyi.youdao.com/')
    print('等待网页加载...')
    time.sleep(3)
    inputArea = browser.find_element_by_id('inputOriginal')
    #fileName = 'Translate-' + time.strftime("%Y-%m-%d_%H.%M.%S", time.localtime()) + '.rpy'
    result = open(fileName, 'w', encoding='utf-8')
    lines = 0

    for line in open('trans.txt', encoding='utf-8', errors='ignore'):
        lines += 1
        if not ('old "' in line or 'translate ' in line or '# ' in line or line == '\n'):  #识别需要翻译的内容
            rawtext = re.search(r'"(.*)"', line).group().strip('"') #提取需要翻译的内容
            if not rawtext == '': #如果这一句有内容则翻译
                inputArea.send_keys(rawtext)
                xpath = '//div[@id=\'transTarget\']/p[1]/span'
                try:
                    WebDriverWait(browser, 15).until(lambda broswer: browser.find_elements_by_xpath(xpath))  #等待翻译结果，超时15秒
                    text = browser.find_elements_by_xpath(xpath)
                    joinedtext = ''
                    for index in range(len(text)):
                        joinedtext += text[index].text
                    if joinedtext != '':
                        line = line.replace(rawtext, joinedtext)
                except: #如果超时则不替换，直接写入原句
                    pass
                time.sleep(random.uniform(0,1))  #设置随机等待时间，防止触发反bot机制
            try:
                browser.find_element_by_class_name('input__original_delete').click() #试图通过叉键清空
            except:
                inputArea.clear()  #否则直接清空输入框
            time.sleep(1)  #等待清空延迟

        print(str(lines)+"   "+line, end='')
        result.write(line)
        result.flush()


def deepl(fileName): #DeepL的翻译显示和彩云不同，并不是翻译完了才显示在结果框内，因此不能用wait until
    browser.get('https://www.deepl.com/translator')
    print('等待网页加载...')
    time.sleep(5)
    inputArea = browser.find_element_by_class_name('lmt__textarea.lmt__source_textarea.lmt__textarea_base_style')
    #fileName = 'Translate-' + time.strftime("%Y-%m-%d_%H.%M.%S", time.localtime()) + '.rpy'
    result = open(fileName, 'w', encoding='utf-8')
    lines = 0

    for line in open('trans.txt', encoding='utf-8', errors='ignore'):
        lines += 1
        if not ('old "' in line or 'translate ' in line or '# ' in line or line == '\n'):
            rawtext = re.search(r'"(.*)"', line).group().strip('"')
            if not rawtext == '':
                inputArea.send_keys(rawtext)
                time.sleep(random.uniform(8,10)) #等待翻译结果，可根据网络调整间隔时间
                text = browser.find_element_by_id('target-dummydiv').get_attribute('innerHTML').strip('\r\n')
                line = line.replace(rawtext, text)
            inputArea.clear()
        print(str(lines)+"   "+line, end='')
        result.write(line)
        result.flush()


if __name__ == "__main__":

    file_name = argv[1] if len(argv) > 1 else 'Translate-' + time.strftime("%Y-%m-%d_%H.%M.%S", time.localtime()) + '.rpy'
    options = webdriver.ChromeOptions()
    options.add_argument("window-size=1920x1080")
    #options.add_argument('headless')  #这两个选项可以关闭窗口显示
    #options.add_argument("disable-gpu")

    time_start = time.time()
    print("RenPy翻译文件机翻工具")
    print("By Koshiro, version 1.4")
    print("使用前请确认待翻译文件trans.txt已放在本目录")
    while True:
        translator = input("\n选择翻译引擎：1 彩云小译 / 2 有道翻译 / 3 DeepL\n （1/2/3？回车确定）\n> ").strip(' ')
        if translator in ['1', '2', '3']:
            break
    print("正在启动chromedriver...")
    try:
        browser = webdriver.Chrome(r'chromedriver.exe', options=options)
    except SessionNotCreatedException as err:
        print("\nchromedriver版本不对，请到 https://registry.npmmirror.com/binary.html?path=chromedriver/ 下载对应版本（Chrome版本信息如下）\n", err)
        input()
        exit(1)
    


    if translator == '1':
        caiyun(file_name)
    elif translator == '2':
        youdao(file_name)
    else:
        deepl(file_name)

    browser.quit()
    browser.stop_client()
    time_end = time.time()
    print("生成完毕，耗时{:.0f}min".format((time_end - time_start)/60))
    input("按回车键退出")
