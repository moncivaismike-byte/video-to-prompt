import streamlit as st
import cv2
from PIL import Image
import requests
import base64
import io

st.set_page_config(page_title="AI视频分镜专家", layout="wide")
st.title("🎬 视频镜头 AI 深度拆解 (稳定版)")

with st.sidebar:
    st.header("⚙️ 设置")
    api_key = st.text_input("输入灵光API令牌", type="password")
    model_name = st.text_input("模型名称", value="gpt-4o-mini")
    gap = st.slider("抽帧频率 (秒/帧)", 1.0, 10.0, 5.0)

uploaded_file = st.file_uploader("上传视频文件", type=["mp4", "mov"])

def analyze_single_frame(image, key, model):
    buffered = io.BytesIO()
    # 关键：压缩质量到 60%，减小体积，极大加快上传速度
    image.save(buffered, format="JPEG", quality=60) 
    img_str = base64.b64encode(buffered.getvalue()).decode()
    
    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    payload = {
        "model": model,
        "messages": [{
            "role": "user",
            "content": [
                {"type": "text", "text": "简要描述画面并提供AI绘图Prompt"},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_str}"}}
            ]
        }]
    }
    try:
        # 设置严格超时，防止无限等待
        response = requests.post("https://api.lingguang.ai/v1/chat/completions", json=payload, headers=headers, timeout=20)
        return response.json()['choices'][0]['message']['content']
    except Exception:
        return "⚠️ 该帧请求超时，正在处理下一帧..."

if uploaded_file and api_key:
    if st.button("🚀 开始逐帧解析"):
        with open("temp.mp4", "wb") as f:
            f.write(uploaded_file.read())
        
        cap = cv2.VideoCapture("temp.mp4")
        fps = cap.get(cv2.CAP_PROP_FPS)
        count = 0
        frame_idx = 1
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret: break
            
            if count % int(fps * gap) == 0:
                img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.image(img, caption=f"镜头 {frame_idx}")
                with col2:
                    with st.spinner(f"正在分析第 {frame_idx} 个镜头..."):
                        res = analyze_single_frame(img, api_key, model_name)
                        st.info(res)
                frame_idx += 1
            count += 1
        cap.release()
        st.success("✨ 所有镜头分析完成！")
