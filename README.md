# Tonic.ai Cloud File Group Automation Script
This Python script automates the process of updating cloud file groups and generating data on Tonic via API. It uses the boto3 library to retrieve the X most recent files in a designated AWS S3 bucket and then updates a respective filegroup within a workspace. The code reads from the parameter.json file in order to determine which filegroups to update and generate data for as well as how many files it needs to pull from S3.

# Prerequisites
Python 3.x

boto3 library for AWS interactions (install using pip install boto3)

requests library for making API requests (install using pip install requests)

json library for formatting data as JSON (install using pip install json)

Access to the Tonic.ai API with a valid API key/token stored in AWS Secrets Manager

An active Tonic.ai workspace

# Usage
Clone this repository or download the script (run.py)

Replace the placeholder in the script with your actual Tonic URl

Update the Parameter file

Run the script using Python:
```python run.py```

The script will retrieve file paths from the specified S3 bucket, update a cloud file group on Tonic.ai, and provide feedback on the process.
