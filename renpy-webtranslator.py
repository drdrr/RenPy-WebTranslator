import time
import re
import random
import time
from selenium.common.exceptions import SessionNotCreatedException
from selenium import webdriver

def caiyun():
    browser.get('https://fanyi.caiyunapp.com/')
    print('等待网页加载...')
    time.sleep(5)
    inputArea = browser.find_element_by_class_name('textinput')

    fileName = 'Translate-' + time.strftime("%Y-%m-%d_%H.%M.%S", time.localtime()) + '.txt'
    result = open(fileName, 'w', encoding='utf-8')
    lines = 0

    for line in open('trans.txt', encoding='utf-8', errors='ignore'):
        lines += 1
        if not ('old "' in line or 'translate ' in line or '# ' in line or line == '\n'):
            rawtext = re.search(r'"(.*?)(?<![^\\\\]\\\\)"', line).group().strip('"')
            inputArea.send_keys(rawtext)
            time.sleep(random.uniform(3,5)) #可根据网络调整间隔时间
            xpath = '//div[@id=\'texttarget\']/p[1]/span'
            text = browser.find_element_by_xpath(xpath)
            cookedtext = line.replace(rawtext, text.text)
            print(str(lines)+"   "+cookedtext)
            result.write(cookedtext)
            result.write('\n')
            result.flush()
            inputArea.clear()
        else:
            print(str(lines)+"   "+line, end='')
            result.write(line)
            result.flush()

def youdao():
    browser.get('https://fanyi.youdao.com/')
    print('等待网页加载...')
    time.sleep(3)
    inputArea = browser.find_element_by_id('inputOriginal')
    fileName = 'Translate-' + time.strftime("%Y-%m-%d_%H.%M.%S", time.localtime()) + '.txt'
    result = open(fileName, 'w', encoding='utf-8')
    lines = 0

    for line in open('trans.txt', encoding='utf-8', errors='ignore'):
        lines += 1
        if not ('old "' in line or 'translate ' in line or '# ' in line or line == '\n'):
            rawtext = re.search(r'"(.*?)(?<![^\\\\]\\\\)"', line).group().strip('"')
            inputArea.send_keys(rawtext)
            time.sleep(random.uniform(3,5)) #可根据网络调整间隔时间
            xpath = '//div[@id=\'transTarget\']/p[1]/span'
            text = browser.find_elements_by_xpath(xpath)
            joinedtext = ''
            for index in range(len(text)):
                joinedtext += text[index].text
            if joinedtext != '':
                cookedtext = line.replace(rawtext, joinedtext)
                print(str(lines)+"   "+cookedtext)
                result.write(cookedtext)
                result.write('\n')
            else:
                print(str(lines)+"   "+line, end='')
                result.write(line)
            result.flush()
            inputArea.clear()
        else:
            print(str(lines)+"   "+line, end='')
            result.write(line)
            result.flush()


time_start = time.time()
print("RenPy翻译文件机翻工具")
print("By Koshiro inspired by Mirage, version 1.0")
print("使用前请确认待翻译文件trans.txt已放在本目录")
while True:
    translator = input("\n选择翻译引擎：1 彩云小译 / 2 有道翻译\n （1/2？回车确定）\n> ").strip(' ')
    if translator == '1' or translator == '2':
        break
print("正在启动chromedriver...")
try:
    browser = webdriver.Chrome(r'chromedriver.exe')
except SessionNotCreatedException as err:
    print('\nchromedriver版本不对，请到http://npm.taobao.org/mirrors/chromedriver/ 下载对应版本（Chrome版本信息如下）\n', err)
    quit()
    
if translator == '1':
    caiyun()
else:
    youdao()

browser.quit()
browser.stop_client()
time_end = time.time()
print("生成完毕，耗时{:.0f}秒".format(time_end - time_start))
input('按回车键退出')
