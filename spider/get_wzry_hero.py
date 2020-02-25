import requests
import os
import json

if __name__ == '__main__':
    url='https://pvp.qq.com/web201605/js/herolist.json'
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding=r.apparent_encoding
        mes_to_dict = json.loads(r.content)
        print("hero count:",len(mes_to_dict))
        for i in mes_to_dict:
            hero_no=i['ename']
            hero_name = i['cname']
            # hero_skins=len(i['skin_name'].split('|'))
            print(hero_no,hero_name)
            pic_url = "https://game.gtimg.cn/images/yxzj/img201606/skin/hero-info/%s/%s-bigskin-%s.jpg" % \
                      (hero_no, hero_no, 1)
            pic_request= requests.get(pic_url)
            # print(pic_url, pic_request.content)
            try:
                fileName = "%s-%s-1.jpg" % \
                          (hero_no, hero_name)
                with open(fileName, 'wb') as fs:
                    fs.write(pic_request.content)
            except IOError as e:
                print(e)

    except OSError as err:

        print("OS error: {0}".format(err))

    except ValueError:

        print("Could not convert data to an integer.")

    except:

        print("Unexpected error:", sys.exc_info()[0])
