import importlib.util
from pathlib import Path


def load_pomodoro_timer():
    root = Path(__file__).resolve().parents[1]
    timer_path = root / "1.pomodoro" / "timer.py"
    spec = importlib.util.spec_from_file_location("pomodoro_timer", str(timer_path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.PomodoroTimer


def test_tick_not_running():
    PomodoroTimer = load_pomodoro_timer()
    t = PomodoroTimer(work_minutes=1 / 60, break_minutes=1 / 60)
    assert not t.running
    before = int(t.remaining)
    t.tick()
    assert int(t.remaining) == before


def test_start_tick_and_finished():
    PomodoroTimer = load_pomodoro_timer()
    t = PomodoroTimer(work_minutes=1 / 60, break_minutes=1 / 60)
    t.start()
    assert t.running
    assert t.state == 'work'
    assert int(t.remaining) == 1
    t.tick()
    assert int(t.remaining) == 0
    assert t.is_finished()


def test_switch_and_reset():
    PomodoroTimer = load_pomodoro_timer()
    t = PomodoroTimer(work_minutes=1 / 60, break_minutes=1 / 60)
    t.start()
    t.tick()
    t.switch()
    assert t.state == 'break'
    assert int(t.remaining) == 1
    t.reset()
    assert not t.running
    assert int(t.remaining) == int(t.break_seconds)


def test_multiple_switches():
    PomodoroTimer = load_pomodoro_timer()
    t = PomodoroTimer(work_minutes=1 / 60, break_minutes=2 / 60)
    t.start()
    t.switch()
    assert t.state == 'break'
    assert int(t.remaining) == 2
    t.switch()
    assert t.state == 'work'
    assert int(t.remaining) == 1
