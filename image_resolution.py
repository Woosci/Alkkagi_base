import cv2
import os

def resize_image(input_path, output_name, size):
    # 1. 원본 이미지 로드
    src = cv2.imread(input_path)
    
    if src is None:
        print(f"Error: {input_path} 파일을 찾을 수 없습니다.")
        return

    # 2. 이미지 리사이즈 (가로, 세로를 size로 통일)
    # 수축 시 품질을 위해 INTER_AREA 보간법을 사용합니다.
    resized_img = cv2.resize(src, (size, size), interpolation=cv2.INTER_AREA)

    # 3. 결과 저장
    cv2.imwrite(output_name, resized_img)
    print(f"완료: {output_name} ({size}x{size}) 저장되었습니다.")

# --- 실행부 ---
original_img = "/home/woosci/test1/Alkkagi/image_data/real_stage/real_stage_2.png"  # 원본 1080x1080 이미지 경로

# 256x256 으로 변환
resize_image(original_img, "image_256.png", 256)

# 512x512 로 변환
resize_image(original_img, "image_512.png", 512)