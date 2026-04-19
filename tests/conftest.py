import pymysql
import pytest
import requests
import certifi
from config import BASE_URL, VALID_EMAIL, VALID_PASSWORD
from api.base_api import BaseApi
from config import DB_CONFIG


@pytest.fixture(scope="session")
def db_connection():
    """数据库链接fixture(整个测试会话只链接一次)"""
    conn = pymysql.connect(**DB_CONFIG,cursorclass=pymysql.cursors.DictCursor)
    yield conn
    conn.close()

@pytest.fixture
def api():
    """提供 BaseApi 实例给所有测试使用"""
    return BaseApi()


@pytest.fixture(scope="class")
def token():
    """一次登录，全局可用 token（大厂标准干净方式）"""
    payload = {"email": VALID_EMAIL, "password": VALID_PASSWORD}

    # 直接使用 requests（避免 fixture 依赖问题）
    response = requests.post(
        f"{BASE_URL}/users/login",
        json=payload,
        verify=certifi.where()
    )

    assert response.status_code == 200, "fixture 登录失败，无法获取 token"

    token_value = response.json()["access_token"]
    print(f"🔑 fixture 已自动登录并提取 token（长度: {len(token_value)}）")

    return token_value