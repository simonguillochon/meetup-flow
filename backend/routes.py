from flask import Blueprint, request, jsonify
from app import db
from models import Conference, ConferenceStatus, ConferenceLevel
from datetime import datetime

api = Blueprint('api', __name__)

@api.route('/conferences', methods=['GET'])
def get_conferences():
    conferences = Conference.query.all()
    # Group by status? Or just return list and let frontend partial it out?
    # Spec said "Kanban columns contain cards", usually easier to send flat list and filter on FE, 
    # but backend can also return grouped. Choosing flat list as per plan "GET /api/conferences".
    return jsonify([c.to_dict() for c in conferences])

@api.route('/conferences', methods=['POST'])
def create_conference():
    data = request.json
    try:
        new_conference = Conference(
            title=data['title'],
            status=ConferenceStatus(data.get('status', 'Idées')), # Default to Idées if not provided, but validate enum
            assignee=data.get('assignee'),
            date=datetime.fromisoformat(data['date']) if data.get('date') else None,
            link_doc=data.get('link_doc'),
            address=data.get('address'),
            level=ConferenceLevel(data.get('level', 'easy'))
        )
        db.session.add(new_conference)
        db.session.commit()
        return jsonify(new_conference.to_dict()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except KeyError as e:
        return jsonify({"error": f"Missing field: {e}"}), 400

@api.route('/conferences/<int:id>', methods=['PUT'])
def update_conference(id):
    conference = Conference.query.get_or_404(id)
    data = request.json
    
    try:
        if 'title' in data:
            conference.title = data['title']
        if 'status' in data:
            conference.status = ConferenceStatus(data['status'])
        if 'assignee' in data:
            conference.assignee = data['assignee']
        if 'date' in data:
            conference.date = datetime.fromisoformat(data['date'])
        if 'link_doc' in data:
            conference.link_doc = data['link_doc']
        if 'address' in data:
            conference.address = data['address']
        if 'level' in data:
            conference.level = ConferenceLevel(data['level'])
            
        db.session.commit()
        return jsonify(conference.to_dict())
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@api.route('/conferences/<int:id>', methods=['DELETE'])
def delete_conference(id):
    conference = Conference.query.get_or_404(id)
    db.session.delete(conference)
    db.session.commit()
    return '', 204
