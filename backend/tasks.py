from celery import Celery
from celery.schedules import crontab
from flask_mail import Message
from flask import Flask
from models import User , Song , Like , Report
from config import Config
from datetime import datetime, timedelta
from flask_mail import Mail, Message

# from app import app
app = Flask(__name__)
app.config.from_object(Config)
mail = Mail(app)


celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Daily reminder task
    sender.add_periodic_task(
        timedelta(days=1),
        send_daily_reminders.s(),
    )

    # Like reminder task
    sender.add_periodic_task(
        crontab(hour=9, minute=0),  # Run every day at 9:00 AM
        send_like_reminders.s(),
    )

    # Monthly update task
    sender.add_periodic_task(
        crontab(day_of_month=17, hour=18, minute=45),  # Run on the 1st day of every month at 10:00 AM
        generate_monthly_activity_report_for_creators.s(),

    )


@celery.task
def send_email(receiver_email, subject, body):
    with app.app_context():

        msg = Message(subject, sender=app.config['MAIL_USERNAME'], recipients=[receiver_email])
        msg.body = body

        # Send the email
        try:
            mail.send(msg)
            return 'Email sent successfully!'
        except Exception as e:
            return f'Error sending email: {str(e)}'


# Celery task for sending daily reminders
@celery.task
def send_daily_reminders():
    with app.app_context():
        users = User.query.all()
        
        # Set the time for evening reminders
        evening_time = datetime.now().replace(hour=16, minute=57, second=0, microsecond=0)
        
        for user in users:
            # Check if the user has visited the app today
            last_visit = user.last_visit_date
            if last_visit is None or last_visit < datetime.now().date():
                # Send the reminder if the user has not visited the app today
                if datetime.now() >= evening_time:
                    send_email.apply_async((user.email, "Daily Reminder", "Don't forget to visit the app!"), countdown=120)  # Sending after 2 minutes
            else:
                # User has visited the app today, no need for reminder
                pass

# Celery task for sending reminders to creators if their songs receive likes
@celery.task
def send_like_reminders():
    with app.app_context():
        creators = User.query.filter_by(is_creator=True).all()
        
        for creator in creators:
            # Get all songs created by the creator
            songs = Song.query.filter_by(user_id=creator.id).all()
            
            # Check if any of the creator's songs have received likes
            for song in songs:
                likes = Like.query.filter_by(song_id=song.id).all()
                if likes:
                    # Send a reminder to the creator
                    send_email.apply_async((creator.email, "Song Like Reminder", "One of your songs has received likes!"), countdown=60)  # Sending after 2 minutes

@celery.task
def generate_monthly_activity_report_for_creators():
    with app.app_context():
        creators = User.query.filter_by(is_creator=True).all()
        
        # Get the first day of the current month
        first_day_of_month = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        for creator in creators:
            # Get songs created by the creator in the current month
            songs = Song.query.filter(
                Song.user_id == creator.id,
                Song.date_created >= first_day_of_month
            ).all()
            
            # Generate the report content
            report_content = f"Monthly Activity Report for {first_day_of_month.strftime('%B %Y')}:\n\n"
            report_content += f"Songs Created:\n"
            for song in songs:
                report_content += f"- {song.name}\n"
            
            # Send the report via email
            send_email.apply_async((creator.email, "Monthly Activity Report", report_content), countdown=120)  # Sending after 2 minutes


# Celery task for generating monthly activity report for users
@celery.task
def generate_monthly_activity_report_for_users():
    with app.app_context():
        users = User.query.all()
        
        # Get the first day of the current month
        first_day_of_month = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        for user in users:
            # Get songs liked by the user in the current month
            liked_songs = Like.query.filter(
                Like.user_id == user.id,
                Like.date_liked >= first_day_of_month
            ).all()
            
            # Generate the report content
            report_content = f"Monthly Liked Songs Report for {first_day_of_month.strftime('%B %Y')}:\n\n"
            report_content += f"Songs Liked:\n"
            for like in liked_songs:
                song = Song.query.get(like.song_id)
                if song:
                    report_content += f"- {song.name}\n"
            
            # Send the report via email
            send_email.apply_async((user.email, "Monthly Liked Songs Report", report_content), countdown=120)  # Sending after 2 minutes

