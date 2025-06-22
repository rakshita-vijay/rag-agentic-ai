# Article Topic Generator with CrewAI 

This project is an automated article topic generator that uses **CrewAI** agents to:
1. Generate engaging topics based on a user-provided theme
2. Research each topic in-depth
3. Create structured article prompts with condensed information and resources
4. Save results as a formatted markdown file in your downloads folder

The system uses **Gemini 2.0 Flash** as its language model and features automatic dependency installation, async processing, and smart file handling.

---

## Overview

This script helps you brainstorm and organize article ideas on any theme you choose. It’s designed for practical use: just run the script, enter your topic, and get a ready-to-use Markdown file with topics, subtopics, and sources.

---

## Features

- **Fully Automatic**: Just run the script - no manual setup needed.
- **Automatic CrewAI Installation**: Installs CrewAI if missing, so you don’t need to manage dependencies.
- **No Extra Dependencies**: Only standard Python libraries and CrewAI are used.
- **Multi-Agent Workflow**: Five specialized agents (planner, researcher, condenser, collector, writer) collaborate to generate, research, summarize, and format topics.
- **Uses Gemini 2.0 Flash**: Built to use Google’s Gemini 2.0 Flash model for language processing (requires a valid `GOOGLE_API_KEY`).
- **Async Processing**: Uses Python’s `asyncio` for efficient, non-blocking task execution ([What is async?](https://www.theserverside.com/tutorial/Asynchronous-programming-in-Python-tutorial)).
- **Error Handling**: Prints clear warnings if the AI model fails or returns empty data, and continues processing where possible.
- **Smart Downloads Folder Handling**: Finds (or creates) your system’s Downloads folder automatically; output is saved there with a timestamped filename.
- **Markdown Output**: Results are saved in easy-to-edit Markdown format; triple backticks are automatically stripped for proper formatting.
- **Output Display**: If run in a Jupyter notebook, uses `IPython.display` to render formatted markdown.
- **Model Customization**: To use a different LLM, change the `model` parameter in the LLM initialization.
- **Resilient to Gemini quirks**: If Gemini occasionally returns `None`, the script will warn you and you can retry. 

---

## Repository Structure 
```
rag-agentic-ai/
├── extra_code/                                      # Utility scripts (not required)
│   ├── py_02_download_py_file.py 
│   ├── py_03_delete_zips.py 
│   └── py_04_where_is_downloads.py 
├── notes/                                           # Reference notes (not required)
│   ├── 001_10_min_crash_course_on_ai_agents.md 
│   ├── 002_anupam_workflow_on_agentic_ai.md 
│   └── 003_RAG_vs_fine_tuning_prompt_engineering.md 
├── README.md
└── py_01_article_topic_generator.py                 # Main script (run this) 
```

**Only `py_01_article_topic_generator.py` is needed for the main workflow. The other `.py` files are utilities/experiments, and not part of the main workflow.**

---

## Dependencies
```python
crewai == 0.28.8         # auto-installed
google-generativeai 
ipython                  # For markdown display in notebooks
```
 
---

## Requirements

- Python 3.10, 3.11, or 3.12
- Internet connection (for CrewAI install and Gemini API)
- Google API key for Gemini (add your key in the script)

---

## Installation
No manual installation required - the script automatically checks for and installs: 
1. CrewAI library
2. Required dependencies

---

## Usage

1. **Clone the repo**:
   ```bash
   git clone https://github.com/yourusername/rag-agentic-ai.git
   cd rag-agentic-ai
   ```
   
2. **Enter your own valid API key**:
   <br>Search for ```GOOGLE_API_KEY```, and replace it with an API key generated from ([Google AI Studio](https://aistudio.google.com/app/apikey)). 
   
4. **Run the script**:
   ```bash
   python py_01_article_topic_generator.py
   ```  

---
 
## Workflow:

1. **User Input**: You enter a theme.
2. **Agents Do the Work**:
   - **Topic Planner**: Suggests 3-7 topics.
   - **Topic Researcher**: Finds info and sources for each topic.
   - **Summary Generator**: Condenses research into titled bullet points.
   - **Link Collector**: Gathers all source links.
   - **Article Prompt Writer**: Assembles everything into a Markdown draft.
3. **Async Processing**: The script uses Python’s async features to speed up agent communication (lets the script handle multiple tasks at once, instead of waiting for each to finish).
4. **Output**: The results are saved as a `.md` file in your Downloads folder, with a timestamped filename - `Article_Topic_Generated_DD-MM-YYYY_HH-MM-SS.md`.
 
---

## Agent Architecture
| Agent | Role | Key Function |
|-------|------|-------------|
| **Topic Planner** | Strategist | Generates theme-related topics |
| **Topic Researcher** | Investigator | Researches each topic in-depth |
| **Content Condenser** | Summarizer | Creates bullet-point summaries |
| **Link Collector** | Archivist | Gathers research sources |
| **Article Prompt Writer** | Compiler | Formats final output | 

---

## Related Resources
- [CrewAI Documentation](https://docs.crewai.com)
- [Gemini API Guide](https://ai.google.dev)
- [Async Programming Tutorial](https://www.theserverside.com/tutorial/Asynchronous-programming-in-Python-tutorial)
- [File Handling Best Practices](https://dnmttechs.com/automatically-installing-required-packages-in-python-script/)

---  

**This project is intended as a practical tool for generating article ideas and outlines. Pull requests and suggestions are welcome!**

---

## Links I Referred to for Ideas:

[1] https://dnmtechs.com/automatically-installing-required-packages-in-python-script/
<br>[2] https://www.theserverside.com/tutorial/Asynchronous-programming-in-Python-tutorial
<br>[3] https://ai.google.dev/gemini-api/docs/text-generation 
<br>[4] https://github.com/rithikamalve/python-file-download-automator 
