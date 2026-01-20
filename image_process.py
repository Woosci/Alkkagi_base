import cv2
import numpy as np
import json
import math

def process_alkkagi_frame(image_path, json_data):
    # 1. 이미지 로드 및 리사이즈 (513x513 통일)
    src = cv2.imread(image_path)
    if src is None:
        return None
    
    img = cv2.resize(src, (1080, 1080))
    img_h, img_w = 1080, 1080

    # 2. JSON 파싱 및 스케일링 설정
    state = json.loads(json_data)
    env = state['data']['environment']
    
    # JSON 최대 좌표가 1050이므로 513에 맞춘 배율 계산
    scale = 513 / 1050.0

    # 3. 마스크 레이어 생성 (돌 주변만 남기기)
    mask = np.zeros((img_h, img_w), dtype=np.uint8)
    
    # 4. 돌 정보 처리 및 그리기
    # 내 팀과 상대 팀을 합쳐서 마스킹 구멍을 뚫음
    all_stones = env['stones']['my_team'] + env['stones']['enemy_team']
    for s in all_stones:
        cx = int(s['position']['x'] * scale)
        cy = int(s['position']['y'] * scale)
        r = int(s['radius'] * scale)
        # 마스크에 구멍 뚫기 (20픽셀 여유)
        cv2.circle(mask, (cx, cy), r + 20, 255, -1)

    # 마스크 적용 (배경 암전)
    result = img.copy()
    result[mask == 0] = 0

    # 5. 개별 팀별 시각 효과 적용
    # 내 팀: 녹색 테두리 + 화살표 가이드
    for s in env['stones']['my_team']:
        cx, cy = int(s['position']['x'] * scale), int(s['position']['y'] * scale)
        r = int(s['radius'] * scale)
        
        cv2.circle(result, (cx, cy), r + 5, (0, 255, 0), 2) # 녹색 테두리
        
        # 15도 간격 화살표 및 번호
        arrow_len = 80
        for i, deg in enumerate(range(0, 360, 15)):
            rad = math.radians(deg)
            ex, ey = int(cx + arrow_len * math.cos(rad)), int(cy + arrow_len * math.sin(rad))
            
            # 화살표
            cv2.arrowedLine(result, (cx, cy), (ex, ey), (255, 255, 0), 1, tipLength=0.2)
            
            # 번호 위치 (경계 보정 포함)
            tx, ty = int(cx + (arrow_len + 15) * math.cos(rad)), int(cy + (arrow_len + 15) * math.sin(rad))
            tx = max(10, min(img_w - 20, tx))
            ty = max(20, min(img_h - 10, ty))
            cv2.putText(result, str(i + 1), (tx, ty), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)

    # 상대 팀: 빨간색 테두리
    for s in env['stones']['enemy_team']:
        cx, cy = int(s['position']['x'] * scale), int(s['position']['y'] * scale)
        r = int(s['radius'] * scale)
        cv2.circle(result, (cx, cy), r + 5, (0, 0, 255), 2) # 빨간색 테두리

    # 6. 장애물(벽) 표시 - 중앙 벽돌 위치 반투명 초록색
    overlay = result.copy()
    # 이미지 픽셀 기준 대략적인 중앙 벽돌 위치 (수동 보정됨)
    cv2.rectangle(overlay, (190, 235), (325, 260), (0, 255, 0), -1)
    cv2.addWeighted(overlay, 0.5, result, 0.5, 0, result)

    return result

# 실행 예시
# processed_img = process_alkkagi_frame("image_41f4f8.png", latest_json_string)
# cv2.imwrite("final_output.png", processed_img)

# --- 사용 예시 ---
# 1. 원본 이미지 저장 (예: game_board.png)
#    - 여기에 첫 번째 이미지 (Image 1)를 저장하고 사용한다고 가정합니다.
#    - Image 1: https://i.imgur.com/example1.png (실제 이미지 경로로 대체 필요)
#    - 로컬에 'game_board.png'로 저장했다고 가정합니다.
image_file = '/home/woosci/test1/Alkkagi/image_data/real_stage/real_stage_1_guide_1.png' 
# (이 부분은 사용자님이 직접 Image 1을 'game_board.png' 파일로 저장한 후에 실행해야 합니다.)
# 예를 들어, 아까 보내주신 첫 번째 이미지 (Image 1)를 'game_board.png'로 저장했다고 가정하겠습니다.

# 2. JSON 데이터 (가장 마지막 state 데이터를 사용)
game_state_data = """
{"time": "2026-01-13T12:10:19.904401", "sid": "-bofyNpcVVXZqK4WAAAM", "event": "state", "data": {"elapse": 0.0, "environment": {"board_boundary": {"bottom_right": {"x": 1050.0, "y": 1050.0}, "top_left": {"x": 31.0, "y": 31.0}}, "stones": {"enemy_team": [{"id": "BP_Stone_AKG2", "position": {"x": 540.0, "y": 227.0, "z": 0.0}, "radius": 41.0}], "my_team": [{"id": "BP_Stone_AKG3", "position": {"x": 540.0, "y": 889.0, "z": 0.0}, "radius": 41.0}]}, "walls": []}, "frame": 0.0, "game_over": false, "my_turn": true, "turn_count": 2.0}}
"""

# 처리된 이미지 얻기
output_image = process_alkkagi_frame(image_file, game_state_data)

if output_image is not None:
    
    # 결과를 파일로 저장
    save_path = "real_stage_2.png"
    cv2.imwrite(save_path, output_image)
    print(f"이미지가 성공적으로 저장되었습니다: {save_path}")
    
