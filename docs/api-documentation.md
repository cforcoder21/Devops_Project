# API Documentation — Incident Post-Mortem Generator

**Base URL:** `http://localhost:8080`  
**Content-Type:** `application/json`

---

## Health

### GET /health
Returns service health status.

**Response 200:**
```json
{
  "status": "healthy",
  "service": "Incident Post-Mortem Generator"
}
```

---

## Incidents

### GET /api/incidents
Returns a list of all incidents ordered by creation date (newest first).

**Response 200:**
```json
[
  {
    "id": 1,
    "title": "Database connection pool exhausted",
    "severity": "P1",
    "status": "resolved",
    "start_time": "2025-06-01T10:00:00",
    "end_time": "2025-06-01T10:45:00",
    "detected_by": "Nagios Alert",
    "reported_by": "SRE Team",
    "created_at": "2025-06-01T10:05:00",
    "updated_at": "2025-06-01T10:50:00"
  }
]
```

---

### POST /api/incidents
Create a new incident.

**Request Body:**
```json
{
  "title": "Database connection pool exhausted",
  "severity": "P1",
  "start_time": "2025-06-01T10:00:00",
  "end_time": "2025-06-01T10:45:00",
  "detected_by": "Nagios Alert",
  "reported_by": "SRE Team",
  "status": "open"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| title | string | Yes | Short description of the incident |
| severity | string | Yes | One of: P0, P1, P2, P3 |
| start_time | ISO datetime | No | Defaults to current UTC time |
| end_time | ISO datetime | No | Leave null if ongoing |
| detected_by | string | No | Who/what detected the incident |
| reported_by | string | No | Who reported it |
| status | string | No | open / resolved / closed |

**Response 201:** Created incident object  
**Response 400:** `{ "error": "title and severity are required" }`

---

### GET /api/incidents/:id
Get a single incident by ID.

**Response 200:** Incident object  
**Response 404:** Not found

---

### PUT /api/incidents/:id
Update an existing incident.

**Request Body:** Any subset of incident fields  
**Response 200:** Updated incident object

---

### DELETE /api/incidents/:id
Delete an incident and its associated post-mortem.

**Response 200:** `{ "message": "Incident deleted" }`

---

## Post-Mortems

### POST /api/incidents/:id/postmortem
Create a post-mortem for an incident.

**Request Body:**
```json
{
  "summary": "The API gateway timed out due to a misconfigured load balancer.",
  "impact": "All users unable to access the application for 45 minutes.",
  "root_cause": "Load balancer health check timeout was set to 1s instead of 10s after a routine config change.",
  "timeline": [
    { "time": "10:00", "event": "Nagios alert triggered — HTTP check failing" },
    { "time": "10:15", "event": "On-call engineer paged" },
    { "time": "10:40", "event": "Root cause identified in load balancer config" },
    { "time": "10:45", "event": "Timeout value corrected and deployed" }
  ],
  "contributing_factors": [
    "No peer review on infrastructure config changes",
    "Lack of staging environment parity"
  ],
  "action_items": [
    {
      "task": "Add mandatory peer review for LB config changes",
      "owner": "DevOps Lead",
      "due_date": "2025-06-08"
    }
  ],
  "lessons_learned": "Always review load balancer configs in staging before applying to production.",
  "detection_method": "Nagios HTTP check",
  "resolution_steps": "Updated health check timeout from 1s to 10s in the LB config and redeployed.",
  "created_by": "Ayush Sinha",
  "reviewed_by": "Team Lead"
}
```

**Response 201:** Created post-mortem object  
**Response 409:** Post-mortem already exists for this incident

---

### GET /api/incidents/:id/postmortem
Retrieve the post-mortem for an incident.

**Response 200:** Post-mortem object  
**Response 404:** Not found

---

### PUT /api/incidents/:id/postmortem
Update an existing post-mortem.

**Request Body:** Any subset of post-mortem fields  
**Response 200:** Updated post-mortem object

---

### GET /api/incidents/:id/postmortem/export
Generate and export the post-mortem as a PDF file.

**Response 200:**
```json
{
  "pdf_path": "/app/deliverables/postmortem_incident_1_20250601123456.pdf",
  "mttr_minutes": 45.0
}
```

---

## Metrics

### GET /api/metrics
Returns aggregate dashboard metrics.

**Response 200:**
```json
{
  "total_incidents": 12,
  "by_severity": {
    "P0": 1,
    "P1": 3,
    "P2": 6,
    "P3": 2
  },
  "resolved_count": 10,
  "average_mttr_minutes": 52.4
}
```

---

## Severity Levels

| Level | Description |
|-------|-------------|
| P0 | Critical — complete service outage |
| P1 | High — major feature unavailable |
| P2 | Medium — degraded performance |
| P3 | Low — minor issue, workaround available |

---

## Error Responses

All errors follow this format:

```json
{
  "error": "Human-readable error message"
}
```

| HTTP Code | Meaning |
|-----------|---------|
| 400 | Bad Request — missing or invalid fields |
| 404 | Not Found |
| 409 | Conflict — resource already exists |
| 500 | Internal Server Error |
