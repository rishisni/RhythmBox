from datetime import timedelta

class Config:
    
    REDIS_URL = 'redis://localhost:6379/0'
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
    CELERY_TIMEZONE = 'Asia/Kolkata'
    # Email configuration
   
