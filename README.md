IoT API
=======

#### Internet of Things HTTP Restfull API

General API to store telemetry data from several sensors for Internet of Things projects.

Endpoints
---------

This API provide several methods to send and retrieve telemetry data from an IoT Entity.

<small>Before execute the examples change the hostname!</small>

#### POST  /data/for/{entity}
Send data to an entity

```
curl -d "{"any": ["json, "string"]}" http://localhost/data/for/my-device
{
  "entity": "my-device",
  "created": "YYYY-MM-DDThh:mm:ss.s",
  "content": {
    "any": ["json", "string"]
  }
}
```

#### GET   /data/from/{entity}
Get the last 100 telemetry data from an entity.

```
curl http://localhost/data/from/my-device
{
  "results: "[
    {
      "entity": "my-device",
      "created": "YYYY-MM-DDThh:mm:ss.s",
      "content": {
        "a": ["json", "string"]
      }
    },
    ...
  ]
}
```

#### GET   /latest/data/from/{entity}
Get the latest telemetry from an entity

```
curl http://localhost/data/from/my-device
{
  "results: "[
    {
      "entity": "my-device",
      "created": "YYYY-MM-DDThh:mm:ss.s",
      "content": {
        "a": ["json", "string"]
      }
    }
  ]
}
```

#### GET   /listen/data/from/{entity}
Listen to any new telemetry from an entity, using a long polling/comet connection.

```
curl --raw http://localhost/listen/data/from/my-device
{
  "entity": "my-device",
  "created": "YYYY-MM-DDThh:mm:ss.s",
  "content": {
    "a": ["json", "string"]
  }
}
...
```


#### WS    /socket/for/{entity}
Open a WebSocket connection with an entity to two-way communication.

```js
var ws = new WebSocket("ws://localhost/socket/for/my-device");
ws.onopen = function(e) {
   console.log('Connection estabilished.');
}
ws.onerror = function(e) {
    console.error(e);
}
ws.onmessage = function (e) {
   console.log('New telemetry recieved:');
   console.log(e.data);
}
ws.onclose = function(e) {
  if (e.code == 1003) {
    // Something happened!
    console.error(e.reason);
  }
}

function send() {
  var telemetry = {
    any: ["valid", "json", "string"]
  };
  ws.send(JSON.stringify(msg));
}
```

Development
-----------

Install [Boot2Docker](http://boot2docker.io/) and prepare your environment:

```bash
$ boot2docker init
$ boot2docker start
$ $(boot2docker shellinit)
$ docker-compose build
```

Then run the development server:

```bash
$ docker-compose up
```

Access the virtual machine IP:

```
$ boot2docker ip
192.168.59.103
```
