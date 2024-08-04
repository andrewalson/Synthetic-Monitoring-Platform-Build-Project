# Build a Synthetic Monitoring Platform

## YAML Configuration File Parser
Write a Python program to read the YAML file and gracefully handle errors to read configuration files in our project.

**Additional Notes:**
- Consider using a try...except block for error handling.
- Use the ‘yaml.safe_load’ method to prevent arbitrary code execution risks. 
- Clearly handle different error scenarios: File not found, invalid YAML syntax, etc.
- Provide meaningful error messages to the user for easier debugging.

## Network Connectivity Monitor
Write a Python program that leverages the pingparsing library to monitor network connectivity.
- Take user input and ping a server
- Extract & present key metrics on console 

## Ping Monitor
Integrate the YAML file parser and network connectivity monitor.
- Read YAML file and fetch a list of servers
- Ping each server after given interval
- Fetch & display ping metrics on console