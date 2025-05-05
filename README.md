LangChain Research Assistant
A powerful research assistant application built with LangChain that helps users generate research papers by gathering information from multiple sources.

Features
- Search the web for information using DuckDuckGo
- Query Wikipedia for detailed topic information
- Save research results to text files
- Structured output with topic, summary, sources, and tools used

Installation
1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```
Usage
Run the application:
```
python main.py
```

Enter your research query when prompted. The assistant will gather information and present structured results. You can choose to save the results to a file.

Technologies
- LangChain framework for agent orchestration
- OpenAI GPT-3.5 Turbo for natural language understanding
- Pydantic for data validation and structure
- DuckDuckGo and Wikipedia APIs for information retrieval

Project Structure
- `main.py`: Main application logic and workflow
- `tools.py`: Custom tools for search, Wikipedia queries, and saving results
- `requirements.txt`: Project dependencies
