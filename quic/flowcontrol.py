
class ReceivedSmallerByteOffset(Exception):
    pass


class FlowController:

    stream_id = None

    contributes_to_conn = False

    conn_params = None

    rtt_stats = None

    bytes_sent = None
    _send_window = None

    last_window_update_time = None

    bytes_read = None
    highest_received = None
    receive_window = None
    receive_window_increment = None
    max_receive_window_increment = None

    def __init__(self, stream_id: int, contributes_to_conn: bool, conn_params: dict, rtt_stats: dict):
        self.stream_id = stream_id
        self.contributes_to_conn = contributes_to_conn
        self.conn_params = conn_params
        self.rtt_stats = rtt_stats

        # cryptographic handshake.
        if stream_id == 0x0:
            self.receive_window = self.receive_window_increment = conn_params.get('recv_conn_fcw')
            self.max_receive_window_increment = conn_params.get('max_recv_conn_fcw')
        else:
            self.receive_window = self.receive_window_increment = conn_params.get('recv_stream_fc_window')
            self.max_receive_window_increment = conn_params.get('max_recv_stream_fcw')

    @property
    def send_window(self):
        if not c._send_window == 0:
            return self._send_window
        if stream_id == 0:
            return self.conn_params.get('send_conn_fcw')
        return self.conn_params.get('send_stream_fcw')

    def update_send_window(self, new: int):
        if new > self.send_window:
            self.send_window = new
            return True
        return False

    @property
    def send_window_size(self):
        return self.send_window - bytes_sent

    def update_highest_received(self, bytes_offset: int):
        if bytes_offset == self.highest_received:
            return 0
        if bytes_offset > self.highest_received:
            incr = bytes_offset - self.highest_received
            self.highest_received = bytes_offset
            return incr
        raise ReceivedSmallerByteOffset
