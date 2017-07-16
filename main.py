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

# for PIR motion method.  We have another method comming.
import PIR_motion.run as run

os.chdir("/home/pi/rawcam")


def _get_time():

    return time.strftime("%Y-%m-%d %H:%M:%S")

def _take_image(cam):
    current = _get_time()
    file_name = current + ".jpg"
    # Try to take a picture, if not, save to logging.
    #try:
    cam.capture(file_name)
    logging.info("Take a picture at: {}".format(current))
    time.sleep(0.5)

    return file_name
'''
    except:

        logging.debug("Failed to take a picture at: {}".format(current))
        time.sleep(0.5)
'''


def _publish(topic, payload=None, qos=0,host="localhost", port=1883, client_id=""):

    import paho.mqtt.publish as publish
    try:
        publish.single(topic, payload=payload, qos=qos,host=host, port=port, client_id=client_id)
        logging.info("Publish a message at: {}".format(_get_time()))

    except ValueError as e:
        logging.debug(e)

    except KeyError as e:
        logging.debug(e)


def main():
    # Take three submissive pics.
    image_num = 3
    # Initialize google drive, picamera.

    drive = auto_drive()
    cam = picamera.PiCamera()

    while True:
        try:
            trigger = run()
            files = list()
            if trigger:
                # if detection motion, take 3 pictures.
                while image_num:
                    files.append(_take_image(cam))
                    image_num -= 1
                    time.sleep(0.5)
                # Publish images to local host.
                for file in files:
                    _publish(topic = 'berrynet/event/localImage', payload=file)
                    logging.info("Publish a file to localhost at {}".format(_get_time()))

            """
            # if have a positive result, upload the file to google drive.
            if result:
               upload_to_cloud(drive,file)
               
            """

            time.sleep(0.5)

        except KeyboardInterrupt as e:
            logging.info("System terminated at : {}".format(_get_time())))
            break

if __name__ == "main":
    main()