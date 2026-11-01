"""Smoke test: run the game headless for a few frames and exit.

Used only during development on PC. Not shipped into the APK.

    python _smoke_test.py

It uses SDL dummy video/audio drivers, fakes a mouse click so the loading
screen closes, counts rendered frames and exits with code 0 after 90 frames.
"""

import os
import sys
import time

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.chdir(HERE)

import pygame  # noqa: E402

_real_get_pressed = pygame.mouse.get_pressed
_t0 = time.time()

# The loading screen waits for a click; after one second we "hold the mouse".
pygame.mouse.get_pressed = lambda *a, **k: (
    (1, 0, 0) if time.time() - _t0 > 1.0 else _real_get_pressed(*a, **k)
)

import config  # noqa: E402

_frames = [0]
_last_report = [0.0]


def counting_present():
    _frames[0] += 1
    config.display.present()
    if _frames[0] in (1, 2, 5, 10, 30, 60):
        print(f"[smoke] frame {_frames[0]} ok", flush=True)
    if _frames[0] >= 90:
        print(f"[smoke] PASS: {_frames[0]} frames rendered", flush=True)
        os._exit(0)


config.present = counting_present

print(
    f"[smoke] android={config.IS_ANDROID} base={config.BASE_DIR} "
    f"window={config.display.window.get_size()} logical={config.display.logical.get_size()} "
    f"scale={config.display.scale:.3f} offset={config.display.offset}",
    flush=True,
)

try:
    import main  # noqa: E402,F401
except SystemExit:
    print("[smoke] exit via SystemExit", flush=True)
    raise
