from active_leaseSet.myutils.config import config
from active_leaseSet.myutils.logger import logger
from active_leaseSet.middle.pull_kafka import KafkaConsumerHandler
from active_leaseSet.middle.push_mysql import DarknetDB


def action():
    mysql_host = config["mysql"]["host"]
    mysql_user = config["mysql"]["user"]
    mysql_password = config["mysql"]["password"]
    mysql_database = config["mysql"]["database"]
    mysql_port = config["mysql"]["port"]
    kafka_server = config["kafka"]["server"]
    kafka_topic = config["kafka"]["topic"]
    # 连接到mysql
    mysql_db = DarknetDB(
        mysql_host, mysql_user, mysql_password, mysql_database, int(mysql_port)
    )
    mysql_db.connect()
    # 连接到kafka
    kafka_consumer = KafkaConsumerHandler(kafka_server, kafka_topic, mysql_db)
    kafka_consumer.connect()

    # 执行消费程序，try
    try:
        kafka_consumer.consume()
    except Exception as e:
        logger.error("遇到问题：" + str(e))


if __name__ == "__main__":
    action()
