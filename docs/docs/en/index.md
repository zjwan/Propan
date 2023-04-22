<p align="center">
    <img src="assets/img/logo-no-background.png" alt="Propan logo" style="height: 250px; width: 600px;"/>
</p>

<p align="center">
    <a href="https://github.com/Lancetnik/Propan/actions/workflows/tests.yml" target="_blank">
        <img src="https://github.com/Lancetnik/Propan/actions/workflows/tests.yml/badge.svg" alt="Tests coverage"/>
    </a>
    <a href="https://coverage-badge.samuelcolvin.workers.dev/redirect/lancetnik/propan" target="_blank">
        <img src="https://coverage-badge.samuelcolvin.workers.dev/lancetnik/propan.svg" alt="Coverage">
    </a>
    <a href="https://pypi.org/project/propan" target="_blank">
        <img src="https://img.shields.io/pypi/v/propan?label=pypi%20package" alt="Package version">
    </a>
    <a href="https://pepy.tech/project/propan" target="_blank">
        <img src="https://static.pepy.tech/personalized-badge/propan?period=total&units=international_system&left_color=grey&right_color=blue&left_text=Downloads" alt="downloads"/>
    </a>
    <br/>
    <a href="https://pypi.org/project/propan" target="_blank">
        <img src="https://img.shields.io/pypi/pyversions/propan.svg" alt="Supported Python versions">
    </a>
    <a href="https://github.com/Lancetnik/Propan/blob/main/LICENSE" target="_blank">
        <img alt="GitHub" src="https://img.shields.io/github/license/Lancetnik/Propan?color=%23007ec6">
    </a>
</p>


# Propan

**Propan** - just *<s>an another one HTTP</s>* a **declarative Python MQ framework**. It's following by [*fastapi*](https://fastapi.tiangolo.com/ru/),
simplify Message Brokers around code writing and provides a helpful development toolkit, which existed only in HTTP-frameworks world until now.

It's designed to create reactive microservices around <a href="https://microservices.io/patterns/communication-style/messaging.html" target="_blank">Messaging Architecture</a>.

It is a modern, high-level framework on top of popular specific Python brokers libraries, based on [*pydantic*](https://docs.pydantic.dev/) and [*fastapi*](https://fastapi.tiangolo.com/ru/), [*pytest*](https://docs.pytest.org/en/7.3.x/) concepts.

!!! warning "Under development"
    The main functional was written, as tests were. But, breaking changes are still able to be until **0.1.0** version. All of these changes will be described at [CHANGELOG](/Propan/11_CHANGELOG/), so watch by releases.

---

## The key features are

* **Easy**: Designed to be easy to use and learn.
* **Intuitive**: Great editor support. Autocompletion everywhere.
* [**Dependencies management**](#dependencies): Minimize code duplication. Multiple features from each argument and parameter declaration.
* [**Integrations**](#http-frameworks-integrations): **Propan** is ready to use in pair with [any HTTP framework](https://lancetnik.github.io/Propan/5_integrations/1_integrations-index/) you want
* **MQ independent**: Single interface to popular MQ:
    * **NATS** (based on [nats-py](https://github.com/nats-io/nats.py)) 
    * **RabbitMQ** (based on [aio-pika](https://aio-pika.readthedocs.io/en/latest/)) 
* [**Greate to develop**](#cli-power): CLI tool provides great development experience:
    * framework-independent way to rule application environment
    * application code hot reloading

---

## Declarative

With declarative tools you should define **what you need to get**. With traditional imperative tools you should write **what you need to do**.

Take a look at classic imperative tools, such as [aio-pika](https://aio-pika.readthedocs.io/en/latest/), [pika](https://pika.readthedocs.io/en/stable/), [nats-py](https://github.com/nats-io/nats.py), etc. 

This is the **Quickstart** with the *aio-pika*:

```python
import asyncio
import aio_pika

async def main():
    connection = await aio_pika.connect_robust(
        "amqp://guest:guest@127.0.0.1/"
    )

    queue_name = "test_queue"

    async with connection:
        channel = await connection.channel()

        queue = await channel.declare_queue(queue_name)

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    print(message.body)

asyncio.run(main())
```

**aio-pika** is a really great tool with a really easy learning curve. But it's still imperative. You need to *connect*, declare *channel*, *queues*, *exchanges* by yourself. Also, you need to manage *connection*, *message*, *queue* context to avoid any troubles.

It is not a bad way, but it can be easy.

```python
from propan import PropanApp, RabbitBroker

broker = RabbitBroker("amqp://guest:guest@localhost:5672/")

app = PropanApp(broker)

@broker.handle("test_queue")
async def base_handler(body):
    print(body)
```

This is the **Propan** declarative way to write the same code. That is so much easier, isn't it?

---

## Supported MQ brokers

!!! note "Need your help"
    The framework is now actively developing. We have a very long list of what has yet to be implemented and various brokers are only part of it. If you want to implement something from this list or help in any other way, take a look [here](/Propan/7_contributing/1_todo/)

|              | async                                                   | sync                 |
|--------------|:-------------------------------------------------------:|:--------------------:|
| **RabbitMQ** | :heavy_check_mark: **stable** :heavy_check_mark:        | :mag: planning :mag: |
| **Nats**     | :warning: **beta** :warning:                            | :mag: planning :mag: |
| **NatsJS**   | :hammer_and_wrench: **in progress** :hammer_and_wrench: | :mag: planning :mag: |
| **MQTT**     | :mag: planning :mag:                                    | :mag: planning :mag: |
| **REDIS**    | :mag: planning :mag:                                    | :mag: planning :mag: |
| **Kafka**    | :mag: planning :mag:                                    | :mag: planning :mag: |
| **SQS**      | :mag: planning :mag:                                    | :mag: planning :mag: |