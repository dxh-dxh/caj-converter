import streamlit as st
import subprocess
import sys
import os

st.title("CAJ 转 PDF 转换器")
st.write("上传您的 CAJ 文件，等待转换后即可下载 PDF。")

uploaded_file = st.file_uploader("选择 CAJ 文件", type=['caj'])

if uploaded_file is not None:
    temp_input = "temp.caj"
    output_file = "output.pdf"
    
    with open(temp_input, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    if st.button("开始转换"):
        try:
            # 使用 sys.executable -m 模式运行，确保调用到正确的环境
            result = subprocess.run([sys.executable, "-m", "caj2pdf", "convert", temp_input, "-o", output_file], 
                                    capture_output=True, text=True)
            
            if result.returncode == 0:
                with open(output_file, "rb") as file:
                    st.download_button(
                        label="下载 PDF",
                        data=file,
                        file_name=uploaded_file.name.replace('.caj', '.pdf'),
                        mime="application/pdf"
                    )
                st.success("转换成功！")
            else:
                st.error(f"转换失败: {result.stderr}")
        except Exception as e:
            st.error(f"系统错误: {e}")
        finally:
            if os.path.exists(temp_input):
                os.remove(temp_input)
