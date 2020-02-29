import requests
import xlwt
import time


# 豆瓣有反爬虫机制，需要添加User-Agent，进行浏览器伪装
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
}


def get_movie_tag():
    url = "https://movie.douban.com/j/search_tags"
    payload = {'type': 'movie', 'source': 'index'}
    try:
        res = requests.get(url, payload, headers=headers)
        res.raise_for_status()
        res.encoding = res.apparent_encoding
        cookies = res.cookies
        movie_tag_json = res.json()
        tags = movie_tag_json.get('tags')
        print(tags)
        return tags;
    except Exception as err:
        print("error: {0}".format(err))


def get_movie_subjects(tags):
    try:
        subjects_list = []
        for index, tag in enumerate(tags):
            url = "https://movie.douban.com/j/search_subjects"
            payload = {'type': 'movie', 'tag': tag, 'page_limit': 50, 'page_start': 0}
            res = requests.get(url, payload, headers=headers)
            res.raise_for_status()
            res_content = res.json()
            subjects = {'tag': tag, 'subjects': res_content.get('subjects')}
            print(subjects)
            subjects_list.insert(index, subjects)

        return subjects_list;
    except Exception as err:
        print("error: {0}".format(err))


def save_to_excel(movies):
    cell_title = ['影片评分', '影片名称', '详情地址', '影片ID', '是否新片', '海报地址']
    # 创建一个excel文档，并设置编码
    workbook = xlwt.Workbook(encoding='utf-8')
    # 遍历数据
    for movie_subject in movies:
        # 创建一个sheet
        sheet_name = movie_subject.get('tag')
        worksheet = workbook.add_sheet(sheet_name)
        movie_date = movie_subject.get('subjects')
        # 插入表格头
        for index, title in enumerate(cell_title):
            worksheet.write(0, index, title)

        for row, movie in enumerate(movie_date):
            # 写入excel,参数对应 行, 列, 值
            worksheet.write(row+1, 0, movie.get('rate'))  # 影片评分
            worksheet.write(row+1, 1, movie.get('title'))  # 影片名称
            worksheet.write(row+1, 2, movie.get('url'))  # 影片详情地址
            worksheet.write(row+1, 3, movie.get('id'))  # 影片ID
            worksheet.write(row+1, 4, movie.get('is_new'))  # 是否新片
            worksheet.write(row+1, 5, movie.get('cover'))  # 海报图片地址

    file_name='movie'+time.strftime("%Y%m%d%H%M%S", time.localtime())+'.xls'
    workbook.save(file_name)


if __name__ == '__main__':
    movie_tags = get_movie_tag()
    movie_subjects = get_movie_subjects(movie_tags)
    save_to_excel(movie_subjects)


