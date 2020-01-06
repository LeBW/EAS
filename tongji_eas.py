"""
docstring
"""
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

OPTIONS = webdriver.ChromeOptions()
OPTIONS.add_argument(
    'user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"')

browser = webdriver.Chrome(options=OPTIONS)

url = "http://1.tongji.edu.cn"


def main():
    browser.get(url)

    teacher_index = int(input("请在浏览器界面中自行登录,进入选课界面,选择好需要抢的课后,在此输入老师的序号,并点击回车:"))

    # choose_course_btn = browser.find_element_by_xpath("//p[text()='选课']")
    # choose_course_btn.click()
    # time.sleep(2)

    # enter_course_btn = browser.find_element_by_css_selector("button.el-button.el-button--large")
    # enter_course_btn.click()
    # time.sleep(2)

    # choose_course_btn = browser.find_element_by_xpath("//span[text()='选择课程']")
    # choose_course_btn.click()
    # time.sleep(2)

    # course_list = browser.find_elements_by_class_name("el-table__row")
    # course = course_list[course_num]

    # print(course.find_element_by_class_name("el-table_1_column_3  ").text)

    # course.find_element_by_css_selector("span.el-checkbox__inner").click()

    # submit_btn = browser.find_element_by_xpath("//span[text()='提交']")
    # submit_btn.click()
    # time.sleep(1)

    trs = browser.find_element_by_css_selector("table.table-selected").find_elements_by_tag_name("tr")
    #
    trs[1].click()
    time.sleep(1)
    tr = browser.find_element_by_css_selector("table.table-class").find_elements_by_tag_name("tr")[teacher_index]
    tds = tr.find_elements_by_tag_name("td")
    print(tds[1].text + ": " + tds[3].text)
    tds[1].click()
    count = 0
    while True:
        try:
            count += 1
            trs[1].click()
            time.sleep(0.5)
            tr = browser.find_element_by_css_selector("table.table-class").find_elements_by_tag_name("tr")[teacher_index]
            tds = tr.find_elements_by_tag_name("td")
            print(time.strftime("[%Y-%m-%d %X] ", time.localtime()) + "第" + str(count) + "次尝试：" + tds[1].text + ": " + tds[3].text)
            n1, n2 = tds[3].text.split('/')
            # print(n1 + " " + n2)
            if n1 < n2:
                save_button = browser.find_element_by_xpath("//span[text()='保存课表']")
                save_button.click()
                print("已选")
                break
            time.sleep(0.5)

        except:
            print("exception")
            try:
                ok_button = browser.find_element_by_xpath("//span[text()='确认']")
                ok_button.click()
                print("已自动点击确认按钮")
            except NoSuchElementException:
                print("没有确认按钮")
            time.sleep(2)



if __name__ == '__main__':
    main()
