# Technical Design Document
## Incident Post-Mortem Generator

**Student:** Ayush Sinha | **Reg. No:** 23FE10CSE00073  
**Course:** CSE3253 DevOps [PE6] | **Semester:** VI (2025-2026)

---

## 1. System Overview

The Incident Post-Mortem Generator is a RESTful web service that provides engineering teams with a standardized platform to document, track, and learn from production incidents. It replaces ad-hoc documentation (spreadsheets, emails, Confluence pages) with a structured API-driven workflow that enforces completeness and enables metrics-driven improvement.

---

## 2. Architecture

### 2.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Client Layer                         │
│              (curl / Postman / Frontend UI)                 │
└──────────────────────────┬──────────────────────────────────┘
                           │ HTTP / REST
┌──────────────────────────▼──────────────────────────────────┐
│                   Flask REST API (Port 8080)                 │
│  ┌─────────────┐  ┌──────────────┐  ┌───────────────────┐  │
│  │  /incidents │  │ /postmortems │  │    /metrics       │  │
│  └─────────────┘  └──────────────┘  └───────────────────┘  │
│                  routes.py + models.py                       │
└──────────────────────────┬──────────────────────────────────┘
                           │ SQLAlchemy ORM
┌──────────────────────────▼──────────────────────────────────┐
│               PostgreSQL 15 (Port 5432)                      │
│         incidents table + postmortems table                  │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│               Nagios Monitoring (Port 8081)                  │
│   HTTP health check │ API check │ PostgreSQL TCP check       │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 Deployment Architecture (Kubernetes)

```
┌────────────────────────────────────────────────────────────┐
│                   Kubernetes Cluster                        │
│                                                            │
│  ┌─────────────────────────────────────────────────────┐  │
│  │                  postmortem-app Deployment           │  │
│  │   ┌────────────────┐    ┌────────────────┐          │  │
│  │   │   Pod (Flask)  │    │   Pod (Flask)  │  2 replicas│ │
│  │   └───────┬────────┘    └───────┬────────┘          │  │
│  └───────────┼────────────────────┼───────────────────-┘  │
│              └──────────┬─────────┘                        │
│         ┌───────────────▼──────────────────┐               │
│         │   postmortem-service (LoadBalancer│               │
│         │            Port 80 → 8080        │               │
│         └───────────────────────────────────               │
└────────────────────────────────────────────────────────────┘
```

---

## 3. Data Models

### 3.1 Incident

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | Integer | PK, Auto | Primary key |
| title | String(200) | NOT NULL | Short incident description |
| severity | String(20) | NOT NULL | P0 / P1 / P2 / P3 |
| status | String(30) | Default: open | open / resolved / closed |
| start_time | DateTime | NOT NULL | When incident began |
| end_time | DateTime | Nullable | When incident was resolved |
| detected_by | String(100) | Nullable | Alert / team / person |
| reported_by | String(100) | Nullable | Reporter name |
| created_at | DateTime | Auto | Row creation timestamp |
| updated_at | DateTime | Auto | Last update timestamp |

### 3.2 PostMortem

| Column | Type | Description |
|--------|------|-------------|
| id | Integer PK | Primary key |
| incident_id | FK → incidents.id | One-to-one relationship |
| summary | Text | Brief overview |
| impact | Text | User/business impact |
| root_cause | Text | Underlying cause |
| timeline | JSON | List of {time, event} objects |
| contributing_factors | JSON | List of strings |
| action_items | JSON | List of {task, owner, due_date} |
| lessons_learned | Text | Key takeaways |
| detection_method | String | How incident was found |
| resolution_steps | Text | How it was fixed |
| created_by | String | Author |
| reviewed_by | String | Reviewer |

### 3.3 Entity Relationship

```
incidents (1) ─────── (0..1) postmortems
   cascade delete: if incident deleted, postmortem is deleted too
```

---

## 4. API Design

The API follows RESTful conventions:
- Resource-based URLs (nouns, not verbs)
- Standard HTTP verbs (GET, POST, PUT, DELETE)
- JSON request and response bodies
- Standard HTTP status codes

See `docs/api-documentation.md` for full endpoint reference.

---

## 5. Key Algorithms

### 5.1 MTTR Calculation
```
MTTR (minutes) = (end_time - start_time).total_seconds() / 60
```
Average MTTR across all resolved incidents is exposed via `/api/metrics`.

### 5.2 PDF Generation (ReportLab)
1. Query incident + postmortem from database
2. Calculate MTTR
3. Build ReportLab Story with: title, metadata table, section paragraphs, timeline table, action items table
4. Write to `deliverables/postmortem_incident_{id}_{timestamp}.pdf`
5. Return file path in API response

---

## 6. CI/CD Pipeline Design

```
Git Push
    │
    ▼
Jenkins Checkout
    │
    ▼
Pylint Code Quality (≥ 7.0 score)
    │
    ▼
pip install -r requirements.txt
    │
    ▼
pytest unit tests + coverage (SQLite in-memory)
    │
    ▼
docker build
    │
    ▼
trivy image security scan
    │
    ▼
[staging] docker-compose up ──── [prod] kubectl apply (manual gate)
```

---

## 7. Security Design

- All secrets stored in environment variables, never in source code
- Docker container runs as non-root `appuser`
- Input validation on all POST/PUT endpoints
- Trivy scans Docker image for CVEs at every build
- `.env` is gitignored; `.env.example` is committed as template

---

## 8. Technology Choices & Rationale

| Choice | Reason |
|--------|--------|
| Flask | Lightweight, minimal boilerplate, ideal for REST APIs |
| SQLAlchemy | ORM abstraction — same models work with SQLite (test) and PostgreSQL (prod) |
| PostgreSQL | ACID-compliant, JSON column support for timeline/action_items |
| ReportLab | Pure Python PDF generation, no external binary dependencies |
| Gunicorn | Production-grade WSGI server with multi-worker support |
| Jenkins | Industry-standard CI/CD with parameterized pipelines and manual gates |
| Nagios | Lightweight monitoring with host/service definitions per the course requirement |
