# Glutemulo

A HA geo socio demo data ingestor


## Run flask demo

```bash
$ FLASK_ENV=development flask run
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 194-409-049
```

## Test

```bash
$ http -j POST localhost:5000/v1/ uno=1 dos=2`
HTTP/1.0 201 CREATED
Content-Length: 13
Content-Type: text/html; charset=utf-8
Date: Thu, 02 May 2019 14:56:07 GMT
Server: Werkzeug/0.15.2 Python/3.7.2

DATA Received
```

## Producer / Consumer

### Kafka + json

Async producer:

```python
from glutemulo.kafka.producer import JsonKafka
productor = JsonKafka(bootstrap_servers="localhost:9092")
future = productor.produce('simple-topic', dict(dos='BB'))
```

Consumer:
```python
from glutemulo.kafka.consumer import JsonKafka
consumer = JsonKafka('simple-topic', bootstrap_servers="localhost:9092")
for msg in consumer.consume():
    print(msg)
```

### Kafka + Avro

sync producer:

```python
SCHEMA = {
    "type": "record",
    "name": "simpledata",
    "doc": "This is a sample Avro schema to get you started.",
    "fields": [
        {"name": "name", "type": "string"},
        {"name": "number1", "type": "int"},
    ],
}
SCHEMA_ID = 1
```

```python
from glutemulo.kafka.producer import AvroKafka as Producer
productor = Producer(SCHEMA, SCHEMA_ID,bootstrap_servers="localhost:9092")
future = productor.produce('simple-topic-avro', dict(name='Un nombre', number1=10))
```

Consumer:
```python
from glutemulo.kafka.consumer import AvroKafka as Consumer
consumer = Consumer('simple-topic-avro', SCHEMA, SCHEMA_ID, bootstrap_servers="localhost:9092")
for msg in consumer.consume():
    print(msg)
```

## For testing

You can setup a Kafka Consumer using the kafka-console-consumer script that comes with Kafka.

```bash
$ bin/kafka-console-consumer.sh --bootstrap-server 192.168.1.240:9092 --topic pylog --from-beginning

this is an awsome log
```

### Testing With KafkaCat

You ca use an application called KafkaCat.

After the application is installed we will run it in consumer mode (which is the default).

```bash
kafkacat -b 192.168.240.41:9092 -t one-test
```

This should not show anything yet because we haven't sent anything to our topic yet...

To send stuff we can copy any text file into our current directory and send it to our Kafka Topic. In another window, run the following command.

```bash
$ cat README | kafkacat -b 192.168.240.41 -t one-test
```
You should see the output in the first window which has KafkaCat still running in consumer mode.


## Links

- [Zoonavigator](http://localhost:8004). Use 'zoo1' as connection string
- [schema-registry-ui](http://localhost:8001)
- [Rebrow](http://localhost:5001)
- [kafka topics ui](http://localhost:8000)
- [kafka rest proxy](http://localhost:8082)
