"""
Local Measure
Bennett Borofka, Solutions Architect - bennett@getlocalmeasure.com

This Python script is intended for use in a Python 3.8 Lambda Function,
invoked by a Contact Flow in Amazon Connect. It accepts the following
function input attributes: summary, description.

Required dependencies to include with the Lambda function:
- certifi
- chardet
- idna
- requests

References:
https://docs.aws.amazon.com/lambda/latest/dg/lambda-python.html
https://docs.aws.amazon.com/lambda/latest/dg/python-package.html
https://developer.atlassian.com/cloud/jira/software/rest/intro/
"""

import json
import requests

def lambda_handler(event, context):
    # Setup variables specific to your Jira Software Cloud instance
    jira_company = "cloud-company"
    jira_project_key = "TS"
    jira_issuetype_id = "10005"
    url = "https://" + jira_company + ".atlassian.net/rest/api/3/issue"
    summary = event["Details"]["Parameters"]["summary"]
    jira_issue_description = event["Details"]["Parameters"]["description"]

    # Body format JSON for /rest/api/3/issue POST
    body = {
        "fields": {
            "summary": summary,
            "project": {
                "key": jira_project_key
            },
            "issuetype": {
                "id": jira_issuetype_id
            },
            "description": {
                "type": "doc",
                "version": "1",
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {
                                "text": jira_issue_description,
                                "type": "text"
                            }
                        ]
                    }
                ]
            }
        }
    }

    # Convert Python dictionary to JSON
    payload = json.dumps(body)

    # Setup Headers
    headers = {
        # Add a 'authorization' Environment Variable to your Lambda function
        # and use the Base64 value of your API token
        'Authorization': authorization,
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return {
        'statusCode': 200,
        'body': json.dumps(response.text)
    }
