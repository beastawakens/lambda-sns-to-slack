#!/usr/bin/python3.9
import urllib3
import json
import os


http = urllib3.PoolManager()


def lambda_handler(event, context):
    url = os.getenv('SLACK_WEBHOOK_URL')
    
    raw_msg = json.loads(event['Records'][0]['Sns']['Message'])
    
    if 'source' in raw_msg:
        alarm_name = raw_msg['detail']['title']
        new_state = 'severity ' + str(raw_msg['detail']['severity'])
        reason = raw_msg['detail']['type']
        icon = ":skull:"
        region = raw_msg['detail']['region']
    else:
        alarm_name = raw_msg['AlarmName']
        new_state = raw_msg['NewStateValue']
        reason = raw_msg['NewStateReason']
        region = raw_msg['Region']
        icon = ":heart:" if new_state == 'OK' else ":fire:"
    
    msg = {
        "channel": os.getenv('SLACK_CHANNEL'),
        "username": os.getenv('SLACK_USERNAME'),
        "text": f'{icon} *{alarm_name}* state from {region} is now *{new_state}*:\n{reason}',
        "icon_emoji": ":warning:",
    }    


    encoded_msg = json.dumps(msg).encode("utf-8")
    resp = http.request("POST", url, body=encoded_msg)
    print(
        {
            "message": event["Records"][0]["Sns"]["Message"],
            "status_code": resp.status,
            "response": resp.data,
        }
    )
