import pytest
import json
from src.main.app import create_app, db


@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


# ─── Health Check ─────────────────────────────────────────────────────────────

def test_health_check(client):
    response = client.get('/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'healthy'


# ─── Incident CRUD ────────────────────────────────────────────────────────────

def test_create_incident(client):
    payload = {
        'title': 'Database connection pool exhausted',
        'severity': 'P1',
        'start_time': '2025-06-01T10:00:00',
        'reported_by': 'SRE Team',
        'detected_by': 'Nagios Alert',
    }
    response = client.post('/api/incidents',
                           data=json.dumps(payload),
                           content_type='application/json')
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['title'] == 'Database connection pool exhausted'
    assert data['severity'] == 'P1'


def test_create_incident_missing_fields(client):
    payload = {'title': 'Incomplete incident'}
    response = client.post('/api/incidents',
                           data=json.dumps(payload),
                           content_type='application/json')
    assert response.status_code == 400


def test_get_incidents_empty(client):
    response = client.get('/api/incidents')
    assert response.status_code == 200
    assert json.loads(response.data) == []


def test_get_incident_by_id(client):
    # Create first
    payload = {'title': 'Memory leak in prod', 'severity': 'P0',
               'start_time': '2025-06-01T08:00:00'}
    create_resp = client.post('/api/incidents',
                              data=json.dumps(payload),
                              content_type='application/json')
    incident_id = json.loads(create_resp.data)['id']

    response = client.get(f'/api/incidents/{incident_id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['id'] == incident_id


def test_update_incident(client):
    payload = {'title': 'Initial title', 'severity': 'P2',
               'start_time': '2025-06-01T08:00:00'}
    create_resp = client.post('/api/incidents',
                              data=json.dumps(payload),
                              content_type='application/json')
    incident_id = json.loads(create_resp.data)['id']

    update_payload = {'status': 'resolved', 'end_time': '2025-06-01T10:30:00'}
    response = client.put(f'/api/incidents/{incident_id}',
                          data=json.dumps(update_payload),
                          content_type='application/json')
    assert response.status_code == 200
    assert json.loads(response.data)['status'] == 'resolved'


def test_delete_incident(client):
    payload = {'title': 'To be deleted', 'severity': 'P3',
               'start_time': '2025-06-01T08:00:00'}
    create_resp = client.post('/api/incidents',
                              data=json.dumps(payload),
                              content_type='application/json')
    incident_id = json.loads(create_resp.data)['id']

    response = client.delete(f'/api/incidents/{incident_id}')
    assert response.status_code == 200

    get_response = client.get(f'/api/incidents/{incident_id}')
    assert get_response.status_code == 404


# ─── Post-Mortem ──────────────────────────────────────────────────────────────

def test_create_postmortem(client):
    # Create incident
    payload = {'title': 'API timeout incident', 'severity': 'P1',
               'start_time': '2025-06-01T08:00:00'}
    create_resp = client.post('/api/incidents',
                              data=json.dumps(payload),
                              content_type='application/json')
    incident_id = json.loads(create_resp.data)['id']

    pm_payload = {
        'summary': 'The API gateway timed out due to a misconfigured load balancer.',
        'impact': 'All users unable to access the application for 45 minutes.',
        'root_cause': 'Load balancer health check timeout was set too low.',
        'timeline': [
            {'time': '10:00', 'event': 'Alert triggered'},
            {'time': '10:15', 'event': 'Engineer on-call paged'},
            {'time': '10:45', 'event': 'Root cause identified'},
            {'time': '10:50', 'event': 'Fix deployed'},
        ],
        'action_items': [
            {'task': 'Increase health check timeout', 'owner': 'DevOps', 'due_date': '2025-06-08'},
        ],
        'lessons_learned': 'Always review load balancer configs after updates.',
        'created_by': 'Ayush Sinha',
    }
    response = client.post(f'/api/incidents/{incident_id}/postmortem',
                           data=json.dumps(pm_payload),
                           content_type='application/json')
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['summary'] == pm_payload['summary']


def test_duplicate_postmortem(client):
    payload = {'title': 'Dup test', 'severity': 'P2',
               'start_time': '2025-06-01T08:00:00'}
    create_resp = client.post('/api/incidents',
                              data=json.dumps(payload),
                              content_type='application/json')
    incident_id = json.loads(create_resp.data)['id']

    pm = {'summary': 'First post-mortem'}
    client.post(f'/api/incidents/{incident_id}/postmortem',
                data=json.dumps(pm), content_type='application/json')
    second = client.post(f'/api/incidents/{incident_id}/postmortem',
                         data=json.dumps(pm), content_type='application/json')
    assert second.status_code == 409


# ─── Metrics ──────────────────────────────────────────────────────────────────

def test_metrics(client):
    response = client.get('/api/metrics')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'total_incidents' in data
    assert 'by_severity' in data
    assert 'average_mttr_minutes' in data
