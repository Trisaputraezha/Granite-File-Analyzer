import streamlit as st
from pathlib import Path
import hashlib
import datetime
import PyPDF2
import docx
import requests

# ===== Granite Analyzer Ringkas & Interaktif =====
class GraniteAnalyzer:
    def __init__(self, lm_base_url="http://127.0.0.1:1234/v1", model="ibm/granite"):
        self.lm_base_url = lm_base_url
        self.model = model

    def analyze_file(self, content, filename):
        lines = content.splitlines()
        words = content.split()
        return {
            "summary": f"{filename} dianalisis: {len(words)} kata, {len(lines)} baris.",
            "insights": ["Struktur baik", "Konten relevan"],
            "conclusion": "File cukup baik, bisa ditingkatkan sesuai saran."
        }

    def chat_with_file(self, question, content):
        # Batasi konten untuk LM Studio agar tidak error 400
        limited_content = "\n".join(content.splitlines()[:100])  # ambil 100 baris pertama

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are a helpful assistant analyzing uploaded file content."},
                {"role": "user", "content": f"File content:\n{limited_content}\n\nQuestion: {question}"}
            ]
        }

        try:
            response = requests.post(f"{self.lm_base_url}/chat/completions", json=payload)
            if response.status_code == 200:
                data = response.json()
                return data['choices'][0]['message']['content']
            else:
                return f"Error dari LM Studio: {response.status_code}"
        except Exception as e:
            return f"Error koneksi ke LM Studio: {e}"

# ===== Fungsi bantu =====
def read_file_content(uploaded_file):
    file_extension = Path(uploaded_file.name).suffix.lower()
    raw = uploaded_file.read()
    if file_extension == '.pdf':
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        return "\n".join([page.extract_text() for page in pdf_reader.pages])
    elif file_extension == '.docx':
        doc = docx.Document(uploaded_file)
        return "\n".join([p.text for p in doc.paragraphs])
    else:
        return raw.decode("utf-8", errors="ignore")

def save_history(filename, analysis, content):
    if 'history' not in st.session_state: st.session_state.history = []
    item = {
        'id': hashlib.md5(f"{filename}{datetime.datetime.now()}".encode()).hexdigest(),
        'filename': filename,
        'timestamp': datetime.datetime.now().isoformat(),
        'analysis': analysis,
        'content': content
    }
    st.session_state.history.insert(0, item)
    if len(st.session_state.history) > 20: st.session_state.history = st.session_state.history[:20]

def delete_all_history():
    st.session_state.history = []
    if 'current_content' in st.session_state: del st.session_state.current_content
    if 'chat_messages' in st.session_state: del st.session_state.chat_messages

# ===== Main App =====
st.title("🧠 Granite File Analyzer")

if 'analyzer' not in st.session_state: st.session_state.analyzer = GraniteAnalyzer()
if 'chat_messages' not in st.session_state: st.session_state.chat_messages = []

# ===== Sidebar =====
st.sidebar.header("📁 History & Controls")
if st.sidebar.button("🗑️ Delete All History"):
    delete_all_history()
    st.sidebar.success("History deleted!")

if 'history' in st.session_state and st.session_state.history:
    for item in st.session_state.history:
        if st.sidebar.button(f"{item['filename']} ({item['timestamp'][:16]})", key=f"history_{item['id']}"):
            st.session_state.current_content = item['content']

# ===== File Upload =====
uploaded_file = st.file_uploader("Upload file (txt, py, csv, json, md, pdf, docx):")
if uploaded_file:
    content = read_file_content(uploaded_file)
    analysis = st.session_state.analyzer.analyze_file(content, uploaded_file.name)
    st.write("**Summary:**", analysis['summary'])
    st.write("**Insights:**", ", ".join(analysis['insights']))
    st.write("**Conclusion:**", analysis['conclusion'])
    save_history(uploaded_file.name, analysis, content)
    st.session_state.current_content = content
    st.session_state.chat_messages = []  # reset chat saat file baru

# ===== Chat Interactive =====
if 'current_content' in st.session_state:
    st.subheader("💬 Chat with File")

    with st.form("chat_form", clear_on_submit=True):
        user_question = st.text_input("Ask anything about the file:")
        submit = st.form_submit_button("Send 💬")
        
        if submit and user_question.strip():
            # Tambahkan user message
            st.session_state.chat_messages.append({"role": "user", "content": user_question})
            # Dapatkan jawaban AI dari LM Studio
            ai_response = st.session_state.analyzer.chat_with_file(user_question, st.session_state.current_content)
            st.session_state.chat_messages.append({"role": "assistant", "content": ai_response})

    # Tampilkan chat secara berurutan
    for msg in st.session_state.chat_messages:
        if msg["role"] == "user":
            st.markdown(f"**You:** {msg['content']}")
        else:
            st.markdown(f"**AI:** {msg['content']}")