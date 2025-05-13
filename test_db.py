import os
from dotenv import load_dotenv
import mysql.connector
import logging

# 配置日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler('db_test.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 加载环境变量
load_dotenv()

def test_connection():
    try:
        # 获取数据库配置
        host = os.getenv('MYSQL_HOST', 'localhost')
        port = os.getenv('MYSQL_PORT', '3306')
        user = os.getenv('MYSQL_USER', 'root')
        password = os.getenv('MYSQL_PASSWORD', '')
        database = os.getenv('MYSQL_DB', 'wheat_classification')

        logger.info(f"尝试连接到数据库: {host}:{port}/{database}")
        logger.info(f"使用用户: {user}")

        # 尝试连接
        conn = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )

        if conn.is_connected():
            logger.info("数据库连接成功！")
            db_info = conn.get_server_info()
            logger.info(f"MySQL服务器版本: {db_info}")
            
            cursor = conn.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            logger.info(f"当前数据库: {db_name}")
            
            cursor.close()
            conn.close()
            logger.info("数据库连接已关闭")
            return True
    except Exception as e:
        logger.error(f"数据库连接失败: {str(e)}")
        return False

if __name__ == "__main__":
    test_connection() 