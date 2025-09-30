# 📘 NVIDIA AI Newsletter - Usage Guide

Complete guide to using the NVIDIA AI Newsletter system.

## 🎯 Quick Start

### 1. Setup Environment

```bash
# Run the quick setup script
./quickstart.sh
```

If you don't have API keys yet, the script will create a `.env` file for you to fill in.

### 2. Get API Keys

#### OpenAI API Key
1. Visit [OpenAI Platform](https://platform.openai.com/api-keys)
2. Sign in or create an account
3. Click "Create new secret key"
4. Copy the key and add to `.env`:
   ```
   export OPENAI_API_KEY=sk-...your-key-here
   ```

#### SerpAPI Key
1. Visit [SerpAPI](https://serpapi.com/manage-api-key)
2. Sign up for a free account (100 searches/month free)
3. Copy your API key from the dashboard
4. Add to `.env`:
   ```
   export SERP_API_KEY=your-key-here
   ```

### 3. Run the Newsletter

#### Option A: Web UI (Recommended)

```bash
uv run streamlit run src/NewsLetter2/app.py
```

Then:
1. Open browser at `http://localhost:8501`
2. Click "Generate New Newsletter" in sidebar
3. Wait 2-5 minutes for generation
4. Explore the newsletter!

#### Option B: Command Line

```bash
uv run python run_newsletter.py
```

Output will be saved to `newsletter_output.json`.

## 📊 Understanding the Workflow

### Agent Pipeline

```
┌─────────────────┐
│ Reporter Agent  │ ← SerpAPI
│ Collects 10     │
│ NVIDIA articles │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Editor Agent    │ ← OpenAI API
│ Summarizes &    │
│ Analyzes        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Senior Editor   │ ← OpenAI API
│ Editorial &     │
│ Validation      │
└────────┬────────┘
         │
         ▼
   📰 Newsletter
```

### What Each Agent Does

**1. Reporter Agent** (uses SerpAPI)
- Searches Google News for "NVIDIA AI GPU technology news"
- Collects 10 most recent articles
- Extracts: title, source, URL, snippet, thumbnail, date
- Time: ~30 seconds

**2. Editor Agent** (uses OpenAI)
- Reviews each article from Reporter
- Creates 2-3 sentence summary for landing page
- Writes 20-30 sentence detailed analysis
- Focuses on business implications for tech leaders
- Time: ~2-3 minutes

**3. Senior Editor Agent** (uses OpenAI)
- Validates all summaries for accuracy
- Writes 800-1000 word editorial
- Performs trend analysis
- Compares NVIDIA vs AMD/Intel/Cloud providers
- Provides actionable insights for product leaders
- Time: ~1-2 minutes

## 🎨 Using the Streamlit UI

### Landing Page

The landing page shows:

1. **Editorial Section** (top)
   - Main headline and narrative
   - Expandable sections for:
     - Trend Analysis
     - Product Leader Insights
     - Competition Analysis

2. **News Grid** (below)
   - 10 articles in 2-column layout
   - Each card shows:
     - Thumbnail image
     - Title and source
     - Short summary
     - "Read Full Article" button

### Individual Article Page

Click any "Read Full Article" button to see:

- Full article title and source
- Publication date
- Featured image
- Detailed 20-30 sentence analysis
- Link to original article
- "Back to Newsletter" button

### Sidebar Controls

- **Generate New Newsletter**: Creates fresh newsletter
- **About**: Information about the system

## 🔧 Customization

### Change Search Focus

Edit `src/NewsLetter2/tools.py`:

```python
def _run(self, query: str = "NVIDIA AI GPU technology news") -> list[dict[str, Any]]:
    # Change query to focus on specific topics
    # Examples:
    # - "NVIDIA data center AI solutions"
    # - "NVIDIA automotive AI partnerships"
    # - "NVIDIA gaming GPU releases"
```

### Adjust Agent Expertise

Edit agent backstories in `src/NewsLetter2/agents.py`:

```python
backstory=(
    "You are an expert tech journalist..."
    # Modify to change tone, focus, or expertise level
)
```

### Change OpenAI Model

Edit `src/NewsLetter2/crew.py`:

```python
llm_config = {
    "model": "gpt-4o-mini",  # Options:
    # - "gpt-4o" (most capable, slower, expensive)
    # - "gpt-4o-mini" (balanced, recommended)
    # - "gpt-3.5-turbo" (faster, cheaper, less detailed)
    "temperature": 0.7,  # 0.0 = focused, 1.0 = creative
}
```

### Modify Article Count

Currently fixed at 10 articles. To change:

1. Edit `src/NewsLetter2/tools.py`:
   ```python
   "num": 10,  # Change this value
   ```

2. Update model validation in `src/NewsLetter2/models.py`:
   ```python
   articles: list[ProcessedNewsArticle] = Field(
       ...,
       min_length=10,  # Change both
       max_length=10,  # of these
   )
   ```

### Customize UI Styling

Edit CSS in `src/NewsLetter2/app.py`:

```python
def load_custom_css() -> None:
    st.markdown(
        """
        <style>
        .main-header {
            color: #76B900;  /* NVIDIA green */
            /* Modify colors, fonts, sizes */
        }
        ...
        </style>
        """,
        unsafe_allow_html=True,
    )
```

## 📝 Output Format

### JSON Structure

When generated via CLI, output is saved as JSON:

```json
{
  "editorial": {
    "headline": "...",
    "narrative": "...",
    "trend_analysis": "...",
    "product_leader_insights": "...",
    "competition_analysis": "...",
    "created_at": "2025-09-30T..."
  },
  "articles": [
    {
      "title": "...",
      "source": "...",
      "url": "...",
      "thumbnail": "...",
      "short_summary": "...",
      "detailed_article": "...",
      "published_date": "..."
    }
    // ... 9 more articles
  ],
  "generated_at": "2025-09-30T...",
  "edition_number": null
}
```

## 🐛 Troubleshooting

### "OPENAI_API_KEY not found"
- Check `.env` file exists in project root
- Verify key is properly formatted: `export OPENAI_API_KEY=sk-...`
- No quotes needed around the value
- Make sure to source the .env or the python-dotenv will load it automatically

### "SERP_API_KEY not found"
- Same as above for SerpAPI key
- Check you have remaining quota (100 free searches/month)

### Generation Takes Too Long
- Normal time: 2-5 minutes
- If > 10 minutes, check:
  - OpenAI API status: https://status.openai.com
  - SerpAPI status: https://serpapi.com/status
  - Your API rate limits

### Import Errors
```bash
# Reinstall dependencies
uv sync

# Check Python version
python --version  # Should be 3.12+
```

### Agent Returns Malformed Data
- Try regenerating (agents are stochastic)
- Lower temperature in `crew.py` for more consistent output
- Check OpenAI API logs for any errors

### Streamlit Port Already in Use
```bash
# Use different port
uv run streamlit run src/NewsLetter2/app.py --server.port 8502
```

## 💰 Cost Estimation

### OpenAI API Costs (GPT-4o-mini)

Per newsletter generation:
- Input tokens: ~5,000-8,000 ($0.15 per 1M tokens)
- Output tokens: ~15,000-20,000 ($0.60 per 1M tokens)
- **Approximate cost per newsletter: $0.02-0.04**

### SerpAPI Costs

- Free tier: 100 searches/month
- Each newsletter = 1 search
- Paid plans start at $50/month for 5,000 searches

### Total Cost Example

Running daily for a month:
- OpenAI: ~$1.00-1.20
- SerpAPI: Free (30 days < 100 searches)
- **Monthly total: ~$1-2**

## 📚 Advanced Usage

### Batch Generation

Generate multiple newsletters:

```python
from NewsLetter2.crew import run_newsletter_generation
import json
from datetime import datetime

for i in range(5):
    result = run_newsletter_generation()
    filename = f"newsletter_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w') as f:
        json.dump(result, f, indent=2)
```

### Custom Agent Tools

Add new tools in `src/NewsLetter2/tools.py`:

```python
class CustomNewsTool(BaseTool):
    name: str = "Custom News Search"
    description: str = "..."
    
    def _run(self, query: str) -> list[dict[str, Any]]:
        # Your custom implementation
        pass
```

Then add to agent:

```python
def create_reporter_agent(llm: Any) -> Agent:
    tools = [create_serpapi_tool(), CustomNewsTool()]
    # ...
```

### Export to Different Formats

```python
from NewsLetter2.models import Newsletter
import markdown
import pdfkit

# Load newsletter
with open('newsletter_output.json') as f:
    newsletter = Newsletter(**json.load(f))

# Export as HTML
html = f"<h1>{newsletter.editorial.headline}</h1>..."

# Export as PDF
pdfkit.from_string(html, 'newsletter.pdf')
```

## 🎓 Learning Resources

- [CrewAI Documentation](https://docs.crewai.com/)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
- [SerpAPI Documentation](https://serpapi.com/docs)
- [Streamlit Documentation](https://docs.streamlit.io/)

## 📞 Support

For questions or issues:
1. Check this guide first
2. Review the README.md
3. Check project issues on repository
4. Open a new issue with:
   - Error message
   - Steps to reproduce
   - Environment details (OS, Python version)

---

**Happy Newsletter Generating! 🚀**
