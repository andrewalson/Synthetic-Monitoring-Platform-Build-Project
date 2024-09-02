# <p align="center"> Develop a Synthetic Monitoring Platform Build Project </p>

<p align="center"> With a projected compound annual growth rate of 15.3% from 2023 to 2028, synthetic monitoring is a rapidly growing global industry. That figure reflects an age where incidents such as the July 2024 worldwide outage of Windows systems caused by a faulty and recklessly-released CrowdStrike sensor configuration update can cause billions in uninsured damages. As such, in our world today, active monitoring is a high-stakes discipline of difficult-to-understate importance. Over this 8-week "Build Project" associated with the Open Avenues Build Fellowship and led by Build Fellow Sonu Gupta, I developed a synthetic monitoring platform that can monitor the performance of an application or system by pinging servers for time-series data from the command line or Flask UI and relaying them through Prometheus to a Grafana dashboard for visualization.</p>

<p align="center">
<img alt="Screenshot 2024-08-23 at 7 32 12 PM" src="https://github.com/user-attachments/assets/68be96cb-f5c3-4023-a848-9ad0f8b2e683">
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
- Displays ping metrics on console while setting Prometheus metrics with `ping_monitor.display_and_expose_results()`.

### Flask Frontend Entry Point & Output Stream

- Python module which integrates Flask microframework to create a frontend for the monitoring platform.
- Accepts YAML path and starts program while redirecting output to a persistent log accessed from homepage.
- Clear previous messages and run on new config with one click.

### Prometheus & Grafana

- Prometheus: Open source monitoring system & alerting tool configured to scrape metrics from the ping monitor.
- Grafana: Open source observability platform & visualization tool with configured time-series data dashboards.

## <p align="center"> Example Dashboard Panels: </p>

<p align="center">
<img alt="Example Dashboard" src="https://github.com/user-attachments/assets/e7034551-6391-4449-bf35-7c5721fb58f5">
</p>

## <p align="center"> Flask UI: </p>

<p align="center">
<img alt="Output Stream" src="https://github.com/user-attachments/assets/d3a63179-5269-46e8-ac37-db32de56c781">
</p>

## <p align="center"> Getting Started </p>

_Pre-requisites: Prometheus & Grafana binaries, Python 3.8+_

- Clone the repository.
- **[Optional]** Add your YAML configuration file to `configs/` directory.
- Add HTTP server port to Prometheus configuration.
- Navigate to Prometheus directory & run Prometheus: `./prometheus --config.file=prometheus.yml`
- Navigate to Grafana directory & run Grafana: `./bin/grafana-server`
- Open and login to Grafana at [http://localhost:3000](http://localhost:3000) with a browser.
- Add Prometheus [http://localhost:9090](http://localhost:9090) as a [data source](https://grafana.com/docs/grafana/latest/datasources/) in Grafana.
- Navigate to root directory of cloned repository.
- Install project dependencies:

```zsh
  pip install -r requirements.txt
```

- **CLI:** Run main script in `main.py` & pass YAML file path with target servers (default provided if no config argument):
  - **Note:** In certain environments use `python3`

```zsh
  python src/main.py configs/example.yml
```

- **Flask UI:** Run `frontend.py` in `flask_frontend` directory & navigate to the development server at [http://127.0.0.1:5000](http://127.0.0.1:5000) in a browser.

```zsh
  flask --app src/flask_frontend/frontend.py run
```

- **If providing custom YAML file (not default provided variety.yaml), format as:**

```
global_settings:
  probes: 4
  interval: 1
  port: 8989

targets:
  - 8.8.8.8
  - example.com
  - another.target.io
```
