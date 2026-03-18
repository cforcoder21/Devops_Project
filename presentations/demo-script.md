# Demo Script — Incident Post-Mortem Generator
## Ayush Sinha | 23FE10CSE00073

Estimated duration: 7–8 minutes

---

## [0:00 – 0:45] Introduction

"Hi, I'm Ayush Sinha, Reg. No. 23FE10CSE00073. My project is the Incident Post-Mortem Generator — a RESTful tool that helps engineering teams document and learn from production incidents in a structured way."

"I'll demonstrate: creating an incident, writing its post-mortem, exporting a PDF report, and showing the CI/CD pipeline with monitoring."

---

## [0:45 – 1:30] Architecture Overview

"The stack is Python Flask on top of PostgreSQL. Everything runs in Docker containers — the app, the database, and Nagios for monitoring. For production I have Kubernetes manifests. The Jenkins pipeline handles the full lifecycle: lint → test → build → security scan → deploy."

---

## [1:30 – 2:30] Start the Application

```bash
docker-compose -f infrastructure/docker/docker-compose.yml up -d
docker ps
curl http://localhost:8080/health
```

"All three services are running. The health endpoint confirms the Flask app is live."

---

## [2:30 – 4:00] Live API Demo

**Create an incident:**
```bash
curl -X POST http://localhost:8080/api/incidents \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Database connection pool exhausted in production",
    "severity": "P1",
    "start_time": "2025-06-01T10:00:00",
    "detected_by": "Nagios Alert",
    "reported_by": "SRE Team"
  }'
```

**Resolve it:**
```bash
curl -X PUT http://localhost:8080/api/incidents/1 \
  -H "Content-Type: application/json" \
  -d '{"status": "resolved", "end_time": "2025-06-01T10:45:00"}'
```

**Write post-mortem:**
```bash
curl -X POST http://localhost:8080/api/incidents/1/postmortem \
  -H "Content-Type: application/json" \
  -d '{
    "summary": "Connection pool exhausted due to missing connection release in new feature code.",
    "root_cause": "A recently deployed feature opened DB connections without closing them on error paths.",
    "impact": "3,000 users unable to log in for 45 minutes.",
    "timeline": [
      {"time": "10:00", "event": "Alert triggered"},
      {"time": "10:15", "event": "On-call paged"},
      {"time": "10:40", "event": "Root cause found in new feature code"},
      {"time": "10:45", "event": "Hotfix deployed"}
    ],
    "action_items": [
      {"task": "Add DB connection leak detection", "owner": "Backend Team", "due_date": "2025-06-08"}
    ],
    "lessons_learned": "All DB connection usage must be wrapped in context managers.",
    "created_by": "Ayush Sinha"
  }'
```

**Export PDF:**
```bash
curl http://localhost:8080/api/incidents/1/postmortem/export
```
"This generates a complete PDF report with MTTR calculated automatically — 45 minutes in this case."

---

## [4:00 – 5:00] Metrics Dashboard

```bash
curl http://localhost:8080/api/metrics
```

"The metrics endpoint shows total incidents by severity and the average MTTR across all resolved incidents — key SRE metrics."

---

## [5:00 – 6:00] Jenkins Pipeline

"Now let me show the Jenkins pipeline." (Open Jenkins UI)

"The pipeline has 9 stages: Checkout → Pylint → Dependencies → Unit Tests → Integration Tests → Docker Build → Trivy Security Scan → Staging Deploy → Production Deploy (with manual approval gate)."

"All 13 unit tests pass with 85% coverage. The Trivy scan reports no critical vulnerabilities."

---

## [6:00 – 6:45] Monitoring

"Nagios is running at port 8081." (Open Nagios UI)

"Three service checks are configured: HTTP health check on /health, the /api/incidents endpoint, and a TCP check on PostgreSQL port 5432. All green."

---

## [6:45 – 7:30] Summary

"To summarize: the project delivers a fully working REST API for incident post-mortem management, PDF export with MTTR, Docker + Kubernetes deployment, a 9-stage Jenkins pipeline, and Nagios monitoring — all documented with API docs, a design document, and user guide."

"Thank you. Happy to take questions."
