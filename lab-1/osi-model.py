import socket
import json
import struct
import pickle
import base64

# Physical Layer: Handles bit-level transmission
class PhysicalLayer:
    def transmit(self, data):
        binary_data = ''.join(format(ord(i), '08b') for i in data)  # Convert to binary
        print(f"[Physical Layer] Transmitting data: {binary_data}\n")
        return binary_data

    def receive(self, data):
        text_data = ''.join(chr(int(data[i:i + 8], 2)) for i in range(0, len(data), 8))  # Convert back to text
        print(f"[Physical Layer] Received data: {text_data}\n")
        return text_data

# Data Link Layer: Adds/removes MAC address and frames
class DataLinkLayer:
    def __init__(self):
        self.mac_address = "AA:BB:CC:DD:EE:FF"

    def add_frame(self, data):
        framed_data = json.dumps({"mac": self.mac_address, "data": data})
        print(f"[Data Link Layer] Adding MAC frame: {framed_data}\n")
        return framed_data

    def remove_frame(self, frame):
        frame_data = json.loads(frame)
        print(f"[Data Link Layer] Removing MAC frame: {frame_data['data']}\n")
        return frame_data["data"]

# Network Layer: Adds/removes IP address and handles routing
class NetworkLayer:
    def __init__(self):
        self.ip_address = "192.168.1.1"

    def add_packet(self, data):
        packet = json.dumps({"ip": self.ip_address, "data": data})
        print(f"[Network Layer] Adding IP packet: {packet}\n")
        return packet

    def remove_packet(self, packet):
        packet_data = json.loads(packet)
        print(f"[Network Layer] Removing IP packet: {packet_data['data']}\n")
        return packet_data["data"]

# Transport Layer: Implements TCP-like sequencing
class TransportLayer:
    def add_tcp_header(self, data):
        segment = json.dumps({"seq": 1, "data": data})
        print(f"[Transport Layer] Adding TCP header: {segment}\n")
        return segment

    def remove_tcp_header(self, segment):
        segment_data = json.loads(segment)
        print(f"[Transport Layer] Removing TCP header: {segment_data['data']}\n")
        return segment_data["data"]

# Session Layer: Manages connection states
class SessionLayer:
    def establish_session(self, data):
        session_data = json.dumps({"session": "active", "data": data})
        print(f"[Session Layer] Establishing session: {session_data}\n")
        return session_data

    def terminate_session(self, session_data):
        session_info = json.loads(session_data)
        print(f"[Session Layer] Terminating session: {session_info['data']}\n")
        return session_info["data"]

# Presentation Layer: Handles encoding and decoding
class PresentationLayer:
    def encode(self, data):
        encoded_data = base64.b64encode(pickle.dumps(data)).decode('utf-8')
        print(f"[Presentation Layer] Encoding data: {encoded_data}\n")
        return encoded_data

    def decode(self, data):
        decoded_data = pickle.loads(base64.b64decode(data))
        print(f"[Presentation Layer] Decoding data: {decoded_data}\n")
        return decoded_data

# Application Layer: Handles user interaction (simulating HTTP request/response)
class ApplicationLayer:
    def send_data(self, message):
        request = f"HTTP REQUEST: {message}"
        print(f"[Application Layer] Sending request: {request}\n")
        return request

    def receive_data(self, response):
        data = response.replace("HTTP RESPONSE: ", "")
        print(f"[Application Layer] Receiving response: {data}\n")
        return data

# Simulation of data transmission
def simulate_osi_model():
    app_layer = ApplicationLayer()
    presentation_layer = PresentationLayer()
    session_layer = SessionLayer()
    transport_layer = TransportLayer()
    network_layer = NetworkLayer()
    data_link_layer = DataLinkLayer()
    physical_layer = PhysicalLayer()

    # Sending Data
    message = input("Enter your message: ")
    app_data = app_layer.send_data(message)
    presentation_data = presentation_layer.encode(app_data)
    session_data = session_layer.establish_session(presentation_data)
    transport_data = transport_layer.add_tcp_header(session_data)
    network_data = network_layer.add_packet(transport_data)
    data_link_data = data_link_layer.add_frame(network_data)
    physical_data = physical_layer.transmit(data_link_data)

    print("\nData Transmitted over Network:\n", physical_data, "\n")

    # Receiving Data
    received_data = physical_layer.receive(physical_data)
    data_link_received = data_link_layer.remove_frame(received_data)
    network_received = network_layer.remove_packet(data_link_received)
    transport_received = transport_layer.remove_tcp_header(network_received)
    session_received = session_layer.terminate_session(transport_received)
    presentation_received = presentation_layer.decode(session_received)
    app_received = app_layer.receive_data(presentation_received)

    print("\nReceived Message:\n", app_received)

simulate_osi_model()
