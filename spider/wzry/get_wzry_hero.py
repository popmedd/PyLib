import requests
import os
import json

def downHeroPic():
    url = 'https://pvp.qq.com/web201605/js/herolist.json'
    try:
        path = 'heroPic/'
        if not os.path.exists(os.path.split(path)[0]):
            # 目录不存在创建
            os.makedirs(os.path.split(path)[0])

        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        mes_to_dict = json.loads(r.content)
        print("hero count:", len(mes_to_dict))
        for i in mes_to_dict:
            hero_no = i['ename']
            hero_name = i['cname']
            hero_skins = 1
            if 'skin_name' in i.keys():
                hero_skins = len(i['skin_name'].split('|'))

            print(hero_no, hero_name, hero_skins)
            for index in range(1, hero_skins + 1):
                pic_url = "https://game.gtimg.cn/images/yxzj/img201606/skin/hero-info/%s/%s-bigskin-%s.jpg" % \
                          (hero_no, hero_no, index)
                print(pic_url)

                pic_request = requests.get(pic_url)
                # print(pic_url, pic_request.content)
                try:
                    if pic_request.status_code == 200:
                        fileName = path + "%s-%s-%s.jpg" % \
                                   (hero_no, hero_name, index)
                        with open(fileName, 'wb') as fs:
                            fs.write(pic_request.content)
                except Exception as e:
                    print(e)

    except Exception as err:
        print("error: {0}".format(err))

if __name__ == '__main__':
    downHeroPic()
