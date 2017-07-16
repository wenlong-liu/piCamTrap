"""
This is the part of piCamTrap, copyright @ Wenlong Liu.
Created on July 15,2017

This script will publish data to MQTT sever.  For now, it is a local sever.

Platform: Raspberry Pi 3 Model B.
"""

import os
import logging
import time
import picamera
from gupload import auto_drive, upload_to_cloud
from tweetAnimal import tweet_pic

# for PIR motion method.  We have another method comming.
import PIR_motion 


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

    import paho.mqtt.publish as publish
    publish.single(topic, payload=payload, qos=qos, port=port, client_id=client_id)
    logging.info("Publish a message at: {}".format(_get_time()))


if __name__ == "__main__":
    print('Program started!')
    drive = auto_drive()
    cam = picamera.PiCamera()
    
    while True:
            image_num = 3
            #trigger = PIR_motion.run()
            trigger = int(input('Please enter a number, 0 or 1'))
            files = list()
            if trigger:
                # if detection motion, take 3 pictures.
                while image_num:
                    files.append(_take_image(cam))
                    print('Taking the {} pic!'.format(image_num))
                    image_num = image_num - 1
                    time.sleep(0.5)
                           # Publish images to local host.
                for file in files:
                    _publish(topic = 'berrynet/event/localImage', payload=file)
                    print('Publish a file')
                    time.sleep(0.5)
                    # Test upload to cloud function.
                    upload_to_cloud(drive, file)
                    status = "I found something at: {}".formart(_get_time())
                    tweet_pic.TweetPic(status=status, media_ids=file)
                    
            time.sleep(0.5)
 