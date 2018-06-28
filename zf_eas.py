import io
import os.path
import threading
import tkinter as tk
import tkinter.messagebox as messagebox

import requests
from PIL import Image, ImageTk
from bs4 import BeautifulSoup
from lxml import etree


def logIn():
    # global userName
    print('start to logIn()')
    valicode = valicodeInput.get()
    selector = etree.HTML(logInRequest.text)
    __VIEWSTATE = selector.xpath('//*[@id="form1"]/input/@value')[0]
    RadioButtonList1 = u"学生".encode('gb2312', 'replace')
    data = {
        '__VIEWSTATE': __VIEWSTATE,
        'hidsc': "",
        'hidPdrs': "",
        'txtUserName': accountInput.get(),
        # 'Textbox1': accountInput.get(),
        'TextBox2': passwordInput.get(),
        'txtSecretCode': valicode,
        'RadioButtonList1': RadioButtonList1,
        'Button1': "",
        'lbLanguage': ""
    }
    # print(__VIEWSTATE)
    # 模拟登陆,获取cookies
    r = s.post(basicURL + "/default2.aspx", data)

    # print(r.text)
    if '验证码错误' in r.text:
        messagebox.showinfo('Error', '验证码错误')

    elif '密码错误' in r.text:
        messagebox.showinfo('Error', '账号或密码错误')
        return
    soup = BeautifulSoup(r.text, "lxml")
    name = soup.find(id='xhxm').string[:-2]
    print("欢迎您: ", name)
    userName.set(name)
    # 模拟选课UI出现
    accountFrame.pack_forget()
    passwordFrame.pack_forget()
    valicodeFrame.pack_forget()
    okButton.pack_forget()

    # optionMenu.pack()
    hintCourseNumberLabel.pack()
    inputCourseFrame.pack()
    userNameLabel.pack()

    # 为选课做初始化准备
    init_for_select()


def init_for_select():
    global queryDict
    global courseListURL
    global __VIEWSTATE
    global courseListRequest

    courseListURL = os.path.join(basicURL, xklx)
    s.headers.update({
        "Upgrade-Insecure-Requests": "1",
        "Referer": basicURL + "/xs_main.aspx?xh=" + accountInput.get(),
    })
    # s.cookies.set()
    queryDict = {
        'xh': accountInput.get(),
        'xm': "",  # userName.encode('gb2312', 'replace'),
        'gnmkdm': gnmkdm,
    }
    courseListRequest = s.get(courseListURL, params=queryDict)
    # print(courseListRequest.text)
    selector = etree.HTML(courseListRequest.text)
    __VIEWSTATE = selector.xpath('//*[@id="xsyxxxk_form"]/input/@value')[2]  # TODO: form在这改
    # print(len(__VIEWSTATE))
    # 进行余量修改，获得真正的VIEWSTATE
    courseListRequest = s.post(courseListURL, params=queryDict, data={
        '__EVENTTARGET': "ddl_ywyl",
        '__EVENTARGUMENT': "",
        '__VIEWSTATE': __VIEWSTATE,
        'ddl_ywyl': "",
        'ddl_xqbs': "1",
    })
    selector = etree.HTML(courseListRequest.text)
    __VIEWSTATE = selector.xpath('//*[@id="xsyxxxk_form"]/input/@value')[2]
    # print(len(__VIEWSTATE))
    # 1页85条记录，呈现所有
    courseListRequest = s.post(courseListURL, params=queryDict, data={
        '__EVENTTARGET': "dpkcmcGrid:txtPageSize",
        '__EVENTARGUMENT': "",
        '__VIEWSTATE': __VIEWSTATE,
        'ddl_ywyl': "",
        'ddl_xqbs': "1",
        'dpkcmcGrid:txtChoosePage': "1",
        'dpkcmcGrid:txtPageSize': '85',
    })
    selector = etree.HTML(courseListRequest.text)
    __VIEWSTATE = selector.xpath('//*[@id="xsyxxxk_form"]/input/@value')[2]

    s.headers.update({
        "Cache-Control": "max-age=0",
        "Origin": os.path.split(basicURL)[0],
        "Upgrade-Insecure-Requests": "1",
        "Content-Type": "application/x-www-form-urlencoded",
        "Referer": courseListRequest.url,

    })
    # print(len(__VIEWSTATE))


def start():
    global is_stop
    is_stop = False

    progressHintLabel.pack()
    countLabel.pack()
    stopButton.pack()

    t = threading.Thread(target=grab_course, name='grabCourseThread', daemon=True)
    t.start()


def stop():
    global is_stop
    is_stop = True


