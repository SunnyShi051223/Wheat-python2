import os
from dotenv import load_dotenv
import mysql.connector
import logging

# 配置日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler('check_users.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 加载环境变量
load_dotenv()

def check_users():
    try:
        # 获取数据库配置
        host = os.getenv('MYSQL_HOST', 'localhost')
        port = os.getenv('MYSQL_PORT', '3306')
        user = os.getenv('MYSQL_USER', 'root')
        password = os.getenv('MYSQL_PASSWORD', '')
        database = os.getenv('MYSQL_DB', 'wheat_classification')

        # 连接数据库
        conn = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )

        cursor = conn.cursor(dictionary=True)
        
        # 查看user表结构
        cursor.execute("DESCRIBE user")
        columns = cursor.fetchall()
        logger.info("用户表结构：")
        for col in columns:
            logger.info(f"字段: {col['Field']}, 类型: {col['Type']}, 允许空: {col['Null']}")
        
        # 查看所有用户（包括密码哈希）
        cursor.execute("SELECT * FROM user")
        users = cursor.fetchall()
        
        logger.info("\n用户列表：")
        for user in users:
            logger.info(f"ID: {user['id']}")
            logger.info(f"用户名: {user['username']}")
            logger.info(f"邮箱: {user['email']}")
            logger.info(f"密码哈希: {user['password_hash']}")
            logger.info(f"是否管理员: {user['is_admin']}")
            logger.info(f"是否激活: {user['is_active']}")
            logger.info(f"创建时间: {user['created_at']}")
            logger.info(f"最后登录: {user['last_login']}")
            logger.info("-" * 50)

        cursor.close()
        conn.close()
        
    except Exception as e:
        logger.error(f"查询失败: {str(e)}")
        raise

if __name__ == "__main__":
    check_users() 