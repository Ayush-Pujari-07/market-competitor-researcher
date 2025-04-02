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
- OpenAI API key
- EXA API key
- Redis (for caching)

## Environment Setup

1. Create and configure environment variables:
```bash
cp .env.example .env
```

Update the `.env` file with your credentials:
```
JWT_ALGORITHM="HS256"
JWT_EXPIRATION=210000
JWT_SECRET="your-secret-key"
OPENAI_API_KEY="your-openai-key"
EXA_API_KEY="your-exa-key"
MONGODB_URI="your-mongodb-uri"
```

3. Set up virtual environment:
```bash
# Option 1: Using venv
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Option 2: Using init_setup.sh
bash init_setup.sh
```

4. Install dependencies:
```bash
# Install UV package manager
pip install uv

# Install project dependencies
uv pip install -r requirements/requirements.txt
```

## Running the Application

1. Start the services:
```bash
# Start Redis using Docker
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

### Competitor Analysis
- Competitor profiling
- Strength/weakness analysis
- Market positioning
- Competitive advantages

## Development

For development work:
```bash
# Install development dependencies
uv pip install -r requirements/requirements_dev.txt
```


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
