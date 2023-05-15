import streamlit as st
import json

# https://www.youtube.com/watch?v=awsjo_1tqIM
# https://discuss.streamlit.io/t/removing-space-before-sidebar-title/28961/4

st.set_page_config(page_title="SRW", page_icon=None,layout="wide")

st.write("## サイエンスリサーチライティング")

st.sidebar.write("## 構想モード")
hidden = st.sidebar.checkbox("Hide input form", value=False)

st.sidebar.write("## アップロード")
uploaded_file = st.sidebar.file_uploader("Choose a dat file", accept_multiple_files=False)


with open("./template.md", encoding="utf-8") as f:
    filelines = f.readlines()
    filelines = [fileline.strip('\n') for fileline in filelines if fileline != '\n']

    chapters = []
    for fileline in filelines:
        if fileline.startswith("##"):
            chapters.append(fileline)
    
    contents = {}
    temp_chapter = ""
    for fileline in filelines:
        if fileline in chapters and temp_chapter != fileline:
            temp_chapter = fileline
            contents[temp_chapter] = []
            continue
        if temp_chapter in chapters:
            contents[temp_chapter].append(fileline)
    
    textbox = {}
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue().decode("utf-8")
        load_data = json.loads(bytes_data)
        for key, value in contents.items():
            with st.expander(key):
                for v in value:
                    if hidden:
                        st.markdown('<p style="font-size: 14px;">'+v+'</p>', unsafe_allow_html=True)
                    else:
                        textbox[v] = st.text_area(label=v, value=load_data[v], key=v)
    else:
        for key, value in contents.items():
            with st.expander(key):
                for v in value:
                    if hidden:
                        st.markdown('<p style="font-size: 14px;">'+v+'</p>', unsafe_allow_html=True)
                    else:
                        # st.write(v)
                        textbox[v] = st.text_area(label=v, key=v)
    

st.sidebar.write("## ダウンロード")
st.sidebar.download_button(
    label="Download",
    data=json.dumps(textbox, ensure_ascii=False),
    file_name='file.dat',
    mime='text/csv',
    disabled=hidden, 
)

def formatExportData(textbox):
    exportdata = "# Science Writing\n\n"
    for key, value in contents.items():
        exportdata += key + '\n'
        for v in value:
            if textbox != {}:
                exportdata += textbox[v]
        exportdata += '\n\n'
    return exportdata

st.sidebar.write("## エクスポート")
st.sidebar.download_button(
    label="Export to Markdown",
    data=formatExportData(textbox),
    file_name='file.md',
    mime='text/csv',
    disabled=hidden,
)

st.markdown("""
    <style>
        .css-1629p8f.e16nr0p31 {
            margin-top: -20px;
        }
    </style>
""", unsafe_allow_html=True)