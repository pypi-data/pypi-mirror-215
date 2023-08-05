import grpc
from .cli_pb2_grpc import CliStub
from .cli_pb2 import CliRequest
from retry import retry
name = "dingman"

class Cli:
    def __init__(self, secret, address):
        self.secret = secret
        self.address = address
        self.channel = None

    def set_secret(self, secret):
        self.secret = secret
        if self.channel:
            self.channel.close()

    def set_address(self, address):
        self.address = address
        if self.channel:
            self.channel.close()

    def _wait_channel_ready(state):
        if not state == grpc.ChannelConnectivity.READY:
            print(f'channel is in state {state}, trying to reconnect...')

    def run(self, cmdline):
        try:
            ret = self.run_command(cmdline)
        except Exception as e:
            ret = '{"error":"Can not run the command, exception '+str(e)+'"}'
            if self.channel:
                self.channel.close()
                self.channel = None
        return ret

    @retry(tries=2, delay=5)
    def run_command(self, cmdline):
        # NOTE(gRPC Python Team): .close() is possible on a channel and should be
        # used in circumstances in which the with statement does not fit the needs
        # of the code.
        ret = ''
        if not self.channel:
        	options = [('grpc.max_receive_message_length', 16 * 1024 * 1024)]
        	self.channel = grpc.insecure_channel(self.address, options=options)
        self.channel.subscribe(self._wait_channel_ready, try_to_connect=True)
        #print(self.channel)
        stub = CliStub(self.channel)
        response = stub.Command(CliRequest(secret=self.secret, command=cmdline))
        ret = response.message
        self.channel.unsubscribe(self._wait_channel_ready)
        
        return ret
