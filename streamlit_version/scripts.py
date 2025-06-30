NOTIFICATION_SCRIPT = """
<script>
document.addEventListener('streamlit:showNotification', function(e) {
    const {message, type, duration} = e.detail;
    const notification = document.createElement('div');
    notification.innerHTML = message;
    notification.style = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px;
        background-color: ${type === 'error' ? '#ff4b4b' : '#9a7bff'};
        color: white;
        border-radius: 10px;
        z-index: 1000;
        font-family: 'Comic Neue', cursive;
        font-weight: bold;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        animation: fadeIn 0.5s, fadeOut 0.5s ${duration ? duration - 500 : 2500}ms;
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, duration || 3000);
});
</script>
"""
