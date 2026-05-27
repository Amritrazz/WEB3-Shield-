# 🛡️ Web3-Shield Monorepo

Web3-Shield is an advanced, end-to-end security ecosystem designed to detect, analyze, and block malicious Web3 threats, phishing scams, and fraudulent smart contracts in real-time. 

This repository is structured as a **high-performance Monorepo** managed by `pnpm workspaces` and orchestrated by `Turborepo`. It houses the user interfaces, browser extension hooks, machine learning models, and high-speed detection backends all under a single, cohesive codebase.

---

## 🏗️ Architecture & Project Structure

The codebase is split into isolated modular applications (`apps/`) and shared utility configurations (`packages/`) to maximize code reusability and cache efficiency.

```text
web3-shield/                   # Monorepo Root Foundations
├── apps/
│   ├── backend/              # FastAPI Python server (AI Inference Engine)
│   ├── frontend/             # Next.js 14 Web Dashboard & Analytics
│   ├── extension/            # Manifest V3 Chrome Extension (On-page Shield)
│   └── ml/                   # Python/Jupyter ML training pipelines & models
├── packages/
│   └── tsconfig/             # Shared TypeScript compiler configurations
├── .github/workflows/         # Automated CI/CD pipelines
├── docker-compose.yml         # Local orchestration for all services
├── .env                       # Local environment variables (Never Commit!)
└── .gitignore                 # Global Git exclusion rulebook

Component Breakdown
apps/frontend (Next.js 14): A modern security dashboard giving users analytical insights into transaction histories, risk assessments, and historical phishing trends.

apps/backend (FastAPI): A high-performance Python asynchronous gateway that ingests transaction payloads, parses smart contract logic, and returns risk classifications instantly.

apps/extension (Chrome MV3): An on-page context-aware browser extension that intercepts malicious wallet signatures, warns users before execution, and handles real-time site injection defacement checks.

apps/ml (Python Ecosystem): The core intelligence layer containing feature extraction scripts, model architecture definitions, and raw dataset processing blocks used to train our predictive threat detection engines.

🛠️ Tech Stack & Tooling
Package Management: pnpm (Blazing fast, disk-efficient workspace installs)

Task Orchestration: Turborepo (Remote caching, intelligent parallel task execution pipelines)

Web Frameworks: Next.js 14 (App Router), FastAPI (Python Async)

Extension API: Chrome Extensions Manifest V3 + TypeScript

Quality Assurance: Husky (Git Pre-commit hooks), Lint-Staged, ESLint, Prettier

🚀 Getting Started
Prerequisites
Ensure you have the following runtimes and engines installed on your local machine:

Node.js (v20+ LTS recommended)

pnpm (v9+ recommended)

Python (v3.10+ for ML/Backend modules)

Docker & Docker Compose (For localized multi-service setups)

Installation
Clone the repository down to your machine:

Bash
git clone [https://github.com/your-username/web3-shield.git](https://github.com/your-username/web3-shield.git)
cd web3-shield
Install all global dependencies across the entire workspace structure:

Bash
pnpm install
Local Development
Our workspace leverages Turborepo to spin up all parts of the application cluster simultaneously with a single root command:

Start All Systems in Development Mode:

Bash
pnpm dev
Build All Production Production Assets:

Bash
pnpm build
Lint & Format the Entire Monorepo:

Bash
pnpm lint
🔒 Security & Git Guardrails
This project utilizes explicit hooks to guarantee that bad, unformatted, or insecure code never reaches production:

Pre-commit Hooks (Husky): Automatically triggers lint-staged on every commit attempt.

Staged Inspections (lint-staged): Automatically executes format corrections (Prettier) and code scanning (ESLint) solely across modified codebase lines to maintain high code health cleanly.

