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
import streamlit as st
import cv2
from PIL import Image
import requests
import base64
import io

st.set_page_config(page_title="视频镜头 AI 抽帧工具", layout="wide")

st.title("🎬 视频镜头 AI 抽帧工具 (灵光API版)")

# 侧边栏设置
with st.sidebar:
    st.header("⚙️ 设置")
    # 灵光API的Key
    api_key = st.text_input("输入灵光API令牌 (Key)", type="password")
    # 灵光API的地址，如果你的地址不一样请修改这里
    base_url = st.text_input("API接口地址", value="https://api.lingguang.ai/v1")
    # 调用的模型名称，建议咨询灵光客服或看文档，通常是 nano-banana 或 gpt-4o-mini 等
    model_name = st.text_input("模型名称", value="gpt-4o-mini") 
    gap = st.slider("抽帧频率 (每秒几帧)", 0.5, 5.0, 1.0)

file = st.file_uploader("上传视频 (MP4/MOV)", type=["mp4", "mov"])

def analyze_frame(image, key, url, model):
    # 将图片转为 Base64 编码
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    
    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    payload = {
        "model": model,
        "messages": [{
            "role": "user",
            "content": [
                {"type": "text", "text": "描述这个视频画面，并生成一段高质量的AI绘图提示词。"},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_str}"}}
            ]
        }]
    }
    try:
        # 拼接完整的请求路径
        full_url = f"{url.rstrip('/')}/chat/completions"
        response = requests.post(full_url, json=payload, headers=headers)
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        return f"解析失败：{str(e)}"

if file and api_key:
    with open("temp.mp4", "wb") as f:
        f.write(file.read())
    
    cap = cv2.VideoCapture("temp.mp4")
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    if st.button("🚀 开始 AI 拆解分析"):
        count = 0
        frame_idx = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret: break
            if count % int(fps / gap) == 0:
                frame_idx += 1
                img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.image(img, caption=f"镜头 {frame_idx}")
                with col2:
                    with st.spinner("AI 正在思考..."):
                        result = analyze_frame(img, api_key, base_url, model_name)
                        st.info(result)
                st.divider()
            count += 1
        cap.release()
elif file and not api_key:
    st.warning("请在左侧填入你的灵光API令牌。")
import streamlit as st
import requests
import cv2
from PIL import Image
import io
import base64

# 灵光API配置 (建议在网页左侧输入)
st.title("🎬 AI 视频分镜专家 (商业演示版)")

with st.sidebar:
    st.header("🔑 收益配置")
    my_key = st.text_input("灵光API Key", type="password")
    # 模拟广告开关
    ad_unlocked = st.toggle("模拟用户已看广告", value=False)

uploaded_video = st.file_uploader("上传剪辑视频", type=["mp4", "mov"])

if uploaded_video and my_key:
    if not ad_unlocked:
        st.warning("📺 这是一个演示：在真实小程序中，用户需看完 30 秒广告才能触发下方的 AI 分析。")
        if st.button("点击模拟观看广告"):
            st.balloons()
            st.info("广告已看完，AI 功能解锁！")
    else:
        # 这里放置你之前的抽帧逻辑
        st.success("✅ AI 正在为您拆解镜头并生成提示词...")
        # 实际调用灵光API的代码逻辑...
