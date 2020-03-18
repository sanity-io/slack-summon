import os
import requests

# debugging
import logging
from http.client import HTTPConnection  # py3

from flask import abort, Flask, jsonify, request

# opsgenie setup
url = 'https://api.eu.opsgenie.com/v2/alerts'

opsgenie_apikey =  os.environ['OPSGENIEAPIKEY']

auth_header = 'GenieKey {}'.format(opsgenie_apikey)

headers = {
        'Content-Type': 'application/json',
        'Authorization': auth_header
        }
# main

app = Flask(__name__)

def is_request_valid(request):
    is_token_valid = request.form['token'] == os.environ['SLACK_VERIFICATION_TOKEN']
    is_team_id_valid = request.form['team_id'] == os.environ['SLACK_TEAM_ID']

    return is_token_valid and is_team_id_valid


@app.route('/summon', methods=['POST'])
def summon():
    if not is_request_valid(request):
        abort(400)


    summoner = request.form['user_name']
    summon_channel = request.form['channel_name']
    text = request.form['text']

    if "SRE" or "sre" in text:
        data = f"""
        {{
            "message": "SRE has been summoned by \\\"{summoner}\\\" on \\\"{summon_channel}\\\"",
            "description":"A manual way to summon SRE on-call",
            "responders":[
                {{"name":"SRE", "type":"team"}}
            ],
            "priority":"P3"
        }}"""
        #.format(summoner,summon_channel)


        log = logging.getLogger('urllib3')
        log.setLevel(logging.DEBUG)

        # logging from urllib3 to console
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        log.addHandler(ch)

        # print statements from `http.client.HTTPConnection` to console/stdout
        HTTPConnection.debuglevel = 1

        response = requests.post(url,headers=headers,data=data)

        if response.status_code != 202:
            return jsonify(
                response_type='in_channel',
                text='Summoning failed. Try alternate means of raising SRE.',
                )
        return jsonify(
            response_type='in_channel',
            text='On-Call SRE has been summoned. Awaiting portal.',
            )
    else:
        return jsonify(
            response_type='in_channel',
            text='No summoning method defined for "{}"...'.format(text),
            )

