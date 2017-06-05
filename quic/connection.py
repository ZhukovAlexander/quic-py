

class QUICConection:

    # ======================================================================
    # Constants used in loss recovery
    # https://tools.ietf.org/html/draft-ietf-quic-recovery-03#section-3.2.1
    # ======================================================================
    kMaxTLPs: int = 2

    kReorderingThreshold = 3

    kTimeReorderingFraction = 1 / 8

    kMinTLPTimeout = 10

    kMinRTOTimeout = 200

    kDelayedAckTimeout = 25

    kDefaultInitialRtt = 100

    # ======================================================================
    # variables required to implement congestion control
    # https://tools.ietf.org/html/draft-ietf-quic-recovery-03#section-3.2.2
    # ======================================================================
    loss_detection_alarm = None

    handshake_count: int = None

    tlp_count = None

    rto_count = None

    largest_sent_before_rto = None

    smoothed_rtt = None

    rttvar = None

    reordering_threshold = None

    time_reordering_fraction = None

    loss_time = None

    sent_packets = None

    def __init__(self):
        infinite = float('inf')

        self.loss_detection_alarm.reset()
        self.handshake_count = 0
        self.tlp_count = 0
        self.rto_count = 0

        if (UsingTimeLossDetection()):
            self.reordering_threshold = infinite
            self.time_reordering_fraction = self.kTimeReorderingFraction
        else:
            self.reordering_threshold = self.kReorderingThreshold
            self.time_reordering_fraction = infinite
        self.loss_time = 0
        self.smoothed_rtt = 0
        self.rttvar = 0
        self.largest_sent_before_rto = 0
