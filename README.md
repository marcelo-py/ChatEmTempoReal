# Chat em tempo real
Se for cair de cara nisso sem saber nada (como eu no começo), lembre-se que as urls que direcionam para uma pagina especifica não influenciam nas urls das conexões websockes.

## Instale
Clone esse repositório e ```pip install -r requirements.txt```

**OU**
daphene ```python -m pip install -U channels["daphne"]```
adicione como uma aplicação
```python
# chat/settings.py
INSTALLED_APPS = [
    'daphne',
    'chat',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
```

```python3 -m pip install channels_redis```

Docker e Redis e rode-os ```docker run -p 6379:6379 -d redis:5```


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
é por que ele chama meio que uma "views.py" (```consumers.ChatConsumer.as_asgi()```) para lidar com as requisições no servidor

### consumers.py
Responsável por receber as mensagens WebSocket de entrada e produzir uma resposta WebSocket de saída.
Melhor ver ele como o "views.py" para o WebSocket com suas particularidades.
Para tal você precisará enviar as mensagens para o grupo correto acessando o scopo da sua url WebSocket
ex descrito nele:
```python
# room_name está na expressão regular da rota em routing.py
# aqui está pegando o valor de room_name para criar um grupo
# pessoas no canal desse grupo receberão as mensagens
self.room_name = self.scope["url_route"]["kwargs"]["room_name"] 
```
você pode criar links personalisados para que somente duas pessoas entre nesse canal e se comunicarem entre si, basta criar um link com um identificador para as duas pessoas, você pode tratar disso criando uma view e direcionando quem os dois usuarios que clicar no link para ela.

