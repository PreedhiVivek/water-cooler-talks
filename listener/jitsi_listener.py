"""
Jitsi listener service to,
    Invoke the lambda that buzzes colleagues on their Raspberry Pi device,
    when a colleague wants to have water cooler conversations.
"""
#!/usr/bin/env python3
import logging
import json
import os
import time
from logging.handlers import RotatingFileHandler
import boto3
import requests

def get_participants_count(log_obj):
    """
    Returns the participants count in the WaterCoolerTalks Jitsi room.
    """
    participants_count = 0
    try:
        response = requests.get(os.environ['JITSI_ROOM_SIZE_ENDPOINT'])
        if response.status_code == 200:
            participants_count = response.json()['participants']
            log_obj.info(f'{participants_count} participant(s) in the room!')
        elif response.status_code == 404:
            log_obj.info('No participants in room!')
    except requests.exceptions.RequestException as request_error:
        log_obj.error(f'\n Request to Jitsi server errored : \n {request_error}', exc_info=True)
    except Exception as error:
        log_obj.error(f'\n Error encountered: \n {error}', exc_info=True)
    return participants_count

def call_pi_integration_lambda(lambda_client):
    """
    Invokes the Raspberry Pi integration lambda asynchronously.
    """
    payload = {"msg": "Your buddy is on Jitsi. Join in if free."}
    lambda_client.invoke(FunctionName = 'raspberry-notifier',\
                         InvocationType = 'Event',\
                         Payload = json.dumps(payload))

def buzz_colleagues(participants_count, log_obj, lambda_client):
    """
    Buzz colleagues based on the status of BUZZ_FLAG, when the room has participants.
    """
    global BUZZ_FLAG
    try:
        if participants_count > 0:
            if BUZZ_FLAG is False:
                log_obj.info('Buzzing colleagues to chit-chat!')
                # Invoke lambda that integrates with Raspberry Pi to buzz colleagues.
                call_pi_integration_lambda(lambda_client)
                BUZZ_FLAG = True
        else:
            BUZZ_FLAG = False
    except Exception as error:
        log_obj.error(f'\n Error encountered: \n {error}', exc_info=True)

def set_logger():
    """
    Sets the logger for the Jitsi listener.
    """
    current_directory = os.getcwd()
    log_file = os.path.join(current_directory, 'jitsi_listener.log')
    log_formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
    my_handler = RotatingFileHandler(log_file, mode='a', maxBytes=5*1024*1024,\
                                backupCount=2, encoding=None, delay=0)
    my_handler.setFormatter(log_formatter)
    my_handler.setLevel(logging.INFO)
    listener_log = logging.getLogger()
    listener_log.setLevel(logging.INFO)
    listener_log.addHandler(my_handler)
    return listener_log

def setup_listener():
    """
    Initializes Jitsi listener's pre-requisites.
    """
    listener_log = set_logger()
    lambda_client = boto3.client('lambda')
    return listener_log, lambda_client

if __name__ =='__main__':
    BUZZ_FLAG = False
    logger_obj, client = setup_listener()
    while True:
        try:
            buzz_colleagues(get_participants_count(logger_obj),\
                                            logger_obj, client)
            time.sleep(5)
        except Exception as listener_error:
            logger_obj.error(f'\n Error encountered: \n {listener_error}', exc_info=True)
