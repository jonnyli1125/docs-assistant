# docs-assistant

Chat bot assistant for asking questions about documentation databases using LangChain.

This uses the `RetrievalQA` chain, in combination with the `Chroma` and `OpenAI` classes.

# Usage

To load documents into the DB, use the scripts in [docs_assistant/loaders](docs_assistant/loaders):
```
python -m docs_assistant.loaders.textfiles /path/to/db/ file1.txt file2.txt
```

To run the bot:
```
CHROMA_DB_DIR="/path/to/db/"
OPENAI_API_KEY="..."
python -m docs_assistant.bot.cli
```

To run the slack bot:
```
CHROMA_DB_DIR="/path/to/db/"
OPENAI_API_KEY="..."
SLACK_APP_TOKEN="..."
SLACK_BOT_TOKEN="..."
python -m docs_assistant.bot.slack
```
