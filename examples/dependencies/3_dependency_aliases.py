'''
Using Alias allows you rename context dependencies passing
to your function
'''
from propan.app import PropanApp
from propan.brokers import RabbitBroker
from propan.utils import Alias


broker = RabbitBroker("amqp://guest:guest@localhost:5672/")

app = PropanApp(broker)


@app.on_startup
def setup(rabbit: RabbitBroker = Alias("broker")):
    assert rabbit is broker