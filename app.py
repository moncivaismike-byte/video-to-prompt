import streamlit as st
import cv2
from PIL import Image
import requests
import base64
import io
import yt_dlp
import validators

st.set_page_config(page_title="AI视频链接解析助手", layout="wide")
st.title("🔗 视频链接转 AI 提示词工具")

with st.sidebar:
    st.header("⚙️ 设置")
    api_key = st.text_input("输入你的灵光API令牌", type="password")
    model_name = st.text_input("模型名称", value="gpt-4o-mini")
    gap = st.slider("抽帧频率（秒/帧）", 1.0, 10.0, 2.0)

# 核心：处理视频链接的函数
def download_video(url):
 ydl_opts = {
    'format': 'best',
    'quiet': True,
    'no_warnings': True,
    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'outtmpl': 'downloaded_video.mp4',
}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return 'downloaded_video.mp4'

# 界面选择：上传文件或输入链接
option = st.radio("选择输入方式", ("输入视频链接", "上传视频文件"))

video_path = None

if option == "输入视频链接":
    url = st.text_input("请粘贴视频网址 (支持抖音/B站/YouTube等)")
    if url:
        if validators.url(url):
            if st.button("获取视频内容"):
                with st.spinner("正在从链接中抓取视频..."):
                    video_path = download_video(url)
                    st.success("视频抓取成功！")
        else:
            st.error("请输入有效的网址。")
else:
    file = st.file_uploader("上传视频文件", type=["mp4", "mov"])
    if file:
        with open("temp_video.mp4", "wb") as f:
            f.write(file.read())
        video_path = "temp_video.mp4"

# 抽帧分析逻辑
if video_path and api_key:
    if st.button("🚀 开始 AI 拆解"):
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        # ... 后续调用灵光API的逻辑与之前一致 ...
        st.info("正在调用灵光API进行深度分析...")

