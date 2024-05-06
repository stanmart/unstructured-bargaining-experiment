import time
from contextlib import contextmanager

from otree import settings
from otree.api import Bot, Submission, expect

from . import Game, Puzzle, Results, Slider
from .task_sliders import SLIDER_SNAP, snap_value


class PlayerBot(Bot):
    def play_round(self):
        print("Testing slider task")
        yield Submission(Game, check_html=False, timeout_happened=True)
        yield Results


# utils

# `m` stands for method
# `p` for player
# `z` for puzzle
# `r` for response


def get_last_puzzle(p) -> Puzzle | None:
    puzzles = Puzzle.filter(player=p, iteration=p.iteration)
    puzzle = puzzles[-1] if len(puzzles) else None
    return puzzle


def get_slider(z, i):
    return Slider.filter(puzzle=z, idx=i)[0]


def get_value(z, i):
    slider = get_slider(z, i)
    return slider.value


def get_target(z, i):
    slider = Slider.filter(puzzle=z, idx=i)[0]
    return slider.target


def get_progress(p):
    return {
        "total": len(Puzzle.filter(player=p)),
    }


def send(m, p, t, **values):
    data = {"type": t}
    data.update(values)
    return m(p.id_in_group, data)[p.id_in_group]


@contextmanager
def expect_failure(*exceptions):
    try:
        yield
    except exceptions:
        return
    except Exception as e:
        raise AssertionError(
            f"A piece of code was expected to fail with {exceptions} but it failed with {e.__class__}"
        )
    raise AssertionError(
        f"A piece of code was expected to fail with {exceptions} but it didn't"
    )


def expect_progress(p, **values):
    progress = get_progress(p)
    expect(progress, values)


def expect_puzzle(z, **values):
    expect(z, "!=", None)
    for k, v in values.items():
        expect(getattr(z, k), v)


def expect_slider(z, i, expected):
    value = get_value(z, i)
    expect(value, expected)


def expect_response(r, t, **values):
    expect(r["type"], t)
    for k, v in values.items():
        expect(k, "in", r)
        expect(r[k], v)


def expect_response_progress(r, **values):
    expect("progress", "in", r)
    p = r["progress"]
    for k, v in values.items():
        expect(k, "in", p)
        expect(p[k], v)


# test case dispatching


def call_live_method(method, group, case, **kwargs):  # noqa
    player = group.get_players()[0]
    conf = group.session.params

    send(method, player, "load")

    print("  - testing submitting prematurely")
    test_submitting_premature(method, player, conf)

    send(method, player, "new")

    puzzle = get_last_puzzle(player)
    num_correct = 0
    current_slider = 0

    print("  - testing unsuccessful attempt")
    test_unsuccessful_attempt(method, player, puzzle, current_slider, num_correct)
    time.sleep(conf["retry_delay"])

    print("  - testing successful attempt")
    num_correct += 1
    test_successful_attempt(method, player, puzzle, current_slider, num_correct)
    time.sleep(conf["retry_delay"])

    print("  - testing second successful attempt")
    current_slider += 1
    num_correct += 1
    test_successful_attempt(method, player, puzzle, current_slider, num_correct)
    time.sleep(conf["retry_delay"])

    print("  - testing snapping")
    current_slider += 1
    test_snapping(method, player, puzzle, current_slider, num_correct)
    time.sleep(conf["retry_delay"])

    print("  - testing submitting null")
    test_snapping(method, player, puzzle, current_slider, num_correct)
    time.sleep(conf["retry_delay"])

    print("  - testing reloading")
    test_reloading(method, player, puzzle, current_slider, num_correct)
    time.sleep(conf["retry_delay"])

    print("  - testing submitting null")
    test_submitting_null(method, player, puzzle, current_slider, num_correct)
    time.sleep(conf["retry_delay"])

    print("  - testing submitting empty")
    test_submitting_empty(method, player, puzzle, current_slider, num_correct)
    time.sleep(conf["retry_delay"])

    print("  - testing submitting none")
    test_submitting_none(method, player, puzzle, current_slider, num_correct)
    time.sleep(conf["retry_delay"])

    print("  - testing submitting blank")
    test_submitting_blank(method, player, puzzle, current_slider, num_correct)
    time.sleep(conf["retry_delay"])

    print("  - testing submitting too many")
    current_slider += 1
    test_submitting_toomany(method, player, puzzle, current_slider, num_correct, conf)
    time.sleep(conf["retry_delay"])

    print("  - testing submitting too fast")
    current_slider += 1
    test_submitting_toofast(method, player, puzzle, current_slider, num_correct, conf)
    time.sleep(conf["retry_delay"])

    print("  - testing skipping")
    test_skipping(method, player, puzzle, current_slider, num_correct)

    print("  - testing cheating")
    test_cheat_nodebug(method, player)


