STYLES = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Comic+Neue:wght@700&family=Press+Start+2P&display=swap');

:root {
    --primary: #9a7bff;
    --secondary: #5e35b1;
    --dark: #1a1a2e;
    --darker: #0d0d1a;
    --text: #ffffff;
}

body {
    background-color: var(--darker);
    color: var(--text);
    font-family: 'Comic Neue', cursive;
}

h1, h2, h3, h4, h5, h6 {
    font-family: 'Press Start 2P', cursive;
    color: var(--primary) !important;
    text-shadow: 0 0 10px rgba(154, 123, 255, 0.7);
}  

stSpinner {
    width: 40px !important;
    height: 40px !important;
    border-width: 10px !important;
}

.stSpinner > div, .stSpinner > div > div {
    font-size: 45px !important; 
}

.stButton>button {
    background-color: var(--secondary) !important;
    color: white !important;
    border-radius: 20px !important;
    border: 2px solid var(--primary) !important;
    font-family: 'Comic Neue', cursive !important;
    font-weight: 700 !important;
    transition: all 0.3s ease;
}

.stButton>button:hover {
    transform: scale(1.05);
    box-shadow: 0 0 15px var(--primary);
}

.stTextInput>div>div>input {
    background-color: var(--dark) !important;
    color: var(--text) !important;
    border: 2px solid var(--primary) !important;
    border-radius: 10px;
}

.stMarkdown {
    background-color: var(--dark) !important;
    border-radius: 10px;
    padding: 15px;
    border-left: 5px solid var(--primary);
    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
}

.history-item {
    background-color: var(--dark);
    border-radius: 10px;
    padding: 10px;
    margin: 10px 0;
    border-left: 3px solid var(--primary);
    transition: all 0.2s ease;
}

.history-item:hover {
    transform: translateX(5px);
    box-shadow: 0 0 10px rgba(154, 123, 255, 0.5);
}

.delete-btn {
    background-color: #ff4b4b !important;
    color: white !important;
    transition: all 0.2s ease;
}

.delete-btn:hover {
    transform: scale(1.1);
}

.stDownloadButton button {
    background-color: #5e35b1 !important;
    color: white !important;
    border-radius: 20px !important;
    border: 2px solid #9a7bff !important;
    font-family: 'Comic Neue', cursive !important;
    font-weight: 700 !important;
    transition: all 0.3s ease;
    padding: 0.4em 1.2em !important;
}

.stDownloadButton button:hover {
    transform: scale(1.05);
    box-shadow: 0 0 15px #9a7bff;
    background-color: #7c4dff !important;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(-20px); }
    to { opacity: 1; transform: translateY(0); }
}
@keyframes fadeOut {
    from { opacity: 1; }
    to { opacity: 0; }
}
</style>
"""
