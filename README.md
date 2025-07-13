# ai-voice-bot
AI Voice Customer Service Platform
The goal with this project is to learn by building an AI-powered voice assistant that automates customer service phone calls for businesses with 24/7 support and natural language understanding.
What This Does

Automate phone customer service with AI
Upload knowledge bases (PDFs, CSVs, FAQs) for instant training
Handle multiple languages automatically
Track call analytics and costs
Scale support without hiring staff

System Architecture
Frontend (Next.js) ↔ FastAPI Backend ↔ Cohere AI ↔ Voice Pipeline
     ↓                    ↓              ↓           ↓
 Dashboard UI        LangChain      Vector DB    Pipecat/WebRTC
Tech Stack
Backend:

FastAPI - Python web framework for APIs
LangChain - AI model integration framework
Pipecat - Real-time voice processing
Cohere - Language AI for responses
ChromaDB - Vector database for knowledge storage

Frontend:

Next.js - React framework
TypeScript - Type-safe JavaScript
Tailwind CSS - Utility CSS framework

Business Model

Cost to run: $0.02 per minute
Price to customers: $0.60 per minute
Gross margin: 97% profit per call
Target: Small to medium businesses

Project Structure
ai-voice-bot/
├── backend/          # FastAPI server, AI logic, voice processing
├── frontend/         # Next.js dashboard and UI components
└── README.md        # This file
Learning Goals

System Architecture
FastAPI development
LangChain integration
Pipecat voice processing
Cohere AI integration

Getting Started
Prerequisites:

Python 3.9+
Node.js 18+
Cohere API key

Quick Start:

Clone repository
Backend: cd backend && pip install -r requirements.txt
Frontend: cd frontend && npm install
Configure environment variables
Run both services
