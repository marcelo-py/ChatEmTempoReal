# Chat em tempo real

## arquivos importantes
* ```consumers.py```
* ```routing.py```
* ```asgi.py```
* ```settings.py```


### settings.py
```python

    ASGI_APPLICATION = "chat.asgi.application"

    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels_redis.core.RedisChannelLayer",
            "CONFIG": {
                "hosts": [("127.0.0.1", 6379)],
            },
        },
    }

```

### routing.py
Semelhante ao ```urls.py```
Lida com as conexões/urls WebSockets, presente na pasta do projeto ```chat```
```python
    websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<room_name>\w+)$", consumers.ChatConsumer.as_asgi()),
]
```
quando eu digo que ele é parecido com o ```urls.py```
é por que ele chama meio que uma "views.py" para lidar com as requisições no servidor

### consumers.py
Nosso arquivo que lida com as 
`````