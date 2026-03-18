# User Guide — Incident Post-Mortem Generator

**Student:** Ayush Sinha | **Reg. No:** 23FE10CSE00073

---

## Getting Started

### Start the Application

**With Docker (recommended):**
```bash
docker-compose -f infrastructure/docker/docker-compose.yml up -d
```

**Without Docker:**
```bash
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python run.py
```

The API will be available at `http://localhost:8080`.

---

## Typical Workflow

### Step 1 — Report an Incident

When a production incident occurs, create an incident record immediately:

```bash
curl -X POST http://localhost:8080/api/incidents \
  -H "Content-Type: application/json" \
  -d '{
    "title": "API gateway returning 504 errors",
    "severity": "P1",
    "start_time": "2025-06-01T10:00:00",
    "detected_by": "Nagios Alert",
    "reported_by": "On-Call Engineer"
  }'
```

**Severity Guide:**
| Level | Use When |
|-------|----------|
| P0 | Complete service outage — all users affected |
| P1 | Major feature broken — significant user impact |
| P2 | Degraded performance — partial user impact |
| P3 | Minor issue — workaround available |

---

### Step 2 — Resolve the Incident

When the incident is resolved, update the record with an end time:

```bash
curl -X PUT http://localhost:8080/api/incidents/1 \
  -H "Content-Type: application/json" \
  -d '{
    "status": "resolved",
    "end_time": "2025-06-01T10:45:00"
  }'
```

---

### Step 3 — Write the Post-Mortem

Within 24–48 hours of resolution, document the full post-mortem:

```bash
curl -X POST http://localhost:8080/api/incidents/1/postmortem \
  -H "Content-Type: application/json" \
  -d '{
    "summary": "The API gateway returned 504 errors for 45 minutes due to a misconfigured load balancer health check timeout.",
    "impact": "Approximately 5,000 users were unable to access the application.",
    "root_cause": "A routine config change set the health check timeout to 1s, causing the LB to mark all backends as unhealthy.",
    "timeline": [
      { "time": "10:00", "event": "Nagios alert triggered — HTTP check failing" },
      { "time": "10:15", "event": "On-call engineer paged via PagerDuty" },
      { "time": "10:40", "event": "Root cause identified in load balancer config" },
      { "time": "10:45", "event": "Timeout corrected to 10s, backends recovered" }
    ],
    "contributing_factors": [
      "No peer review required for infrastructure config changes",
      "Staging environment did not replicate production LB settings"
    ],
    "action_items": [
      {
        "task": "Require peer review for all LB config changes",
        "owner": "DevOps Lead",
        "due_date": "2025-06-08"
      },
      {
        "task": "Mirror production LB config in staging",
        "owner": "Infrastructure Team",
        "due_date": "2025-06-15"
      }
    ],
    "lessons_learned": "Always validate infrastructure config changes in a staging environment that mirrors production before applying them.",
    "detection_method": "Nagios HTTP health check",
    "resolution_steps": "Updated LB health check timeout from 1s to 10s via config management and redeployed.",
    "created_by": "Ayush Sinha",
    "reviewed_by": "Team Lead"
  }'
```

---

### Step 4 — Export PDF Report

Generate a professionally formatted PDF:

```bash
curl http://localhost:8080/api/incidents/1/postmortem/export
```

The response includes the path to the generated PDF and the MTTR:

```json
{
  "pdf_path": "/app/deliverables/postmortem_incident_1_20250601123456.pdf",
  "mttr_minutes": 45.0
}
```

---

### Step 5 — View Dashboard Metrics

Track your team's incident trends:

```bash
curl http://localhost:8080/api/metrics
```

```json
{
  "total_incidents": 12,
  "by_severity": { "P0": 1, "P1": 3, "P2": 6, "P3": 2 },
  "resolved_count": 10,
  "average_mttr_minutes": 52.4
}
```

---

## Managing Incidents

### List All Incidents
```bash
curl http://localhost:8080/api/incidents
```

### Get a Specific Incident
```bash
curl http://localhost:8080/api/incidents/1
```

### Delete an Incident
```bash
curl -X DELETE http://localhost:8080/api/incidents/1
```
> **Note:** Deleting an incident also deletes its associated post-mortem.

---

## Monitoring Dashboard

Access Nagios at `http://localhost:8081` to view:
- Application HTTP health status
- API endpoint availability
- PostgreSQL database connectivity

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `Connection refused on port 8080` | Check if Docker containers are running: `docker ps` |
| `404 on /api/incidents/1` | The incident ID does not exist — check with GET /api/incidents |
| `409 Conflict on POST /postmortem` | A post-mortem already exists — use PUT to update it |
| `Database connection error` | Ensure PostgreSQL is healthy: `docker logs postmortem_db` |
| PDF not generating | Check `deliverables/` folder permissions and ReportLab installation |
