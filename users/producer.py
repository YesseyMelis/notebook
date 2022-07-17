import uuid

import pika
import json

params = pika.URLParameters('amqps://mcmaaeit:gn6IUolkO-1VI-7ieVW30COo-_Po71RC@sparrow.rmq.cloudamqp.com/mcmaaeit')

connection = pika.BlockingConnection(params)

channel = connection.channel()


class UserInfoRpcClient(object):

    def __init__(self):
        self.connection = pika.BlockingConnection(params)

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

        self.response = None
        self.corr_id = None

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='info',
            properties=pika.BasicProperties(
                content_type='user_info',
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=json.dumps(''))
        self.connection.process_data_events(time_limit=None)
        return self.response


def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key='info', body=json.dumps(body), properties=properties)
