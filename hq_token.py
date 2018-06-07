import re
import os.path
import urllib.request
import urllib.error
import base64
import gzip
import zlib
from io import BytesIO
import json
import time
import random


def stage1():

    global phoneNumber
    phoneNumber = input("Please enter your phone number below with the country prefix.\nExample: +40758721982\n")



    def make_requests():
        response = [None]

        if(request_api_quiz_hype_space(response)):
            responseText = read_response(response[0])
            codlink = json.loads(responseText)
            global cod
            try:
                cod = codlink["verificationId"]
            except:
                print("Invalid phone number, cancelling...")
                quit()
            print("Verification id code is: {}".format(cod))
            response[0].close()


    def read_response(response):
        if response.info().get('Content-Encoding') == 'gzip':
            buf = BytesIO(response.read())
            return gzip.GzipFile(fileobj=buf).read().decode('utf8')

        elif response.info().get('Content-Encoding') == 'deflate':
            decompress = zlib.decompressobj(-zlib.MAX_WBITS)
            inflated = decompress.decompress(response.read())
            inflated += decompress.flush()
            return inflated.decode('utf8')

        return response.read().decode('utf8')


    def request_api_quiz_hype_space(response):
        response[0] = None

        try:
            req = urllib.request.Request("https://api-quiz.hype.space/verifications")

            req.add_header("Content-Type", "application/json")
            req.add_header("Accept-Encoding", "br, gzip, deflate")
            req.add_header("User-Agent", "HQ-iOS/90 CFNetwork/897.15 Darwin/17.5.0")
            req.add_header("Connection", "keep-alive")
            req.add_header("x-hq-device", "iPhone7,2")
            req.add_header("Accept", "*/*")
            req.add_header("Accept-Language", "ro-ro")
            req.add_header("x-hq-client", "iOS/1.3.7 b90")
            req.add_header("x-hq-test-key", "")

            body = b"{\"phone\":\"" + phoneNumber.encode("utf-8") + b"\",\"method\":\"sms\"}"


            response[0] = urllib.request.urlopen(req, body)

        except urllib.error.URLError as e:
            if not hasattr(e, "code"):
                return False
            response[0] = e
        except:
            return False

        return True


    make_requests()

def stage2():

    smscode = input("Now enter the sms code that you've received: ")

    def make_requests():
        response = [None]

        if(request_api_quiz_hype_space(response)):
            responseText = read_response(response[0])
            try:
                raspuns = json.loads(responseText)
                token = raspuns["auth"]["accessToken"]
                print("Your HQ Trivia Token is: {}".format(token))
            except Exception as e:
                print("The sms code you've provided is invalid, exiting...")
                quit()

            response[0].close()


    def read_response(response):
        if response.info().get('Content-Encoding') == 'gzip':
            buf = BytesIO(response.read())
            return gzip.GzipFile(fileobj=buf).read().decode('utf8')

        elif response.info().get('Content-Encoding') == 'deflate':
            decompress = zlib.decompressobj(-zlib.MAX_WBITS)
            inflated = decompress.decompress(response.read())
            inflated += decompress.flush()
            return inflated.decode('utf8')

        return response.read().decode('utf8')


    def request_api_quiz_hype_space(response):
        response[0] = None

        try:
            req = urllib.request.Request("https://api-quiz.hype.space/verifications/{}".format(cod))

            req.add_header("Content-Type", "application/json")
            req.add_header("Accept-Encoding", "br, gzip, deflate")
            req.add_header("User-Agent", "HQ-iOS/90 CFNetwork/897.15 Darwin/17.5.0")
            req.add_header("Connection", "keep-alive")
            req.add_header("x-hq-device", "iPhone7,2")
            req.add_header("Accept", "*/*")
            req.add_header("Accept-Language", "ro-ro")
            req.add_header("x-hq-client", "iOS/1.3.7 b90")
            req.add_header("x-hq-test-key", "")

            body = b"{\"code\":\"" + smscode.encode("utf-8") + b"\"}"

            response[0] = urllib.request.urlopen(req, body)

        except urllib.error.URLError as e:
            if not hasattr(e, "code"):
                return False
            response[0] = e
        except:
            return False

        return True


    make_requests()


stage1()
print("Sending you the sms code...")
time.sleep(random.randint(5, 10))
print("\nSms Code Sent\n")
stage2()
