import streamlit as st
import subprocess
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
            # 调用 caj2pdf 命令行
            subprocess.run(['caj2pdf', 'convert', temp_input, '-o', output_file], check=True)
            
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
