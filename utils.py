import cv2
import numpy as np
import base64

def decode_base64_to_cv2(base64_string):
    """
    Base64 문자열을 디코딩하여 OpenCV 이미지 객체(numpy array)로 변환합니다.
    """
    try:
        # 1. Base64 데이터에 헤더(data:image/png;base64, ...)가 포함된 경우 처리
        if "," in base64_string:
            base64_string = base64_string.split(",")[1]
            
        # 2. 문자열을 바이트 데이터로 디코딩
        img_bytes = base64.b64decode(base64_string)
        
        # 3. 바이트 데이터를 1차원 넘파이 배열로 변환
        img_arr = np.frombuffer(img_bytes, dtype=np.uint8)
        
        # 4. 넘파이 배열을 OpenCV 이미지 객체(BGR)로 디코딩
        img = cv2.imdecode(img_arr, cv2.IMREAD_COLOR)
        
        if img is None:
            print("Error: 이미지 디코딩에 실패했습니다. (결과가 None임)")
            return None
            
        return img

    except Exception as e:
        print(f"Error during Base64 decoding: {e}")
        return None
    

def encode_cv2_to_base64(image_obj, format=".png"):
    """
    OpenCV 이미지 객체(numpy array)를 Base64 문자열로 변환합니다.
    """
    try:
        # 1. 이미지를 메모리 버퍼로 인코딩 (파일 저장 없이 메모리에서 압축)
        # 기본적으로 손실이 없는 .png 포맷을 추천합니다.
        success, buffer = cv2.imencode(format, image_obj)
        
        if not success:
            print("Error: 이미지 인코딩에 실패했습니다.")
            return None
            
        # 2. 버퍼 데이터를 바이트로 변환 후 Base64로 인코딩
        base64_str = base64.b64encode(buffer).decode('utf-8')
        
        # 3. 필요 시 웹에서 바로 사용할 수 있도록 헤더를 붙여서 반환
        # (헤더가 필요 없다면 base64_str만 반환해도 됩니다.)
        prefix = f"data:image/{format[1:]};base64,"
        return prefix + base64_str

    except Exception as e:
        print(f"Error during Base64 encoding: {e}")
        return None
    
