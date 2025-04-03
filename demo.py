from src.login import UESTC_login
from utils.utils import load_json, save_json


def main():
    cfg = load_json('configs/config.json')
    login = UESTC_login(cfg['baseurl'], cfg['login_url'], cfg['headers'])
    id_ = input('Student id: ')
    pwd = input('Password: ')
    status_code, headers = login.login(id_, pwd)
    print(status_code)
    print(headers)


if __name__ == '__main__':
    main()
