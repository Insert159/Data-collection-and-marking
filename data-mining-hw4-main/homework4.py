from lxml import html
from lxml import etree
import requests
import csv
from time import sleep
from pprint import pprint

# Парсинг новостей с news.mail.ru, используя XPath
url = "https://news.mail.ru" 
# строка агента пользователя в заголовке HTTP-запроса, чтобы имитировать веб-браузер и избежать блокировки сервером
header = {'User-Agent' : 
          'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'}
session = requests.session()

response = session.get(url, headers=header) 
print(response.status_code)
if response.status_code < 200 or response.status_code > 206:
        print(response.text)
        exit # выходим, если нет следующей страницы
dom = html.fromstring(response.text)
# Поиск ссылок на новости:
xpath_text = '''
    //a[contains(@href, "news.mail.ru")
      or contains(@href, "pogoda.mail.ru")
      or contains(@href, "finance.mail.ru")
      or contains(@href, "vfokuse.mail.ru")]/@href
'''
news = []
urls = [str(u) for u in dom.xpath(xpath_text)] # конвертация ссылок в string
print(f'найдено {len(urls)} новостей')
for url in urls:
    if url != 'None':
        sleep(2) # задержка, чтобы избежать status_code 429 от сервера
        print(url)
        # переходим на страницу новости
        response = session.get(url, headers=header) 
        print(response.status_code)
        if response.status_code >= 200 and response.status_code <= 206:
            new_ = {}
            # сохраняем ссылку на новость
            new_['url'] = url
            dom = html.fromstring(response.text)
            # поиск заголовка новости:
            hdr = dom.xpath("//h1[@class='hdr__inner']/text()")
            if len(hdr) > 0:
                new_['header'] = hdr[0]
            else:
                new_['header'] = '' # если заголовок не найден
            # поиск источника новости:
            source = dom.xpath("//span[@class='link__text']/text()")
            if len(source) > 0:
                new_['source'] = source[0]
            else:
                new_['source'] = '' # если источник не найден
            # поиск времени создания новости:
            datetime = dom.xpath("//span[contains(@class, 'js-ago')]/@datetime")
            if len(datetime) > 0:
                new_['datetime'] = datetime[0]
            else:
                new_['datetime'] = ''  # если время создания не найдено
            pprint(new_)
            news.append(new_)
print('-----------------------------------------')
pprint(news)

with open('news.csv', 'w', newline='') as csvfile:
    fieldnames = ['url', 'header', 'source', 'datetime']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for new_ in news:
        writer.writerow({'url': new_['url'], 
                          'header': new_['header'], 
                          'source': new_['source'], 
                          'datetime': new_['datetime']})



    
