import kafka_producer
import avro_utils
import pytest


def test_context_string():
    with avro_utils.ContextStringIO() as out:
        out.write(b"uno")
        out.write(b"dos")
        assert out.getvalue() == b"unodos"


SCHEMA = {
    "type": "record",
    "name": "evolution",
    "namespace": "com.landoop",
    "doc": "This is a sample Avro schema to get you started. Please edit",
    "fields": [
        {"name": "name", "type": "string"},
        {"name": "number1", "type": "int"},
        {"name": "number2", "type": "float"},
    ],
}
SCHEMA_ID = 1


def test_fast_avro_utils_success():
    encoder = kafka_producer.FastAvroEncoder(SCHEMA, SCHEMA_ID)
    result = encoder.encode({"name": "Una prueba", "number1": 3, "number2": 1.5})
    assert result == b"\x00\x00\x00\x00\x01\x14Una prueba\x06\x00\x00\xc0?"


def test_fast_avro_utils_bad_data():
    encoder = kafka_producer.FastAvroEncoder(SCHEMA, SCHEMA_ID)
    with pytest.raises(kafka_producer.ValidationError) as excinfo:
        encoder.encode({"name": "Una prueba", "number1": "3", "number2": 1.5})
    assert "number1 is <3> of type <class 'str'> expected int" in excinfo.value.message


def test_avro_kafka_produder(mocker):
    mocker.patch("kafka_producer.KafkaProducer")

    producer = kafka_producer.AvroKafka(
        SCHEMA, SCHEMA_ID, bootstrap_servers="localhost:9092"
    )

    producer.produce(
        "avro-topic", {"number1": 1, "number2": 1.3, "name": f"Name for 1"}
    )
    producer.producer.send.assert_called_once_with(
        "avro-topic", b"\x00\x00\x00\x00\x01\x14Name for 1\x02ff\xa6?"
    )


def test_json_kafka_produder(mocker):
    mocker.patch("kafka_producer.KafkaProducer")
    producer = kafka_producer.JsonKafka("un-topic", bootstrap_servers="localhost:9092")
    producer.produce(
        "json-topic", {"number1": 1, "number2": 1.3, "name": f"Name for 1"}
    )
    producer.producer.send.assert_called_once_with(
        "json-topic", b'{"number1": 1, "number2": 1.3, "name": "Name for 1"}'
    )
