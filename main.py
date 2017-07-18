"""
This is the part of piCamTrap, copyright @ Wenlong Liu.
Created on July 15,2017

This script will publish data to MQTT sever.  For now, it is a local sever.

Platform: Raspberry Pi 3 Model B.
"""

import os
import logging
import time
import yaml
import picamera

import paho.mqtt.subscribe as subscribe
import paho.mqtt.publish as publish

from gupload import auto_drive, upload_to_cloud
from tweet_pic import tweet_auth, update_pic

# for PIR motion method.  We have another method comming.
import PIR_motion 


def _config(file):
    with open(file) as f:
         config = yaml.load(f)
    return config


def _get_time():
    return time.strftime("%Y-%m-%d %H:%M:%S")


def _take_image(cam):
    current = _get_time()
    path = '/home/pi/github/piCamTrap/rawcam/'
    file_name = current + ".jpg"
    file_path = path + file_name
    # Try to take a picture, if not, save to logging.
    #try:
    cam.capture(file_path)
    logging.info("Take a picture at: {}".format(current))
    time.sleep(0.5)

    return file_path
'''
    except:
        print('Failed to take a pic!')
        logging.debug("Failed to take a picture at: {}".format(current))
        time.sleep(0.5)
'''


def _publish(topic, payload=None, qos=0, port=1883, client_id=""):

    publish.single(topic, payload=payload, qos=qos, port=port, client_id=client_id)
    logging.info("Publish a message at: {}".format(_get_time()))


def _subscribe(topic):
    msg = subscribe.simple(topic)
    message = msg.payload.decode()
    results = yaml.load(message)

    return results


def _filter(results, _targets, confidence_threshold):
    findings = list()
    for result in results:
        print('We have these results: ', result['label'])

        if result['label'] in _targets and result['confidence'] > confidence_threshold:
            findings.append(result['label'])
        if len(findings):
            print('Nothing found.')

    return findings


if __name__ == "__main__":
    os.system('berrynet-manager start')
    print('Warming up...')
    time.sleep(10)
    print('Program started!')

    # initialize all the components.
    print('Initializing...')
    config = _config('config.yml')
    img_num = config['img_num']
    recover_time = config['recover_time']
    camera = config['camera']
    google_secret = config['google_secret']
    twitter_secret = config['twitter_secret']
    targets = config['targets']
    location = config['location']
    id = config['id']
    confidence_threshold = config['confidence_threshold']
    publish_topic = config['publish_topic']
    subscribe_topic = config['subscribe_topic']

    if camera == 'picamera':
        cam = picamera.PiCamera()
    if google_secret:
        drive = auto_drive(google_secret)
    if twitter_secret:
        tweet_api = tweet_auth(twitter_secret)
    print('Done initialization.')

    while True:
         try:
              image_num = img_num
              # trigger = PIR_motion.run()
              trigger = int(input('Please enter a number, 0 or 1'))
              files = list()
              if trigger:

                    # if detection motion, take 3 pictures.
                    while image_num:
                        files.append(_take_image(cam))
                        print('Taking the {}th pic!'.format(image_num))
                        image_num = image_num - 1
                        time.sleep(0.5)

                    for file in files:
                        # Publish images to local host.
                        _publish(topic=publish_topic, payload=file)
                        print('Publish a pic')
                        results = _subscribe(topic=subscribe_topic)
                        findings = _filter(results, targets, confidence_threshold)
                        if len(findings):
                            if google_secret:
                                upload_to_cloud(drive, file)
                            if twitter_secret:
                                status = "{} found {} in {}.".format(id, findings, location)
                                update_pic(tweet_api, status, file)
                    print('Recovering...')
                    time.sleep(recover_time)

              time.sleep(0.5)

         except (KeyboardInterrupt, SystemExit): 
              os.system('berrynet-manager stop')
              print('System stopped')
              exit()