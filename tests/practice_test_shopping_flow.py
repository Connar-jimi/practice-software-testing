import pytest
from api.base_api import BaseApi

class TestShoppingFlow:
    def test_full_shopping_flow(self):
        # 1. 浏览商品列表（链路起点）

        # 2. 创建购物车（关键步骤！）



        # 3. 把商品加到购物车

        # 4. 下单（从购物车创建订单）

# ========================================   数据库校验    =====================================================
        # 5.数据库校验
        with db_connection.cursor() as cursor:
            cursor.execute("",)



        # 6. 查看我的订单