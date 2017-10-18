# coding:utf-8
import pika
import collections

# 需要发送数据给rabbitmq,需要获取数据从rabbitmq

RABBIT_SERVER = 'localhost'


class SendPublishData:
    def __init__(self):
        self._data = {}
        # self._task = task
        self._connection = pika.BlockingConnection(pika.ConnectionParameters(RABBIT_SERVER))
        self._channel = self._connection.channel()
        self._queue = self._channel.queue_declare(queue='publish', durable=True)
        self._channel.confirm_delivery()

    def send(self, data):
        # _queue对象是个METHOD,里面有个method元素,这个元素里有个queue,为字符串(是_queue的名字)
        if isinstance(data, collections.Mapping):
            self._data = data

            if self._channel.basic_publish('', self._queue.method.queue,
                                           str(self._data),
                                           pika.BasicProperties(delivery_mode=2)):
                print 'Message was send!'
                return True
            else:
                print "Message was lost!,Try again"
                return False
        else:
            print 'Wrong Data type,Try again'
            return False

    def close(self):
        self._channel.close()
        self._connection.close()
        return True

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class GetPublishData:
    def __init__(self):
        self._connection = pika.BlockingConnection(pika.ConnectionParameters(RABBIT_SERVER))
        self._channel = self._connection.channel()
        self._queue = self._channel.queue_declare(queue='publish', durable=True)
        self._currentMessage = None
        self._currentDelivery = None

    def get(self):
        # if self._checkMessageNum():

        if self._currentDelivery:
            return self._currentMessage
        else:
            # consumeAction = self._channel.consume(self._queue.method.queue,True)
            # consumeAciton.close()
            get_frame, properties, body = self._channel.basic_get(self._queue.method.queue)
            self._currentMessage = body
            self._currentDelivery = get_frame

            return self._currentMessage

    def checkout(self):
        if self._currentDelivery:
            self._channel.basic_ack(self._currentDelivery.delivery_tag)
            self._currentMessage = None
            self._currentDelivery = None
            return True
        else:
            print 'Can not checkout current Message!'
            return False

    def _checkMessageNum(self):
        q = self._channel.queue_declare(queue='publish', durable=True)
        return q.method.message_count

    def close(self):
        self._channel.close()
        self._connection.close()
        return True

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
