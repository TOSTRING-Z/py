#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import requests
import js2py
import json
import pyperclip
import os
import threading
# from pygame import mixer
import time
from requests.cookies import RequestsCookieJar
from tkinter import *
import tkinter.font as tkFont

path_relative = '/install/git/py/trans_sample'


# 解析json
def for_mat(html_in):
    j = json.loads(html_in)
    try:
        t = '英[{}]\n美[{}]\n'.format(j['dict_result']['simple_means']['symbols'][0]['ph_en'],
                                    j['dict_result']['simple_means']['symbols'][0]['ph_am'])
        t += ';'.join(j['dict_result']['simple_means']['word_means'])
        with open(path_relative + '/json/' + j['trans_result']['data'][0]['src'] + '.json', mode='w',
                  encoding='utf-8') as f:
            f.write(html_in)
    except:
        t = j['trans_result']['data'][0]['dst']
    # it = re.finditer(r'<span [^{^<]+?</span>', html_in)
    text = ''
    # for match in t:
    #     text += (match.group()+'\n')
    return str(t)


# 判断翻译方式
def mo_shi(text):
    it = re.search('[\u4e00-\u9fa5]', text)
    if it != None:
        return ('zh', 'en')
    else:
        return ('en', 'zh')


clip = [pyperclip.paste()]


def fan_yi(event):
    content = text_start.get('1.0', END)

    pubmid_judge = re.findall("(.*?)\[pubmid\]", re.sub('\.', '', content))
    if pubmid_judge:
        params = [{"pmjab": Periodical} for Periodical in pubmid_judge]
        url = 'https://api.pubmedplus.com/v1/pmjournal/impactfactor'
        res = json.loads(requests.post(url, json=params).text)
        text_result.delete('1.0', END)
        text_result.insert(INSERT,
                           "\n".join([f"Periodical:{res[v][p]}\tIF:{res[v][i]}" for v, (p, i) in enumerate(res)]))
    else:
        with open(path_relative + '/www/sign_m.js', 'r', encoding='utf8') as h:
            hash = h.read()

        # 判断模式
        # with open(path_relative+'/www/static.json','r',encoding= 'utf8') as h:
        #     static = json.loads(h.read())
        # pyperclip.paste()
        if event.keycode == 1:
            clip.append(pyperclip.paste())

        # if static["copy"] != i and i != '':
        if clip[-2] != clip[-1]:
            # copy翻译
            # static["copy"] = pyperclip.paste()
            # if event.keycode == 65:
            # static["status"] = "0"
            # t = json.dumps(static)
            # with open(path_relative+'/www/static.json','w', encoding='utf8') as h:
            #    h.write(t)
            content = clip[-1] + " "
            root.wm_attributes('-topmost', 1)  # 锁定窗口置顶
            root.wm_attributes('-topmost', 0)  # 释放窗口置顶

        else:
            # return 0
            if content == "\n":
                # print("return")
                return

        # content = text_start.get('1.0', END)
        content = re.sub('[\s^\n]{2,}', ' ', content)
        content = re.sub('\n{1,}', ' ', content)
        hash = js2py.eval_js(hash)
        sign = hash(content)

        params = {
            'from': mo_shi(content)[0],
            'to': mo_shi(content)[1],
            'query': content,
            'sign': sign,
            'simple_means_flag': '3',
            'token': 'e8b16a6734ac43b19cb93a65b0ff72e9',
            'transtype': 'realtime'
        }
        # 判断是否缓存
        json_name = content.replace(' ', '+')[0:-1]
        i = re.search('\+', json_name)
        text_result.delete('1.0', END)
        for_mat_t = ''
        if len(json_name) < 12 and i == None:
            if os.path.isfile(path_relative + '/json/' + json_name + '.json'):
                with open(path_relative + '/json/' + json_name + '.json', encoding='utf-8') as f:
                    t = f.read()
                    for_mat_t = for_mat(t)
                    text_result.insert(INSERT, for_mat_t)
            else:
                url = 'https://fanyi.baidu.com/v2transapi'
                cookie_jar = RequestsCookieJar()
                cookie_jar.set("BAIDUID", "C47ABF807AA99773882AD9BBFCDDB568:FG=1")
                try:
                    t = requests.post(url, cookies=cookie_jar, data=params).text
                    for_mat_t = for_mat(t)
                    text_result.insert(INSERT, for_mat_t)
                except:
                    # print("not connnect!")
                    return
        else:
            url = 'https://fanyi.baidu.com/v2transapi'
            cookie_jar = RequestsCookieJar()
            cookie_jar.set("BAIDUID", "C47ABF807AA99773882AD9BBFCDDB568:FG=1")
            try:
                t = requests.post(url, cookies=cookie_jar, data=params).text
                for_mat_t = for_mat(t)
                text_result.insert(INSERT, for_mat_t)
            except:
                print("not connnect!")
        # 音频下载
        # mp3_name = json_name
        # if len(re.split('\+',mp3_name)) == 1:
        #     url = 'https://fanyi.baidu.com/gettts?lan='+mo_shi(content)[1]+'&text='+mp3_name+'&spd=3&source=web'
        #     path = path_relative+"/mei_ti/"+mp3_name+".mp3"
        #     try:
        #         if os.path.isfile(path):
        #             mixer.init()
        #             mixer.music.load(path)
        #             mixer.music.play()
        #             time.sleep((len(mp3_name)+5) / 5)
        #             mixer.music.stop()
        #         else:
        #             r = requests.get(url)
        #             if len(json_name)<12 and i == None:
        #                 with open(path, "wb") as f:
        #                     f.write(r.content)
        #             with open(path_relative+"/mei_ti/tem.mp3", "wb") as f:
        #                 f.write(r.content)
        #             mixer.init()
        #             mixer.music.load(path_relative+"/mei_ti/tem.mp3")
        #             mixer.music.play()
        #             time.sleep((len(mp3_name)+5) / 5)
        #             mixer.music.stop()
        #     except Exception as e:
        #         print(e)


