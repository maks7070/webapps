import thriftpy2
from thriftpy2.rpc import make_client
from thriftpy2.transport.buffered.cybuffered import TTransportException

timestamp_thrift = thriftpy2.load(
    'timestamp.thrift', module_name='timestamp_thrift')
Timestamp = timestamp_thrift.TimestampService


def make_timestamp_rpc_call():
    try:
        print('here')
        client = make_client(timestamp_thrift.TimestampService, '127.0.0.1', 10000)
        print('here1')
        tstamp = client.getCurrentTimestamp().unix_timestamp
        print('ts', tstamp)
        return tstamp
    except TTransportException as e:
        print('Error here', e)
    except Exception as e:
        print('Error2:', e)


if __name__ == '__main__':
    print(make_timestamp_rpc_call())