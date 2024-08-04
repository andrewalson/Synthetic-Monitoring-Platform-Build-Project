import pingparsing
import time


# Ping server function
# Accepts target address, number of probes default 4, interval in seconds default 1
def ping_server(target, count=4, interval=1):
    ping_parser = pingparsing.PingParsing()
    transmitter = pingparsing.PingTransmitter()
    transmitter.destination = target
    transmitter.count = 1

    results = []  # To-return collection for all results added from loop

    # '_' variable not used within loop; starts @ 0, auto-increment upon iteration
    for _ in range(count):

        # Returns raw output in loosely formatted string
        result = transmitter.ping()

        # 'parse()' of pingparsing.py processes & formats raw ping results
        parsed_result = ping_parser.parse(result).as_dict()

        results.append(parsed_result)  # Each individual set of results added to collection

        if _ < count - 1:  # Unless the requested or default count is reached...
            time.sleep(interval)  # Wait for the requested or default interval

    return results


def display_operation_results(results):
    if not results:
        print("No results, check request validity.")
        return

    # Print destination with embedded string
    print(f"Ping Results for {results[0]['destination']}")

    # enumerate()
    for i, result in enumerate(results, 1):
        print(f"\nPing {i}:")
        print(f"Packets Transmitted: {result['packet_transmit']}")
        print(f"Packets Received: {result['packet_receive']}")
        print(f"Packet Loss Rate: {result['packet_loss_rate']}%")
        print(f"Round Trip Time (ms):")
        print(f"  Minimum: {result['rtt_min']}")
        print(f"  Average: {result['rtt_avg']}")
        print(f"  Maximum: {result['rtt_max']}")


def main():
    # User prompts for independent usage
    target = input("Enter target IP address or hostname to ping: ")
    count = int(input("Enter the number of pings to send: "))
    interval = float(input("Enter interval in seconds between pings: "))

    try:
        results = ping_server(target, count, interval)
        display_operation_results(results)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
