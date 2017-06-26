
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


class FlowControlManager:

    conn_params = None

    rtt_stats = None

    straem_flow_controllers = None

    conn_flow_controller = None

    def __init__(self, conn_params: dict, rtt_stats: dict):
        self.conn_params = conn_params
        self.rtt_stats = rtt_stats
        self.conn_flow_controller = FlowController(0, False, conn_params, rtt_stats)
        self.straem_flow_controllers = {0: self.conn_flow_controller}

    def new_stream(self, stream_id: int):
        try:
            self.conn_flow_controller[stream_id]
        except KeyError as e:
            fc = FlowController(stream_id, True, self.conn_params, self.rtt_stats)
            self.straem_flow_controllers[stream_id] = fc

    def remove_stream(self, stream_id: int):
        del self.straem_flow_controllers[stream_id]

    def update_highest_received(self, stream_id: int, bytes_offset: int):
        fc = self.straem_flow_controllers[stream_id]
        inc = fc.update_highest_received(bytes_offset)

        if fc.check_flow_control_vialotion():
            # TODO: put some real exception here
            raise Exception(Error.QUIC_FLOW_CONTROL_RECEIVED_TOO_MUCH_DATA.value)

        if fc.contributes_to_conn:
            self.conn_flow_controller.highest_received += bytes_offset
            if check_flow_control_vialotion:
                # TODO: put some real exception here
                raise Exception(Error.QUIC_FLOW_CONTROL_RECEIVED_TOO_MUCH_DATA.value)

    def reset_stream(self, stream_id: int, bytes_offset: int):
        return self.update_highest_received(stream_id, bytes_offset)

    def add_bytes_read(self, stream_id: int, n: int):
        fc = self.straem_flow_controllers[stream_id]

        fc.add_bytes_read(n)
        if fc.contributes_to_conn:
            self.conn_flow_controller.add_bytes_read(n)

    def get_window_updates(self):
        res = []
        for sid, fc in self.straem_flow_controllers.items():
            need, new_incr, offset = fc.maybe_update_window()
            if need:
                res.append((sid, offset))
                if fc.contributes_to_conn and new_incr =! 0:
                    self.conn_flow_controller.ensure_min_window_increment(new_incr * 1.5)  # Chromium

        return res

    def get_receive_window(self, stream_id: int):
        if stream_id == 0:
            return f.conn_flow_controller.receive_window
        return self.straem_flow_controllers[stream_id].receive_window

    def add_bytes_sent(self, stream_id: int, n: int):
        fc = self.straem_flow_controllers[stream_id]
        fc.add_bytes_sent(n)
        if fc.contributes_to_conn:
            self.conn_flow_controller.add_bytes_sent(n)

    def send_window_size(self, stream_id: int):
        fc = self.straem_flow_controllers[stream_id]
        res = fc.send_window_size
        if fc.contributes_to_conn:
            return min(res, self.conn_flow_controller.send_window_size)
        return res

    def remaining_conn_window_size(self):
        return self.conn_flow_controller.send_window_size

    def update_window(self, stream_id: int, bytes_offset: int):
        (self.conn_flow_controller if stream_id == 0
         else self.straem_flow_controllers[stream_id]).update_send_window(n)
