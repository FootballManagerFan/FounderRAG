# Setup Instructions

## 1. Environment Variables

Create a `.env` file in the project root with your OpenAI API key:

```bash
OPENAI_API_KEY=your-api-key-here
```

**Get your API key from:** https://platform.openai.com/api-keys

⚠️ **NEVER commit `.env` to Git!** It's already in `.gitignore`.

## 2. Install Dependencies

```bash
pip install -r requirements.txt
```

## 3. Create the Database

```bash
python create_database.py
```

## 4. Run the Web UI

```bash
python app.py
```

Then visit: http://localhost:8000

## 5. Query from Command Line (Optional)

```bash
python query_data.py "How did Elon Musk approach rapid iteration?"
```

---

## Security Best Practices

✅ **DO:**
- Keep `.env` in your local directory only
- Use environment variables for all secrets
- Check `.gitignore` before committing

❌ **DON'T:**
- Hardcode API keys in scripts
- Commit `.env` files
- Share API keys in screenshots or documentation

