import re
import requests

def hackinglab_jbg_q2():
    """
    #小明要参加一个高技能比赛，要求每个人都要能够快速口算四则运算，2秒钟之内就能够得到结果，
    # 但是小明就是一个小学生没有经过特殊的培训，
    # 那小明能否通过快速口算测验呢？
    """
    url = "http://lab1.xseclab.com/xss2_0d557e6d2a4ac08b749b61473a075be1/index.php"
    headers = {'Cookie': 'PHPSESSID=21043f4dd0550ef63816741ae089ea7f'}
    r = requests.get(url, headers=headers, allow_redirects=False)
    c = r.content
    regstr = re.compile(r'[0-9+*()]+[)]')
    obj = regstr.findall(c.decode('utf-8'))
    if obj:
        result = eval(obj[0])
        data = {'v': result}
        r = requests.post(url, data=data, headers=headers)
        print(r.content)




if __name__ == '__main__':
    hackinglab_jbg_q2()
