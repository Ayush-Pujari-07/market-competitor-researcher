# Market Competitor Research Assistant

An AI-powered tool that generates comprehensive market research and competitor analysis reports using LangChain and OpenAI.

## Features

- **Market Research Reports**: Generate detailed market analysis for any industry
- **Competitor Analysis**: Create in-depth competitor comparison reports
- **User Authentication**: Secure login and registration system
- **Report Management**: Save, view, and manage your research reports
- **Modern Tech Stack**: Built with FastAPI, Streamlit, MongoDB, and LangChain

## Prerequisites

- Python 3.11 or higher
- MongoDB instance
- OpenAI API key (for GPT-4 and embeddings)
- EXA API key (for web search capabilities)
- Redis (for caching)
- Docker and Docker Compose (for running services)

## Environment Setup

1. Create and configure environment variables:
```bash
cp .env.example .env
```

Update the `.env` file with your credentials:
```
# JWT Settings
JWT_ALGORITHM="HS256"
JWT_EXPIRATION=210000
JWT_SECRET="your-secret-key"

# API Keys
OPENAI_API_KEY="your-openai-key"
EXA_API_KEY="your-exa-key"

# Database
MONGODB_URI="your-mongodb-uri"

# Server Settings
SITE_DOMAIN=127.0.0.1
SECURE_COOKIES=false
ENVIRONMENT=TESTING

# CORS Settings
CORS_HEADERS=["*"]
CORS_ORIGINS=["http://localhost:3000"]

# Redis Configuration
REDIS_PORT=6379
REDIS_HOST="localhost"

# Chroma Settings
CHROMA_PORT=8000
CHROMA_HOST="localhost"
```

2. Set up virtual environment:
```bash
# Option 1: Using venv
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Option 2: Using init_setup.sh (Linux/Mac)
bash init_setup.sh
```

3. Install dependencies:
```bash
# Install all requirements
pip install -r requirements.txt
```

## Development Setup

1. Install pre-commit hooks:
```bash
pip install pre-commit
pre-commit install
```

2. The project uses the following code quality tools:
- Ruff for linting
- Black for code formatting
- Pre-commit hooks for automated checks

## Running the Application

1. Start the services:
```bash
# Start Redis and other services using Docker
docker-compose up -d

# Start both frontend and backend
bash init_app.sh
```

2. Access the application:
- Backend API: http://localhost:9000
- Frontend UI: http://localhost:8501
- API Documentation: http://localhost:9000/docs

## Project Structure

```
market-competitor-researcher/
├── backend/
│   ├── auth/           # Authentication system
│   ├── research_chain/ # Research generation logic
│   ├── vector_db/      # Vector database integration
│   └── main.py        # FastAPI application
├── frontend/
│   ├── pages/         # Streamlit pages
│   └── main.py       # Frontend application
└── docker-compose.yaml
```

## Features in Detail

### Market Research
- Industry analysis
- Market size and growth
- Key trends and drivers
- Competitive landscape
- Web-based data gathering using EXA
- AI-powered report generation using GPT-4

### Competitor Analysis
- Competitor profiling
- Strength/weakness analysis
- Market positioning
- Competitive advantages
- Real-time data collection
- AI-driven insights

## Logging

The application uses two logging configurations:
- `logging.ini` for development
- `logging_production.ini` for production with JSON formatting

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
