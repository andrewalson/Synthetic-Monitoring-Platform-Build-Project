import pingparsing
import json


# Ping server function
# Accepts target address, number of probes default 4, interval in seconds default 1
def ping_server(target, count=4, interval=1):

    # Initialize Transmitter instance from the library
    transmitter = pingparsing.PingTransmitter()
    transmitter.destination = target
    transmitter.count = count
    transmitter.ping_option = f"-i {interval}" # Between pings

    # print("Raw result type:", type(transmitter.ping()))
    # print("Raw result:")
    # print(transmitter.ping())

    # Returns PingResult object from Pingparsing library
    return transmitter.ping()


def display_ping_results(ping_result):
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
        print(f"  Minimum: {parsed_result.rtt_min}")
        print(f"  Average: {parsed_result.rtt_avg}")
        print(f"  Maximum: {parsed_result.rtt_max}")
    except Exception as e:
        print(f"Error processing result: {e}")
        print("Raw stdout:")
        print(ping_result.stdout)

def main():
    # User prompts for independent usage
    target = input("Enter target IP address or hostname: ")
    count = int(input("Enter the number of probes: "))
    interval = float(input("Enter interval in seconds between probes: "))

    # Main operation
    try:
        results = ping_server(target, count, interval)
        display_ping_results(results)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
