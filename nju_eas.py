import requests
import time
import configparser

from bs4 import BeautifulSoup


class NJUEas:
    """NJU Educational Administration System.

    Provides some operations such as grabbing course on NJU Educational Administration System.
    """

    def __init__(self):
        self.s = requests.Session()
        self.login_url = 'http://elite.nju.edu.cn/jiaowu/login.do'
        self.code_url = 'http://elite.nju.edu.cn/jiaowu/ValidateCode.jsp'
        self.select_course_url = 'http://elite.nju.edu.cn/jiaowu/student/elective/selectCourse.do'
        self.renew_course_url = 'http://elite.nju.edu.cn/jiaowu/student/elective/courseList.do'
        self.user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                          'Chrome/63.0.3239.132 Safari/537.36 '
        # 0: 通识补选 1: 公选补选 2: 体育补选 3: 阅读补选 4: 专业选课
        self.course_types = ['submitDiscussRenew', 'submitPublicRenew', 'addGymSelect', 'readRenewCourseSelect', 'addSpecialitySelect']

    def __get_val_code(self):
        val_code = self.s.get(self.code_url)
        with open('val_code.png', 'wb') as f:
            f.write(val_code.content)

    def log_in(self):
        config = configparser.ConfigParser()
        config.read('nju_eas.ini')
        try:
            username = config['account']['username']
            password = config['account']['password']
        except KeyError:
            username = input('请输入用户名: ')
            password = input('请输入密码: ')
        self.__get_val_code()
        code = input('请输入验证码: ')
        data = {'returnUrl': 'null', 'userName': username, "password": password, 'ValidateCode': code}
        # log in
        r = self.s.post(self.login_url, data)
        soup = BeautifulSoup(r.text, 'lxml')
        print(soup.find(id='UserInfo').text)

    def grab_course(self):
        while True:
            course_type = input('请输入课程类型(0: 通识补选 1: 公选补选 2: 体育补选 3: 阅读补选 4: 专业选课): ')
            try:
                course_type = int(course_type)
                method = self.course_types[course_type]
                break
            except ValueError or IndexError:
                print('请重新输入：')

        course_number = input('请输入课程编号: ')
        headers = {
            'Accept': 'text/javascript, text/html, application/xml, text/xml, */*',
            'X-Prototype-Version': '1.5.1',
            'Origin': 'http://elite.nju.edu.cn',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': self.user_agent,
            'Content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Referer': 'http://elite.nju.edu.cn/jiaowu/student/elective/specialityCourseList.do',  # 专业课
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh,en-US;q=0.9,en;q=0.8,zh-CN;q=0.7'
        }
        self.s.headers = headers
        count = 1
        r = requests.Response()
        try:
            if course_type == 0 or course_type == 1:
                r = self.s.get(self.renew_course_url, params={'method': method, 'classId': course_number, 'campus': '仙林校区'})
            elif course_type == 2:
                r = self.s.post(self.select_course_url, data={'method': method, 'classId': course_number})
            elif course_type == 3:
                r = self.s.post(self.renew_course_url, data={'method': method, 'classId': course_number, 'type': 5, '_': ''})
            elif course_type == 4:
                r = self.s.post(self.select_course_url, data={'method': method, 'classId': course_number})
            while '已满' in r.text:
                print(count)
                count += 1
                time.sleep(2)
                if course_type == 0 or course_type == 1:
                    r = self.s.get(self.renew_course_url, params={'method': method, 'classId': course_number, 'campus': '仙林校区'})
                elif course_type == 2:
                    r = self.s.post(self.select_course_url, data={'method': method, 'classId': course_number})
                elif course_type == 3:
                    r = self.s.post(self.renew_course_url, data={'method': method, 'classId': course_number, 'type': 5, '_': ''})
                elif course_type == 4:
                    r = self.s.post(self.select_course_url, data={'method': method, 'classId': course_number})
        except requests.exceptions.RequestException as e:
            print(e)
        finally:
            print(r.text)


def main():
    eas = NJUEas()
    eas.log_in()
    # test to grab some class.
    eas.grab_course()


if __name__ == '__main__':
    main()
