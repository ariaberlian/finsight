# FinSight

A comprehensive personal finance platform powered by Agent Development Kit that helps you store, analyze, and gain insights into your personal finances.

## Features

- **Receipt Management**: Store and process receipt data automatically
- **CSV Import**: Import expense data from CSV files for bulk analysis
- **Category Analysis**: Generate detailed monthly reports organized by spending categories
- **Smart Summarization**: Get intelligent summaries of your spending patterns
- **Financial Insights**: Get intelligent insights about your spending patterns and financial habits

## Technology Stack

- **Backend**: FastAPI for robust API development
- **AI Agent**: Google Agent Development Kit (ADK) with Gemini 2.5 Flash
- **Frontend**: Gradio for intuitive user interface
- **Python**: 3.12+ required

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd finsight
```

2. Install dependencies using uv (recommended):
```bash
uv sync
```

Or using pip:
```bash
pip install -e .
```

3. Set up environment variables:
```bash
cp finsight_agent/.env.example finsight_agent/.env
# Edit .env with your configuration
```

## Quick Start

1. Run the application:
```bash
python main.py
```

2. Access the Gradio interface in your browser (typically at `http://localhost:7860`)

3. Start uploading receipts or CSV files to begin tracking your expenses

## How It Works

1. **Data Input**: Upload receipts (images) or CSV files containing expense data
2. **AI Processing**: The ADK-powered agent processes and categorizes your expenses
3. **Analysis**: Generate monthly reports and spending summaries by category
4. **Insights**: Get AI-powered insights about your spending patterns and financial habits

## Development

### Project Structure
```
finsight/
├── finsight_agent/           # Core agent logic
│   ├── agent.py             # Main agent configuration
│   └── .env                 # Environment variables
├── main.py                  # Application entry point
├── pyproject.toml           # Project configuration
└── README.md               # This file
```

### Dependencies
- `fastapi>=0.118.0` - Web framework
- `google-adk>=1.15.1` - Agent Development Kit
- `gradio>=5.48.0` - UI framework

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and commit: `git commit -m "Add feature"`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

If you encounter any issues or have questions, please open an issue on GitHub.

---

**Take control of your finances with FinSight!**