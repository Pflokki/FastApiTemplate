Сервис, который используется для мока основных внешних сервисов в которые идут обращения от сервисов команды рейтинги:
- 

Доступ к мок сервису по следующему url:
* api - `http://host.docker.internal:10500`  (TODO: при совпадении урлов разных сервисов - азделить сервисы на разные порты)
* swagger - `http://localhost:10500/docs/#/`
* rabbitmq-admin - `http://localhost:15672/#/queues`

Так же поднимается инстанс rabbitmq-management
Для создания VHOST и users использовать следующие команды:
```
rabbitmqctl add_vhost vhost_name
rabbitmqctl add_user user password
rabbitmqctl set_permissions -p vhost_name user ".*" ".*" ".*"
```

DSN к кролику: 

* `amqp://user:password@host.docker.internal:5672/vhost_name`