# WEB3-Shield-
**Web3-Shield** is a full-stack security monorepo that stops crypto phishing and wallet drainers. A Next.js frontend monitors threat alerts, a Python FastAPI backend runs AI detection to block malicious smart contracts, and a containerized Docker suite (PostgreSQL, Redis, Neo4j, MongoDB) securely logs data and traces hacker wallets live.


🛡️ Web3-Shield: Real-Time Phishing Detection & Transaction Interception Layer
Web3-Shield is an automated, full-stack security framework designed to act as a real-time anti-fraud interceptor for blockchain transactions. It protects decentralized applications (dApps) and user wallets by evaluating incoming transaction logic, smart contract behavior, and domain metadata before threats can reach the blockchain network.

If a user interacts with a malicious website or a wallet-drainer script, Web3-Shield blocks the action instantly—preventing unauthorized asset drainage and logging hacker relationships for network wide-threat intelligence.

🏗️ Architecture & Component Stack
The project is built as a high-performance monorepo distributed across three decoupled layers:

1. Frontend Command Center (Next.js & React)
Directory: /apps/frontend

Role: A fast UI dashboard optimized with Next.js Turbopack that provides security analysts with a live stream of system health, intercepted transaction graphs, and real-time threat alert matrices.

2. Core Detection Brain (FastAPI & Python)
Directory: /apps/backend

Role: An asynchronous Python engine running Uvicorn. It parses transaction payloads, analyzes smart contract heuristics (e.g., catching stealthy approveAll() functions), and processes automated threat scores via interactive REST endpoints.

3. Isolated Data Infrastructure (Docker Suite)
Orchestration: docker-compose.prod.yml

Role: Manages four specialized, persistent database nodes running concurrently inside background containers:

PostgreSQL: Handles permanent application logging, user states, and threat telemetry metadata.

Redis: Powers lightning-fast caching and real-time state broadcasting.

Neo4j: Maps out graph relationships to trace connections between malicious hacker clusters.

MongoDB: Serves as a flexible document store for raw transaction payloads.

🚀 Quick Start & Deployment
Prerequisites
Make sure you have Docker Desktop installed on your machine and configured to run on login.

Setup Instructions
Clone the Repository and Navigate to the Root File Path:

Bash
cd "D:\Python project\Web3\my-monorepo"
Launch the Containerized Database Suite (Background Mode):

Bash
docker-compose -f docker-compose.prod.yml up -d
Fire Up the Backend Security Engine:

Bash
cd apps/backend
# Activate your local virtual environment (Windows PowerShell)
.\venv\Scripts\Activate.ps1
# Run the server
uvicorn app.main:app --reload --port 8000
Access interactive API documentation at: http://localhost:8000/docs

Boot Up the Next.js Threat Monitor Dashboard:

Bash
cd apps/frontend
npm install
npm run dev
Access the live graphical user interface at: http://localhost:3000

🎯 Key Capabilities Verified
Real-time API Heartbeat Diagnostics: Verified 200 OK status performance via FastAPI Swagger routing loops.

Resilient State Management: Configured with absolute pathing locks to maintain stability across cross-platform host machines.

Proactive Extension Protection: Embedded custom hydration overrides to gracefully isolate third-party browser noise without breaking client-side rendering.
