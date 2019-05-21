import sys

from glutemulo.config import config
from glutemulo.kafka.consumer import JsonKafka as Consumer
from glutemulo.kafka.producer import JsonKafka as Producer
from glutemulo.logger import log

if config["backend"] == "carto":
    from glutemulo.backend.carto import CartoBackend as Backend

    log.debug("Using CARTO backend")
elif config["backend"] == "postgres":
    from glutemulo.backend.postgres import PostgresBackend as Backend

    log.debug("Using POSTGRES backend")
else:
    from glutemulo.backend.logger import LoggerBackend as Backend

    log.debug("Using LOGGER backend")


if __name__ == "__main__":
    if not config["ingestor_topic"]:
        log.error("No topic found. Please set GLUTEMULO_INGESTION_TOPIC")
        sys.exit(1)

    consumer = Consumer(
        config["ingestor_topic"],
        bootstrap_servers=config["ingestor_bootstap_servers"],
        group_id=config["ingestor_group_id"],
    )

    backend = Backend(
        config["ingestor_dataset"],
        config["ingestor_dataset_columns"],
        config["ingestor_dataset_ddl"],
        config["ingestor_dataset_autocreate"],
    )
    while True:
        for msg in consumer.consume(config["ingestor_wait_interval"]):
            log.debug(f"Received: {msg}")
            backend.consume(msg)