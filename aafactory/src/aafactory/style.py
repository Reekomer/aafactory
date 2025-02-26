CSS = """
/* Main theme colors */
:root {
    --primary-color: #73111e;
    --secondary-color: #18A1FA;
    --accent-color: #06BEE1;
    --background-dark: #0F172A;
    --background-light: #1E293B;
    --text-light: #F8FAFC;
    --text-muted: #94A3B8;
    --border-color: rgba(45, 127, 249, 0.2);
    --shadow-color: rgba(45, 127, 249, 0.1);
    --gradient-bg: linear-gradient(135deg, var(--background-dark) 0%, var(--background-light) 100%);
}

/* Global styles */
.gradio-container {
    background: var(--gradient-bg) !important;
    color: var(--text-light) !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

/* Headers */
h1, h2, h3 {
    color: var(--text-light) !important;
    font-weight: 600 !important;
    letter-spacing: -0.02em !important;
    margin-bottom: 1rem !important;
}

/* Buttons */
button, .button {
    background: var(--primary-color) !important;
    border: none !important;
    color: var(--text-light) !important;
    padding: 0.5rem 1rem !important;
    border-radius: 8px !important;
    font-weight: 500 !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 2px 4px var(--shadow-color) !important;
}

button:hover, .button:hover {
    background: var(--secondary-color) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 8px var(--shadow-color) !important;
}

/* Input fields */
input, textarea {
    background: var(--background-light) !important;
    border: 1px solid var(--border-color) !important;
    color: var(--text-light) !important;
    border-radius: 8px !important;
    padding: 0.75rem !important;
    transition: all 0.2s ease !important;
}

input:focus, textarea:focus {
    border-color: var(--primary-color) !important;
    box-shadow: 0 0 0 2px var(--shadow-color) !important;
    outline: none !important;
}

/* Labels */
label {
    color: var(--text-muted) !important;
    font-size: 0.875rem !important;
    font-weight: 500 !important;
    margin-bottom: 0.5rem !important;
}

/* Chat interface */
.chatbot {
    background: var(--background-light) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 12px !important;
    box-shadow: 0 4px 6px var(--shadow-color) !important;
    overflow: hidden !important;
}

.message {
    background: var(--background-dark) !important;
    border-radius: 8px !important;
    margin: 0.5rem !important;
    padding: 1rem !important;
    color: var(--text-light) !important;
}

/* Dropdowns and Selects */
select, .select {
    background: var(--background-light) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 8px !important;
    color: var(--text-light) !important;
    padding: 0.5rem !important;
}

/* Progress bars */
.progress-bar {
    background: var(--primary-color) !important;
    height: 4px !important;
    border-radius: 2px !important;
}

/* Scrollbar */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}

::-webkit-scrollbar-track {
    background: var(--background-dark);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb {
    background: var(--primary-color);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: var(--secondary-color);
}

/* Containers and Cards */
.container, .card {
    background: var(--background-light) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 12px !important;
    padding: 1.5rem !important;
    margin: 1rem 0 !important;
    box-shadow: 0 4px 6px var(--shadow-color) !important;
}

/* Fix for Gradio specific elements */
.gr-box, .gr-form {
    border-radius: 12px !important;
    border: 1px solid var(--border-color) !important;
    background: var(--background-light) !important;
}

.gr-padded {
    padding: 1.5rem !important;
}

/* Responsive adjustments */
@media (max-width: 640px) {
    .container, .card {
        padding: 1rem !important;
    }
    
    button, .button {
        width: 100% !important;
    }
}

/* Audio and Video elements */
audio, video {
    border-radius: 8px !important;
    background: var(--background-dark) !important;
    margin: 0.5rem 0 !important;
}

/* File upload areas */
.upload-box {
    border: 2px dashed var(--border-color) !important;
    border-radius: 12px !important;
    background: var(--background-dark) !important;
    padding: 2rem !important;
    text-align: center !important;
}

.upload-box:hover {
    border-color: var(--primary-color) !important;
}
"""