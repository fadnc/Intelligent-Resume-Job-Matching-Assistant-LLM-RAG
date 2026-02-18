# Intelligent Resume-Job Matching Assistant

A production-ready AI-powered system that analyzes resumes against job descriptions using Retrieval Augmented Generation (RAG), vector embeddings, and large language models. The application provides quantitative match scoring, skills gap analysis, and actionable recommendations to optimize resumes for Applicant Tracking Systems (ATS).

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## Table of Contents

- [Features](#features)
- [System Architecture](#system-architecture)
- [Technology Stack](#technology-stack)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Deployment](#deployment)
- [Project Structure](#project-structure)
- [Performance Optimization](#performance-optimization)
- [Contributing](#contributing)
- [License](#license)

## Features

### Core Capabilities

- **Intelligent Match Scoring**: 0-100 scale evaluation of resume-job alignment with four quality tiers (Excellent, Good, Fair, Poor)
- **Skills Gap Analysis**: Identifies 3-5 critical missing skills from job requirements
- **Actionable Recommendations**: Provides 3-5 specific, implementable improvements
- **ATS Optimization**: Generates keyword-rich, achievement-focused bullet points
- **Multi-format Export**: Results available in formatted text and JSON formats
- **Analysis History**: Tracks up to 10 recent analyses for comparison

### Technical Highlights

- **RAG Pipeline**: FAISS-powered vector search with 384-dimensional embeddings
- **LLM Integration**: Groq API with Llama-3.3-70B for reliable JSON generation
- **Async Processing**: Non-blocking PDF parsing and text extraction
- **Performance Caching**: LRU cache for job description embeddings (100 entries)
- **Optimized Chunking**: 200-word segments with 30-word overlap for context preservation

## System Architecture

```
┌─────────────────┐
│   Streamlit UI  │
│  (Frontend)     │
└────────┬────────┘
         │
         │ HTTP/REST
         ▼
┌─────────────────┐
│   FastAPI       │
│  (Backend)      │
└────────┬────────┘
         │
    ┌────┴────┬──────────┬──────────┐
    ▼         ▼          ▼          ▼
┌────────┐ ┌──────┐ ┌────────┐ ┌──────────┐
│PyMuPDF │ │FAISS │ │Sentence│ │Groq API  │
│(Parser)│ │Vector│ │Transform│ │(LLM)     │
│        │ │Store │ │(Embedder│ │          │
└────────┘ └──────┘ └────────┘ └──────────┘
```

### Workflow

1. **Document Upload**: PDF resume parsed using PyMuPDF with async processing
2. **Text Chunking**: Resume segmented into 200-word chunks with 30-word overlap
3. **Vector Embedding**: Text converted to 384-dimensional vectors using all-MiniLM-L6-v2
4. **Index Creation**: FAISS IndexFlatL2 built for semantic similarity search
5. **Query Processing**: Job description embedded and top-3 relevant chunks retrieved
6. **LLM Analysis**: Groq API (Llama-3.3-70B) generates structured insights
7. **Result Presentation**: Score, gaps, suggestions, and optimized bullets displayed

## Technology Stack

### Backend

- **FastAPI**: High-performance async web framework
- **Python 3.12**: Latest stable Python runtime
- **PyMuPDF (fitz)**: PDF text extraction
- **Sentence Transformers**: Neural embedding models
- **FAISS**: Facebook AI Similarity Search for vector operations
- **Groq SDK**: LLM API integration
- **Pydantic**: Data validation and settings management

### Frontend

- **Streamlit**: Interactive web application framework
- **Requests**: HTTP client for backend communication
- **Custom CSS**: Professional styling with gradient animations

### Infrastructure

- **Docker**: Containerization with multi-stage builds
- **Uvicorn**: ASGI server for FastAPI
- **Amazon SageMaker**: (Optional) Model deployment support

## Prerequisites

- Python 3.12 or higher
- Docker (optional, for containerized deployment)
- Groq API key (free tier available at https://console.groq.com)
- Minimum 4GB RAM for optimal performance
- CUDA-compatible GPU (optional, for accelerated embeddings)

## Installation

### Local Setup

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/intelligent-resume-matcher.git
cd intelligent-resume-matcher
```

2. **Create virtual environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Download embedding model**

```bash
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')"
```

### Docker Setup

1. **Build the image**

```bash
docker build -t resume-analyzer .
```

2. **Run the container**

```bash
docker run -p 8000:8000 -e GROQ_API_KEY=your_key_here resume-analyzer
```

## Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# Required
GROQ_API_KEY=gsk_your_groq_api_key_here

# Optional
USE_SAGEMAKER=False
SAGEMAKER_ENDPOINT=
EMBED_MODEL=sentence-transformers/all-MiniLM-L6-v2
FAISS_PATH=embeddings_store/faiss_index
META_PATH=embeddings_store/meta.npy
```

### Configuration Parameters

**Embedding Configuration** (`backend/config.py`):
- `EMBED_MODEL`: Pre-trained sentence transformer model
- `FAISS_PATH`: Vector index storage location
- `META_PATH`: Metadata storage path

**LLM Parameters** (`backend/services/llm.py`):
- `model`: "llama-3.3-70b-versatile"
- `temperature`: 0.3 (consistency over creativity)
- `max_tokens`: 800 (comprehensive responses)
- `response_format`: JSON object (structured output)

**Chunking Settings** (`backend/services/pipeline.py`):
- `size`: 200 words per chunk
- `overlap`: 30 words between chunks
- `k`: 3 top chunks retrieved
- `context_limit`: 1500 characters (resume) + 1000 characters (job description)

## Usage

### Starting the Backend

```bash
cd /path/to/project
uvicorn backend.app:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at `http://localhost:8000`

### Starting the Frontend

Open a new terminal:

```bash
cd /path/to/project
streamlit run frontend/streamlit_app.py
```

The web interface will open automatically at `http://localhost:8501`

### Using the Application

1. **Upload Resume**: Click the file uploader and select your PDF resume (max 10MB)
2. **Paste Job Description**: Copy the complete job posting into the text area
3. **Analyze**: Click "Analyze My Resume" to process
4. **Review Results**: Examine the match score, missing skills, suggestions, and optimized bullets
5. **Export**: Download results as formatted text or JSON for records

### Example API Request

```bash
curl -X POST http://localhost:8000/analyze \
  -F "resume=@path/to/resume.pdf" \
  -F "job_description=Job Title: Software Engineer..."
```

### Example API Response

```json
{
  "score": 78,
  "missing_skills": [
    "Kubernetes container orchestration",
    "GraphQL API development",
    "CI/CD pipeline management"
  ],
  "suggestions": [
    "Add quantifiable metrics to project achievements (e.g., 'Improved performance by 40%')",
    "Include specific cloud technologies mentioned in job requirements (AWS Lambda, S3)",
    "Emphasize leadership experience with concrete team size and project scope"
  ],
  "rewritten_bullets": [
    "Architected microservices infrastructure using Docker and Kubernetes, reducing deployment time by 60% and improving system reliability to 99.9% uptime",
    "Led cross-functional team of 8 engineers to deliver RESTful API platform supporting 10M+ daily requests with sub-100ms latency",
    "Implemented automated CI/CD pipelines using Jenkins and GitLab, decreasing release cycle from 2 weeks to 3 days"
  ]
}
```

## API Documentation

### Endpoints

#### POST /analyze

Analyzes a resume against a job description.

**Request**:
- `resume` (file): PDF file containing the resume
- `job_description` (string): Complete job posting text

**Response**:
```json
{
  "score": int,
  "missing_skills": [string],
  "suggestions": [string],
  "rewritten_bullets": [string]
}
```

#### GET /health

Health check endpoint.

**Response**:
```json
{
  "status": "ok"
}
```

#### GET /

API root information.

**Response**:
```json
{
  "message": "Welcome to the Resume LLM Assistant API"
}
```

### Interactive Documentation

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Deployment

### Docker Deployment

```bash
# Build production image
docker build -t resume-analyzer:latest .

# Run with environment variables
docker run -d \
  -p 8000:8000 \
  -e GROQ_API_KEY=${GROQ_API_KEY} \
  --name resume-analyzer \
  resume-analyzer:latest
```

### AWS SageMaker Deployment (Future Support)

The project includes infrastructure for SageMaker deployment:

```python
# sagemaker/inference.py
from transformers import pipeline

def model_fn(model_dir):
    generator = pipeline(
        "text-generation",
        model="mistralai/Mistral-7B-Instruct-v0.2",
        max_new_tokens=500,
        temperature=0.3,
        do_sample=True
    )
    return generator
```

### Production Considerations

- **Rate Limiting**: Implement request throttling for API endpoints
- **Authentication**: Add JWT or API key authentication for production
- **Logging**: Configure structured logging with log rotation
- **Monitoring**: Set up health checks and performance metrics
- **Scaling**: Use load balancers for horizontal scaling
- **Security**: Enable HTTPS, implement CORS policies, sanitize inputs

## Project Structure

```
intelligent-resume-matcher/
├── backend/
│   ├── __init__.py
│   ├── app.py                  # FastAPI application entry point
│   ├── config.py               # Configuration management
│   ├── models/
│   │   ├── __init__.py
│   │   ├── prompts.py          # LLM prompt templates
│   │   └── schemas.py          # Pydantic data models
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── analyze.py          # Analysis endpoint
│   │   └── health.py           # Health check endpoint
│   └── services/
│       ├── __init__.py
│       ├── chunker.py          # Text chunking logic
│       ├── embeddings.py       # Vector embedding generation
│       ├── llm.py              # LLM API integration
│       ├── parser.py           # PDF text extraction
│       ├── pipeline.py         # Main analysis workflow
│       └── retriever.py        # FAISS vector search
├── frontend/
│   └── streamlit_app.py        # Streamlit web interface
├── sagemaker/
│   └── inference.py            # SageMaker deployment script
├── notebooks/
│   └── experiments.ipynb       # Development experiments
├── embeddings_store/           # FAISS index storage
│   ├── faiss_index
│   └── meta.npy
├── Dockerfile                  # Container configuration
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── LICENSE                     # MIT License
└── .env.example                # Environment template
```

## Performance Optimization

### Memory Management

- **Float32 Precision**: Reduces embedding memory footprint by 50%
- **Batch Processing**: 64-sample batches for efficient GPU utilization
- **LRU Caching**: Stores 100 most recent job embeddings

### Processing Speed

- **Async I/O**: Non-blocking PDF parsing with ThreadPoolExecutor
- **Context Limits**: 1500-char resume + 1000-char job description prevents timeout
- **Optimized Chunking**: 200-word segments balance context and performance

### Scalability

- **Stateless Design**: All endpoints are stateless for horizontal scaling
- **In-Memory Indexing**: FAISS index cached in RAM for sub-second retrieval
- **Connection Pooling**: Reuses HTTP connections to Groq API

### Benchmarks

| Operation | Duration | Notes |
|-----------|----------|-------|
| PDF Parsing | 0.5-2s | Depends on file size |
| Embedding Generation | 0.3-1s | 200-word chunks |
| FAISS Search | <0.1s | Top-3 retrieval |
| LLM Generation | 2-5s | Groq API latency |
| **Total Analysis** | **3-8s** | End-to-end |

## Development

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run test suite
pytest tests/ -v
```

### Code Quality

```bash
# Format code
black backend/ frontend/

# Lint
flake8 backend/ frontend/

# Type checking
mypy backend/
```

### Adding New Features

1. Create feature branch: `git checkout -b feature/new-feature`
2. Implement changes following existing code structure
3. Add tests for new functionality
4. Update documentation
5. Submit pull request with detailed description

## Troubleshooting

### Common Issues

**Backend Connection Failed**
```
Error: Cannot connect to backend at http://localhost:8000
```
Solution: Ensure backend is running with `uvicorn backend.app:app --reload`

**Groq API Error**
```
Error: API Error: Invalid API key
```
Solution: Verify `GROQ_API_KEY` in `.env` file is correct

**PDF Parsing Failure**
```
Error: Failed to extract text from PDF
```
Solution: Ensure PDF is not password-protected or corrupted

**Memory Issues**
```
Error: Out of memory
```
Solution: Reduce batch size in `embeddings.py` or increase system RAM

### Debug Mode

Enable verbose logging:

```python
# backend/app.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Contribution Areas

- Enhanced LLM prompts for better analysis quality
- Additional export formats (PDF, DOCX)
- Multi-language support
- Resume templates and examples
- Performance optimizations
- Unit and integration tests
- Documentation improvements

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2026 Fadhil Muhammed N C

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Acknowledgments

- **Groq**: Fast, reliable LLM inference platform
- **Sentence Transformers**: High-quality text embeddings
- **FAISS**: Efficient similarity search library
- **FastAPI**: Modern Python web framework
- **Streamlit**: Rapid UI development platform

## Contact

**Author**: Fadhil Muhammed N C  
**Project Repository**: https://github.com/fadnc/intelligent-resume-job-matching-assistant-llm-rag-sagemaker

For questions, issues, or feature requests, please open an issue on GitHub.

---

**Version**: 2.0.0  
**Last Updated**: January 2026  
**Status**: Production Ready
