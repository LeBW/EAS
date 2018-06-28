import requests
import time

s = requests.Session()
loginURL = 'http://elite.nju.edu.cn/jiaowu/login.do'
codeURL = 'http://elite.nju.edu.cn/jiaowu/ValidateCode.jsp'
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'

# s.headers.update({'User-Agent': user_agent})
valcode = s.get(codeURL)
data = {}
# 将验证码写入文件内
with open('valcode.png', 'wb') as f:
    f.write(valcode.content)

code = input('请输入验证码')
data['ValidateCode'] = code
data['userName'] = 151220048
data['password'] = '3654741Lbw'
data['returnUrl'] = 'null'
# 模拟登陆,获取cookies
r = s.post(loginURL, data)

# 模拟选课
s.headers.update({
    'Accept': 'text/javascript, text/html, application/xml, text/xml, */*',
    'X-Prototype-Version': '1.5.1',
    'Origin': 'http://elite.nju.edu.cn',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': user_agent,
    'Content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Referer': 'http://elite.nju.edu.cn/jiaowu/student/elective/specialityCourseList.do',  # 专业课
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh,en-US;q=0.9,en;q=0.8,zh-CN;q=0.7'
})
del (s.headers['Connection'])
selectCourseURL = 'http://elite.nju.edu.cn/jiaowu/student/elective/selectCourse.do'
# 尝试选课“人工智能”
# selectRequest = s.post(selectCourseURL, data={'method': 'addSpecialitySelect', 'classId': 80413, '-': ''})
# count = 1
# while '班级已满' in selectRequest.text:
#     selectRequest = s.post(selectCourseURL, data={'method': 'addSpecialitySelect', 'classId': 80413, '-': ''})
#     count += 1
#     print(count)
#     time.sleep(3)
# print(selectRequest.text)
