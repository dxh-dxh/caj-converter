import streamlit as st
import subprocess
import os

st.title("CAJ 转 PDF 转换器")
st.write("上传您的 CAJ 文件，点击转换即可获取 PDF。")
st.warning("注意：此工具依赖于后台安装了 caj2pdf 命令行工具。")

uploaded_file = st.file_uploader("选择 CAJ 文件", type=['caj'])

if uploaded_file is not None:
    # 保存上传的文件
    temp_input = "temp.caj"
    output_file = "output.pdf"
    
    with open(temp_input, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    if st.button("开始转换"):
        try:
            # 调用 caj2pdf 转换
            # 确保 caj2pdf 已安装在系统环境中
            subprocess.run(['caj2pdf', 'convert', temp_input, '-o', output_file], check=True)
            
            # 读取生成的 PDF 文件
            with open(output_file, "rb") as file:
                btn = st.download_button(
                    label="下载 PDF",
                    data=file,
                    file_name=uploaded_file.name.replace('.caj', '.pdf'),
                    mime="application/pdf"
                )
            st.success("转换成功！请点击上方按钮下载。")
        except Exception as e:
            st.error(f"转换失败，请检查文件格式是否合法，或后台 caj2pdf 是否正确安装: {e}")
        finally:
            # 清理输入文件
            if os.path.exists(temp_input):
                os.remove(temp_input)
