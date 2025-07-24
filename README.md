# AI Voice Bot

A voice-powered AI customer service bot that learns from uploaded documents and responds to questions via voice.
<img width="808" height="466" alt="Screenshot 2025-07-24 173052" src="https://github.com/user-attachments/assets/068046f1-6995-4658-bbdf-5af76df5fd59" />

## Overview

This project demonstrates how to build a full-stack AI application that combines document processing, vector similarity search, and real-time voice interaction.

Users can upload documents (PDFs or plain text files), then ask questions using their microphone. The AI will search through the document content and respond using voice.

## Tech Stack

### Backend

- **FastAPI** – REST API and WebSocket server
- **Cohere** – Language processing and embeddings
- **ChromaDB** – Vector storage and similarity search
- **Pipecat** – Voice processing pipeline

### Frontend

- **Next.js** with TypeScript
- **Tailwind CSS** for styling
- **Web Audio API** for microphone access
- **WebSocket** for real-time communication

## Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- A Cohere API key (available at [cohere.com](https://cohere.com))

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/eamateli/ai-voice-bot.git
cd ai-voice-bot
```
## Backend Setup
```bash
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
# Create a .env file
cp .env.example .env
# Edit the .env file and add your Cohere API key
COHERE_API_KEY=your_api_key_here
# Start the backend server
python run.py
```
# Frontend Setup 
```bash
cd frontend
# Install dependencies
npm install
# Start the development server
npm run dev


