import time
from datetime import datetime
from typing import *
import requests as requests

username = 51215901064
password = '123456'
area = 40  # 中北 1B

if __name__ == '__main__':
    today = f'{time.strftime("%Y-%m-%d", time.localtime())}'
    segment = 1425400 + (datetime.strptime(today, "%Y-%m-%d") - datetime.strptime('2022-03-01', "%Y-%m-%d")).days

    session = requests.session()
    session.headers = {'Referer': 'http://www.skalibrary.com/'}
    login_result = session.post('http://202.120.82.17/api.php/login',
                                data={'username': username, 'password': password, 'from': 'mobile'}).json()
    access_token = login_result['data']['_hash_']['access_token']

    succeed = False
    while not succeed:
        current_time = time.strftime("%H:%M", time.localtime())
        response = session.get(
            f'http://202.120.82.17/api.php/spaces_old?area={area}&day={today}&endTime=23:50&segment={segment}&startTime={current_time}')
        data = response.json()
        seat_list: List = data['data']['list']
        seat_list.reverse()
        for seat in seat_list:
            if seat['status'] == 1 and int(seat['no']) >= 79:
                id = seat['id']
                result = session.post(f'http://202.120.82.17/api.php/spaces/{id}/book',
                                      data={'access_token': access_token, 'userid': username, 'segment': segment,
                                            'type': 1}).json()
                print(result)
                print(seat)
                succeed = True
                break
        print(succeed)
        time.sleep(1)
