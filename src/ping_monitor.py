import pingparsing
import json
from prometheus_client import Gauge

# Define Prometheus metrics
round_trip_time = Gauge('round_trip_time',
                        'Ping latency in milliseconds',
                        ['target'])
packet_loss_rate = Gauge('packet_loss_rate',
                         'Packet loss rate percentage',
                         ['target'])

def ping_server(target, count=4, interval=1):
    transmitter = pingparsing.PingTransmitter()
    transmitter.destination = target
    transmitter.count = count
    transmitter.ping_option = f"-i {interval}"
    return transmitter.ping()

def display_and_expose_results(ping_result, target):
    if not ping_result:
        print("No ping results, check request validity.")
        return

    if ping_result.returncode != 0:
        print(f"Ping failed with return code: {ping_result.returncode}")
        print("Error output:")
        print(ping_result.stderr)
        return

    ping_parser = pingparsing.PingParsing()
    try:
        parsed_result = ping_parser.parse(ping_result.stdout)

        print("\nPing Results:")
        print(f"Destination: {parsed_result.destination}")
        print(f"Packets Transmitted: {parsed_result.packet_transmit}")
        print(f"Packets Received: {parsed_result.packet_receive}")
        print(f"Packet Loss Rate: {parsed_result.packet_loss_rate}%")
        print(f"Round Trip Time (ms):")
        print(f"  Average: {parsed_result.rtt_avg}")

        # Update Prometheus metrics
        round_trip_time.labels(target=target).set(parsed_result.rtt_avg)
        packet_loss_rate.labels(target=target).set(parsed_result.packet_loss_rate)

    except Exception as e:
        print(f"Error processing result: {e}")
        print("Raw stdout:")
        print(ping_result.stdout)

def main():
    target = input("Enter target IP address or hostname: ")
    count = int(input("Enter the number of probes: "))
    interval = float(input("Enter interval in seconds between probes: "))

    try:
        results = ping_server(target, count, interval)
        display_and_expose_results(results, target)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()