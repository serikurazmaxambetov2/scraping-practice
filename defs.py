from bs4 import BeautifulSoup
import requests

from config import headers, cookies

# Получение всех направлений
def get_all_directions() -> list[dict[str, str | int]]:
    response = requests.get('https://mandat.uzbmb.uz/ru.json')
    return response.json()

def get_users_by_direction(direction: dict[str, str | int]) -> list[dict[str, str | int]]:
    first_subject = direction.get('S4Subject')
    second_language = direction.get('S5Subject')
    education_language_id = direction.get('EdLangId')
    education_language = direction.get('Educlanguage')

    # Небольшое логирование
    print('Первый предмет:', first_subject)
    print('Второй предмет:', second_language)
    print('Язык обучения:', education_language, end='\n\n')
    
    body = {
        'pageNumber': '1',
        'pageSize': '100000000', # У них вообще не указаны лимиты на pageSize.
        's4subject': first_subject,
        's5subject': second_language,
        'edLangId': education_language_id,
        'lang': 'ru', # ни на что не влияет, но backend требует его
        # Без этого не работает, но сервер это даже не проверяет с какого IP это приходит.
        '__RequestVerificationToken': 'CfDJ8CzSYY35RFBNm9xcyoWBJWdQzqYpP47CMw4oDv7Tty34V-DsWBP_MKBt8aWkCjNikSONMFP6VJqj3dH2-1vjBvWX2_2dVItUihargieT2D9lbjmd3QN8SlayRDmiGjfpbyIUQeFQByYjnwzyEs3woyc',
    }

    response = requests.post('https://mandat.uzbmb.uz/Bakalavr2024/Paginate', data=body, headers=headers, cookies=cookies)
    soup = BeautifulSoup(response.text, 'lxml')

    statistics_raw = soup.select('table > tbody > tr')
    users = []

    for statistic_raw in statistics_raw:
        user_raw = statistic_raw.select('td')

        user_id = user_raw[0].text.strip()
        user_name = user_raw[1].text.strip()
        user_points = user_raw[2].text.strip()

        try:
            user_details = 'https://mandat.uzbmb.uz' + user_raw[3].select_one('a').get('href')
        except Exception:
            user_details = ''

        users.append({
            'id': user_id,
            'name': user_name,
            'points': user_points,
            'detail': user_details,
            'first_subject': first_subject,
            'second_subject': second_language,
            'education_language': education_language
        })

    return users
