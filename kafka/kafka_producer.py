from quixstreams import Application
from settings import KAFKA_URL

class KafkaProducerSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(KafkaProducerSingleton, cls).__new__(cls)
            cls._instance._application = Application(broker_address=KAFKA_URL, loglevel="DEBUG")
        return cls._instance

    @classmethod
    def produce_message(cls, topic: str, key: str, value: str):
        instance = cls()  # Garantiza que _instance esté creado
        with instance._application.get_producer() as producer:
            producer.produce(
                topic=topic,
                key=key,
                value=value
            )
