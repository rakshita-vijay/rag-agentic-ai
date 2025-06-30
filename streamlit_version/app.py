__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import os, asyncio, random, uuid, datetime, base64, styles, scripts
import streamlit as st

# from streamlit_extras.let_it_rain import rain 

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
    # st.write(f"✅ Completed {p['current']}/{p['total']} tasks")
    # st.session_state.status_text.text(f"✅ Completed {p['current']}/{p['total']} tasks")
    st.text(f"✅ Completed {p['current']}/{p['total']} tasks")
    # st.markdown(f'<span style="color: #fff; font-size: 1.05rem; font-family: inherit;">✅ Completed {p["current"]}/{p["total"]} tasks</span>', unsafe_allow_html=True)
    
    # Messages
    for msg in st.session_state.progress_messages:
        st.success(msg)
    
    # Completion celebration
    if p["current"] == p["total"] and st.session_state.result_data:
        st.balloons() 
        # st.snow()
        
        # rain(
        #     emoji="🎉",
        #     font_size=60,
        #     falling_speed=3,
        #     animation_length=5000
        # )
        st.success("🎉 All tasks completed!")

# Main input area
with st.form("generator_form"):
    theme = st.text_input("Enter theme:", placeholder="e.g., Artificial Intelligence")
    generate_btn = st.form_submit_button("🚀 Generate Topics")
    
    st.session_state.num_topics = random.randint(5, 10) 
    st.balloons()
    # st.snow()
    
    # rain(
    #     emoji="🎉",
    #     font_size=60,
    #     falling_speed=3,
    #     animation_length=5000
    # ) 
    
    if generate_btn and theme:
        # Reset state for new generation
        st.session_state.generation_started = True
        st.session_state.progress = {"current": 0, "total": 5}
        st.session_state.progress_messages = []
        st.session_state.result_data = None 
        # st.balloons()
        # rain()
        st.success(f"🎉 {st.session_state.num_topics} topics will be generated!")
        
        # Show initial progress
        show_progress()
        
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
    ts = datetime.datetime.now()
    in_ts = f"{ts.day}_{ts.month}_{ts.year}_{ts.hour}_{ts.minute}_{ts.second}"
    filename = f"article_topics_{theme.replace(' ', '_')}_{in_ts}.md"
     
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
        expander_label = f"{item['theme']} ({item['topic_count']} topics)"
        with st.sidebar.expander(expander_label):
            expanded_key = f"expanded_{item['id']}"
            if expanded_key not in st.session_state:
                st.session_state[expanded_key] = False

            # Show preview or full content based on expanded state
            if not st.session_state[expanded_key]:
                st.markdown(f"**Generated:** {item['timestamp']}")
                st.markdown(f"**Preview:** {item['content'][:200]}...")

                col1, col2 = st.columns(2)
                with col1:
                    if st.button("🔎 Expand", key=f"expand_{item['id']}", use_container_width=True):
                        st.session_state[expanded_key] = True
                        st.rerun()
                with col2:
                    if st.button("🗑️ Delete", key=f"delete_{item['id']}", use_container_width=True):
                        st.session_state.history = [h for h in st.session_state.history if h['id'] != item['id']]
                        st.rerun()
            else:
                st.markdown(f"**Generated:** {item['timestamp']}")
                st.markdown("**Full Content:**")
                st.markdown(item['content'])

                col1, col2 = st.columns(2)
                with col1:
                    if st.button("🔙 Collapse", key=f"collapse_{item['id']}", use_container_width=True):
                        st.session_state[expanded_key] = False
                        st.rerun()
                with col2:
                    if st.button("🗑️ Delete", key=f"delete_{item['id']}_expanded", use_container_width=True):
                        st.session_state.history = [h for h in st.session_state.history if h['id'] != item['id']]
                        st.rerun()
else:
    st.sidebar.info("No history yet")

# Add custom notification component
st.markdown(scripts.NOTIFICATION_SCRIPT, unsafe_allow_html=True)

# Footer 
st.markdown("🤖 Powered by CrewAI & Gemini 2.0 Flash") 
