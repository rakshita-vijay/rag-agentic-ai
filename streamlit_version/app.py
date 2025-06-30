__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import os, sys, datetime, uuid, asyncio, base64, random
import styles, scripts # custom modules

import streamlit as st

def monitor_progress():
    """Display progress messages as they come in"""
    if 'progress_messages' in st.session_state and st.session_state.progress_messages:
        st.markdown("### 🔄 Progress Updates")
        for i, msg in enumerate(st.session_state.progress_messages):
            st.success(msg)

try:
    from generator import generate_article_topics
    GENERATOR_AVAILABLE = True
except ImportError as e:
    GENERATOR_AVAILABLE = False
    st.error(f"Missing dependencies: {e}")
    st.info("Please ensure requirements.txt includes all dependencies")
    st.stop()

# Apply custom styles
st.markdown(styles.STYLES, unsafe_allow_html=True)

# Initialize session state
if 'history' not in st.session_state:
    st.session_state.history = []

if 'notification' not in st.session_state:
    st.session_state.notification = None

if 'progress_messages' not in st.session_state:
    st.session_state.progress_messages = []

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
    st.components.v1.html(js)

# Progress callback for real-time updates
def progress_callback(message):
    st.session_state.progress_messages.append(message)

# UI Components
st.title("✨ AI Article Topic Generator")
st.subheader("Create engaging article topics with AI")

# API Key check
if not os.environ.get("GOOGLE_API_KEY"):
    st.error("🔑 GOOGLE_API_KEY environment variable not set. Please set your Gemini API key.")
    st.info("For local development, run: `export GOOGLE_API_KEY='your-api-key'`")
    st.stop()

# Main input area
with st.form("generator_form"):
    theme = st.text_input(
        "Enter your theme:",
        placeholder="e.g., Artificial Intelligence in Healthcare",
        help="Be specific for better results"
    )
    generate_btn = st.form_submit_button("🚀 Generate Topics with AI")

    if generate_btn and theme:
        # Clear previous progress messages
        st.session_state.progress_messages = []

        num_topics = random.randint(5, 10)
        st.session_state['num_topics'] = num_topics

        st.balloons()
        st.success(f"🎉  {num_topics} topics will be generated!")
        progress_placeholder = st.empty()

        with st.spinner("🔮 AI agents are working on your request..."):
            try:
                # Function to update progress display
                def update_progress_display():
                    with progress_placeholder.container():
                        for msg in st.session_state.get('progress_messages', []):
                            st.success(msg)

                # Initial progress display
                update_progress_display()

                # Run the async generator
                result_data = asyncio.run(generate_article_topics(theme, num_topics, progress_callback))

                # Final update
                update_progress_display()

                # Add to history
                history_item = {
                    "id": str(uuid.uuid4()),
                    "theme": theme,
                    "content": result_data['content'],
                    "topic_count": result_data['topic_count'],
                    "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                st.session_state.history.insert(0, history_item)
                st.session_state.notification = f"✨ Generated {result_data['topic_count']} topics successfully!"

                # Display results
                st.markdown("### 📝 Generated Topics")
                st.markdown(result_data['content'])

                # Download button
                ts = datetime.datetime.now()
                in_ts = f"{ts.day}_{ts.month}_{ts.year}_{ts.hour}_{ts.minute}_{ts.second}"
                filename = f"article_topics_{theme.replace(' ', '_')}_{in_ts}.md"
                content_with_header = f"# Theme: {theme}\n\n---\n\n{result_data['content']}"

                b64 = base64.b64encode(content_with_header.encode()).decode()
                href = f'<a href="data:file/md;base64,{b64}" download="{filename}" style="color: #9a7bff; font-weight: bold; font-size: 18px; text-decoration: none;">📥 Download Topics as Markdown</a>'
                st.markdown(href, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"❌ Error generating topics: {str(e)}")
                st.info("Please check your API key and try again.")

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
        with st.sidebar.expander(f"{item['theme']} ({item['topic_count']} topics)"):
            st.markdown(f"**Generated:** {item['timestamp']}")
            st.markdown("**Preview:**")
            # Show first 200 characters
            preview = item['content'][:200] + "..." if len(item['content']) > 200 else item['content']
            st.markdown(preview)

            col1, col2 = st.columns(2)
            with col1:
                if st.button("📖 View Full", key=f"view_{item['id']}", use_container_width=True):
                    st.session_state[f"show_full_{item['id']}"] = True
            with col2:
                if st.button("🗑️ Delete", key=f"delete_{item['id']}", use_container_width=True, type="primary"):
                    st.session_state.history = [h for h in st.session_state.history if h['id'] != item['id']]
                    st.session_state.notification = "🗑️ History item deleted!"
                    st.rerun()

            # Show full content if requested
            if st.session_state.get(f"show_full_{item['id']}", False):
                st.markdown("**Full Content:**")
                st.markdown(item['content'])
                if st.button("Hide", key=f"hide_{item['id']}"):
                    st.session_state[f"show_full_{item['id']}"] = False
                    st.rerun()

# Add custom notification component
st.markdown(scripts.NOTIFICATION_SCRIPT, unsafe_allow_html=True)

# Footer
st.markdown("🤖 Powered by CrewAI & Gemini 2.0 Flash")
