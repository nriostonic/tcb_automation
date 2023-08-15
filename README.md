# Tonic.ai Cloud File Group Automation Script
This Python script automates the process of creating and updating cloud file groups on Tonic.ai using their API. It uses the boto3 library to retrieve file paths from an AWS S3 bucket and interacts with the Tonic.ai API to manage cloud file groups within a specified workspace.

# Prerequisites
Python 3.x

boto3 library for AWS interactions (install using pip install boto3)

requests library for making API requests (install using pip install requests)

json library for formatting data as JSON (install using pip install json)

Access to the Tonic.ai API with a valid API key/token

An active Tonic.ai workspace

# Usage
Clone this repository or download the script (run.py)

Replace the placeholders in the script with your actual API key/token, Tonic URl

Run the script using Python:
```python run.py```

The script will retrieve file paths from the specified S3 bucket, update a cloud file group on Tonic.ai, and provide feedback on the process.
