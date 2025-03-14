# app/main.py

from flask import Blueprint, render_template, request, session
from .task_scheduler import Scheduler

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    scheduler = Scheduler()
    scheduler.load_from_session()
    schedule = scheduler.get_schedule()
    return render_template('index.html', schedule=schedule)

@bp.route('/add_task', methods=['POST'])
def add_task():
    task_name = request.form['task']
    scheduled_date = request.form.get('scheduled_date', None)
    importance = request.form['importance']
    duration = request.form['duration']
    dependency = request.form.get('dependency', None)

    if scheduled_date and not scheduled_date.strip():
        scheduled_date = None

    scheduler = Scheduler()
    scheduler.load_from_session()
    scheduler.add_task(task_name, scheduled_date, importance, duration, dependency)
    scheduler.save_to_session()

    schedule = scheduler.get_schedule()
    return render_template('index.html', schedule=schedule)

@bp.route('/remove_task', methods=['POST'])
def remove_task():
    task_name = request.form['task']

    scheduler = Scheduler()
    scheduler.load_from_session()
    scheduler.remove_task(task_name)
    scheduler.save_to_session()
    schedule = scheduler.get_schedule()

    return render_template('index.html', schedule=schedule)
