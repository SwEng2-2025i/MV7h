from flask import Blueprint, request, jsonify
from services.notification_service import NotificationService

notif_bp = Blueprint('notif_bp', __name__)
service = NotificationService()

@notif_bp.route('/notifications/send', methods=['POST'])
def send_notification():
    data = request.get_json()
    result = service.send_notification(data)
    return jsonify(result), 200