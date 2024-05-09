import mysql.connector

import datetime
from active_leaseSet.myutils.logger import logger
from lock import lock


class DarknetDB:
    def __init__(self, host, user, password, database, port):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port
        self.conn = None
        self.cursor = None

    def connect(self):
        try:
            self.conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                port=self.port,
                connection_timeout=300,
            )
            self.cursor = self.conn.cursor()
            with lock:
                self.create_database()
                self.create_domain_table()
            logger.info("已经成功连接到mysql服务器")
        except mysql.connector.Error as error:
            logger.error(f"Error connecting to MySQL database: {error}")

    def create_database(self):
        self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")
        self.cursor.execute(f"USE {self.database}")

    def create_domain_table(self):
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS Domain ("
            "id INT AUTO_INCREMENT,"
            "domain VARCHAR(128) NOT NULL,"
            "fftime DATETIME,"
            "updatetime DATETIME,"
            "PRIMARY KEY (id),"
            "UNIQUE (domain)"
            ")"
        )

    def close(self):
        if self.conn:
            self.conn.close()
            print("MySQL connection closed")

    def add_domain(self, domain_dic):
        # 构建插入语句
        # + 记录首次发现时间
        public = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        update = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        domain_dic["fftime"] = public
        domain_dic["updatetime"] = update

        insert_query = (
            "INSERT INTO Domain "
            "(domain, fftime, updatetime) "
            "VALUES (%(domain)s, %(fftime)s, %(updatetime)s) "
            "ON DUPLICATE KEY UPDATE "
            "updatetime=VALUES(updatetime)"
        )

        # 执行插入操作
        self.cursor.execute(insert_query, domain_dic)
        self.conn.commit()
        logger.debug(f"Domain信息存储成功，domain为 {domain_dic['domain']}")


# 使用示例
if __name__ == "__main__":
    mysql_db = DarknetDB("127.0.0.1", "root", "darknet", "Dark", 3306)
    mysql_db.connect()
    domain_dic = {"domain": "abcdefg.b32.i2p"}
    mysql_db.add_domain(domain_dic)
