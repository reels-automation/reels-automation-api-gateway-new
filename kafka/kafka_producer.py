from quixstreams import Application

class KafkaProducerSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(KafkaProducerSingleton, cls).__new__(cls)
            cls._aplication = Application(broker_address="localhost:9092", loglevel="DEBUG")
        return cls._instance

    def produce_message(self, topic: str, key: str, value: str):
        with self._aplication.get_producer() as producer:
            producer.produce(
                topic=topic,
                key=key,
                value=value
            )