from confluent_kafka import Consumer, KafkaError
from confluent_kafka.admin import AdminClient, NewTopic
from push_mysql import DarknetDB
import time
from active_leaseSet.myutils.logger import logger
from lock import lock


def hash2address(base32_hash):
    # 去掉"="字符
    str_without_equals = base32_hash.replace("=", "")
    # 将所有大写字母转换为小写
    lowercase_str = str_without_equals.lower()

    address = ".".join([lowercase_str, "b32", "i2p"])
    address = "http://" + address
    return address


class KafkaConsumerHandler:
    def __init__(self, server, topic, mysql_db):
        self.bootstrap_servers = server
        self.topic = topic
        self.mysql_db = mysql_db
        self.group_id = "90"
        self.auto_offset_reset = "latest"  # Start consuming from the current position, ignoring old messages (real-time consumption)

    def connect(self):
        consumer_config = {
            "bootstrap.servers": self.bootstrap_servers,
            "group.id": self.group_id,
            "auto.offset.reset": self.auto_offset_reset,
        }

        try:
            time.sleep(0.3)
            self.consumer = Consumer(consumer_config)

            self.consumer.subscribe([self.topic])
        except Exception as e:
            print("kafka error " + str(e))

        logger.info("已经成功连接到Kafka服务器")

    def handle(self, fields):
        domain_dic = {
            "domain": fields[1],
        }
        domain_dic["domain"] = hash2address(domain_dic["domain"])
        with lock:
            self.mysql_db.add_leaseset(domain_dic)

    def consume(self):
        try:
            while True:
                msg = self.consumer.poll(timeout=1.0)  # Poll for messages
                if msg is None:
                    continue
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        # End of partition, continue to next message
                        continue
                    else:
                        # Handle other errors
                        logger.error("Consumer error: {}".format(msg.error()))
                        break

                # Process the message value
                message_value = msg.value().decode(
                    "utf-8"
                )  # Decode message bytes to string

                # Split the message value into individual fields

                fields = message_value.split("[|]")
                self.handle(fields)

        except KeyboardInterrupt:
            pass

        finally:
            self.consumer.close()
