from utils import decode_base64_to_cv2, encode_cv2_to_base64
from vector import get_action_vector_from_model
from image_generator import process_alkkagi_frame_v5
from vlm import call_alkkagi_ai

import cv2

MODEL = "gpt-4o"
SYSTEM_PRMT_PATH = "prompt_planning.txt"
STAGE = "1001"
game_state_text = open("game_state2.txt", "r", encoding="utf-8").read()


# 1. base64 이미지를 받는다.
# 2. 이미지를 디코딩한다.
# 3. 디코딩된 이미지를 image라고 생각한다.

image = cv2.imread('real_stage_2.png')
json_data = game_state_text

processed_image = process_alkkagi_frame_v5(image, json_data, resolution=512)

# 4. 이미지를 다시 인코딩한다.
encoded_image = encode_cv2_to_base64(processed_image)

# 5. 모델에 이미지를 보내고 출력값을 받는다.
response = call_alkkagi_ai(MODEL, SYSTEM_PRMT_PATH, game_state_text, encoded_image, STAGE, "log3")

# 6. 출력값을 벡터로 변환한다.
action_vector = get_action_vector_from_model(response)

print(action_vector)


