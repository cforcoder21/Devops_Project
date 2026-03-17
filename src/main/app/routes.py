from flask import Blueprint, request, jsonify
from src.main.app import db
from src.main.app.models import Incident, PostMortem
from src.main.app.utils import generate_postmortem_pdf, calculate_mttr
from datetime import datetime

main_bp = Blueprint('main', __name__)


# ─── Health Check ────────────────────────────────────────────────────────────

@main_bp.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'service': 'Incident Post-Mortem Generator'}), 200


# ─── Incidents ────────────────────────────────────────────────────────────────

@main_bp.route('/api/incidents', methods=['GET'])
def get_incidents():
    incidents = Incident.query.order_by(Incident.created_at.desc()).all()
    return jsonify([i.to_dict() for i in incidents]), 200


@main_bp.route('/api/incidents/<int:incident_id>', methods=['GET'])
def get_incident(incident_id):
    incident = Incident.query.get_or_404(incident_id)
    return jsonify(incident.to_dict()), 200


@main_bp.route('/api/incidents', methods=['POST'])
def create_incident():
    data = request.get_json()
    if not data or not data.get('title') or not data.get('severity'):
        return jsonify({'error': 'title and severity are required'}), 400

    incident = Incident(
        title=data['title'],
        severity=data['severity'],
        status=data.get('status', 'open'),
        start_time=datetime.fromisoformat(data['start_time']) if data.get('start_time') else datetime.utcnow(),
        end_time=datetime.fromisoformat(data['end_time']) if data.get('end_time') else None,
        detected_by=data.get('detected_by'),
        reported_by=data.get('reported_by'),
    )
    db.session.add(incident)
    db.session.commit()
    return jsonify(incident.to_dict()), 201


@main_bp.route('/api/incidents/<int:incident_id>', methods=['PUT'])
def update_incident(incident_id):
    incident = Incident.query.get_or_404(incident_id)
    data = request.get_json()

    for field in ['title', 'severity', 'status', 'detected_by', 'reported_by']:
        if field in data:
            setattr(incident, field, data[field])
    if 'start_time' in data:
        incident.start_time = datetime.fromisoformat(data['start_time'])
    if 'end_time' in data:
        incident.end_time = datetime.fromisoformat(data['end_time'])

    db.session.commit()
    return jsonify(incident.to_dict()), 200


@main_bp.route('/api/incidents/<int:incident_id>', methods=['DELETE'])
def delete_incident(incident_id):
    incident = Incident.query.get_or_404(incident_id)
    db.session.delete(incident)
    db.session.commit()
    return jsonify({'message': 'Incident deleted'}), 200


# ─── Post-Mortems ─────────────────────────────────────────────────────────────

@main_bp.route('/api/incidents/<int:incident_id>/postmortem', methods=['GET'])
def get_postmortem(incident_id):
    pm = PostMortem.query.filter_by(incident_id=incident_id).first_or_404()
    return jsonify(pm.to_dict()), 200


@main_bp.route('/api/incidents/<int:incident_id>/postmortem', methods=['POST'])
def create_postmortem(incident_id):
    Incident.query.get_or_404(incident_id)
    if PostMortem.query.filter_by(incident_id=incident_id).first():
        return jsonify({'error': 'Post-mortem already exists for this incident'}), 409

    data = request.get_json()
    if not data or not data.get('summary'):
        return jsonify({'error': 'summary is required'}), 400

    pm = PostMortem(
        incident_id=incident_id,
        summary=data['summary'],
        impact=data.get('impact'),
        root_cause=data.get('root_cause'),
        timeline=data.get('timeline', []),
        contributing_factors=data.get('contributing_factors', []),
        action_items=data.get('action_items', []),
        lessons_learned=data.get('lessons_learned'),
        detection_method=data.get('detection_method'),
        resolution_steps=data.get('resolution_steps'),
        created_by=data.get('created_by'),
        reviewed_by=data.get('reviewed_by'),
    )
    db.session.add(pm)
    db.session.commit()
    return jsonify(pm.to_dict()), 201


@main_bp.route('/api/incidents/<int:incident_id>/postmortem', methods=['PUT'])
def update_postmortem(incident_id):
    pm = PostMortem.query.filter_by(incident_id=incident_id).first_or_404()
    data = request.get_json()

    for field in ['summary', 'impact', 'root_cause', 'timeline', 'contributing_factors',
                  'action_items', 'lessons_learned', 'detection_method', 'resolution_steps',
                  'created_by', 'reviewed_by']:
        if field in data:
            setattr(pm, field, data[field])

    db.session.commit()
    return jsonify(pm.to_dict()), 200


@main_bp.route('/api/incidents/<int:incident_id>/postmortem/export', methods=['GET'])
def export_postmortem(incident_id):
    incident = Incident.query.get_or_404(incident_id)
    pm = PostMortem.query.filter_by(incident_id=incident_id).first_or_404()
    mttr = calculate_mttr(incident)
    pdf_path = generate_postmortem_pdf(incident, pm, mttr)
    return jsonify({'pdf_path': pdf_path, 'mttr_minutes': mttr}), 200


# ─── Dashboard / Metrics ──────────────────────────────────────────────────────

@main_bp.route('/api/metrics', methods=['GET'])
def get_metrics():
    total = Incident.query.count()
    by_severity = {}
    for sev in ['P0', 'P1', 'P2', 'P3']:
        by_severity[sev] = Incident.query.filter_by(severity=sev).count()

    resolved = Incident.query.filter_by(status='resolved').all()
    avg_mttr = 0
    if resolved:
        mttrs = [calculate_mttr(i) for i in resolved if i.end_time]
        avg_mttr = sum(mttrs) / len(mttrs) if mttrs else 0

    return jsonify({
        'total_incidents': total,
        'by_severity': by_severity,
        'resolved_count': len(resolved),
        'average_mttr_minutes': round(avg_mttr, 2),
    }), 200
