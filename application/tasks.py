import csv
import os
import time
from datetime import datetime
from application.celery_app import celery
from application.models import *
from application.database import db

@celery.task(name="tasks.process_bulk_booking")
def process_bulk_booking(user_id, spacecraft_id, seat_count):
    craft = SpaceCraft.query.get(spacecraft_id)
    if not craft:
        return {"status": "FAILED", "reason": "Spacecraft not found..."}
    created_ids = []
    for i in range(seat_count):
        current_count = Booking.query.filter_by(spacecraft_id=craft.id).count()
        if current_count >= craft.capacity:
            break
        cur_booking = Booking(user=user_id, spacecraft=craft.id, booking_date=datetime.utcnow())
        db.session.add(cur_booking)
        db.session.commit()
        created_ids.append(cur_booking.id)
        
        return {
            "status" : "SUCCESS",
            "seats_booked": len(created_ids),
            "requested": seat_count
        }

@celery.task(name="tasks.export_bookings_csv")
def export_booking_csv():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    export_dir = os.path.join(base_dir, "exports")
    os.makedirs(export_dir, exist_ok=True) 
    
    filename = f"bookings_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    filepath = os.path.join(export_dir, filename)
    
    bookings = Booking.query.all()
    
    with open(filepath, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Booking ID", "Passenger", "SpaceCraft", "Date"])
        for b in bookings:
            writer.writerow([b.id,
                             b.user.name if b.user else "Unknown", 
                             b.spacecraft.name if b.spacecraft else "Unknown",
                             b.booking_date.strftime('%Y%m%d_%H%M%S') if b.booking_date else ""])
    return {"status": "SUCCESS", 
            "filename": filename,
            "total_records": len(bookings)
            }

@celery.task(name="tasks.heartbeat_ping")
def heartbeat_ping():
    now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{now_str}] Heartbeat ping received [HEART BEAT TICK]")
    return {"status": "ALIVE", "timestamp": now_str}

@celery.task(name="tasks.daily_flight_reminder")
def daily_flight_reminder():
    bookings = Booking.query.all()
    reminder_rec = []
    print(f"\n [Celery BEAT] --- INITIATING DAILY FLIGHT REMINDER TASK --- \n")
    print(f"Found {len(bookings)} bookings to process for reminders.")
    
    for b in bookings:
        passenger_name = b.user.name if b.user else "Unknown"
        craft_name = b.spacecraft.name if b.spacecraft else "Unknown"
        flight_date = b.booking_date.strftime('%Y-%m-%d %H:%M:%S') if b.booking_date else "Scheduled Soon..."
        
        reminder_msg = (
            f"Dear {passenger_name}, this is a reminder for your upcoming flight on {craft_name} scheduled for {flight_date}. Please arrive at Launchpad 2 hours prior. Safe travel!"
        )
        
        print(f"Sending reminder to {passenger_name} for flight on {craft_name} scheduled for {flight_date}.")
        reminder_rec.append({
            "booking_id": b.id,
            "passenger": passenger_name,
            "spacecraft": craft_name,
            "dispatched_at": datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
        })
    print(f"\n [Celery BEAT] --- DAILY FLIGHT REMINDER TASK ({len(reminder_rec)}) COMPLETED --- \n")
    return {
        "status": "SUCCESS",
        "reminders_sent": len(reminder_rec),
        "details": reminder_rec
    }

@celery.task(name="tasks.monthly_fleet_manifest_report")
def monthly_fleet_manifest_report():
    total_users = User.query.count()
    total_spacecrafts = SpaceCraft.query.count()
    total_bookings = Booking.query.count()
    
    report_sum = {
        "generated_at": datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
        "total_registered_cadets": total_users,
        "active_fleet_size": total_spacecrafts,
        "total_tickets_issued": total_bookings
    }
    
    print(f"\n [Celery BEAT] --- MONTHLY FLEET MANIFEST REPORT GENERATED --- \n")
    print(f" Total Registered Cadets: {total_users}")
    print(f" Active Fleet Size: {total_spacecrafts}")
    print(f" Total Tickets Issued: {total_bookings}")
    
    return {"status": "SUCCESS", "report": report_sum}