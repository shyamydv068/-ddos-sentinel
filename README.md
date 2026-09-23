# DDoS Sentinel

Real-Time DDoS Attack Detection and Automated Prevention using Machine Learning, Apache Kafka, and Apache Spark.

This repository is being developed as a final-year cybersecurity project. The current stage establishes the project skeleton, configuration, environment setup, backend health endpoint, PostgreSQL configuration, Kafka topic definitions, and a minimal React dashboard shell.

## Stage A status

The initial project scaffolding includes:
- repository structure for backend, ML, Kafka, Spark, mitigation, alerts, database, frontend, logs, docs, tests, and scripts
- configuration files for app, Kafka, Spark, and ML settings
- Python requirements and environment template
- Docker Compose foundation for core services
- FastAPI health and project-status endpoints
- PostgreSQL connection configuration
- Kafka topic definitions
- minimal React + Vite frontend shell

## Quick start

1. Python setup
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. Run the backend
   ```bash
   uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
   ```

3. Run the frontend
   ```bash
   cd frontend
   npm install
   npm run dev -- --host 0.0.0.0
   ```

4. Start infrastructure with Docker Compose
   ```bash
   docker compose up -d postgres redis zookeeper kafka spark backend frontend
   ```

## Documentation

Project architecture and workflow details will be expanded as the major subsystems are implemented.

## Current limitation

This repository is intentionally in the initial scaffolding stage. The full streaming, ML, mitigation, and dashboard features are not yet complete.
