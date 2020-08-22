import json
import requests,re,os
import js2py
from bs4 import BeautifulSoup
from selenium import webdriver
from requests.packages import urllib3
from selenium.webdriver.chrome.options import Options

username = 'xiongqi1@cmbc.com.cn'
password ='Xiongqi@215'
urllib3.disable_warnings()
dir_path = 'd:/CFSP/'
chrome_options = Options()
# 设置chrome浏览器无界面模式
chrome_options.add_argument('--headless')


def validate_filename(filename):
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
    new_filename = re.sub(rstr, "_", filename)  # 替换为下划线
    return new_filename


def execute_login(driver):
    driver.get("https://learning.b.qianxin.com/login/index.php")
    driver.find_element_by_id('username').send_keys(username)
    driver.find_element_by_id('password').send_keys(password)  # password
    driver.find_element_by_id('loginbtn').click()
    print(driver.get_cookies())
    print('模拟登录完成')
    return driver


def build_download_head(driver):
    cookies = driver.get_cookies()
    cookie_str = ''
    for cookie in cookies:
        cookie_str = cookie_str + cookie['name'] + "=" + cookie['value'] + ";"
    print(cookie_str)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        'Cookie': '%s' % cookie_str,
        'Referer': 'https://learning.b.qianxin.com/my/'
    }
    print(headers)
    return headers


def find_video_url(driver):
    print('开始获取视频链接：')
    a = re.findall(r'(var H5PIntegration = .*?;)', driver.page_source)
    days = driver.find_elements_by_xpath('//*[@id="page-navbar"]/ul/li[3]/span/a/span')[0].text

    title = driver.find_elements_by_xpath('//*[@id="region-main"]/div/h2')[0].text

    H5PIntegration = js2py.eval_js(a[0] + 'H5PIntegration')
    key = ''
    prefix = ''
    for k in H5PIntegration['contents']:
        if k.startswith('cid'):
            key = k
            prefix = H5PIntegration['contents'][k]['contentUrl']
            break
    json_content = H5PIntegration['contents'][key]['jsonContent']
    path = json.loads(json_content)['interactiveVideo']['video']['files'][0]['path']
    video_url = str(prefix) + '/' + path

    video_dict = {'days': days, 'title': title, 'video_url': video_url}
    print('获取到视频链接：'+video_dict['days'] + '-' + video_dict['title'] + '-' + video_dict['video_url'])
    return video_dict


def download_video(driver):
    headers = build_download_head(driver)
    driver.get("https://learning.b.qianxin.com/course/view.php?id=27")
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    print('开始爬取课程页面链接')
    video_pages = soup.select('ul[class="section img-text"] li[class="activity hvp modtype_hvp "] a ')
    for i in video_pages:
        href = i['href']
        driver.get(href)
        print('进入课程页面链接:' + href)
        video_dict = find_video_url(driver)
        days = video_dict['days']
        n_dir_path = dir_path+os.sep+days
        if not os.path.isdir(n_dir_path):
            os.makedirs(n_dir_path)

        days = video_dict['days']
        video_url = video_dict['video_url']
        title = validate_filename(video_dict['title'])

        filename = n_dir_path + os.sep + title + '.mp4'
        if not os.path.isfile(filename):
            print('开始下载：' + days + '-' + title + '-' + video_url)

            s = requests.Session()
            res = s.get(url=video_url, headers=headers, stream=True, verify=False)
            with open(filename, "wb") as f:
                for chunk in res.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
            print(filename + '下载完成!')
        else:
            print('跳过存在的文件：' + days + '-' + title + '-' + video_url)


if __name__ == '__main__':
    if not os.path.isdir(dir_path):
        os.makedirs(dir_path)
    driver = webdriver.Chrome(options=chrome_options)
    execute_login(driver)
    download_video(driver)


