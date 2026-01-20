import os
import re
import base64
from openai import OpenAI
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

def get_next_trial_number(folder_path):
    if not os.path.exists(folder_path):
        return 1
    files = os.listdir(folder_path)
    trial_numbers = [int(m.group(1)) for f in files if (m := re.search(r'trial_(\d+)', f))]
    return max(trial_numbers) + 1 if trial_numbers else 1

def save_log(base_dir, model, stage, content, usage):
    # 경로: base_dir/model/stage/trial_n.txt
    folder_path = os.path.join(base_dir, model, stage)
    os.makedirs(folder_path, exist_ok=True)
    
    trial_num = get_next_trial_number(folder_path)
    file_path = os.path.join(folder_path, f"trial_{trial_num}.txt")
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(f"--- RESPONSE ---\n{content}\n\n--- USAGE ---\n{usage}")
    print(f"Log saved: **{file_path}**")

# 1. 핵심 API 호출 함수 (시스템 프롬프트 경로 입력 방식)
def call_alkkagi_ai(model, system_prompt_path, game_state, image_base64, stage_name, base_log_dir="log"):
    client = OpenAI(api_key=os.getenv('api_key'))

    # 시스템 프롬프트 파일 읽기
    with open(system_prompt_path, "r", encoding="utf-8") as f:
        system_content = f.read()

    # API 호출
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_content},
            {"role": "user", "content": [
                {"type": "text", "text": game_state},
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_base64}"}}
            ]}
        ]
    )

    result_text = response.choices[0].message.content
    usage_info = str(response.usage)
    
    # 로그 저장
    save_log(base_log_dir, model, stage_name, result_text, usage_info)
    
    return result_text
