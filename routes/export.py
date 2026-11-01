from application.tasks import process_bulk_booking, export_booking_csv
from celery.result import AsyncResult
from flask import Blueprint, request, jsonify, send_from_directory, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
import os
from application.models import *
from application.celery_app import celery


export_bp = Blueprint('export', __name__)

@export_bp.route('/booking/bulk', methods=["POST"])
@jwt_required()
def trigger_bulk_booking():
    cur_username = get_jwt_identity()
    user = User.query.filter_by(name=cur_username).first()
    
    data = request.get_json()
    spacecraft_id = data.get('spacecraft_id')
    seat_count = int(data.get('seat_count', 5))
    
    task = process_bulk_booking.delay(user.id, spacecraft_id, seat_count)
    
    return jsonify({
        "message": "Bulk Bokkings order queued",
        "task_id": task.id,
        "status": "PENDING"
    }), 202


@export_bp.route('/export/bookings', methods=["POST"])
@jwt_required()
def trigger_export():
    task = export_booking_csv.delay()
    return jsonify({
        "message": "Export initiated",
        "task_id": task.id,
        "status": "PENDING"
    }), 202

@export_bp.route('/task/status/<string:task_id>', methods=["GET"])
def get_task_status(task_id):
    result = AsyncResult(task_id, app=celery)
    if result.state == 'PENDING':
        return jsonify({"status": "PENDING"}), 200
    elif result.state == 'SUCCESS':
        return jsonify({"status":"SUCCESS", "result": result.result}), 200
    return jsonify({
        "status": result.state
    }), 200
    

@export_bp.route('/export/download/<string:filename>', methods=['GET'])
def download_file(filename):
    root_dir = os.path.dirname(current_app.root_path)
    export_dir = os.path.join(root_dir, "exports")
    return send_from_directory(export_dir, filename, as_attachment=True)

def format_schedule(sched):
    if isinstance(sched, (int, float)):
        return f"Every {int(sched)}s (Interval)"
    sched_str = str(sched)
    if "crontab:" in sched_str:
        cron_expr = sched_str.split("crontab:")[1].split("(")[0].strip()
        parts = cron_expr.split()
        if len(parts) >= 2 and parts[0].isdigit() and parts[1].isdigit():
            return f"Daily at {int(parts[1]):02d}:{int(parts[0]):02d} (Cron: {cron_expr})"
        return f"Cron: {cron_expr}"
    return sched_str

@export_bp.route('/system/automation-status', methods=["GET"])
@jwt_required()
def get_automation_status():
    schedules = []
    for name, conf in celery.conf.beat_schedule.items():
        sched_obj = conf.get("schedule")
        schedules.append({
            "name": name,
            "task": conf.get("task"),
            "schedule": str(sched_obj),
            "frequency": format_schedule(sched_obj)
        })
    return jsonify({
        "status": "ONLINE",
        "scheduler": "Celery Beat",
        "registered_jobs": schedules,
        "total_jobs": len(schedules)
    }), 200