import datetime
import os

import lxml.html as html
import requests

LINKS='//a[@class="finanzasSect"]/@href'
TITULO = '//*[@id="vue-container"]//div[@class="mb-auto"]/h2/span/text()'
RESUMEN = '//div[@class="lead"]/p/text()'
CUERPO = "//div[@class='html-content']/p/text()"

URL_REPUBLICA='https://www.larepublica.co/'
def get_text_to_xpath(parsed,xpath):
    return parsed.xpath(xpath)[0] 


def parse_notice(link,today):
    try:
        response=requests.get(link)
        if response.status_code == 200:
            notice = response.content.decode('utf-8')
            parsed = html.fromstring(notice)
            try:
                title=get_text_to_xpath(parsed,TITULO)
                title=title.replace('\"','').replace('/', '-').replace('\n', '_')
                summary=get_text_to_xpath(parsed,RESUMEN)
                body=parsed.xpath(CUERPO)

            except IndexError:
                return

            with open(f'{today}/{title}.txt','w',encoding='utf-8') as file:
                file.write(title)
                file.write('\n\n')
                file.write(summary)
                file.write('\n\n')
                for p in body:
                    file.write(p)
                    file.write('\n')


        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)


def parse_home():
    try:
        response = requests.get(URL_REPUBLICA)
        if response.status_code == 200:
            home= response.content.decode('utf-8') #trae un string y pasamos los caracteres raros a utf-8, tildes...
            parsed = html.fromstring(home)
            links_to_notices=parsed.xpath(LINKS)
            print(links_to_notices)
            today = datetime.date.today().strftime('%Y-%m-%d')
            if not os.path.isdir(today):
                os.mkdir(today)
            for link in links_to_notices:
                parse_notice(link,today)
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)
def run():
    parse_home()

if __name__=='__main__':
    run()