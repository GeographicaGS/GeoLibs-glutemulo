import json
import time
import uuid

from kafka import KafkaConsumer

from .avro_utils import FastAvroDecoder
from glutemulo.errors import SerializerError


class Kafka:
    def __init__(
        self,
        topic,
        decoder,
        bootstrap_servers,
        group_id=str(uuid.uuid4()),
        auto_offset_reset="latest",
        max_poll_records=500,
    ):
        self.consumer = KafkaConsumer(
            topic,
            group_id=group_id,
            bootstrap_servers=bootstrap_servers,
            auto_offset_reset=auto_offset_reset,
            consumer_timeout_ms=10000,  # StopIteration if no message after 10sec
            max_poll_records=max_poll_records,
        )

        self.decoder = decoder

    def consume(self, wait_interval=1):
        """Consume interface.
           Use multiple consumers in parallel w/ 0.9 kafka brokers
           Typically you would run each on a different server / process / CPU"""
        while True:
            for msg in self._consumer_generator():
                yield self.deserialize(msg.value)
                time.sleep(wait_interval)

    def _consumer_generator(self):
        """Driver specific. Consumer generator"""
        return self.consumer

    def deserialize(self, message, *extra_options):
        """Driver specific. Deerialize data message"""
        return self.decoder.decode(message)


class JsonKafka(Kafka):
    def __init__(
        self,
        topic,
        bootstrap_servers,
        group_id=str(uuid.uuid4()),
        auto_offset_reset="latest",
        max_poll_records=500,
    ):
        super().__init__(
            topic,
            None,
            bootstrap_servers,
            group_id=str(uuid.uuid4()),
            auto_offset_reset="latest",
            max_poll_records=500,
        )

    def deserialize(self, message, *extra_options):
        return json.loads(message)


class AvroKafka(Kafka):
    def __init__(
        self,
        topic,
        schema,
        schema_id,
        bootstrap_servers,
        group_id=str(uuid.uuid4()),
        auto_offset_reset="latest",
        max_poll_records=500,
    ):
        super().__init__(
            topic,
            FastAvroDecoder(schema_id, schema),
            bootstrap_servers,
            group_id=str(uuid.uuid4()),
            auto_offset_reset="latest",
            max_poll_records=500,
        )
