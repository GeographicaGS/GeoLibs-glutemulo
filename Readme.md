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
