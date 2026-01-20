import cv2
import base64
import os
import re
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv('api_key'))

# --- 설정 (Log 경로를 여기서 한 번에 관리하세요) ---
LOG_BASE_DIR = "log2"

def encode_image_from_cv2(image_obj):
    """OpenCV 이미지 객체를 Base64로 인코딩"""
    success, buffer = cv2.imencode(".png", image_obj)
    if not success:
        raise ValueError("이미지 인코딩에 실패했습니다.")
    return base64.b64encode(buffer).decode('utf-8')

def get_next_trial(folder_path):
    """다음 실행 번호 계산"""
    if not os.path.exists(folder_path): return 1
    nums = [int(m.group(1)) for f in os.listdir(folder_path) if (m := re.search(r'trial_(\d+)', f))]
    return max(nums) + 1 if nums else 1

def save_log(response_text, usage, model, image_name):
    """로그 저장 경로 설정 및 파일 저장"""
    # 가독성을 위해 경로 구조화: log / 모델명 / 이미지명 / trial_N.txt
    folder_path = os.path.join(LOG_BASE_DIR, model, image_name)
    os.makedirs(folder_path, exist_ok=True)
    
    trial_num = get_next_trial(folder_path)
    file_path = os.path.join(folder_path, f"trial_{trial_num}.txt")
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(f"--- RESPONSE ---\n{response_text}\n\n")
        f.write(f"--- USAGE ---\n{usage}")
    print(f"Log saved: {file_path}")

def get_alkkagi_decision(model, system_prompt, user_prompt, image_obj, image_name="current_state"):
    """이미지 객체를 입력받아 모델 답변 획득"""
    
    # 1. 이미지 인코딩 (Base64)
    base64_image = encode_image_from_cv2(image_obj)
    
    # 2. API 호출
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": [
                {"type": "text", "text": user_prompt},
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"}}
            ]}
        ]
    )
    
    answer = response.choices[0].message.content
    
    # 3. 로그 저장
    save_log(answer, response.usage, model, image_name)
    
    return answer

# --- 실행 예시 ---
if __name__ == "__main__":
    # 데이터 로드
    with open("prompt_planning.txt", "r", encoding="utf-8") as f: sys_p = f.read()
    with open("game_state.txt", "r", encoding="utf-8") as f: user_p = f.read()
    
    # 이미지 객체 (이미 로드되어 있다고 가정하거나 경로에서 읽기)
    test_image = cv2.imread("alkkagi_v5_clamped_512.png")
    
    if test_image is not None:
        res = get_alkkagi_decision("gpt-4o", sys_p, user_p, test_image, "3001")
        print(f"\nModel Decision:\n{res}")