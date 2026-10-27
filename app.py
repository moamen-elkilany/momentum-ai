import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="Momentum AI", page_icon="⚡", layout="centered")

st.title("⚡ Momentum Chatbot")
st.write("Welcome to Momentum AI!")

# سحب مفتاح السر من إعدادات السيرفر الآمنة أوتوماتيكياً
try:
    api_key = st.secrets["GROQ_API_KEY"]
except:
    st.error("⚠️ Please configure your GROQ_API_KEY in Streamlit Secrets.")
    api_key = None

if api_key:
    try:
        client = OpenAI(
            base_url="https://api.groq.com/openai/v1",
            api_key=api_key
        )
        
        # اختيار الموديل المتاح تلقائياً
        models = client.models.list()
        model_ids = [model.id for model in models.data]
        active_model = model_ids[0] if model_ids else "llama-3.3-70b-versatile"

        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("Type your message here..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                stream = client.chat.completions.create(
                    model=active_model,
                    messages=[
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.messages
                    ],
                    stream=True,
                )
                
                full_response = st.write_stream(stream)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
                    
    except Exception as e:
        st.error(f"Connection Error: {e}")