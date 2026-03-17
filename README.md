# Incident Post-Mortem Generator

**Ayush Sinha** | 23FE10CSE00073 | CSE3253 DevOps [PE6] | Sem VI (2025-26)

---

## What is this?

A REST API that helps engineering teams document production incidents in a structured way. When something breaks in production, you log the incident, write a post-mortem (root cause, timeline, action items), and export a PDF report — all via API calls.

Built this because teams usually end up writing post-mortems in random Google Docs with no standard format, no metrics, and no follow-up tracking.

---

## Stack

- **Backend:** Python 3.11 + Flask
- **Database:** PostgreSQL (SQLite for tests)
- **PDF Export:** ReportLab
- **Containerization:** Docker + Kubernetes
- **CI/CD:** Jenkins
- **Monitoring:** Nagios

---

## Running the project

```bash
# Clone and enter
git clone https://github.com/ayushsinha/devops-project-incident-postmortem.git
cd devops-project-incident-postmortem

# Copy env file
cp .env.example .env

# Start everything
docker-compose up --build
```

- API: http://localhost:8080/health
- Nagios: http://localhost:8081

---

## API Endpoints

| Method | Endpoint | What it does |
|--------|----------|--------------|
| GET | /health | Health check |
| GET | /api/incidents | List all incidents |
| POST | /api/incidents | Create incident |
| PUT | /api/incidents/:id | Update incident |
| DELETE | /api/incidents/:id | Delete incident |
| POST | /api/incidents/:id/postmortem | Write post-mortem |
| GET | /api/incidents/:id/postmortem | Get post-mortem |
| PUT | /api/incidents/:id/postmortem | Update post-mortem |
| GET | /api/incidents/:id/postmortem/export | Export as PDF |
| GET | /api/metrics | MTTR + incident stats |

---

## Project Structure

```
src/main/app/
├── __init__.py      Flask app factory
├── models.py        Incident + PostMortem DB models
├── routes.py        All API endpoints
└── utils.py         MTTR calculation + PDF generation

infrastructure/
├── docker/          Dockerfile + docker-compose
└── kubernetes/      deployment, service, configmap YAMLs

pipelines/
├── Jenkinsfile      9-stage Jenkins pipeline
└── .github/         GitHub Actions workflow

tests/unit/          13 pytest test cases
monitoring/nagios/   Nagios service config
docs/                API docs, design doc, user guide
```

---

## CI/CD Pipeline (Jenkins)

Checkout → Pylint → Install deps → Unit tests → Docker build → Trivy scan → Staging deploy → Production deploy (manual gate)

---

## Tests

```bash
pytest tests/unit/ -v
# Overall coverage: ~85%
```

