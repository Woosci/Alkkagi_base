from openai import OpenAI
from dotenv import load_dotenv
import os
import base64

load_dotenv()
api_key = os.getenv('api_key')

# 1. 클라이언트 초기화 (API 키 입력)
# 환경 변수에 저장했다면 키 값을 생략해도 자동으로 불러옵니다.
client = OpenAI(api_key=api_key)

def get_chatgpt_answer(system_content, user_question, image_base64=None):
    
    if image_base64:
        # 이미지가 있을 경우 user_question에 이미지 정보를 추가
        user_question += f"\n[Image in base64]: {image_base64}"
        
        # 2. API 호출
        response = client.chat.completions.create(
            model="gpt-5",                                   
            messages=[                                        
                {"role": "system", "content": system_content}, 
                {"role": "user", "content": [
                    {"type": "text", "text": user_question},
                    {"type": "image_url", "image_url": {
                        "url": f"data:image/png;base64,{image_base64}"}}
            ]}                                         
            ]                                                 
        )
        
    else:    
        # 2. API 호출
        response = client.chat.completions.create(
            model="gpt-4o",                                   # model에서 사용할 모델 이름을 입력한다.
            messages=[                                        # 대화 내역을 리스트 형태로 전달
                {"role": "system", "content": system_content}, # system : 행동지침, 페르소나
                {"role": "user", "content": user_question}    # 리스트 원소로 role과 content가 있는 딕셔너리를 가진다.
            ]                                                 # role : user(사용자 입력), assistant(과거 답변), system(행동지침, 페르소나), tool(함수 호출)
        )
    
    # 3. 답변 반환
    return response.choices[0].message.content

def load_prompt(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')



# 파일 경로 설정 (파이썬 파일과 같은 폴더에 있을 경우)
system_content = load_prompt("prompt_planning_3.txt")
game_state = load_prompt("game_state.txt")
image = encode_image("image.png")


# 실행 예시
answer = get_chatgpt_answer(system_content, game_state)
print(f"ChatGPT의 답변 이미지X: {answer}")
answer = get_chatgpt_answer(system_content, game_state, image)
print(f"ChatGPT의 답변 이미지O : {answer}")

# response 속 정보
# {
#   "id": "chatcmpl-123",            // 요청의 고유 ID
#   "object": "chat.completion",     // 객체 유형
#   "created": 1677652288,           // 생성 시간 (Unix 타임스탬프)
#   "model": "gpt-4o-2024-05-13",    // 답변을 생성한 구체적인 모델 버전
#   "system_fingerprint": "fp_447...", // 모델 인프라 식별자 (재현성 확인용)
#   "choices": [                     // 답변 후보군 (n 파라미터로 여러 개 요청 가능)
#     {
#       "index": 0,
#       "message": {                 // 실제 답변 내용
#         "role": "assistant",
#         "content": "안녕하세요! 무엇을 도와드릴까요?",
#         "tool_calls": null         // 함수 호출이 필요한 경우 정보가 담김
#       },
#       "logprobs": null,            // 각 단어의 선택 확률 (요청 시 활성화 가능)
#       "finish_reason": "stop"      // 답변이 끝난 이유 (stop: 완료, length: 토큰 초과 등)
#     }
#   ],
#   "usage": {                       // 과금과 직결되는 토큰 사용량 정보
#     "prompt_tokens": 9,            // 질문에 사용된 토큰
#     "completion_tokens": 12,       // 답변에 사용된 토큰
#     "total_tokens": 21             // 총 사용 토큰
#   }
# }