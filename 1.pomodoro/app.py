# Pomodoro Timer App
import sqlite3
import json
import os
import random
from datetime import datetime, timedelta, timezone
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pomodoro.db')

BADGES = [
    {'id': 'first_tomato',  'name': 'First Tomato',   'icon': '🍅', 'description': 'Complete your first Pomodoro'},
    {'id': 'on_fire',       'name': 'On Fire',         'icon': '🔥', 'description': 'Complete 5 Pomodoros in a day'},
    {'id': 'streak_3',      'name': '3-Day Streak',    'icon': '📅', 'description': '3 consecutive days'},
    {'id': 'streak_7',      'name': '7-Day Streak',    'icon': '🗓️', 'description': '7 consecutive days'},
    {'id': 'week_champion', 'name': 'Week Champion',   'icon': '🏆', 'description': 'Complete 10 Pomodoros in a week'},
    {'id': 'century',       'name': 'Century',         'icon': '⭐', 'description': 'Complete 100 total Pomodoros'},
    {'id': 'daily_goal',    'name': 'Daily Goal',      'icon': '🎯', 'description': 'Complete 4 Pomodoros in a day'},
]
BADGE_MAP = {b['id']: b for b in BADGES}

XP_PER_POMODORO = 25
XP_PER_LEVEL = 100

