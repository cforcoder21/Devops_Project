# Self-Assessment
## Incident Post-Mortem Generator

**Student:** Ayush Sinha  
**Registration No:** 23FE10CSE00073  
**Course:** CSE3253 DevOps [PE6]  
**Semester:** VI (2025-2026)

---

## Assessment Table

| Criteria | Max Marks | Self Score | Remarks |
|----------|-----------|------------|---------|
| Implementation | 4 | 4 | Full REST API (11 endpoints), PDF generation, MTTR calculation, metrics dashboard, PostgreSQL integration |
| Documentation | 3 | 3 | README, API docs, design document, user guide, project plan all completed with full detail |
| Innovation | 2 | 2 | Automated PDF post-mortem export with ReportLab; MTTR auto-calculation as a key SRE metric |
| Presentation | 1 | 1 | 7-minute demo script prepared with live curl commands and Jenkins pipeline walkthrough |
| **Total** | **10** | **10** | |

---

## Project Challenges & Solutions

1. **SQLAlchemy cascade delete relationship**  
   When deleting an incident, the related post-mortem record was left orphaned in the database.  
   *Solution:* Added `cascade='all, delete-orphan'` to the PostMortem backref in the Incident model.

2. **ReportLab rendering of JSON fields**  
   The `timeline` and `action_items` fields are stored as JSON arrays. Rendering them as plain text produced unreadable output in the PDF.  
   *Solution:* Iterated over each JSON list and built ReportLab `Table` objects with headers for clean, structured display.

3. **Kubernetes readiness probe timing**  
   The readiness probe was failing on initial deployment because it checked before Gunicorn workers were fully initialized.  
   *Solution:* Increased `initialDelaySeconds` from 5 to 10 seconds for the readiness probe and to 30 seconds for the liveness probe.
