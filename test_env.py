import os
from dotenv import load_dotenv

# 尝试加载.env文件
load_dotenv()

# 打印所有环境变量
print("环境变量检查：")
print(f"FLASK_ENV: {os.getenv('FLASK_ENV')}")
print(f"SECRET_KEY: {os.getenv('SECRET_KEY')}")
print(f"MYSQL_HOST: {os.getenv('MYSQL_HOST')}")
print(f"MYSQL_PORT: {os.getenv('MYSQL_PORT')}")
print(f"MYSQL_USER: {os.getenv('MYSQL_USER')}")
print(f"MYSQL_PASSWORD: {os.getenv('MYSQL_PASSWORD')}")
print(f"MYSQL_DB: {os.getenv('MYSQL_DB')}") 