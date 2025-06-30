import streamlit as st
import datetime
import uuid
from streamlit.components.v1 import html
import base64
import styles
import scripts

# Apply custom styles
st.markdown(styles.STYLES, unsafe_allow_html=True)

# Initialize session state
if 'history' not in st.session_state:
    st.session_state.history = []

if 'notification' not in st.session_state:
    st.session_state.notification = None

# Notification system
def show_notification(message, type="success"):
    js = f'''
    <script>
        document.dispatchEvent(new CustomEvent("streamlit:showNotification", {{
            detail: {{
                message: "{message}",
                type: "{type}",
                duration: 3000
            }}
        }}));
    </script>
    '''
    html(js)

# Article generator function (replace with your actual implementation)
def generate_article_topics(theme):
    # This would call your CrewAI agents
    # For demo, we'll return mock data
    topics = [
        f"## {theme} Topic 1\n- Point A\n- Point B\n- Point C",
        f"## {theme} Topic 2\n- Point X\n- Point Y\n- Point Z"
    ]
    return "\n\n".join(topics)

# UI Components
st.title("✨ AI Article Topic Generator")
st.subheader("Create engaging article topics with AI")

# Main input area
with st.form("generator_form"):
    theme = st.text_input("Enter your theme:", placeholder="e.g., Artificial Intelligence")
    generate_btn = st.form_submit_button("✨ Generate Topics")
    
    if generate_btn and theme:
        with st.spinner("🔮 AI is generating your topics..."):
            # Generate content
            result = generate_article_topics(theme)
            
            # Add to history
            history_item = {
                "id": str(uuid.uuid4()),
                "theme": theme,
                "content": result,
                "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            st.session_state.history.insert(0, history_item)
            st.session_state.notification = "✨ Topics generated successfully!"
            
            # Display results
            st.markdown("### Generated Topics")
            st.markdown(result, unsafe_allow_html=True)
            
            # Download button
            b64 = base64.b64encode(result.encode()).decode()
            href = f'<a href="data:file/md;base64,{b64}" download="topics.md" style="color: #9a7bff; font-weight: bold; font-size: 18px;">📥 Download Topics</a>'
            st.markdown(href, unsafe_allow_html=True)

# Display notification if exists
if st.session_state.notification:
    show_notification(st.session_state.notification)
    st.session_state.notification = None

# History sidebar
st.sidebar.title("📚 Generation History")
st.sidebar.markdown("Your previously generated topics:")

if not st.session_state.history:
    st.sidebar.info("No history yet. Generate some topics first!")
else:
    for i, item in enumerate(st.session_state.history[:5]):
        with st.sidebar.container():
            st.markdown(
                f"<div class='history-item'>"
                f"<b>{item['theme']}</b><br>"
                f"<small>{item['timestamp']}</small>"
                f"</div>", 
                unsafe_allow_html=True
            )
            if st.button("🗑️ Delete", key=f"delete_{item['id']}", use_container_width=True, type="primary"):
                st.session_state.history = [h for h in st.session_state.history if h['id'] != item['id']]
                st.session_state.notification = "🗑️ History item deleted!"
                st.rerun()

# Add custom notification component
st.markdown(scripts.NOTIFICATION_SCRIPT, unsafe_allow_html=True)
