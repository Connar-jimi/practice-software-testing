from api.base_api import BaseApi
import pytest


pytestmark = pytest.mark.product_crud   # ← 这条链路叫“商品管理链路”
class TestProducts:
    """商品模块测试类 - 使用 fixture 注入 BaseApi"""
    #进入商品页面
    def test_gets_products_with_token(self, api, token):
        """使用登录后的 token 调用商品列表接口 - 核心链路测试"""

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        # 使用 fixture 注入的 api 对象
        response = api.get("/products", headers=headers)

        assert response.status_code == 200, "带 token 调用商品列表失败"
        assert "application/json" in response.headers.get("Content-Type", ""), "返回格式必须是 application/json"

        data = response.json()
        assert "data" in data, "返回体必须包含 data 字段"
        assert len(data["data"]) > 0, "商品列表应该至少有一条数据"

        print(f"✅ 带 token 调用商品列表成功！返回商品数量 = {len(data['data'])}")

    @pytest.mark.parametrize("payload,expected_status,case_name", [
        # ==================== 正向测试 ====================
        pytest.param(
            {
                "name": "IPhone19ProMax沪橙风1TB",
                "description": "瑶瑶领先",
                "price": 788.99,
                "category_id": "1",
                "brand_id": "1",
                "product_image_id": "1",
                "is_location_offer": 1,
                "is_rental": 0,
                "co2_rating": "A"
            },
            200,
            "product_001_正常创建商品成功",
            marks=pytest.mark.xfail(
                reason="Toolshop 练习 API 已知 bug: 正常创建商品返回 500 而非 200/201",
                strict=False
            )
        ),

        # ==================== 反向测试 ====================
        ({

             "description": "瑶瑶领先",
             "price": 788.99,
             "category_id": "1",
             "brand_id": "1",
             "product_image_id": "1"
                                 "",
             "is_location_offer": 1,
             "is_rental": 0,
             "co2_rating": "A"
         }, 422, "product_002_缺少商品名称_创建失败"),

        ({
             "name": "IPhone19ProMax沪橙风1TB",
             "description": "瑶瑶领先",
             "category_id": "1",
             "brand_id": "1",
             "product_image_id": "1",
             "is_location_offer": 1,
             "is_rental": 0,
             "co2_rating": "A"
         }, 422, "product_003_缺少价格_创建失败"),

        ({
             "name": "",
             "description": "瑶瑶领先",
             "price": 788.99,
             "category_id": "1",
             "brand_id": "1",
             "product_image_id": "1",
             "is_location_offer": 1,
             "is_rental": 0,
             "co2_rating": "A"
         }, 422, "product_003_商品名为空_创建失败"),




    ])


    #创建商品页
    def test_post_products_with_token(self, api, token, payload, expected_status,case_name):
        """创建商品接口测试 - 核心链路（已严格对齐 OpenAPI 422 错误码）"""
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        response = api.post("/products", json=payload, headers=headers)

        print(f"{case_name} 实际返回状态码：{response.status_code}")
        print(f"返回内容：{response.json()}")

        assert response.status_code == expected_status, f"{case_name} 状态码错误"

        if expected_status == 200:
            json_data = response.json()
            assert "id" in json_data, f"{case_name} 成功时必须返回商品 id"
            print(f"{case_name} 通过！新商品 id = {json_data.get('id')}")
        else:  # 422 错误
            json_data = response.json()
            assert isinstance(json_data, dict) and len(json_data) > 0, \
                f"{case_name} 失败时应返回错误信息"
            # 可选：进一步校验错误信息里包含 "message" 或具体字段错误
            print(f"{case_name} 通过！状态码 = {response.status_code}")



    #删除商品页
    @pytest.mark.xfail(reason="练习API创建商品接口已知bug，返回500 'Something went wrong'")
    def test_delete_products_with_token(self,api,token):
        """创建商品接口测试 - 核心链路（已严格对齐 OpenAPI 422 错误码）"""
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        # 第一步：先创建一个商品（用于测试删除）
        create_payload = {

            "name": "Iphone19ProMax沪橙风1TB",
            "description": "瑶瑶领先",
            "price": 788.99,
            "category_id": "1",
            "brand_id": "1",
            "product_image_id": "1",
            "is_location_offer": 1,
            "is_rental": 0,
            "co2_rating": "A"
        }
        create_response = api.post("/products",json=create_payload, headers=headers)
        assert create_response.status_code == 201,"状态码错误，创建商品失败"
        product_id = create_response.json().get("id")

        # 第二步：删除刚创建的商品
        delete_response = api.delete(f"/products/{product_id}", headers=headers)
        assert delete_response.status_code == 204,f"删除商品失败，状态码 = {delete_response.status_code}"
        print(f"✅ 成功删除商品 ID = {product_id}")




