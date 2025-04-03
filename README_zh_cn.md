# UESTC_Login：一个简单的 Python 包，用于从新 CAS 系统获取服务认证

**[English version](README.md)**

## 先决条件

### 0. 克隆此仓库
```Bash
git clone https://github.com/xyangzhou/UESTC_login
cd UESTC_login
```

### 1. 安装依赖项
此代码在 Python 3.9 下进行测试。使用 [Requests](https://github.com/psf/requests)、[BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/) 和 [Js2Py](https://github.com/PiotrDabkowski/Js2Py) 库。
```Bash
######## 可选 #######
conda create --name UESTC_login python=3.9
conda actiavte UESTC_login
######## 可选 #######
pip install -r requirements.txt
```

## 用法
[UESTC_login](src/login.py) 提供了一个简单的接口来登录到 [https://idas.uestc.edu.cn/](https://idas.uestc.edu.cn/)。详细配置列在 [config.json](configs/config.json) 中。也给出了一个可用的 [demo](demo.py) 。

```python
login = UESTC_login(cfg['baseurl'], cfg['login_url'], cfg['headers'])
status_code, headers = login.login(<STUDENT_ID>, <PASSWORD>)
```

参数：
- `cfg['headers']` 是 [config.json](configs/config.json) 中固定的请求头
- `cfg['baseurl']` 是固定的 服务器根url `https://idas.uestc.edu.cn`
- `cfg['login_url']` 是必需的服务网址，格式为 `https://idas.uestc.edu.cn/authserver/login?service=<SERVICE_URL>`，由服务网站生成。我们的项目 [UESTC_schedule](https://github.com/xyangzhou/UESTC_schedule) 提供了一个实例。

返回：
- `status_code` 是 HTTP 状态代码，应该是 302 重定向
- `headers` 是响应的标头。如果登录成功，服务网址应位于 `headers['Location']` 中，格式为 `https://<SERVICE_URL>&ticket=<ST_TOKEN>`

## TODO
- [ ] 将此包构建为wheel。
- [ ] 由于验证码从未触发过，因此尚不支持验证码。