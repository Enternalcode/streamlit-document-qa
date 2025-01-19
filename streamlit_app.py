import streamlit as st
from utils.zhipu_service import ZhipuService


st.title("遇见:sunglasses:")
st.markdown("## 微信头像性格分析")
st.write("大量研究表明，头像不仅是个性展示的窗口，更是内心世界的映射。")
st.write(
    "我们往往会将自己的爱好和属性投射到头像上。想知道你关心的人在头像背后隐藏的真实个性吗？"
)
st.write("只需上传他们的头像，便能揭示他们内心的倾向与喜好。")

uploaded_file = st.file_uploader("上传头像", accept_multiple_files=False)
if uploaded_file:
    st.image(uploaded_file)

knowledge = """
1. 用自拍照头像：这类人对自己的长相有信心，喜欢把自己最好的一面展示出来。在工作和社交方面也更主动一些。
2. 风景照：这类人生活经验丰富，懂得享受平淡的幸福。
3. 动漫人物：这类人偏理想主义，希望自己也成为对应的人物角色。
4. 童年照片：这类人重视家庭，富有童真且感性。
5. 小动物头像：这类人通常性格温和，受欢迎，包容性强，有创造力，且富有爱心。
"""
question = f"""
    # 已知信息
    {knowledge}
    # 人设
    - 你是一个心理学专家，社交头像是人们内心的映射，你的任务是分析头像，分析这个人的性格。
    # 目标
    从以下5个维度进行分析和打分，每一项10分满分。并最后汇总分数。
    1. 是什么样的性格
    2. 会怎么看待自己
    3. 会怎么看待他人
    4. 对父母的看法
    5. 牛马指数
    """
content = None
if uploaded_file and question:
    response_container = st.empty()
    with response_container.container():
        with st.spinner("分析中..."):
            bytes_data = uploaded_file.getvalue()
            zhipu_service = ZhipuService(api_key=st.secrets["ZHIPU_API_KEY"])
            img_base = zhipu_service.bytes_to_base64(bytes_data)
            content = zhipu_service.chat_stream(content=question, img_base=img_base)
            st.write_stream(content)
