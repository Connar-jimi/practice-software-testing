import pytest
from api.base_api import BaseApi
from config import VALID_EMAIL, VALID_PASSWORD   # ← 必须加上这一行


class TestLogin:
    """登录模块测试类 - 使用 fixture 注入 BaseApi"""

    @pytest.mark.parametrize('email,password,expected_status,case_name', [
        # ==================== 正向测试 ====================
        (VALID_EMAIL, VALID_PASSWORD, 200, "login_001_有效邮箱密码_登录成功"),

        # ==================== 邮箱密码边界测试（先写成负向，因为未注册） ====================
        ("a@b.c", VALID_PASSWORD, 401, "login_002_最短合法邮箱格式_但未注册_登录失败"),
        ("a" * 50 + "@qq.com", VALID_PASSWORD, 401, "login_003_超长邮箱_登录失败"),
        ("user+test@domain.com", VALID_PASSWORD, 401, "login_004_邮箱含+特殊字符_登录失败"),
        ("user.name@domain.com", VALID_PASSWORD, 401, "login_005_邮箱含.字符_登录失败"),
        ("3@qq.com", VALID_PASSWORD, 401, "login_006_验证邮箱为最短字符_登录成功"),

        # ==================== 逆向测试 ====================
        ("12345@", VALID_PASSWORD, 401, "login_002_无效邮箱_登录失败"),
        ("12345qq.com", VALID_PASSWORD, 401, "login_003_无@符号_无效邮箱_登录失败"),
        (VALID_EMAIL, "short", 401, "login_004_密码太短_登录失败"),
        (VALID_EMAIL, "worngpassword123", 401, "login_005_无效密码_登录失败"),
        ("", VALID_PASSWORD, 401, "login_006_邮箱为空_登录失败"),
        (VALID_EMAIL, "", 401, "login_007_密码为空_登录失败"),
    ])
    def test_login(self, api, email, password, expected_status, case_name):
        """登录接口测试"""
        payload = {'email': email, 'password': password}

        # 使用 fixture 注入的 api 对象调用 post 方法
        response = api.post("/users/login", json=payload)

        assert response.status_code == expected_status, f"{case_name} 状态码错误"

        if expected_status == 200:
            assert "access_token" in response.json(), f"{case_name} 登录成功必须返回 access_token"
        else:
            # 反向测试的正确断言（根据实际返回结构修改）
            json_data = response.json()
            assert len(json_data) > 0, f"{case_name} 失败时应返回错误信息"
            print(f"{case_name} 通过！状态码 = {response.status_code}")