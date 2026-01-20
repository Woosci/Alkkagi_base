from utils import decode_base64_to_cv2, encode_cv2_to_base64
from vector import get_action_vector_from_model
from image_generator import process_alkkagi_frame_v5
import cv2

image = cv2.imread('real_stage_2.png')

json_data = ""

processed_image = process_alkkagi_frame_v5(image, json_data, resolution=512)


