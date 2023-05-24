# docs-assistant

Chat bot assistant for asking questions about documentation databases using LangChain.

This uses the `RetrievalQA` chain, in combination with the `Chroma` and `OpenAI` classes.

## Usage

Steps:
1. Run the scripts in [docs_assistant/loaders](docs_assistant/loaders) to load documents into the vector DB (Chroma)
2. Run any of the scripts in [docs_assistant/bot](docs_assistant/bot) to start a bot that queries the DB
3. Start chatting with the bot to query the DB and get LLM-generated responses to the question.

All scripts require the the following environment variables to be set:
```
OPENAI_API_KEY="..."
CHROMA_DB_DIR="/path/to/chroma/db"
```

### Loading documents ([docs_assistant/loaders](docs_assistant/loaders))

Text files:
```
python -m docs_assistant.loaders.textfiles /path/to/chroma/db/ file1.txt file2.txt ...
```

Confluence:
```
CONFLUENCE_API_KEY="..."
CONFLUENCE_URL="https://domain.com/wiki"
CONFLUENCE_USERNAME="username@domain.com"
python -m docs_assistant.loaders.confluence "type=page and space=SPACE"
```

### Running the bot ([docs_assistant/bot](docs_assistant/bot))

Within the terminal:
```
python -m docs_assistant.bot.cli
```

As a slack bot:
```
SLACK_APP_TOKEN="..."
SLACK_BOT_TOKEN="..."
python -m docs_assistant.bot.slack
```