# copy翻译消息循环
# def copy_jian_ting():
#     while 1:
#         time.sleep(0.5)
#         class key():
#             keycode = 1
#         fan_yi(key)
# with open(path_relative+'/www/static.json','r',encoding= 'utf8') as h:
# static = json.loads(h.read())
# if static["status"] == "0":
#     break
# print('ok!')
def copy_jian_ting_time(this):
    if this.keysym == 'q':
        copy_thread.pause()
    if this.keysym == 'w':
        copy_thread.resume()
    # print(copy)


root = Tk()
ft = tkFont.Font(family='Fixdsys', size=10, weight=tkFont.NORMAL)
text_start = Text(root, width=50, height=10, font=ft)
text_start.bind("<Control-space>", fan_yi)
text_start.bind("<Control-w>", copy_jian_ting_time)
text_start.bind("<Control-q>", copy_jian_ting_time)
text_result = Text(root, width=50, height=10, font=ft)

text_result.pack(side=BOTTOM)
text_start.pack(side=TOP)

root.title('简单翻译')
root.resizable(0, 0)


# def cpu_limit():
# 		os.system("cpulimit -e python3 -l 50")
#
# def on_closing():
#     os.system("kill -9 `pgrep cpulimit`")
#     #os.system("kill -9 `pgrep python3`")
#     root.destroy()

class Job(threading.Thread):

    def __init__(self, *args, **kwargs):
        super(Job, self).__init__(*args, **kwargs)
        self.flag = threading.Event()  # 用于暂停线程的标识
        self.flag.set()  # 设置为True
        self.running = threading.Event()  # 用于停止线程的标识
        self.running.set()  # 将running设置为True

    def run(self):
        while self.running.isSet():
            self.flag.wait()  # 为True时立即返回, 为False时阻塞直到内部的标识位为True后返回

            class key():
                keycode = 1

            fan_yi(key)
            time.sleep(1)

    def pause(self):
        self.flag.clear()  # 设置为False, 让线程阻塞

    def resume(self):
        self.flag.set()  # 设置为True, 让线程停止阻塞

    def stop(self):
        self.flag.set()  # 将线程从暂停状态恢复, 如何已经暂停的话
        self.running.clear()  # 设置为False


if __name__ == '__main__':
    # os.system("klipper")
    copy_thread = Job()
    copy_thread.start()
    # Thread(target=copy_jian_ting).start()
    # Thread(target=cpu_limit).start()
    # print("主线程开始")
    # root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()
