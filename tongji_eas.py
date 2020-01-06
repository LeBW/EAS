from selenium import webdriver
# 导入Keys 模块[键盘]
from selenium.webdriver.common.keys import Keys
# 导入Wait相关
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import sys
import time


options = webdriver.ChromeOptions()
options.add_argument('user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"')

browser = webdriver.Chrome(options=options)

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
            time.sleep(2)



if __name__ == '__main__':
    main()




def getHotelInfo():
    # wait until the button is clickable
    wait = WebDriverWait(browser, 10)
    more_info_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, '_1jyr48cu')))
    # click the button
    more_info_button.send_keys(Keys.RETURN)
    # get the information
    total_details = browser.find_element_by_class_name('_wpwi48')
    facs = total_details.find_elements_by_class_name('_ppgibgk')
    for facc in facs:
        print(facc.text)

    # ss = browser.find_elements_by_tag_name('div')
    # for s in ss:
    #     st=s.text
    #     num=st.find('熨斗')
    #     if num!=-1:
    #         print(st.find('熨斗'))


def getHotelComment():
    commentDates = browser.find_elements_by_css_selector('div._zjunba')
    # print(len(commentDates))
    for commentDate in commentDates:
        data = commentDate.find_element_by_css_selector('span._ppgibgk').text
    commentDates = browser.find_elements_by_css_selector('div._11dqbld7')
    for commentDate in commentDates:
        data = commentDate.text
        print(data)

