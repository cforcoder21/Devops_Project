# Project Plan & Timeline
## Incident Post-Mortem Generator

**Student:** Ayush Sinha | **Reg. No:** 23FE10CSE00073  
**Course:** CSE3253 DevOps [PE6] | **Semester:** VI (2025-2026)

---

## Project Timeline

| Week | Dates | Milestone | Status |
|------|-------|-----------|--------|
| 1 | Jun 1–7 | Project setup, repo structure, Flask skeleton, data models | ✅ Done |
| 2 | Jun 8–14 | REST API endpoints (Incidents CRUD + PostMortem CRUD) | ✅ Done |
| 3 | Jun 15–21 | PDF export (ReportLab), MTTR calculation, metrics endpoint | ✅ Done |
| 4 | Jun 22–28 | Dockerization, docker-compose, PostgreSQL integration | ✅ Done |
| 5 | Jun 29–Jul 5 | Jenkins pipeline, unit tests, coverage reports | ✅ Done |
| 6 | Jul 6–12 | Kubernetes manifests, Nagios monitoring config | ✅ Done |
| 7 | Jul 13–19 | Documentation, final testing, demo video preparation | ✅ Done |

---

## Deliverables Checklist

### Code & Implementation
- [x] Flask REST API with full CRUD for incidents and post-mortems
- [x] PDF generation with ReportLab
- [x] MTTR calculation and metrics dashboard
- [x] SQLAlchemy models with PostgreSQL support
- [x] Input validation and error handling

### Infrastructure
- [x] Dockerfile with non-root user and Gunicorn
- [x] docker-compose.yml (app + db + Nagios)
- [x] Kubernetes deployment, service, and configmap YAMLs
- [x] Nagios monitoring config

### CI/CD
- [x] Jenkinsfile with 9 stages
- [x] GitHub Actions workflow
- [x] Trivy security scanning integrated

### Testing
- [x] Unit tests (pytest) — 13 test cases
- [x] 85%+ test coverage
- [x] Integration test structure

### Documentation
- [x] README.md (complete template filled)
- [x] API documentation
- [x] Design document
- [x] User guide
- [x] Project plan

### Assessment
- [x] Self-assessment table
- [x] Project challenges documented
- [x] Learnings documented

---

## Risk Register

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Docker build failure | Low | High | Use slim base image, pin dependency versions |
| DB migration issues | Medium | Medium | Use SQLAlchemy's create_all for simple schema |
| Jenkins agent unavailable | Low | High | Document manual test steps as fallback |
| ReportLab PDF rendering bug | Medium | Low | Unit test PDF path independently |

---

## Resource Requirements

| Resource | Tool | Purpose |
|----------|------|---------|
| Version Control | Git + GitHub | Source code management |
| Language Runtime | Python 3.11 | Application execution |
| Web Framework | Flask 2.3 | REST API |
| Database | PostgreSQL 15 | Persistent storage |
| Containerization | Docker + Compose | Consistent environments |
| Orchestration | Kubernetes | Production scaling |
| CI/CD | Jenkins | Automated pipeline |
| Monitoring | Nagios | Health checks and alerts |
| PDF Generation | ReportLab | Report export |
| Security Scanning | Trivy | Vulnerability detection |
