# Incident Post-Mortem Generator

Student Name: Ayush Sinha  
Registration No: 23FE10CSE00073  
Course: CSE3253 DevOps [PE6]  
Semester: VI (2025-2026)  
Project Type: CI/CD + Containerization + Monitoring  
Difficulty: Intermediate

---

## Project Overview

### Problem Statement
Production incidents are often documented in inconsistent formats, making it difficult to track root causes, recovery timelines, and long-term preventive actions.

### Objectives
- [x] Build a REST API for incident lifecycle management
- [x] Generate structured post-mortem reports with PDF export
- [x] Implement a DevOps workflow using CI/CD, Docker, Kubernetes, and monitoring

### Key Features
- Incident CRUD APIs
- Post-mortem creation/update/retrieval and PDF export
- MTTR and incident metrics endpoint

---

## Technology Stack

### Core Technologies
- Programming Language: Python 3.11
- Framework: Flask
- Database: PostgreSQL (SQLite for tests)

### DevOps Tools
- Version Control: Git
- CI/CD: Jenkins + GitHub Actions
- Containerization: Docker
- Orchestration: Kubernetes
- Configuration Management: Puppet (template directory scaffolded)
- Monitoring: Nagios

---

## Getting Started

### Prerequisites
- [x] Docker Desktop v20.10+
- [x] Git 2.30+
- [x] Python 3.11+
- [x] Docker Compose

### Installation

1. Clone the repository:

```bash
git clone https://github.com/ayushsinha/devops-project-incident-postmortem.git
cd devops-project-incident-postmortem
```

2. Build and run using Docker:

```bash
docker-compose up --build
```

3. Access the application:
- Web/API Interface: http://localhost:8080
- Health Endpoint: http://localhost:8080/health
- Nagios: http://localhost:8081

### Alternative Installation (Without Docker)

```bash
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python run.py
```

---

## Project Structure

```text
devops-project-incident-postmortem/
|
|-- README.md
|-- .gitignore
|-- LICENSE
|
|-- src/
|   |-- main/
|   |   |-- app/
|   |   |-- config/
|   |-- test/
|   |-- scripts/
|
|-- docs/
|   |-- project-plan.md
|   |-- design-document.md
|   |-- user-guide.md
|   |-- api-documentation.md
|   |-- screenshots/
|   |-- architecture/
|   |-- deployment.md
|   |-- troubleshooting.md
|
|-- infrastructure/
|   |-- docker/
|   |   |-- Dockerfile
|   |   |-- docker-compose.yml
|   |-- kubernetes/
|   |   |-- deployment.yaml
|   |   |-- service.yaml
|   |   |-- configmap.yaml
|   |-- puppet/
|   |-- terraform/
|
|-- pipelines/
|   |-- Jenkinsfile
|   |-- .github/workflows/ci-cd.yml
|   |-- gitlab-ci.yml
|
|-- tests/
|   |-- unit/
|   |-- integration/
|   |-- selenium/
|   |-- test-data/
|
|-- monitoring/
|   |-- nagios/
|   |-- alerts/
|   |-- dashboards/
|
|-- presentations/
|   |-- project-presentation.pdf
|   |-- demo-script.md
|
|-- deliverables/
|   |-- demo-video.mp4
|   |-- final-report.pdf
|   |-- assessment/
```

---

## Configuration

### Environment Variables
Create a `.env` file in the root directory:

```env
APP_ENV=development
DB_HOST=localhost
DB_PORT=5432
API_KEY=your_api_key_here
```

### Key Configuration Files
1. `src/main/config/config.py` - Application configuration
2. `docker-compose.yml` - Multi-container setup
3. `infrastructure/kubernetes/` - K8s deployment files

---

## CI/CD Pipeline

### Pipeline Stages
1. Code Quality Check - Linting, Static Analysis
2. Build - Package and containerize application
3. Test - Run unit and integration tests
4. Security Scan - Vulnerability scanning with Trivy
5. Deploy to Staging - Automated staging deployment
6. Deploy to Production - Manual approval required

### Pipeline Status
![Pipeline Status](https://img.shields.io/badge/pipeline-configured-brightgreen)

---

## Testing

### Test Types
- Unit Tests: `pytest tests/unit/ -v`
- Integration Tests: `pytest tests/integration/ -v`
- E2E Tests: Selenium scaffold available in `tests/selenium/`

### Test Coverage
Current target coverage: > 80% (latest unit run around 85%).

---

## Monitoring and Logging

### Monitoring Setup
- Nagios: configured for service-level monitoring
- Custom Metrics: MTTR and incident statistics endpoint
- Alerts: baseline alert directory scaffolded under `monitoring/alerts/`

### Logging
- Structured application logs can be routed via container runtime
- Optional centralized logging integration can be added later
- Suggested retention: 30 days

---

## Docker and Kubernetes

### Docker Images
```bash
# Build image
docker build -t devops-project-incident-postmortem:latest .

# Run container
docker run -p 8080:8080 devops-project-incident-postmortem:latest
```

### Kubernetes Deployment
```bash
# Apply K8s manifests
kubectl apply -f infrastructure/kubernetes/

# Check deployment status
kubectl get pods,svc,deploy
```

---

## Performance Metrics

| Metric | Target | Current |
|--------|--------|---------|
| Build Time | < 5 min | ~3-5 min |
| Test Coverage | > 80% | ~85% |
| Deployment Frequency | Daily | As required by milestones |
| Mean Time to Recovery | < 1 hour | Available via `/api/metrics` |

---

## Documentation

### User Documentation
- [User Guide](docs/user-guide.md)
- [API Documentation](docs/api-documentation.md)

### Technical Documentation
- [Design Document](docs/design-document.md)
- [Architecture Diagrams](docs/architecture/)

### DevOps Documentation
- [Deployment Guide](docs/deployment.md)
- [Troubleshooting Guide](docs/troubleshooting.md)

---

## Demo

### Demo Video
Add the 5-10 minute demo file in `deliverables/demo-video.mp4`.

### Live Demo
URL: N/A  
Username: N/A  
Password: N/A

---

## Development Workflow

### Git Branching Strategy

```text
main
|-- develop
|   |-- feature/incident-crud
|   |-- feature/postmortem-export
|   |-- hotfix/security-patch
|-- release/v1.0.0
```

### Commit Convention
- feat: New feature
- fix: Bug fix
- docs: Documentation
- test: Test-related
- refactor: Code refactoring
- chore: Maintenance tasks

---

## Security

### Security Measures Implemented
- [x] Input validation and sanitization
- [ ] Authentication and authorization
- [x] Environment-based configuration
- [x] Regular dependency updates
- [ ] Security headers in web applications

### Security Scanning
```bash
trivy image devops-project-incident-postmortem:latest
```

---

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## Faculty Assessment

### Self-Assessment

| Criteria | Max Marks | Self Score | Remarks |
|----------|-----------|------------|---------|
| Implementation | 4 | [ ] | [Comments] |
| Documentation | 3 | [ ] | [Comments] |
| Innovation | 2 | [ ] | [Comments] |
| Presentation | 1 | [ ] | [Comments] |
| Total | 10 | [ ] | |

### Project Challenges
1. Maintaining consistency between incident APIs and post-mortem lifecycle operations.
2. Building reproducible deployments across local Docker and Kubernetes.
3. Enforcing quality gates while keeping CI pipeline execution time low.

### Learnings
- Practical CI/CD pipeline design for Python services.
- Container-based deployment and orchestration fundamentals.
- Monitoring and post-incident engineering best practices.

---

