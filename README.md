# AI Voice Bot

A voice-powered AI customer service bot that learns from uploaded documents and responds to questions via voice.

## Overview

This project demonstrates building a full-stack AI application with document processing, vector search, and real-time voice interaction. Upload your documents (PDFs or text files), then ask questions using your microphone. The AI searches through your documents and responds with voice.

## Tech Stack

**Backend**
- Python with FastAPI for the REST API and WebSocket server
- Cohere for AI language processing and embeddings
- ChromaDB for vector storage and similarity search
- Pipecat for voice processing pipeline

**Frontend**
- Next.js with TypeScript
- Tailwind CSS for styling
- Web Audio API for microphone access
- WebSocket for real-time communication

## Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- A Cohere API key (free tier available at cohere.com)

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/eamateli/ai-voice-bot.git
cd ai-voice-bot
```

##  Backend Setup

cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env

## Edit the .env file and add your Cohere API key: COHERE_API_KEY=your_api_key_here

## Start the backend server: ```python run.py```

 #  Frontend Setup

 cd frontend

# Install dependencies
npm install

# Start development server
npm run dev

