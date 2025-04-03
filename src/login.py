from typing import Any, Dict, Tuple
import requests
from bs4 import BeautifulSoup
import js2py
import os
import requests.structures
from ..utils import mkdirp

# Get the directory of the current file
root_directory = os.path.abspath(os.getcwd())


class UESTC_login:
    def __init__(self, baseurl: str, login_url: str, headers: Dict[str, Any]) -> None:
        self.headers = headers
        self.baseurl = baseurl
        self.login_url = login_url

        self.session = requests.Session()
        self.session.headers.update(self.headers)
        self.js_context = js2py.EvalJs()

        self.raw = self.get_page()
        self.login_page = BeautifulSoup(self.raw, "html.parser")

    def get_page(self) -> str:
        response = self.session.get(self.login_url)
        if response.status_code != 200:
            raise ConnectionError(f"Failed to connect to {self.weekInfoUrl}, code: {response.status_code}")
        return response.text
    
    def get_encryption(self) -> str:
        script_tags = self.login_page.find_all('script', {'type': 'text/javascript'})
        
        encrypt_url = None
        for script_tag in script_tags:
            src = script_tag.get('src')
            if src:
                if 'encrypt' in src:
                    encrypt_url = self.baseurl + src
                    break
        
        if not encrypt_url:
            with open(f'{root_directory}/html.err', 'w') as f:
                f.write(str(self.raw))
                raise RuntimeError("Failed to find encrypt script, ")
        
        encrypt_js = self.session.get(encrypt_url)
        if encrypt_js.status_code != 200:
            raise ConnectionError(f"Failed to connect to {encrypt_url}, code: {encrypt_js.status_code}")
        
        mkdirp(f'{root_directory}/javascript')
        with open(f'{root_directory}/javascript/encrypt.js', 'w') as f:
            f.write(encrypt_js.text)

        return encrypt_js.text

    def get_form_data(self) -> Dict[str, str]:
        form = self.login_page.find('div', {'id': 'pwdLoginDiv', 'style': 'display: none'})
        form_data = {}
        pwdEncryptSalt = None
        if form:
            input_tags = form.find_all('input')
            for input_tag in input_tags:
                input_id = input_tag.get('id', 'N/A')
                input_value = input_tag.get('value', 'N/A')
                if input_id == 'pwdEncryptSalt':
                    pwdEncryptSalt = input_value
                if input_id != 'N/A' and input_value != 'N/A':
                    form_data[input_id] = input_value
                    
        assert pwdEncryptSalt, "Failed to get pwdEncryptSalt"
        return form_data, pwdEncryptSalt

    def encrypt(self, js_code: str, username: str, password: str, pwdEncryptSalt: str) -> str:
        self.js_context.execute(js_code)
        encrypted = self.js_context.encryptPassword(password, pwdEncryptSalt)
        return username, encrypted

    def login(self, username: str, password: str) -> Tuple[int, requests.structures.CaseInsensitiveDict[str]]:
        js_code = self.get_encryption()
        form_data, pwdEncryptSalt = self.get_form_data()

        username, password = self.encrypt(js_code, username, password, pwdEncryptSalt)
        form_data['username'] = username
        form_data['password'] = password

        response = self.session.post(self.login_url, data=form_data, allow_redirects=False)
        if response.status_code != 302:
            raise ConnectionError(f"Geted {self.login_url}, failed to redirect, code: {response.status_code}")
        
        return response.status_code, response.headers
