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

## How it Works

1. **User Input**: You enter a theme.
2. **Agents Do the Work**:
   - **Topic Planner**: Suggests 3-7 topics.
   - **Topic Researcher**: Finds info and sources for each topic.
   - **Summary Generator**: Condenses research into titled bullet points.
   - **Link Collector**: Gathers all source links.
   - **Article Prompt Writer**: Assembles everything into a Markdown draft.
3. **Async Processing**: The script uses Python’s async features to speed up agent communication (see [Python async/await](https://superfastpython.com/python-async-function/): lets the script handle multiple tasks at once, instead of waiting for each to finish).
4. **Output**: The results are saved as a `.md` file in your Downloads folder, with a timestamped filename.

---

## Features

- **Fully Automatic**: Just run the script — no manual setup needed.
- **Automatic CrewAI Installation**: Installs required packages if missing.
- **No Extra Dependencies**: Only standard Python libraries and CrewAI are used. 
- **Multi-Agent Workflow**: 5 specialized agents collaborate:
  - Topic Planner
  - Topic Researcher
  - Content Condenser
  - Link Collector
  - Article Prompt Writer  
- **Uses Gemini 2.0 Flash**: Script is set up to use the fast, efficient language model from Google AI, Gemini 2.0 Flash.
- **Async Processing**: Uses Python's `asyncio` for efficient task execution ([What is async?](https://www.theserverside.com/tutorial/Asynchronous-programming-in-Python-tutorial))
- **Handles Errors**: If something goes wrong (e.g., Gemini API fails), the script prints clear messages and continues where possible. 
- **Handles Downloads Folder**: Finds (or creates) your system’s Downloads folder for output.  
- **Markdown Output**: Results are saved in Markdown format for easy editing or sharing.

---

## Technical Highlights
- Automatic Dependency Handling
- Async Processing
- Smart File Handling
- Output Formatting

---

## Repository Structure

```
rag-agentic-ai/
├── 001_10_min_crash_course_on_ai_agents.md        # Notes (not required)    
├── 002_anupam_workflow_on_agentic_ai.md           # Notes (not required)    
├── 003_RAG_vs_fine_tuning_prompt_engineering.md   # Notes (not required)    
├── README.md
├── py_01_article_topic_generator.py                                        # Main script (run this)
├── py_02_download_py_file.py                      # Utility (not required)
├── py_03_delete_zips.py                           # Utility (not required)
└── py_04_where_is_downloads.py                    # Utility (not required)
```

**Only `py_01_article_topic_generator.py` is needed for the main workflow. Other files are not required.**

---

## Dependencies
```python
crewai == 0.28.8
google-generativeai 
ipython # For markdown display in notebooks
```
 
---

## Requirements

- Python 3.10, 3.11, or 3.12
- Internet connection (for CrewAI install and Gemini API)
- Google API key for Gemini (add your key in the script)

---

## Installation
No manual installation required - the script automatically checks for and installs:
1. Python 3.10-3.13
2. CrewAI library
3. Required dependencies

---

## Usage

1. **Clone the repo**:
   ```bash
   git clone https://github.com/yourusername/rag-agentic-ai.git
   cd rag-agentic-ai
   ```

2. **Run the script**:
   ```bash
   python py_01_article_topic_generator.py
   ```  

---

### Workflow:
1. Enter your theme (e.g., "Artificial Intelligence")
2. System generates 3-7 topics
3. Agents research and condense information
4. Output saved as `Article_Topic_Generated_DD-MM-YYYY_HH-MM-SS.md` in your downloads folder

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

## Details & Quirks

- **Automatic Downloads Folder**: The script checks for your Downloads folder and creates it if missing.
- **Async/await**: Used for agent calls to keep things responsive and efficient.
- **Gemini API Requirements**: Requires valid `GOOGLE_API_KEY`. May occasionally return `None` responses (retry if occurs).
- **Markdown Output**: The file is formatted for easy reading or further editing. Triple backticks are automatically stripped from the markdown output to ensure proper formatting.
- **Error Handling**: If the AI model returns an empty or failed response, the script prints a warning but continues.
- **CrewAI Install**: The script checks for CrewAI and installs it if not present, so you don’t need to worry about dependencies.
- **Model**: Uses `gemini/gemini-2.0-flash` by default (you can change this in the code if needed).
  
---

## Notes

- Only the main script (`py_01_article_topic_generator.py`) is needed for normal use.
- The other `.py` files are utilities or experiments and not part of the main workflow.
- For related code about file and downloads folder handling, see [this discussion](https://www.perplexity.ai/search/import-os-import-zipfile-impor-E0IlKSJuSkqZHNCqtW5UIQ).

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
[2] https://www.theserverside.com/tutorial/Asynchronous-programming-in-Python-tutorial
[3] https://ai.google.dev/gemini-api/docs/text-generation 
[4] https://github.com/rithikamalve/python-file-download-automator 
