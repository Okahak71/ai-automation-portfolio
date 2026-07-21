# ⚡ n8n AI Content Processing Workflow

An automated workflow pipeline built for **n8n** that receives raw webhook data, runs custom Python pre-processing to sanitize text, and routes formatted prompts to OpenAI LLM nodes for urgency classification and summarization.

---

## 🚀 Features
- **Webhook Trigger:** Configured HTTP endpoint to receive incoming `POST` data payloads.
- **Python Data Pre-processing (`parser.py`):** Strips whitespace, validates non-empty payloads, and constructs structured prompts.
- **LLM Intelligence:** Integrates with OpenAI models to extract summary insights and classify message urgency.
- **Ready for Import:** Includes `workflow.json` for 1-click import into any self-hosted or cloud n8n instance.

---

## 📁 Repository Layout
```text
03-n8n-ai-workflow/
├── parser.py            # Custom Python payload sanitizer script
├── workflow.json        # Exported n8n visual workflow configuration
├── requirements.txt      # Python dependencies for local testing
├── .env.example          # Environment variable template
└── README.md             # Documentation
```

---

## ⚙️ Setup & Usage

### 1. Local Python Testing
1. Navigate to the project directory:
   ```bash
   cd 03-n8n-ai-workflow
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the local test script:
   ```bash
   python parser.py
   ```

### 2. Importing into n8n
1. Open your **n8n** dashboard.
2. Select **Workflows** ➔ **Import from File...**
3. Upload `workflow.json` from this folder.
4. Add your OpenAI API key under n8n Credentials and activate the webhook.

---

## 📝 License
This project is open-source and available under the [MIT License](../LICENSE).
