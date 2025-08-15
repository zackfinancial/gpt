# Finance Services Chatbot (Streamlit)

A generic finance Q&A chatbot that also suggests up to three relevant services from a simple `services.yaml` catalog.
**Educational use only — not legal or tax advice.**

## Quick Start (Local)
```bash
pip install -r requirements.txt
# Add a local secrets file (optional):
#   .streamlit/secrets.toml  ->  OPENAI_API_KEY="sk-..."
streamlit run app.py
```

## Deploy: Streamlit Community Cloud (fastest)
1. Push these files to a **public GitHub repo**.
2. On Streamlit Cloud, create an app from your repo.
3. In the app's **Secrets**, add:
   ```
   OPENAI_API_KEY="sk-..."
   FIRM_NAME="Zack Financial"
   CONTACT_EMAIL="hello@example.com"
   MODEL_NAME="gpt-4o-mini"
   ```
4. Open the app → copy its public URL (ends with `.streamlit.app`).

### Embed on your website (Squarespace/any site)
Add a Code block and paste:
```html
<iframe
  src="https://YOUR-APP-URL"
  style="width:100%; height:900px; border:0;"
  allow="clipboard-read; clipboard-write;"
  loading="lazy"
  referrerpolicy="no-referrer-when-downgrade">
</iframe>
```

## Environment Variables (optional)
- `FIRM_NAME` (default: "Zack Financial")
- `CONTACT_EMAIL` (default: "hello@example.com")
- `MODEL_NAME` (default: "gpt-4o-mini")

## Notes
- Uses OpenAI **Responses API** via `openai` Python SDK.
- Service matching is a simple keyword heuristic to keep hosting free and fast.
- To ground answers in your docs later, add retrieval (embeddings or file search) and cite sources in responses.
