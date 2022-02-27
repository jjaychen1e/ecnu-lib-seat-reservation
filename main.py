# This is a sample Python script.

# Press ⌥⇧R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import time
from typing import *
import requests as requests

username = 51215901064
password = '123456'
area = 40  # 中北一楼
segment = 1425398  # 1B

if __name__ == '__main__':
    today = f'{time.strftime("%Y-%m-%d", time.localtime())}'

    session = requests.session()
    session.headers = {'Referer': 'http://www.skalibrary.com/'}
    login_result = session.post('http://seats.lib.ecnu.edu.cn/api.php/login',
                                data={'username': username, 'password': password, 'from': 'mobile'}).json()
    access_token = login_result['data']['_hash_']['access_token']

    succeed = False
    while not succeed:
        current_time = time.strftime("%H:%M", time.localtime())
        response = session.get(
            f'http://seats.lib.ecnu.edu.cn/api.php/spaces_old?area={area}&day={today}&endTime=23:50&segment={segment}&startTime={current_time}')
        data = response.json()
        seat_list: List = data['data']['list']
        for seat in seat_list:
            if seat['status'] == 1:
                id = seat['id']
                result = session.post(f'http://seats.lib.ecnu.edu.cn/api.php/spaces/{id}/book',
                                      data={'access_token': access_token, 'userid': username, 'segment': segment,
                                            'type': 1}).json()
                print(result)
                succeed = True
                break
        print(succeed)
        time.sleep(1)
