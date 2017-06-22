import enum


class Error(enum.Enum):

    # Connection has reached an invalid state.
    QUIC_INTERNAL_ERROR = 0x80000001

    # There were data frames after the a fin or reset.
    QUIC_STREAM_DATA_AFTER_TERMINATION = 0x80000002

    # Control frame is malformed.
    QUIC_INVALID_PACKET_HEADER = 0x80000003

    # Frame data is malformed.
    QUIC_INVALID_FRAME_DATA = 0x80000004

    # Multiple final offset values were received on the same stream
    QUIC_MULTIPLE_TERMINATION_OFFSETS = 0x80000005

    # The stream was cancelled
    QUIC_STREAM_CANCELLED = 0x80000006

    # A stream that is critical to the protocol was closed.
    QUIC_CLOSED_CRITICAL_STREAM = 0x80000007

    # The packet contained no payload.
    QUIC_MISSING_PAYLOAD = 0x80000030

    # STREAM frame data is malformed.
    QUIC_INVALID_STREAM_DATA = 0x8000002E

    # Received STREAM frame data is not encrypted.
    QUIC_UNENCRYPTED_STREAM_DATA = 0x8000003D

    # Received a frame which is likely the result of memory corruption.
    QUIC_MAYBE_CORRUPTED_MEMORY = 0x80000059

    #   RST_STREAM frame data is malformed.
    QUIC_INVALID_RST_STREAM_DATA = 0x80000006

    # CONNECTION_CLOSE frame data is malformed.
    QUIC_INVALID_CONNECTION_CLOSE_DATA = 0x80000007

    # GOAWAY frame data is malformed.
    QUIC_INVALID_GOAWAY_DATA = 0x80000008

    # WINDOW_UPDATE frame data is malformed.
    QUIC_INVALID_WINDOW_UPDATE_DATA = 0x80000039

    # BLOCKED frame data is malformed.
    QUIC_INVALID_BLOCKED_DATA = 0x8000003A

    # PATH_CLOSE frame data is malformed.
    QUIC_INVALID_PATH_CLOSE_DATA = 0x8000004E

    # ACK frame data is malformed.
    QUIC_INVALID_ACK_DATA = 0x80000009

    # Version negotiation packet is malformed.
    QUIC_INVALID_VERSION_NEGOTIATION_PACKET = 0x8000000A

    # Public RST packet is malformed.
    QUIC_INVALID_PUBLIC_RST_PACKET = 0x8000000b

    # There was an error decrypting.
    QUIC_DECRYPTION_FAILURE = 0x8000000c

    # There was an error encrypting.
    QUIC_ENCRYPTION_FAILURE = 0x8000000d

    # The packet exceeded kMaxPacketSize.
    QUIC_PACKET_TOO_LARGE = 0x8000000e

    # The peer is going away.  May be a client or server.
    QUIC_PEER_GOING_AWAY = 0x80000010

    # A stream ID was invalid.
    QUIC_INVALID_STREAM_ID = 0x80000011

    # A priority was invalid.
    QUIC_INVALID_PRIORITY = 0x80000031

    # Too many streams already open.
    QUIC_TOO_MANY_OPEN_STREAMS = 0x80000012

    # The peer created too many available streams.
    QUIC_TOO_MANY_AVAILABLE_STREAMS = 0x8000004c

    # Received public reset for this connection.
    QUIC_PUBLIC_RESET = 0x80000013

    # Invalid protocol version.
    QUIC_INVALID_VERSION = 0x80000014

    # The Header ID for a stream was too far from the previous.
    QUIC_INVALID_HEADER_ID = 0x80000016

    # Negotiable parameter received during handshake had invalid value.
    QUIC_INVALID_NEGOTIATED_VALUE = 0x80000017

    # There was an error decompressing data.
    QUIC_DECOMPRESSION_FAILURE = 0x80000018

    # The connection timed out due to no network activity.
    QUIC_NETWORK_IDLE_TIMEOUT = 0x80000019

    # The connection timed out waiting for the handshake to complete.
    QUIC_HANDSHAKE_TIMEOUT = 0x80000043

    # There was an error encountered migrating addresses.
    QUIC_ERROR_MIGRATING_ADDRESS = 0x8000001a

    # There was an error encountered migrating port only.
    QUIC_ERROR_MIGRATING_PORT = 0x80000056

    # We received a STREAM_FRAME with no data and no fin flag set.
    QUIC_EMPTY_STREAM_FRAME_NO_FIN = 0x80000032

    # The peer received too much data, violating flow control.
    QUIC_FLOW_CONTROL_RECEIVED_TOO_MUCH_DATA = 0x8000003b

    # The peer sent too much data, violating flow control.
    QUIC_FLOW_CONTROL_SENT_TOO_MUCH_DATA = 0x8000003f

    # The peer received an invalid flow control window.
    QUIC_FLOW_CONTROL_INVALID_WINDOW = 0x80000040

    # The connection has been IP pooled into an existing connection.
    QUIC_CONNECTION_IP_POOLED = 0x8000003e

    # The connection has too many outstanding sent packets.
    QUIC_TOO_MANY_OUTSTANDING_SENT_PACKETS = 0x80000044

    # The connection has too many outstanding received packets.
    QUIC_TOO_MANY_OUTSTANDING_RECEIVED_PACKETS = 0x80000045

    # The QUIC connection has been cancelled.
    QUIC_CONNECTION_CANCELLED = 0x80000046

    # Disabled QUIC because of high packet loss rate.
    QUIC_BAD_PACKET_LOSS_RATE = 0x80000047

    # Disabled QUIC because of too many PUBLIC_RESETs post handshake.
    QUIC_PUBLIC_RESETS_POST_HANDSHAKE = 0x80000049

    # Disabled QUIC because of too many timeouts with streams open.
    QUIC_TIMEOUTS_WITH_OPEN_STREAMS = 0x8000004a

    # QUIC timed out after too many RTOs.
    QUIC_TOO_MANY_RTOS = 0x80000055

    # A packet was received with the wrong encryption level (i.e. it should have been
    # encrypted but was not.)
    QUIC_ENCRYPTION_LEVEL_INCORRECT = 0x8000002c

    # This connection involved a version negotiation which appears to have been
    # tampered with.
    QUIC_VERSION_NEGOTIATION_MISMATCH = 0x80000037

    # IP address changed causing connection close.
    QUIC_IP_ADDRESS_CHANGED = 0x80000050

    # Client address validation failed.
    QUIC_ADDRESS_VALIDATION_FAILURE = 0x80000051

    # Stream frames arrived too discontiguously so that stream sequencer
    # buffer maintains too many gaps.
    QUIC_TOO_MANY_FRAME_GAPS = 0x8000005d

    # Connection closed because server hit max number of sessions allowed.
    QUIC_TOO_MANY_SESSIONS_ON_SERVER = 0x80000060
