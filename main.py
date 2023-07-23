import json
import requests
import bs4
from fake_headers import Headers

url = 'https://spb.hh.ru/search/vacancy?text=python+django+flask&salary=&area=1&area=2&ored_clusters=true' \
      '&search_field=description'
headers = Headers(browser='firefox', os='win')
headers_data = headers.generate()
response = requests.get(url, headers=headers_data)
html_data = response.text
soup = bs4.BeautifulSoup(html_data, 'lxml')


info = [['ссылка', 'вилка зп', 'название компании', 'город']]

div_tag = soup.find_all('div', class_='serp-item')

# Проходим циклом по всем вакансиям, очищаем данные, наполняем список res с данными по вакансии, добавляем список в info
for el in div_tag:
    res = []
    a_tag = el.find('a', class_='serp-item__title')
    res.append(a_tag['href'])
    span_tag = el.find('span', class_='bloko-header-section-3')
    if span_tag:
        salary = span_tag.text.replace('\u202F', ' ')
        res.append(salary)
    else:
        res.append('')
    company_tag = el.find('a', class_='bloko-link bloko-link_kind-tertiary')
    company_name = company_tag.text.replace('\xa0', ' ')
    company_name = company_name.replace('\u200b', ' ')
    res.append(company_name)

    # Вопрос
    # информация о городе содержится здесь:
    # <div data-qa='vacancy-serp__vacancy-address' class='bloko-text'>Москва</div>
    # почему ее нужно искать не с помощью вот такой строки:
    # city_tag = el.find('div', class_='bloko-text'),
    # а с помощью странной конструкции ниже?

    city_tag = el.find('div', {'data-qa': 'vacancy-serp__vacancy-address'})
    city = city_tag.text.replace('\xa0', ' ')
    res.append(city)
    info.append(res)

with open('info.json', 'w', encoding='utf-8') as f:
    json.dump(info, f, ensure_ascii=False)
