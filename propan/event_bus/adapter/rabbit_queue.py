from typing import NoReturn, Callable

from asyncio import AbstractEventLoop
import aio_pika

from propan.logger.model.usecase import LoggerUsecase
from propan.logger.adapter.empty import EmptyLogger

from propan.event_bus.model.bus_connection import ConnectionData
from propan.event_bus.model.bus_usecase import EventBusUsecase
from propan.event_bus.push_back_watcher import PushBackWatcher


class AsyncRabbitQueueAdapter(EventBusUsecase):
    logger: LoggerUsecase
    _watcher: PushBackWatcher
    _connection: aio_pika.RobustConnection
    _channel: aio_pika.RobustChannel
    _process_message: Callable

    def __init__(self, logger: LoggerUsecase = EmptyLogger()):
        self.logger = logger
        self._watcher = PushBackWatcher()

    async def connect(
        self,
        connection_data: ConnectionData,
        loop: AbstractEventLoop,
    ) -> NoReturn:
        self._connection = await aio_pika.connect_robust(
            host=connection_data.host,
            login=connection_data.login,
            password=connection_data.password,
            virtualhost=connection_data.virtualhost,
            loop=loop
        )

    async def init_channel(self, max_consumers: int = None) -> NoReturn:
        self._channel = await self._connection.channel()
        if max_consumers:
            await self._channel.set_qos(prefetch_count=max_consumers)

    async def set_queue_handler(
        self, queue_name: str,
        handler: Callable, retrying_on_error: bool = False
    ) -> NoReturn:
        queue = await self._channel.declare_queue(queue_name)
        self._process_message = self.retry_on_error(queue_name)(handler) if retrying_on_error else handler
        self.logger.success('[*] Waiting for messages. To exit press CTRL+C')
        await queue.consume(self.handle_message)

    async def publish_message(self, queue_name: str, message: str) -> NoReturn:
        await self._channel.default_exchange.publish(
            aio_pika.Message(str(message).encode()),
            routing_key=queue_name,
        )

    async def handle_message(self, message: aio_pika.IncomingMessage) -> NoReturn:
        body = message.body.decode()
        async with message.process():
            self.logger.info(f"[x] Received {body}")
            await self._process_message(body)

    async def close(self):
        await self._connection.close()

    def retry_on_error(self, queue_name):
        def decorator(func):
            async def wrapper(message: str):
                try:
                    response = await func(message)

                except Exception as e:
                    self._watcher.add(message)
                    if not self._watcher.is_max(message):
                        self.logger.error(f'In "{message}" error is occured. Pushing back it to rabbit.')
                        await self.publish_message(queue_name, message)
                    else:
                        self.logger.error(f'"{message}" already retried {self._watcher.max_tries} times. Skipped.')
                    raise e

                else:
                    self._watcher.remove(message)
                    return response
            return wrapper
        return decorator