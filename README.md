# <p align="center"> Develop a Synthetic Monitoring Platform Build Project </p>

<p align="center"> With a projected compound annual growth rate of 15.3% from 2023 to 2028, synthetic monitoring is a rapidly growing global industry. That figure reflects an age where incidents such as the July 2024 worldwide outage of Windows systems caused by a faulty and recklessly-released CrowdStrike sensor configuration update can cause billions in uninsured damages. As such, in our world today, active monitoring is a high-stakes discipline of difficult-to-understate importance. Over this 8-week "Build Project" associated with the Open Avenues Build Fellowship and led by Build Fellow Sonu Gupta, I developed a synthetic monitoring platform that can monitor the performance of an application or system by pinging servers for time-series data and relaying them through Prometheus to a Grafana dashboard for visualization.</p>

<p align="center">
<img width="917" alt="Screenshot 2024-08-23 at 7 32 12 PM" src="https://github.com/user-attachments/assets/68be96cb-f5c3-4023-a848-9ad0f8b2e683">
</p>

## <p align="center"> System Components: </p>
### YAML Configuration File Parser
- Python module which reads & parses YAML configuration files to return as a Python dictionary.
- Detects top-level keys & common configuration types based on YAML structure when ran independently.
- Handles various error scenarios such as file not found, invalid YAML syntax, etc.

### Network Connectivity Monitor
- Python module which leverages **'pingparsing'** library to monitor network connectivity.
- Takes targets, probes, and interval from user input, pings server(s) after given interval, parses results.
- Initializes Prometheus metrics for each target server and each latency/packet loss metric returned.
- Extracts & present key metrics on console with confirmation of updating Prometheus metrics.

### Integrated Modules @ main.py
- Main Python script which integrates the YAML file parser and network connectivity monitor modules.
- Starts HTTP server (in prometheus.yml) on port 8989.
- Takes command line argument for YAML file path (else default provided).
- Reads YAML file and fetches a list of servers and pings each target server after given interval.
- Displays ping metrics on console while setting Prometheus metrics with ```ping_monitor.display_and_expose_results()```.

### Prometheus & Grafana
- Prometheus: Open source monitoring system & alerting tool configured to scrape metrics from the ping monitor.
- Grafana: Open source observability platform & visualization tool with configured time-series data dashboards.

## <p align="center"> Example Dashboard Panels: </p>
<p align="center">
<img width="930" alt="Screenshot 2024-08-23 at 10 32 17 PM" src="https://github.com/user-attachments/assets/cc7df356-f226-4503-8b8c-07db4d734ba1">
</p>

## <p align="center"> Getting Started </p>
_Pre-requisites: Prometheus & Grafana binaries, Python 3.8+_
- Clone the repository
- Add HTTP server port to Prometheus config
- Navigate to Prometheus directory & run Prometheus './prometheus'
- Navigate to Grafana directory & run Grafana './bin/grafana-server'
- Open and login to Grafana at localhost:3000
- Add Prometheus (localhost:9090) as a data source in Grafana
- Navigate to root directory of cloned repository
- Install dependencies, run main script & pass YAML file with target servers (default provided):
- **Note:** In certain environments use ```python3```
```bash
  pip install -r requirements.txt
  cd src/
  python main.py example.yml
```
- **If providing custom YAML file (not default provided targets_probes_intervals.yaml), format as:**
```
global_settings:
  probes: 4
  interval: 1

targets:
  - 8.8.8.8
  - example.com
  - another.target.io
```
