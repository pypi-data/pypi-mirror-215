from flask import Flask, request, Response
import cv2
import numpy as np
import ssl
import json
import time
import threading
import logging
from setuptools import setup, find_packages
import os

setup(
    name='pychame',
    version='0.0.1',
    description='A simple way to use the ChromeBook integred camera to OpenCV',
    author='Lucas Barros',
    author_email='lucas.barros1804@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        '': ["index.html","cert.pem","key.pem"]
    },
    install_requires=[
        'flask',
        'opencv-python',
        'numpy'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ]
)

class Pychame:
    previousTime = 0
    frame_rate = 0
    frame = None
    frame_receive = True

    def __init__(self):
        self.app = Flask(__name__)

        log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)

        @self.app.route("/",methods=["GET"])
        def index():
            file_path = os.path.join(os.path.dirname(__file__), "index.html")
            with open(file_path, 'r') as file:
                response = file.read()
                return Response(response, mimetype='text/html')

        @self.app.route("/frame",methods=["POST"])
        def frame():
            if self.frame_receive:
                image = request.files.get('frame')
                if not image:
                    return Response(json.dumps({
                        'error': 'No image data received.',
                        'success': False
                    }), mimetype="application/json", status=500)

                self.frame = self.ConvertImage(image)

                currentTime = time.time()
                self.frame_rate = int(1 / (currentTime - self.previousTime))
                self.previousTime = currentTime

            return Response(json.dumps({'success': True}), mimetype="application/json")

        thread = threading.Thread(target=self.StartServer)
        thread.start()

    def ConvertImage(self,image):
        image_array = np.frombuffer(image.read(), np.uint8)
        frame_cv = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
        return frame_cv

    def StartServer(self):
        context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        cert = os.path.join(os.path.dirname(__file__), "cert.pem")
        key = os.path.join(os.path.dirname(__file__), "key.pem")
        context.load_cert_chain(cert,key)

        self.app.run(host='0.0.0.0', port=5000, ssl_context=context)

    def Read(self):
        return [
            self.frame,
            (False if self.frame is None else True)
        ]

    def Release(self):
        self.frame_receive = False