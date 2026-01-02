import streamlit as st
import cv2
from PIL import Image
import requests
import base64
import io

st.set_page_config(page_title="Nano Banana 视频解析", layout="wide")

st.title("🎬 Nano Banana 视频镜头 AI 抽帧工具")

# 侧边栏：配置
with st.sidebar:
    st.header("⚙️ 设置")
    api_key = st.text_input("输入 Nano Banana API Key", type="password")
    gap = st.slider("抽帧频率 (每秒几帧)", 0.5, 5.0, 1.0)

file = st.file_uploader("上传视频 (MP4/MOV)", type=["mp4", "mov"])

def analyze_frame(image, key):
    # 这里是调用 Nano Banana 接口的标准逻辑
    # 注意：实际 URL 请替换为 Nano Banana 官方提供的 Endpoint
    api_url = "https://api.nanobanana.com/v1/vision" 
    
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    
    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    payload = {
        "model": "nano-banana-vision",
        "messages": [{
            "role": "user",
            "content": [
                {"type": "text", "text": "请详细描述此画面，并生成一段高质量的 AI 绘图提示词 (Prompt)"},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_str}"}}
            ]
        }]
    }
    try:
        response = requests.post(api_url, json=payload, headers=headers)
        return response.json()['choices'][0]['message']['content']
    except:
        return "API 调用失败，请检查 Key 或网络。"

if file and api_key:
    with open("temp.mp4", "wb") as f:
        f.write(file.read())
    
    cap = cv2.VideoCapture("temp.mp4")
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    if st.button("🚀 开始 AI 拆解分析"):
        count = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret: break
            if count % int(fps / gap) == 0:
                img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                col1, col2 = st.columns([1, 2])
                with col1: st.image(img)
                with col2:
                    result = analyze_frame(img, api_key)
                    st.write("**AI 解析结果：**")
                    st.info(result)
                st.divider()
            count += 1
        cap.release()
