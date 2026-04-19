import pytest
from api.base_api import BaseApi

# ==================== 标记整条购物 E2E 链路（只需这一行） ====================
pytestmark = pytest.mark.shopping_flow
# ====================   定义测试shoppingflow类    =======================================

class TestShoppingFlow:
    """第2条核心业务链路：登录 → 浏览商品 → 加购物车 → 下单 → 查我的订单"""

    def test_full_shopping_flow(self, api, token,db_connection):
        """完整购物 E2E 链路测试 - 大厂标准写法"""
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        # 1. 浏览商品列表（链路起点）
        browse_response = api.get("/products", headers=headers)
        assert browse_response.status_code == 200, "浏览商品列表失败"
        products = browse_response.json()["data"]
        assert len(products) > 0, "商品列表应该有数据"
        product_id = products[0]["id"]
        print(f"✅ 1. 浏览商品成功，取商品ID = {product_id}")

        # 2. 创建购物车（关键步骤！）
        create_cart_response = api.post("/carts", json={}, headers=headers)
        assert create_cart_response.status_code in [200, 201], f"创建购物车失败，状态码={create_cart_response.status_code}"
        cart_id = create_cart_response.json().get("id")   # 或 "cartId"，看实际返回
        print(f"✅ 2. 创建购物车成功，cartId = {cart_id}")

        # 3. 把商品加到购物车
        add_item_payload = {
            "product_id": product_id,
            "quantity": 1
        }
        cart_response = api.post(f"/carts/{cart_id}", json=add_item_payload, headers=headers)
        assert cart_response.status_code in [200, 201], f"加购物车失败，状态码={cart_response.status_code}"
        print("✅ 3. 加购物车成功")


        # 4. 下单（从购物车创建订单）——已严格按 Swagger Invoice request object 填写
        order_payload = {
            "cart_id": cart_id,                    # 必须传前面创建的 cart_id
            "payment_method": "bank-transfer",     # Swagger 示例值
            "billing_street": "123 Test Street",
            "billing_city": "Test City",
            "billing_state": "CA",
            "billing_country": "US",
            "billing_postal_code": "12345",
            "payment_details": {
                "bank_name": "Test Bank",
                "account_name": "Test User",
                "account_number": "1234567890"
            }
        }

        invoice_response = api.post("/invoices", json=order_payload, headers=headers)
        assert invoice_response.status_code == 201, f"下单失败，状态码={invoice_response.status_code}"
        invoice_id = invoice_response.json().get("id")  # ← 这里提取 invoice_id
        print(f"✅ 4. 下单成功！状态码 = {invoice_response.status_code}")
        print(f"返回内容：{invoice_response.json()}")

        # ==================== 新增：数据库校验 ====================
        #5.数据库校验
        with db_connection.cursor() as cursor:
            cursor.execute("SELECT * FROM invoices WHERE id = %s", (invoice_id,))  # ← 使用 invoice_id
            invoice_record = cursor.fetchone()

            assert invoice_record is not None, f"数据库中未找到发票/订单 ID = {invoice_id}"
            assert invoice_record['status'] == 'AWAITING_FULFILLMENT', f"订单状态应该为AWAITING_FULFILLMENT，实际是 {invoice_record.get('status')}"
            print(f"✅ 数据库校验通过：订单 {invoice_id} 已落库，状态 = {invoice_record['status']}")



        # 6. 查看我的订单
        orders_response = api.get("/invoices", headers=headers)  # ← 必须是 /invoices
        assert orders_response.status_code == 200, "查看我的订单失败"
        data = orders_response.json().get("data", [])
        print(f"✅ 5. 查看我的订单成功！共 {len(data)} 条订单")
        print(f"返回内容：{orders_response.json()}")
        print("🎉 完整购物 E2E 链路全部通过！")