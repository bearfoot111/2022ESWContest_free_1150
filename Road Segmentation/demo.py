import cv2
import time
from PIL import Image
from torchvision.transforms.functional import to_pil_image
import tensorflow as tf
from model.pspunet import pspunet
from data_loader.display import create_mask
import numpy as np
gpus = tf.config.experimental.list_physical_devices('GPU')

if gpus:
    try:
        tf.config.experimental.set_virtual_device_configuration(
       gpus[0],
        [tf.config.experimental.VirtualDeviceConfiguration(memory_limit=500)])
    except RuntimeError as e:
        print(e)
        
IMG_WIDTH = 480
IMG_HEIGHT = 272
n_classes = 7

model = pspunet((IMG_HEIGHT, IMG_WIDTH ,3), n_classes)
model.load_weights("pspunet_weight.h5")

frame = cv2.imread('image.jpg')

frame = cv2.resize(frame, (IMG_WIDTH, IMG_HEIGHT))
frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
frame = frame[tf.newaxis, ...]
frame = frame/255
pre = model.predict(frame)
pre = create_mask(pre).numpy()

frame2 = frame/2
frame2[0][(pre==1).all(axis=2)] += [0, 0, 0] #""bike_lane_normal", "sidewalk_asphalt", "sidewalk_urethane""
frame2[0][(pre==2).all(axis=2)] += [0.5, 0.5,0] # "caution_zone_stairs", "caution_zone_manhole", "caution_zone_tree_zone", "caution_zone_grating", "caution_zone_repair_zone"]
frame2[0][(pre==3).all(axis=2)] += [0.2, 0.7, 0.5] #"alley_crosswalk","roadway_crosswalk"
frame2[0][(pre==4).all(axis=2)] += [0, 0.5, 0.5] #"braille_guide_blocks_normal", "braille_guide_blocks_damaged"
frame2[0][(pre==5).all(axis=2)] += [0, 0, 0.5] #"roadway_normal","alley_normal","alley_speed_bump", "alley_damaged""
frame2[0][(pre==6).all(axis=2)] += [0.5, 0, 0] #"sidewalk_blocks","sidewalk_cement" , "sidewalk_soil_stone", "sidewalk_damaged","sidewalk_other"

#print(frame2.shape)
frame2 = tf.squeeze(frame2)
#print(frame2.shape)
#print(type(frame2))
frame2 = frame2.numpy()
frame2 = frame2*255
frame2 = np.uint8(frame2)
frame2 = to_pil_image(frame2)
#print('result')
#cv2.imwrite('result.jpg', frame2)
frame2.save('result.jpg')