def grab_course():
    global queryDict
    global courseListURL
    global __VIEWSTATE
    global courseListRequest

    course_number = courseNumberInput.get()
    print("start to grab course: ", course_number)
    # s.cookies.set("tabId", "1")
    # TODO: 选什么课，第几页，可以在这里修改
    data = {
        '__EVENTTARGET': "",
        '__EVENTARGUMENT': "",
        '__VIEWSTATE': __VIEWSTATE,
        'ddl_xqbs': "1",
        'dpkcmcGrid:txtChoosePage': "1",
        'Button1': u'  提交  '.encode('gb2312', 'replace'),

        'kcmcGrid:_ctl' + course_number + ':xk': "on",
        # 'kcmcGrid:_ctl12:xk': "on",
        # 'kcmcGrid:_ctl13:xk': "on",
        # 'kcmcGrid:_ctl14:xk': "on",
        # 'kcmcGrid:_ctl12:xk': "on",
    }
    current_count = 1
    count.set(current_count)
    select_request = s.post(courseListURL, params=queryDict, data=data)
    temp_string = select_request.content.decode(encoding="gb2312")[:100]
    print(temp_string)
    while not is_stop:
        try:
            select_request = s.post(courseListURL, params=queryDict, data=data)
            temp_string = select_request.content.decode(encoding="gb2312")[:200]
            print("courseNumber: " + course_number, temp_string)
            current_count += 1
            # print(currentCount)
            count.set(current_count)

            if "上限" in temp_string:
                break
        except Exception as error:
            print(error)
            pass
    print("End: ", temp_string)


# 初始化部分
s = requests.Session()
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36'
basicHeaders = {
    'User-Agent': user_agent,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh,en-US;q=0.9,en;q=0.8,zh-CN;q=0.7'
}
s.headers.update(basicHeaders)

global __VIEWSTATE
global courseListURL
global courseListRequest
global queryDict
global is_stop
# global userName
is_stop = False

# TODO: 需要修改的东西
basicURL = 'http://119.145.67.59//'
title = "Get courses (正方)"
gnmkdm = "N121203"
xklx = "xf_xsqxxxk.aspx"
formID = "xsyxxxk_form"  # 起提示作用，form在这里更改无效

# UI部分
root = tk.Tk()

root.title(title)

width, height = 400, 200
root.geometry(
    "%dx%d+%d+%d" % (width, height, (root.winfo_screenwidth() - width) / 2, (root.winfo_screenheight() - height) / 2))

root.maxsize(width, height)
root.minsize(width, height)
##账号
accountFrame = tk.Frame(root)
accountHintLabel = tk.Label(accountFrame, text="账号")
accountInput = tk.Entry(accountFrame)
# accountInput.insert(0, '415173447') #TODO:
accountHintLabel.pack(side=tk.LEFT)
accountInput.pack(side=tk.RIGHT)
accountFrame.pack()
##密码
passwordFrame = tk.Frame(root)
passwordHintLabel = tk.Label(passwordFrame, text="密码")
passwordInput = tk.Entry(passwordFrame, show='*')
# passwordInput.insert(0, 'cqh001008') #TODO:
passwordHintLabel.pack(side=tk.LEFT)
passwordInput.pack(side=tk.RIGHT)
passwordFrame.pack()

valicodeFrame = tk.Frame(root)
hintValicodeLabel = tk.Label(valicodeFrame, text="验证码")
hintValicodeLabel.pack(side=tk.LEFT)
valicodeInput = tk.Entry(valicodeFrame, width=10)
valicodeInput.pack(side=tk.LEFT)

# 验证码界面
logInRequest = s.get(basicURL)
basicURL = logInRequest.url
basicURL = os.path.split(basicURL)[0]
codeURL = os.path.join(basicURL, 'CheckCode.aspx')
print(codeURL)
try:
    rawData = s.get(codeURL)
except requests.exceptions.RequestException as e:
    messagebox.showinfo('Error', e)
    exit(1)
image = Image.open(io.BytesIO(rawData.content))
tkImage = ImageTk.PhotoImage(image)
valicodeLabel = tk.Label(valicodeFrame, image=tkImage)
valicodeLabel.pack(side=tk.LEFT)
valicodeFrame.pack()

okButton = tk.Button(root, text='确认', command=logIn)
okButton.pack()
# 课程选择界面
courseClass = tk.StringVar(root)
courseClass.set("通识课")
optionMenu = tk.OptionMenu(root, courseClass, "通识课", "公选课", "体育课", "阅读课(自然)")

hintCourseNumberLabel = tk.Label(root, text='请输入课程编号')

inputCourseFrame = tk.Frame(root)
courseNumberInput = tk.Entry(inputCourseFrame)
courseNumberInput.pack(side=tk.LEFT)
startButton = tk.Button(inputCourseFrame, text='确认', command=start)
startButton.pack(side=tk.RIGHT)

progressHintLabel = tk.Label(root, text='正在抢课中...')

count = tk.IntVar()
countLabel = tk.Label(root, textvariable=count)

userName = tk.StringVar(root)
userNameLabel = tk.Label(root, textvariable=userName)

stopButton = tk.Button(root, text="停止", command=stop)

'''
accountFrame.pack_forget()
passwordFrame.pack_forget()
valicodeFrame.pack_forget()
okButton.pack_forget()

#optionMenu.pack()
hintCourseNumberLabel.pack()
inputCourseFrame.pack()
'''

root.mainloop()