MOTIVATIONAL = [
    "Great work! Keep it up! 💪",
    "Another one done! You are on fire! 🔥",
    "Focus like a laser! 🎯",
    "Crushing it! 🚀",
    "Productivity level: MAX! ⚡",
    "You are unstoppable! 🏆",
    "One step closer to your goals! 🌟",
]


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                completed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                session_type TEXT DEFAULT 'work'
            );
            CREATE TABLE IF NOT EXISTS user_data (
                id INTEGER PRIMARY KEY DEFAULT 1,
                total_xp INTEGER DEFAULT 0,
                current_streak INTEGER DEFAULT 0,
                longest_streak INTEGER DEFAULT 0,
                last_session_date TEXT DEFAULT NULL,
                badges TEXT DEFAULT '[]'
            );
            INSERT OR IGNORE INTO user_data (id) VALUES (1);
        """)


def get_user():
    with get_db() as conn:
        row = conn.execute("SELECT * FROM user_data WHERE id = 1").fetchone()
    return dict(row)


def save_user(data):
    with get_db() as conn:
        conn.execute("""
            UPDATE user_data SET
                total_xp = ?,
                current_streak = ?,
                longest_streak = ?,
                last_session_date = ?,
                badges = ?
            WHERE id = 1
        """, (data['total_xp'], data['current_streak'], data['longest_streak'],
              data['last_session_date'], data['badges']))


def xp_to_level(xp):
    return xp // XP_PER_LEVEL + 1


def xp_to_next_level(xp):
    return XP_PER_LEVEL - (xp % XP_PER_LEVEL)


def xp_progress_pct(xp):
    return xp % XP_PER_LEVEL


def update_streak(user):
    today = datetime.now(timezone.utc).date().isoformat()
    last = user.get('last_session_date')
    if last is None:
        user['current_streak'] = 1
    else:
        last_date = datetime.strptime(last, '%Y-%m-%d').date()
        today_date = datetime.strptime(today, '%Y-%m-%d').date()
        diff = (today_date - last_date).days
        if diff == 0:
            pass
        elif diff == 1:
            user['current_streak'] = user['current_streak'] + 1
        else:
            user['current_streak'] = 1
    user['last_session_date'] = today
    if user['current_streak'] > user['longest_streak']:
        user['longest_streak'] = user['current_streak']
    return user


def check_badges(user, total_today, total_week, total_all):
    earned = json.loads(user['badges'])
    new_badges = []

    def award(badge_id):
        if badge_id not in earned:
            earned.append(badge_id)
            new_badges.append(badge_id)

    if total_all >= 1:
        award('first_tomato')
    if total_today >= 5:
        award('on_fire')
    if user['current_streak'] >= 3:
        award('streak_3')
    if user['current_streak'] >= 7:
        award('streak_7')
    if total_week >= 10:
        award('week_champion')
    if total_all >= 100:
        award('century')
    if total_today >= 4:
        award('daily_goal')

    user['badges'] = json.dumps(earned)
    return new_badges


def get_daily_counts(days=7):
    result = []
    with get_db() as conn:
        for i in range(days - 1, -1, -1):
            d = (datetime.now(timezone.utc).date() - timedelta(days=i)).isoformat()
            row = conn.execute(
                "SELECT COUNT(*) as cnt FROM sessions WHERE date(completed_at) = ? AND session_type = 'work'", (d,)
            ).fetchone()
            result.append({'date': d, 'count': row['cnt']})
    return result


def get_weekly_counts(weeks=4):
    result = []
    today = datetime.now(timezone.utc).date()
    with get_db() as conn:
        for i in range(weeks - 1, -1, -1):
            week_end = today - timedelta(weeks=i)
            week_start = week_end - timedelta(days=6)
            row = conn.execute(
                "SELECT COUNT(*) as cnt FROM sessions WHERE date(completed_at) BETWEEN ? AND ? AND session_type = 'work'",
                (week_start.isoformat(), week_end.isoformat())
            ).fetchone()
            label = "{} - {}".format(week_start.strftime('%b %d'), week_end.strftime('%b %d'))
            result.append({'week': label, 'count': row['cnt']})
    return result


def get_today_count():
    today = datetime.now(timezone.utc).date().isoformat()
    with get_db() as conn:
        row = conn.execute(
            "SELECT COUNT(*) as cnt FROM sessions WHERE date(completed_at) = ? AND session_type = 'work'", (today,)
        ).fetchone()
    return row['cnt']


def get_week_count():
    today = datetime.now(timezone.utc).date()
    week_start = (today - timedelta(days=today.weekday())).isoformat()
    with get_db() as conn:
        row = conn.execute(
            "SELECT COUNT(*) as cnt FROM sessions WHERE date(completed_at) >= ? AND session_type = 'work'", (week_start,)
        ).fetchone()
    return row['cnt']


def get_all_time_count():
    with get_db() as conn:
        row = conn.execute("SELECT COUNT(*) as cnt FROM sessions WHERE session_type = 'work'").fetchone()
    return row['cnt']


@app.route('/')
def index():
    user = get_user()
    level = xp_to_level(user['total_xp'])
    xp_next = xp_to_next_level(user['total_xp'])
    xp_pct = xp_progress_pct(user['total_xp'])
    today_count = get_today_count()
    earned_badges = json.loads(user['badges'])
    badges_display = [{**b, 'earned': b['id'] in earned_badges} for b in BADGES]
    return render_template('index.html', user=user, level=level, xp_next=xp_next,
                           xp_pct=xp_pct, today_count=today_count, badges=badges_display)


@app.route('/complete', methods=['POST'])
def complete():
    with get_db() as conn:
        conn.execute("INSERT INTO sessions (session_type) VALUES ('work')")

    user = get_user()
    old_level = xp_to_level(user['total_xp'])
    user['total_xp'] += XP_PER_POMODORO
    user = update_streak(user)

    total_today = get_today_count()
    total_week = get_week_count()
    total_all = get_all_time_count()

    new_badge_ids = check_badges(user, total_today, total_week, total_all)
    save_user(user)

    new_level = xp_to_level(user['total_xp'])
    leveled_up = new_level > old_level
    new_badge_details = [BADGE_MAP[bid] for bid in new_badge_ids]

    return jsonify({
        'xp_gained': XP_PER_POMODORO,
        'total_xp': user['total_xp'],
        'level': new_level,
        'xp_pct': xp_progress_pct(user['total_xp']),
        'xp_next': xp_to_next_level(user['total_xp']),
        'leveled_up': leveled_up,
        'current_streak': user['current_streak'],
        'new_badges': new_badge_details,
        'message': random.choice(MOTIVATIONAL),
        'today_count': total_today,
    })


@app.route('/stats')
def stats():
    user = get_user()
    level = xp_to_level(user['total_xp'])
    today_count = get_today_count()
    week_count = get_week_count()
    all_time = get_all_time_count()
    earned_badges = json.loads(user['badges'])
    daily = get_daily_counts(7)
    avg_daily = round(sum(d['count'] for d in daily) / 7, 1)
    badges_display = [{**b, 'earned': b['id'] in earned_badges} for b in BADGES]
    return render_template('stats.html', user=user, level=level, today_count=today_count,
                           week_count=week_count, all_time=all_time, avg_daily=avg_daily,
                           badges=badges_display)


@app.route('/api/stats')
def api_stats():
    daily = get_daily_counts(7)
    weekly = get_weekly_counts(4)
    user = get_user()
    today_count = get_today_count()
    week_count = get_week_count()
    all_time = get_all_time_count()
    avg_daily = round(sum(d['count'] for d in daily) / 7, 1)
    return jsonify({
        'daily': daily, 'weekly': weekly,
        'today_count': today_count, 'week_count': week_count,
        'all_time': all_time,
        'current_streak': user['current_streak'],
        'longest_streak': user['longest_streak'],
        'avg_daily': avg_daily,
    })


@app.route('/api/user')
def api_user():
    user = get_user()
    earned = json.loads(user['badges'])
    badges_full = [BADGE_MAP[bid] for bid in earned if bid in BADGE_MAP]
    return jsonify({
        'total_xp': user['total_xp'],
        'level': xp_to_level(user['total_xp']),
        'xp_pct': xp_progress_pct(user['total_xp']),
        'xp_next': xp_to_next_level(user['total_xp']),
        'current_streak': user['current_streak'],
        'longest_streak': user['longest_streak'],
        'badges': badges_full,
    })


if __name__ == '__main__':
    init_db()
    debug = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
    app.run(debug=debug, port=5000)
