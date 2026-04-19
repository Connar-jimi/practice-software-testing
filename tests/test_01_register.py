import pytest
import time
from api.base_api import BaseApi


class TestRegister:
    """注册模块测试类 - 大厂标准写法"""

    @pytest.mark.parametrize("payload, expected_status, case_name", [
        # ==================== 正向测试 ====================
        # 用一个全新的、从未注册过的邮箱
        ({"email": "newuser{int(time.time())}@qq.com", "password": "Welcome123111!", "first_name": "New", "last_name": "User"},
         201, "register_001_正常注册成功"),

        # ==================== 反向测试 ====================
        ({"email": "", "password": "Strong!@#2026Pass", "first_name": "Dai", "last_name": "User"},
         422, "register_002_空邮箱注册失败"),
        ({"email": "newuser001@q.com", "password": "", "first_name": "Dai", "last_name": "User"},
         422, "register_003_空密码注册失败"),
        ({"email": "invalidemail", "password": "Welcome123!", "first_name": "New", "last_name": "User"},
         422, "register_004_非法邮箱格式_注册失败"),
        ({"email": "a@b.c", "password": "Welcome123!", "first_name": "New", "last_name": "User"},
         422, "register_005_最短合法邮箱格式_注册失败"),
        ({"email": "a" * 50 + "@qq.com", "password": "Welcome123!", "first_name": "New", "last_name": "User"},
         422, "register_006_超长邮箱_注册失败"),
        ({"email": "newuser002@q.com", "password": "short", "first_name": "", "last_name": "User"},
         422, "register_008_密码太短_注册失败"),
        ({"email": "newuser002@q.com", "password": "Welcome123!", "first_name": "New", "last_name": "asdad"},
         422, "register_009_first_name为空_注册失败"),
        ({"email": "newuser002@q.com", "password": "Welcome123!", "first_name": "New", "last_name": ""},
         422, "register_010_last_name为空_注册失败"),
    ])
    def test_register(self, api, payload, expected_status, case_name):
        """注册接口测试"""

        response = api.post("/users/register", json=payload)

        print(f"{case_name} 实际返回状态码：{response.status_code}")
        print(f"返回内容：{response.json()}")

        assert response.status_code == expected_status, f"{case_name} 状态码错误"

        if expected_status == 201:
            json_data = response.json()
            assert "id" in json_data, f"{case_name} 成功时必须返回用户 id"
            print(f"{case_name} 通过！新用户 id = {json_data.get('id')}")
        else:
            # 反向测试的正确断言（根据实际返回结构修改）
            json_data = response.json()
            assert len(json_data) > 0, f"{case_name} 失败时应返回错误信息"
            print(f"{case_name} 通过！状态码 = {response.status_code}")