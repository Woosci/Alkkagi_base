import cv2

import numpy as np

import json

import math



def process_alkkagi_frame_v5(image_path, json_data, resolution):

    # 1. 이미지 로드 및 리사이즈

    src = cv2.imread(image_path)

    if src is None:

        print(f"Error: 이미지를 불러올 수 없습니다: {image_path}")

        return None

    

    img = cv2.resize(src, (resolution, resolution), interpolation=cv2.INTER_AREA)

    img_h, img_w = resolution, resolution



    # 2. JSON 파싱 및 스케일링 설정 (1080 기준)

    state = json.loads(json_data)

    env = state['data']['environment']

    scale = resolution / 1080.0



    # 3. 마스크 레이어 생성 및 돌/벽 영역 확보

    mask = np.zeros((img_h, img_w), dtype=np.uint8)

    all_stones = env['stones']['my_team'] + env['stones']['enemy_team']

    for s in all_stones:

        cx, cy = int(s['position']['x'] * scale), int(s['position']['y'] * scale)

        r = int(s['radius'] * scale)

        padding = int(resolution * 0.05) 

        cv2.circle(mask, (cx, cy), r + padding, 255, -1)



    if 'walls' in env and env['walls']:

        for wall in env['walls']:

            x1, y1 = int(wall['top_left']['x'] * scale), int(wall['top_left']['y'] * scale)

            x2, y2 = int(wall['bottom_right']['x'] * scale), int(wall['bottom_right']['y'] * scale)

            cv2.rectangle(mask, (x1, y1), (x2, y2), 255, -1)



    # 4. 마스킹 적용

    result = img.copy()

    result[mask == 0] = 0



    # 5. 시각 효과 설정

    thickness = max(1, int(resolution / 256))

    font_scale = resolution / 1200.0

    # 기본 화살표 길이 설정 (여유가 있을 때의 최대 길이)

    base_arrow_len = int(resolution / 5.0) 



    # 6. 내 팀 가이드 (가변 길이 인코딩 적용)

    for s in env['stones']['my_team']:

        cx, cy = int(s['position']['x'] * scale), int(s['position']['y'] * scale)

        r = int(s['radius'] * scale)

        cv2.circle(result, (cx, cy), r + 2, (0, 255, 0), thickness)

        

        for i, deg in enumerate(range(0, 360, 15)):

            rad = math.radians(deg)

            cos_a, sin_a = math.cos(rad), math.sin(rad)



            # --- [핵심] 경계면까지의 거리 계산 ---

            # 각 방향으로 이미지 끝까지의 거리 중 최소값을 찾음

            dist_x = (img_w - 25 - cx) / cos_a if cos_a > 0 else (25 - cx) / cos_a if cos_a < 0 else float('inf')

            dist_y = (img_h - 25 - cy) / sin_a if sin_a > 0 else (25 - cy) / sin_a if sin_a < 0 else float('inf')

            max_possible_dist = min(abs(dist_x), abs(dist_y))



            # 실제 화살표 길이는 base_arrow_len과 경계면 거리 중 작은 값 선택

            # 번호가 들어갈 공간(약 20~30px)을 추가로 뺌

            safe_arrow_len = min(base_arrow_len, max_possible_dist - 15)

            if safe_arrow_len < 10: safe_arrow_len = 10 # 최소 길이 보장



            # 색상 지정 (4분면)

            if 0 <= i < 6: color = (0, 0, 255)

            elif 6 <= i < 12: color = (0, 255, 255)

            elif 12 <= i < 18: color = (0, 255, 0)

            else: color = (255, 255, 0)



            # 화살표 그리기

            ex, ey = int(cx + safe_arrow_len * cos_a), int(cy + safe_arrow_len * sin_a)

            cv2.arrowedLine(result, (cx, cy), (ex, ey), color, thickness, tipLength=0.2)

            

            # 번호 중심 보정 (가변 길이에 맞춰 배치)

            text = str(i + 1)

            (t_w, t_h), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, 1)

            

            dist_to_text = safe_arrow_len + 18

            tx = int(cx + dist_to_text * cos_a - t_w / 2)

            ty = int(cy + dist_to_text * sin_a + t_h / 2)

            

            cv2.putText(result, text, (tx, ty), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 255), 1, cv2.LINE_AA)



    # 7. 상대 팀 및 벽 하이라이트 (생략 가능, 이전 코드와 동일)

    for s in env['stones']['enemy_team']:

        cx, cy = int(s['position']['x'] * scale), int(s['position']['y'] * scale)

        cv2.circle(result, (cx, cy), int(s['radius'] * scale) + 2, (0, 0, 255), thickness)



    if 'walls' in env and env['walls']:

        overlay = result.copy()

        for wall in env['walls']:

            x1, y1 = int(wall['top_left']['x'] * scale), int(wall['top_left']['y'] * scale)

            x2, y2 = int(wall['bottom_right']['x'] * scale), int(wall['bottom_right']['y'] * scale)

            cv2.rectangle(overlay, (x1, y1), (x2, y2), (0, 255, 0), -1)

        cv2.addWeighted(overlay, 0.4, result, 0.6, 0, result)



    cv2.imwrite(f"alkkagi_v5_clamped_{resolution}.png", result)

    return result



game_state_data = '{"time": "2026-01-13T16:54:35.740358", "sid": "W7l4KjYwvQniq0i_AAAH", "event": "state", "data": {"elapse": 0.0, "environment": {"board_boundary": {"bottom_right": {"x": 1050.0, "y": 1050.0}, "top_left": {"x": 31.0, "y": 31.0}}, "stones": {"enemy_team": [{"id": "BP_Stone_AKG6", "position": {"x": 537.0, "y": 309.0, "z": 0.0}, "radius": 41.0}, {"id": "BP_Stone_AKG8", "position": {"x": 466.0, "y": 213.0, "z": 0.0}, "radius": 41.0}, {"id": "BP_Stone_AKG9", "position": {"x": 604.0, "y": 216.0, "z": 0.0}, "radius": 41.0}, {"id": "BP_Stone_AKG10", "position": {"x": 389.0, "y": 90.0, "z": 0.0}, "radius": 41.0}, {"id": "BP_Stone_AKG11", "position": {"x": 669.0, "y": 91.0, "z": 0.0}, "radius": 41.0}, {"id": "BP_Stone_AKG12", "position": {"x": 541.0, "y": 86.0, "z": 0.0}, "radius": 41.0}], "my_team": [{"id": "BP_Stone_AKG7", "position": {"x": 539.0, "y": 833.0, "z": 0.0}, "radius": 82.0}]}, "walls": []}, "frame": 0.0, "game_over": false, "my_turn": true, "turn_count": 2.0}}'



# --- 사용 예시 ---

output = process_alkkagi_frame_v5("/home/woosci/test1/Alkkagi/image_data/real_stage/real_stage_2.png", game_state_data, 512)