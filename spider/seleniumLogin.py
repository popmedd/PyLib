from selenium import webdriver
import json

if __name__ == '__main__':
    driver = webdriver.Chrome()
    # 设置浏览器窗口的位置和大小
    #driver.set_window_position(20, 40)
    #driver.set_window_size(1100, 700)

    # 打开一个页面（QQ空间登录页）
    driver.get("https://learning.b.qianxin.com/login/index.php")

    # 通过使用选择器选择到表单元素进行模拟输入和点击按钮提交
    driver.find_element_by_id('username').send_keys('xiongqi1@cmbc.com.cn')
    driver.find_element_by_id('password').send_keys('Xiongqi@215')  # password
    driver.find_element_by_id('loginbtn').click()

    dictCookies = driver.get_cookies()
    jsonCookies = json.dumps(dictCookies)
    print(jsonCookies)

    driver.get("https://learning.b.qianxin.com/course/view.php?id=27")
    # do something

    # 退出窗口
    # driver.quit()