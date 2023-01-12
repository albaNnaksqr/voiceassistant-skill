import base64
import math
from os import confstr
import time
import cv2
import sys

MYCROFT_VERSION = True
TEST_IMAGE_PATH = './1.jpeg'
if MYCROFT_VERSION:
    from util import callAPI, encode_image_from_file
    from mycroft.util import LOG
else:
    from util import callAPI, encode_image_from_file
    
def getObjectsThenLabel(image_file):

    image_base64 = encode_image_from_file(image_file)
    image_cv = cv2.imread(image_file)

    # get location of each objects
    response = callAPI(image_base64, 'LOC')
    # print(response)

    obj_loc_list = response['responses'][0]["localizedObjectAnnotations"]

    h, w, _ = image_cv.shape

    res = {'objectNum': len(obj_loc_list), 'objectList': []}
    for obj_loc in obj_loc_list:
        vx_list = obj_loc["boundingPoly"]["normalizedVertices"]
        ux = int(math.floor(vx_list[0]['x'] * w))
        uy = int(math.floor(vx_list[0]['y'] * h))
        dx = int(math.floor(vx_list[2]['x'] * w))
        dy = int(math.floor(vx_list[2]['y'] * h))

        image_cv_single_obj = image_cv[uy:dy, ux:dx]

        # im_arr: image in Numpy one-dim array format.
        _, image_cv_single_obj_arr = cv2.imencode('.jpg', image_cv_single_obj)
        image_cv_single_obj_bytes = image_cv_single_obj_arr.tobytes()
        image_base64_single_obj = base64.b64encode(image_cv_single_obj_bytes)

        label_list = getLabel(image_base64_single_obj)

        loc_str = 'center'
        cx = (vx_list[2]['x'] - vx_list[0]['x']) / 2.0 + vx_list[0]['x']
        cy = (vx_list[2]['y'] - vx_list[0]['y']) / 2.0 + vx_list[0]['y']
        if cx < 0.5 and cy < 0.5:
            loc_str = 'upper right'
        elif cx < 0.5 and cy > 0.5:
            loc_str = 'lower right'
        elif cx > 0.5 and cy < 0.5:
            loc_str = 'upper left'
        elif cx > 0.5 and cy > 0.5:
            loc_str = 'lower left'

        obj_label = {'name': label_list, 'loc': loc_str}
        res['objectList'].append(obj_label)


    return res


def getLabel(image_base64):
    # get label of a single object

    response = callAPI(image_base64, 'LABEL')
    labelList = response['responses'][0]["labelAnnotations"]
    res = []
    # for label in labelList:
    #     if float(label['score']) >= 0.8:
    #         res.append(label["description"])
    #     if float(label['score']) < 0.8:
    #         break
    for i in range(3):
        res.append(labelList[i]["description"])
    return res

if not MYCROFT_VERSION:
    print('start', time.time())
    a = getObjectsThenLabel(TEST_IMAGE_PATH)
    print(a)
    print('end', time.time())
    

