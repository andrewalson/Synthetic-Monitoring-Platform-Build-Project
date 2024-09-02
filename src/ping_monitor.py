import pingparsing
import json
from prometheus_client import Gauge

# Define Prometheus metrics
round_trip_time_average = Gauge('round_trip_time_average',
                        'Average ping latency in milliseconds',
                        ['target'])
round_trip_time_best = Gauge('round_trip_time_best',
                        'Fastest ping latency in milliseconds',
                        ['target'])
round_trip_time_worst = Gauge('round_trip_time_worst',
                        'Slowest ping latency in milliseconds',
                        ['target'])
packet_loss_rate = Gauge('packet_loss_rate',
                         'Packet loss rate percentage',
                         ['target'])

def ping_server(target, count=5, interval=1):
    '''
    This function uses the pingparsing library to send ICMP echo requests (pings)
    to the specified target servers and return the results as PingResult object.

    Args:
        target (str): The IP address or hostname of the target server.
        count (int, optional): The number of ping requests to send. Defaults to 4.
        interval (int, optional): The interval between ping requests in seconds. Defaults to 1.
    '''
    transmitter = pingparsing.PingTransmitter()
    transmitter.destination = target
    transmitter.count = count
    transmitter.ping_option = f"-i {interval}"
    return transmitter.ping()

def display_and_expose_results(ping_result, target):
    '''
    This function takes the raw ping results, parses them, displays them in a
    human-readable format, and updates Prometheus metrics with the results.
    '''
    output = []
    if not ping_result:
        output.append("No ping results, check request validity.")
        return "\n".join(output)

    if ping_result.returncode != 0:
        output.append(f"Ping failed with return code: {ping_result.returncode}")
        output.append("Error output:")
        output.append(ping_result.stderr)
        return "\n".join(output)

    ping_parser = pingparsing.PingParsing()
    try:
        parsed_result = ping_parser.parse(ping_result.stdout)

        output.append("\nPing Results:")
        output.append(f"Destination: {parsed_result.destination}")
        output.append(f"Packets Transmitted: {parsed_result.packet_transmit}")
        output.append(f"Packets Received: {parsed_result.packet_receive}")
        output.append(f"Packet Loss Rate: {parsed_result.packet_loss_rate}%")
        output.append(f"Average Round Trip Time: {parsed_result.rtt_avg} ms")
        output.append(f"Local Best Round Trip Time: {parsed_result.rtt_min} ms")
        output.append(f"Local Worst Round Trip Time: {parsed_result.rtt_max} ms")

        round_trip_time_average.labels(target=target).set(parsed_result.rtt_avg)
        round_trip_time_best.labels(target=target).set(parsed_result.rtt_min)
        round_trip_time_worst.labels(target=target).set(parsed_result.rtt_max)
        packet_loss_rate.labels(target=target).set(parsed_result.packet_loss_rate)

    except Exception as e:
        output.append(f"Error processing result: {e}")
        output.append("Raw stdout:")
        output.append(ping_result.stdout)

    return "\n".join(output)

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