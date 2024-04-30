import thriftpy2
from thriftpy2.rpc import make_server
import time

timestamp_thrift = thriftpy2.load(
    'timestamp.thrift', module_name='timestamp_thrift')
Timestamp = timestamp_thrift.TimestampService


class TimestampHandler:
    def getCurrentTimestamp(self):
        current_time = int(time.time())
        return timestamp_thrift.Timestamp(unix_timestamp=current_time)


def thrift_server():
    handler = TimestampHandler()
    server = make_server(Timestamp, handler, '127.0.0.1', 10000)
    server.serve()


if __name__ == '__main__':
    handler = TimestampHandler()
    server = make_server(Timestamp, handler, '127.0.0.1', 10000)
    server.serve()
