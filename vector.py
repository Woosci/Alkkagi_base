import json

def get_action_vector_from_model(model_output):
    """
    모델의 JSON 출력에서 방향 번호를 추출하여 (dx, dy) 단위 벡터를 반환합니다.
    """
    # 1. 1~24번 방향에 대한 단위 벡터 매핑 테이블
    DIRECTION_VECTORS = {
    "1": (1.0000, 0.0000),    # 0도 (오른쪽)
    "2": (0.9659, 0.2588),    # 15도
    "3": (0.8660, 0.5000),    # 30도
    "4": (0.7071, 0.7071),    # 45도
    "5": (0.5000, 0.8660),    # 60도
    "6": (0.2588, 0.9659),    # 75도
    "7": (0.0000, 1.0000),    # 90도 (위쪽)
    "8": (-0.2588, 0.9659),   # 105도
    "9": (-0.5000, 0.8660),   # 120도
    "10": (-0.7071, 0.7071),  # 135도
    "11": (-0.8660, 0.5000),  # 150도
    "12": (-0.9659, 0.2588),  # 165도
    "13": (-1.0000, 0.0000),  # 180도 (왼쪽)
    "14": (-0.9659, -0.2588), # 195도
    "15": (-0.8660, -0.5000), # 210도
    "16": (-0.7071, -0.7071), # 225도
    "17": (-0.5000, -0.8660), # 240도
    "18": (-0.2588, -0.9659), # 255도
    "19": (0.0000, -1.0000),  # 270도 (아래쪽)
    "20": (0.2588, -0.9659),  # 285도
    "21": (0.5000, -0.8660),  # 300도
    "22": (0.7071, -0.7071),  # 315도
    "23": (0.8660, -0.5000),  # 330도
    "24": (0.9659, -0.2588)   # 345도
}

    try:
        # 2. 입력 데이터 파싱 (문자열인 경우 dict로 변환)
        if isinstance(model_output, str):
            data = json.loads(model_output)
        else:
            data = model_output
            
        # 3. selected_direction 값 추출
        selected_idx = str(data['selected_direction'])
        
        # 4. 벡터 매핑
        if selected_idx in DIRECTION_VECTORS:
            dx, dy = DIRECTION_VECTORS[selected_idx]
            return dx, dy
        else:
            print(f"Error: {selected_idx} 는 잘못된 방향 인덱스입니다.")
            return None

    except (KeyError, ValueError, json.JSONDecodeError) as e:
        print(f"Error parsing model output: {e}")
        return None
