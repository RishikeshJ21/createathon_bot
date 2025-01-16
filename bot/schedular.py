from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()
scheduler.add_job(send_daily_prompt, "interval", days=1, start_date="2025-01-16 09:00:00")
scheduler.add_job(analyze_challenge_progress, "interval", days=1, start_date="2025-02-06 09:00:00")
scheduler.start()

# Remember to gracefully shut down scheduler during bot exit
import atexit
atexit.register(lambda: scheduler.shutdown())
