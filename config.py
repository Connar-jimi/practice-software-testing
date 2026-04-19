# config.py  —— 大厂接口自动化项目标准配置文件
# 所有公共参数都集中在这里管理

BASE_URL = "https://api.practicesoftwaretesting.com"

# 登录模块默认账号（官方练习账号）
VALID_EMAIL = "customer@practicesoftwaretesting.com"
VALID_PASSWORD = "welcome01"

# 管理员账号（后面做权限测试会用到）
ADMIN_EMAIL = "admin@practicesoftwaretesting.com"
ADMIN_PASSWORD = "welcome01"

# 公共请求头（以后可以扩展）
DEFAULT_HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

# 如果以后要切换环境，只需要改下面这一行即可
# 例如：BASE_URL = "https://test.api.practicesoftwaretesting.com"
# ==================== 数据库配置（练习项目默认配置） ====================
DB_CONFIG = {
    "host": "127.0.0.1",
    "port": 3307,
    "user": "user",           # 默认用户名
    "password": "root",   # 默认密码（如果你的数据库密码不一样，请改成你自己的）
    "database": "toolshop"      # 这个练习项目默认的数据库名
}