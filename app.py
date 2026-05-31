import streamlit as st
import subprocess
import sys
import os

# 动态安装依赖函数
def install_dependencies():
    try:
        # 使用 pip 强制安装 caj2pdf
        subprocess.check_call([sys.executable, "-m", "pip", "install", "git+https://github.com/flyfoxs/caj2pdf.git"])
    except Exception as e:
        st.error(f"依赖安装失败: {e}")

# 启动时运行
if not os.path.exists("installed_marker"):
    with st.spinner('正在初始化环境，请稍候...'):
        install_dependencies()
        with open("installed_marker", "w") as f:
            f.write("installed")

st.title("CAJ 转 PDF 转换器")
st.write("上传您的 CAJ 文件，点击下方按钮开始转换。")

uploaded_file = st.file_uploader("选择 CAJ 文件", type=['caj'])

if uploaded_file is not None:
    temp_input = "temp.caj"
    output_file = "output.pdf"
    
    with open(temp_input, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    if st.button("开始转换"):
        try:
            # 关键修改：使用 sys.executable -m 模式运行，确保能找到命令
            subprocess.run([sys.executable, "-m", "caj2pdf", "convert", temp_input, "-o", output_file], check=True)
            
            with open(output_file, "rb") as file:
                st.download_button(
                    label="下载 PDF",
                    data=file,
                    file_name=uploaded_file.name.replace('.caj', '.pdf'),
                    mime="application/pdf"
                )
            st.success("转换成功！")
        except Exception as e:
            st.error(f"转换失败: {e}")
        finally:
            if os.path.exists(temp_input):
                os.remove(temp_input)