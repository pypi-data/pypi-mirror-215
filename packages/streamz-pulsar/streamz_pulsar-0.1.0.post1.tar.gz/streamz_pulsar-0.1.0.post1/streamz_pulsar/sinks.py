"""
Create custom streamz sinks.

Classes:

    to_pulsar
"""
import pulsar
from streamz import Stream, Sink
from streamz_pulsar.base import PulsarNode


@Stream.register_api()
class to_pulsar(PulsarNode, Sink):  # pylint: disable=C0103
    """ Writes data in the stream to Pulsar

    This stream accepts a string or bytes object. Call ``flush`` to ensure all
    messages are pushed. Responses from Pulsar are pushed downstream.

    Parameters
    ----------
    topic : string
        The topic which to write
    producer_config : dict
        Settings to set up the stream, see
        https://pulsar.apache.org/api/python/3.2.x/pulsar.Client.html
        Examples:
        service_url: The Pulsar service url eg: pulsar://my-broker.com:6650/

    Examples
    --------
    >>> import pulsar
    >>> from streamz import Stream
    >>> s = Stream.from_pulsar(
    ...     ['my-topic'],
    ...     subscription_name='my-sub',
    ...     consumer_params={'service_url': 'pulsar://localhost:6650'}
    ...     )
    >>> s.map(lambda x: x.decode())
    >>> L = s.sink_to_list()
    """
    def __init__(self, upstream, topic, producer_config, **kwargs):

        self.topic = topic
        self.client = pulsar.Client(**producer_config)
        self.producer = self.client.create_producer(self.topic)

        kwargs["ensure_io_loop"] = True
        Stream.__init__(self, upstream, **kwargs)
        self.stopped = False
        self.polltime = 0.2
        self.futures = []

    def update(self, x, who=None, metadata=None):
        self.producer.send(x)

    def flush(self):
        self.producer.flush()