def test_unsuccessful_attempt(method, player, puzzle, slider, num_correct):
    target = get_target(puzzle, slider)
    value = target + SLIDER_SNAP * 2

    resp = send(method, player, "value", slider=slider, value=value)
    expect_puzzle(puzzle, iteration=1, num_correct=num_correct, is_solved=False)
    expect_slider(puzzle, slider, value)
    expect_response(
        resp,
        "feedback",
        slider=slider,
        value=value,
        is_correct=False,
        is_completed=False,
    )


def test_successful_attempt(method, player, puzzle, slider, num_correct):
    target = get_target(puzzle, slider)
    value = target

    resp = send(method, player, "value", slider=slider, value=value)
    expect_puzzle(puzzle, iteration=1, num_correct=num_correct, is_solved=False)
    expect_slider(puzzle, slider, value)
    expect_response(
        resp,
        "feedback",
        slider=slider,
        value=value,
        is_correct=True,
        is_completed=False,
    )


def test_snapping(method, player, puzzle, slider, num_correct):
    solution0 = get_target(puzzle, slider)
    value = solution0 + 100
    snapped = snap_value(value, solution0)
    send(method, player, "value", slider=slider, value=value)
    expect_slider(puzzle, slider, snapped)


def test_reloading(method, player, puzzle, slider, num_correct):
    resp = send(method, player, "load")
    expect_response(resp, "status")
    new_puzzle = get_last_puzzle(player)
    expect_puzzle(puzzle, iteration=1, num_correct=num_correct)
    for sl in range(slider + 1):
        expect_slider(new_puzzle, sl, get_value(puzzle, sl))


def test_submitting_null(method, player, puzzle, slider, num_correct):
    with expect_failure(TypeError):
        method(player.id_in_group, None)

    expect_puzzle(puzzle, iteration=1, num_correct=num_correct, is_solved=False)


def test_submitting_empty(method, player, puzzle, slider, num_correct):
    with expect_failure(KeyError):
        method(player.id_in_group, {})

    expect_puzzle(puzzle, iteration=1, num_correct=num_correct, is_solved=False)


def test_submitting_none(method, player, puzzle, slider, num_correct):
    with expect_failure(KeyError):
        send(method, player, "value")

    expect_puzzle(
        get_last_puzzle(player), iteration=1, num_correct=num_correct, is_solved=False
    )


def test_submitting_blank(method, player, puzzle, slider, num_correct):
    with expect_failure(ValueError):
        send(method, player, "value", slider=0, value="")

    expect_puzzle(puzzle, iteration=1, num_correct=num_correct, is_solved=False)


def test_submitting_premature(method, player, conf):
    with expect_failure(RuntimeError):
        send(method, player, "value", slider=0, value=100)


def test_submitting_toomany(method, player, puzzle, slider, num_correct, conf):
    retry_delay = conf["retry_delay"]
    target = get_target(puzzle, slider)

    v1 = snap_value(100, target)
    v2 = snap_value(50, target)

    for _ in range(conf["attempts_per_slider"]):
        resp = send(method, player, "value", slider=slider, value=v1)
        expect_response(resp, "feedback")
        expect_slider(puzzle, slider, v1)
        time.sleep(retry_delay)

    with expect_failure(RuntimeError):
        send(method, player, "value", slider=slider, value=v2)

    expect_slider(puzzle, slider, v1)


def test_submitting_toofast(method, player, puzzle, slider, num_correct, conf):
    target = get_target(puzzle, slider)

    v1 = snap_value(100, target)
    v2 = snap_value(50, target)

    resp = send(method, player, "value", slider=slider, value=v1)
    expect_response(resp, "feedback")
    expect_slider(puzzle, slider, v1)

    with expect_failure(RuntimeError):
        send(method, player, "value", slider=slider, value=v2)

    expect_slider(puzzle, slider, v1)


def test_skipping(method, player, puzzle, slider, num_correct):
    with expect_failure(RuntimeError):
        send(method, player, "new")

    expect_puzzle(
        get_last_puzzle(player), iteration=1, num_correct=num_correct, is_solved=False
    )


def test_cheat_nodebug(method, player):
    debug_old = settings.DEBUG
    settings.DEBUG = False

    with expect_failure(RuntimeError):
        send(method, player, "cheat")

    settings.DEBUG = debug_old
