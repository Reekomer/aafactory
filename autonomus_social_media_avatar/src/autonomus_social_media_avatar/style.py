CSS_STYLE = """
/* Main theme colors */
:root {
    --primary-color: #00f2ff;
    --secondary-color: #7b2ff7;
    --background-dark: #0a0b1e;
    --text-light: #ffffff;
    --accent-glow: 0 0 10px var(--primary-color);
    --gradient-bg: linear-gradient(135deg, #0a0b1e 0%, #1a1b3e 100%);
}

/* Global styles */
.gradio-container {
    background: var(--gradient-bg) !important;
    color: var(--text-light) !important;
    font-family: 'Space Grotesk', sans-serif !important;
}

/* Headers */
h1, h2, h3 {
    color: var(--primary-color) !important;
    text-shadow: var(--accent-glow) !important;
    font-weight: 600 !important;
}

/* Buttons */
button, .button {
    background: linear-gradient(45deg, var(--primary-color), var(--secondary-color)) !important;
    border: none !important;
    color: var(--text-light) !important;
    box-shadow: var(--accent-glow) !important;
    transition: all 0.3s ease !important;
    text-shadow: none !important;
}

button:hover, .button:hover {
    transform: scale(1.05) !important;
    box-shadow: 0 0 20px var(--primary-color) !important;
    filter: brightness(1.2) !important;
}

/* Input fields */
input, textarea {
    background: rgba(255, 255, 255, 0.05) !important;
    border: 1px solid rgba(0, 242, 255, 0.2) !important;
    color: var(--text-light) !important;
    backdrop-filter: blur(5px) !important;
}

input:focus, textarea:focus {
    border-color: var(--primary-color) !important;
    box-shadow: none !important;
}

/* Chat interface */
.chatbot {
    background: rgba(10, 11, 30, 0.7) !important;
    border: 1px solid var(--primary-color) !important;
    border-radius: 15px !important;
    box-shadow: var(--accent-glow) !important;
}

.message {
    background: rgba(255, 255, 255, 0.05) !important;
    border-radius: 10px !important;
    margin: 10px !important;
    padding: 15px !important;
}

/* Sliders and progress bars */
.slider {
    background: linear-gradient(90deg, var(--primary-color), var(--secondary-color)) !important;
}

.progress-bar {
    background: linear-gradient(90deg, var(--primary-color), var(--secondary-color)) !important;
    height: 4px !important;
    border-radius: 2px !important;
}

/* Tabs and accordions */
.tab-nav {
    border-bottom: 2px solid var(--primary-color) !important;
}

.tab-nav button.selected {
    background: var(--primary-color) !important;
    color: var(--background-dark) !important;
}

/* Cards and containers */
.container {
    background: rgba(255, 255, 255, 0.05) !important;
    backdrop-filter: blur(10px) !important;
    border: 1px solid var(--primary-color) !important;
    border-radius: 15px !important;
    box-shadow: var(--accent-glow) !important;
}

/* Animations */
@keyframes glow {
    0% { box-shadow: 0 0 5px var(--primary-color); }
    50% { box-shadow: 0 0 20px var(--primary-color); }
    100% { box-shadow: 0 0 5px var(--primary-color); }
}

.animate-glow {
    animation: glow 2s infinite;
}

/* Scrollbar */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: var(--background-dark);
}

::-webkit-scrollbar-thumb {
    background: var(--primary-color);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: var(--secondary-color);
}

/* Fix for submit button */
#component-0 > div.wrap.svelte-byatnx > div.wrap.svelte-byatnx > div.grow.svelte-byatnx > div > button,
#component-3 > div.wrap.svelte-byatnx > div.wrap.svelte-byatnx > div.grow.svelte-byatnx > div > button {
    background: linear-gradient(45deg, var(--primary-color), var(--secondary-color)) !important;
    border: none !important;
    color: white !important;
    box-shadow: var(--accent-glow) !important;
    transition: all 0.3s ease !important;
}

#component-0 > div.wrap.svelte-byatnx > div.wrap.svelte-byatnx > div.grow.svelte-byatnx > div > button:hover,
#component-3 > div.wrap.svelte-byatnx > div.wrap.svelte-byatnx > div.grow.svelte-byatnx > div > button:hover {
    transform: scale(1.05) !important;
    box-shadow: 0 0 20px var(--primary-color) !important;
    filter: brightness(1.2) !important;
}
"""