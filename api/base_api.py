import requests
import certifi
from config import BASE_URL


class BaseApi:
    """API 基础类 - 大厂通用封装（所有接口测试都继承它）,大厂用封装继承，你别用，你用实例调用"""

    def __init__(self):
        self._base_url = BASE_URL
        self._session = None

    @property
    def session(self):
        """懒加载 session（第一次使用时才创建）"""
        if self._session is None:
            self._session = requests.Session()
            self._session.verify = certifi.where()
        return self._session

    def _request(self, method: str, url: str, **kwargs):
        """所有请求的统一入口"""
        full_url = f"{self._base_url}{url}"
        response = self.session.request(method, full_url, **kwargs)
        print(f"🔍 {method} {url} → 状态码: {response.status_code}")
        return response

    def post(self, url: str, json=None, headers=None):
        """封装 POST 请求"""
        return self._request("POST", url, json=json, headers=headers)

    def get(self, url: str, params=None, headers=None):
        """封装 GET 请求"""
        return self._request("GET", url, params=params, headers=headers)
    def delete(self, url: str, json=None, headers=None):
        """封装 DELETE 请求"""