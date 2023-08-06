import cv2
import numpy as np

def add_one(number):
    return number + 10

def mask_postprocess(mask, thres=20):
    mask[:thres, :] = 0; mask[-thres:, :] = 0
    mask[:, :thres] = 0; mask[:, -thres:] = 0        
    mask = cv2.GaussianBlur(mask, (91, 91), 11)
    mask = cv2.GaussianBlur(mask, (91, 91), 11)
    return mask.astype(np.float32)

def preprocess_border(full_img, y1, y2, x1, x2, default_padding = 50): ## extend border
    h,w,c = full_img.shape
    if x1 - default_padding > 0:
        ex_x1 = x1 - default_padding
    else:
        ex_x1 = 0

    if x2 + default_padding < w:
        ex_x2 = x2 + default_padding
    else:
        ex_x2 = w
    ###### Y
    if y1 - default_padding > 0:
        ex_y1 = y1 - default_padding
    else:
        ex_y1 = 0

    if y2 + default_padding < h:
        ex_y2 = y2 + default_padding
    else:
        ex_y2 = h
    return ex_y1, ex_y2, ex_x1, ex_x2