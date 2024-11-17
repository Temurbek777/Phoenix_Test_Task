from bs4 import BeautifulSoup
from datetime import datetime
from django.utils import timezone
import pytz
import locale
import requests
import json

'''
Это утилита для получения 10 новостей из сайта "https://uznews.uz/categories/sport"
'''

web_url = "https://uznews.uz/categories/sport"
json_list = []
data_list = []
count = 1

locale.setlocale(locale.LC_TIME, "ru_RU.UTF-8")

#===========Функция для получения 10 новостей из сайта https://uznews.uz/categories/sport=======
def getNews():
    res = requests.get(web_url)
    if res.status_code == 200:
        html_content = res.text
        soup = BeautifulSoup(html_content, "html.parser")
        script_tags = soup.find_all('script')
        for index, tag in enumerate(script_tags):
            if (index + 1) == 17:
                data = tag.string
                json_file = json.dumps(json.loads(data), indent=4, ensure_ascii=False)
                json_data = json.loads(json_file)['props']['pageProps']['initialState']['posts']['posts']

        for i in json_data:
            json_list = dict(i)['data']
            for j in json_list:
                if len(data_list) >= 10:
                    break
                date_obj = datetime.strptime(dict(j)['created_at'], "%d %B, %H:%M").replace(year=datetime.now().year)
                aware_datetime = timezone.make_aware(date_obj, pytz.utc)
                # formatted_date = aware_datetime.strftime("%Y-%m-%d %H:%M:%S")
                clean_data = {
                    'title': dict(j)['title'],
                    'description': dict(j)['meta_description'],
                    'image': dict(j)['image'],
                    'views_count': dict(j)['views_count'],
                    'created_at': aware_datetime,
                    'category': dict(j)['category']['name'],
                }
                data_list.append(clean_data)
            if len(data_list) >= 10:
                break

        return {"res": True, "data": data_list}
    else:
        return {"res": False, "status": res.status_code}



