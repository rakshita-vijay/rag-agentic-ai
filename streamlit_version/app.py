__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import os
import streamlit as st
import asyncio
import random
import uuid
import datetime
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
if 'progress' not in st.session_state:
    st.session_state.progress = {"current": 0, "total": 5}
if 'progress_messages' not in st.session_state:
    st.session_state.progress_messages = []
if 'generation_started' not in st.session_state:
    st.session_state.generation_started = False
if 'result_data' not in st.session_state:
    st.session_state.result_data = None

# UI Components
st.title("✨ AI Article Topic Generator")
st.subheader("Create engaging article topics with AI")

# API Key check
if not os.environ.get("GOOGLE_API_KEY"):
    st.error("🔑 GOOGLE_API_KEY not set. Add it in Streamlit Secrets")
    st.stop()

# Progress display function
def show_progress():
    """Display current progress state"""
    p = st.session_state.progress
    progress_pct = int((p["current"] / p["total"]) * 100)
    
    # Progress bar
    st.progress(progress_pct)
    
    # Status text
    st.subheader(f"✅ Completed {p['current']}/{p['total']} tasks")
    
    # Messages
    for msg in st.session_state.progress_messages:
        st.success(msg)
    
    # Completion celebration
    if p["current"] == p["total"] and st.session_state.result_data:
        st.balloons()
        st.success("🎉 All tasks completed!")

# Main input area
with st.form("generator_form"):
    theme = st.text_input("Enter theme:", placeholder="e.g., Artificial Intelligence")
    generate_btn = st.form_submit_button("🚀 Generate Topics")
    
    if generate_btn and theme:
        # Reset state for new generation
        st.session_state.generation_started = True
        st.session_state.progress = {"current": 0, "total": 5}
        st.session_state.progress_messages = []
        st.session_state.result_data = None
        
        # Show initial progress
        show_progress()
        
        # Start generation
        st.session_state.num_topics = random.randint(5, 10)
        st.rerun()

# Generation runner
if st.session_state.get('generation_started') and not st.session_state.result_data:
    try:
        # Show spinner while working
        with st.spinner("🔮 AI agents are working..."):
            result = asyncio.run(
                generate_article_topics(
                    theme,
                    st.session_state.num_topics
                )
            )
            st.session_state.result_data = {
                'content': result.raw,
                'theme': theme,
                'topic_count': st.session_state.num_topics,
                'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        st.session_state.generation_started = False

# Show progress if generation started
if st.session_state.get('generation_started'):
    show_progress()

# Show results when available
if st.session_state.get('result_data'):
    data = st.session_state.result_data
    st.markdown("### 📝 Generated Topics")
    st.markdown(data['content'])
    
    # Download button
    filename = f"topics_{data['theme']}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    b64 = base64.b64encode(data['content'].encode()).decode()
    href = f'<a href="data:file/md;base64,{b64}" download="{filename}" style="color: #9a7bff; font-weight: bold;">📥 Download Topics</a>'
    st.markdown(href, unsafe_allow_html=True)
    
    # Add to history
    st.session_state.history.insert(0, {
        "id": str(uuid.uuid4()),
        "theme": data['theme'],
        "content": data['content'],
        "topic_count": data['topic_count'],
        "timestamp": data['timestamp']
    })
    
    # Reset flags
    st.session_state.generation_started = False

# History sidebar
st.sidebar.title("📚 Generation History")
if st.session_state.history:
    for item in st.session_state.history[:5]:
        with st.sidebar.expander(f"{item['theme']} ({item['topic_count']} topics)"):
            st.markdown(f"**Generated:** {item['timestamp']}")
            st.markdown(f"**Preview:** {item['content'][:100]}...")
            if st.button("🗑️ Delete", key=f"delete_{item['id']}"):
                st.session_state.history = [h for h in st.session_state.history if h['id'] != item['id']]
                st.rerun()
else:
    st.sidebar.info("No history yet")

# Add custom notification component
st.markdown(scripts.NOTIFICATION_SCRIPT, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("🤖 Powered by CrewAI & Gemini 2.0 Flash")


'''
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import os, sys, datetime, uuid, asyncio, base64, random
import styles, scripts # custom modules

import streamlit as st 
 
def update_progress():
    if 'progress' in st.session_state:
        p = st.session_state.progress
        progress_pct = int((p["current"] / p["total"]) * 100)
        
        # Update progress bar and status
        if 'progress_bar' in st.session_state and 'status_text' in st.session_state:
            st.session_state.progress_bar.progress(progress_pct)
            st.session_state.status_text.text(f"✅ Completed {p['current']}/{p['total']} tasks")
        
        # Update messages
        if 'message_container' in st.session_state:
            with st.session_state.message_container.container():
                if 'progress_messages' in st.session_state:
                    # st.markdown("### 🔄 Progress Updates")
                    for msg in st.session_state.progress_messages:
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
    js = f"""
    <script>
        document.dispatchEvent(new CustomEvent("streamlit:showNotification", {{
            detail: {{
                message: "{message}",
                type: "{type}",
                duration: 3000
            }}
        }}));
    </script>
    """
    st.components.v1.html(js)

# Progress callback for real-time updates
def progress_callback(message):
    st.session_state.progress_messages.append(message)

# UI Components
st.title("✨ AI Article Topic Generator !!! ~~~")
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

        # Initialize progress tracking
        st.session_state.progress = {"current": 0, "total": 5}  # 5 tasks
 
        st.session_state.progress_bar = st.progress(0)
        st.session_state.status_text = st.empty()
        st.session_state.message_container = st.container()
     
        update_progress()

        num_topics = random.randint(5, 10)
        st.session_state['num_topics'] = num_topics

        st.balloons()
        st.success(f"🎉 {num_topics} topics will be generated!")
        st.write()
        
        with st.spinner("🔮 AI agents are working on your request..."):
            try:  
                result_data = asyncio.run(generate_article_topics(theme, num_topics, progress_callback))  

                # Add to history
                history_item = {
                    "id": str(uuid.uuid4()),
                    "theme": theme,
                    "content": result_data['content'],
                    "topic_count": result_data['topic_count'],
                    "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                } 
                st.session_state.history.insert(0, history_item) 
             
                st.balloons()
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
'''
