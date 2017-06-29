import math


INITIAL_RTT = 100 * 1000

RTT_ALPHA = 0.125

ONE_MINUS_ALPHA = 1 - RTT_ALPHA

RTT_BETA = 0.25

ONE_MINUS_BETA = 1 - RTT_BETA

HALF_WINDOW = 0.5

QUARTER_WINDOW = 0.25


class RTTSample:
    __slots__ = ('rtt', 'time')


class RTTStats:

    initial_rtt = INITIAL_RTT

    recent_min_rtt_window = None

    min_rtt = None

    latest_rtt = None

    smoothed_rtt = None

    mean_deviation = None

    num_min_rtt_samples_remaining = None

    new_min_rtt = None

    recent_rtts = []

    recent_min_rtt = None

    half_window_rtt = None

    quarter_window_rtt = None

    def __init__(self, initial_rtt, recent_min_rtt_window):
        self.initial_rtt = initial_rtt
        self.recent_min_rtt_window = recent_min_rtt_window

    def update_rtt(self, send_delta, ack_delay, now):
        if send_delta == math.inf or send_delta <= 0:
            return

        if self.min_rtt == 0 or self.min_rtt > send_delta:
            self.min_rtt = send_delta

        self.update_recent_min_rtt(send_delta, now)

        sample = send_delta if send_delta < ack_delay else send_delta - ack_delay

        self.latest_rtt = sample

        if self.smoothed_rtt == 0:
            self.smoothed_rtt = sample
            self.mean_deviation = sample / 2
        else:
            self.mean_deviation = ONE_MINUS_BETA * self.mean_deviation + RTT_BETA * abs(self.smoothed_rtt - sample)
            self.smoothed_rtt = ONE_MINUS_ALPHA * self.smoothed_rtt + RTT_ALPHA * sample

    def update_recent_min_rtt(self, sample, now):
        if self.num_min_rtt_samples_remaining > 0:
            self.num_min_rtt_samples_remaining -= 1
            if self.new_min_rtt.rtt == 0 or sample <= self.new_min_rtt.rtt:
                self.new_min_rtt = (sample, now)

            if self.num_min_rtt_samples_remaining == 0:
                self.recent_rtts = [self.new_min_rtt] * 3

        for i, rtt in enumerate(self.recent_rtts):
            self.recent_rtts[i] = min(rtt, sample)
            if rtt[0] < now - self.recent_min_rtt_window * 1 / 2 ** (len(self.recent_rtts) - i):
                if i == 0:
                    self.recent_rtts[i] = sample
                else:
                    self.recent_rtts[i] = self.recent_rtts[i - 1]


    def sample_new_recent_min_rtt(self, num_samples: int):
        self.num_min_rtt_samples_remaining = num_samples

    def on_connection_migration(self):
        self.latest_rtt = 0
        self.min_rtt = 0
        self.smoothed_rtt = 0
        self.mean_deviation = 0
        self.initial_rtt = INITIAL_RTT
        self.num_min_rtt_samples_remaining = 0
        self.recent_min_rtt_window = math.inf
        self.recent_rtts = []

    def expire_smoothed_metrics(self):
        self.mean_deviation = max(self.mean_deviation, self.smoothed_rtt - self.latest_rtt)
        self.smoothed_rtt = max(self.smoothed_rtt, latest_rtt)






