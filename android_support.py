"""
android_support.py - Pocket Edition platform layer.

The game itself stays the same on Windows and on Android
(python-for-android + pygame-ce / SDL2). This module hides the differences:

  * where the game files live (CWD / Data folder);
  * how the window is created (fixed 1400x800 vs. a fullscreen phone display);
  * how frames are presented (letterboxed scaling + flip);
  * how touch coordinates are converted back to the logical 1400x800 space;
  * what to do with desktop-only things (mouse cursors, Discord RPC).

Nothing here is imported by the game directly - config.py pulls it in.
"""

import os
import sys

# --------------------------------------------------------------------------
# Platform detection
# --------------------------------------------------------------------------

IS_ANDROID = bool(
    os.environ.get("ANDROID_ARGUMENT")
    or os.environ.get("ANDROID_PRIVATE")
    or os.environ.get("ANDROID_APP_PATH")
)

IS_DESKTOP = not IS_ANDROID


def _app_dir():
    """Directory that holds main.py and the Data folder.

    На Android p4a задаёт несколько переменных, и они означают РАЗНОЕ:
      ANDROID_ARGUMENT - папка приложения (там main.py и Data)  <- то, что нужно
      ANDROID_PRIVATE  - родительская приватная папка (".../files")
    Поэтому сначала ищем ту, в которой реально лежит Data, иначе легко получить
    ".../files/Data" вместо ".../files/app/Data".
    """
    if IS_ANDROID:
        keys = ("ANDROID_ARGUMENT", "ANDROID_UNPACK", "ANDROID_APP_PATH", "ANDROID_PRIVATE")

        for key in keys:
            value = os.environ.get(key)
            if value and os.path.isdir(os.path.join(value, "Data")):
                return value

        for key in keys:
            value = os.environ.get(key)
            if value and os.path.isdir(value):
                return value

        # Последний шанс: папка, в которой лежит этот файл.
        here = os.path.dirname(os.path.abspath(__file__))
        if os.path.isdir(os.path.join(here, "Data")):
            return here

    return os.path.dirname(os.path.abspath(__file__))


BASE_DIR = _app_dir()
DATA_DIR = os.path.join(BASE_DIR, "Data")
SAVE_DIR = os.path.join(BASE_DIR, "saves")


def res(*parts):
    """Absolute path inside the game folder: res("Data", "font", "a.ttf")."""
    return os.path.join(BASE_DIR, *parts)


def ensure_workdir():
    """Make sure relative paths ("Data/font/x.ttf") resolve on Android too."""
    try:
        os.chdir(BASE_DIR)
    except OSError:
        pass


def ensure_save_dir():
    try:
        os.makedirs(SAVE_DIR, exist_ok=True)
        return SAVE_DIR
    except OSError:
        return BASE_DIR


# --------------------------------------------------------------------------
# Display: logical 1400x800 surface + real window, with letterboxing
# --------------------------------------------------------------------------

class Display:
    def __init__(self):
        self.window = None
        self.logical = None
        self.scale = 1.0
        self.offset = (0, 0)
        self._scaled = None
        self._scaled_size = None
        self._patched = False

    # -- setup -------------------------------------------------------------
    def init(self, width, height, title="Kot Defense", icon_path=None):
        import pygame

        pygame.display.set_caption(title)

        self.scaled_by_sdl = False

        if IS_ANDROID:
            os.environ.setdefault("SDL_VIDEO_MINIMIZE_ON_FOCUS_LOSS", "0")

            # Идеальный вариант для телефона: SDL сам растягивает кадр 1400x800
            # под экран средствами GPU (pygame.SCALED). Тогда не нужно каждый
            # кадр гонять transform.scale на CPU - это стоило нам 20 мс/кадр.
            try:
                self.window = pygame.display.set_mode(
                    (width, height), pygame.FULLSCREEN | pygame.SCALED, depth=16
                )
                self.logical = self.window
                self.scaled_by_sdl = True
                self.scale = 1.0
                self.offset = (0, 0)
                print(f"[display] SDL SCALED {self.window.get_size()} depth={self.window.get_bitsize()}")
            except Exception as error:
                print(f"[display] SCALED failed ({error}), falling back")

        if not self.scaled_by_sdl:
            win_w, win_h = width, height
            flags = 0
            if IS_ANDROID:
                try:
                    info = pygame.display.Info()
                    if info.current_w > 0 and info.current_h > 0:
                        win_w, win_h = info.current_w, info.current_h
                except Exception:
                    pass
                flags = pygame.FULLSCREEN

            self.window = self._set_mode((win_w, win_h), flags)
            self.logical = pygame.Surface((width, height)).convert()
            self.scale = 1.0
            self.offset = (0, 0)
            self._update_geometry()
            print(f"[display] software scale {self.window.get_size()} -> {(width, height)}")

        if icon_path:
            try:
                pygame.display.set_icon(pygame.image.load(icon_path).convert_alpha())
            except Exception:
                pass

        return self.window, self.logical

    def _set_mode(self, size, flags):
        import pygame

        # vsync is nice on desktop and unsupported / ignored on some Android builds.
        for kwargs in ({"vsync": 1}, {}):
            try:
                return pygame.display.set_mode(size, flags, **kwargs)
            except Exception:
                continue
        return pygame.display.set_mode(size, flags)

    # -- geometry ----------------------------------------------------------
    def _update_geometry(self):
        if self.window is None or self.logical is None:
            return
        win_w, win_h = self.window.get_size()
        lw, lh = self.logical.get_size()
        if win_w <= 0 or win_h <= 0:
            self.scale = 1.0
            self.offset = (0, 0)
            return
        self.scale = min(win_w / lw, win_h / lh)
        if abs(self.scale - 1.0) < 1e-3:
            self.scale = 1.0
            self.offset = (0, 0)
        else:
            nw = int(lw * self.scale + 0.5)
            nh = int(lh * self.scale + 0.5)
            self.offset = ((win_w - nw) // 2, (win_h - nh) // 2)

    def to_logical(self, pos):
        """Window pixel coordinates -> logical 1400x800 coordinates."""
        if self.scale == 1.0 and self.offset == (0, 0):
            return pos
        x = (pos[0] - self.offset[0]) / self.scale
        y = (pos[1] - self.offset[1]) / self.scale
        return (x, y)

    # -- frame -------------------------------------------------------------
    def present(self):
        import pygame

        # В режиме SDL SCALED кадр уже является экранной поверхностью:
        # масштабированием занимается GPU, нам остаётся только flip.
        if self.scaled_by_sdl:
            pygame.display.flip()
            return

        self._update_geometry()
        win_w, win_h = self.window.get_size()
        lw, lh = self.logical.get_size()

        if self.scale == 1.0 and self.offset == (0, 0):
            self.window.blit(self.logical, (0, 0))
        else:
            nw, nh = int(lw * self.scale + 0.5), int(lh * self.scale + 0.5)
            if self._scaled_size != (nw, nh):
                self._scaled = pygame.Surface((nw, nh)).convert()
                self._scaled_size = (nw, nh)
            pygame.transform.scale(self.logical, (nw, nh), self._scaled)
            if self.offset[0] or self.offset[1]:
                self.window.fill((0, 0, 0))
            self.window.blit(self._scaled, self.offset)

        pygame.display.flip()

    # -- input -------------------------------------------------------------
    def install_event_translation(self):
        """Rewrite mouse positions of every event into logical coordinates."""
        import pygame

        if self._patched:
            return
        self._patched = True
        original_get = pygame.event.get
        display = self

        mouse_types = (
            pygame.MOUSEMOTION,
            pygame.MOUSEBUTTONDOWN,
            pygame.MOUSEBUTTONUP,
        )

        def get(*args, **kwargs):
            events = original_get(*args, **kwargs)
            if display.scale == 1.0 and display.offset == (0, 0):
                return events
            result = []
            for event in events:
                if event.type in mouse_types and getattr(event, "pos", None) is not None:
                    data = dict(getattr(event, "dict", {}) or {})
                    data["pos"] = display.to_logical(event.pos)
                    result.append(pygame.event.Event(event.type, data))
                else:
                    result.append(event)
            return result

        pygame.event.get = get


# --------------------------------------------------------------------------
# Desktop-only features
# --------------------------------------------------------------------------

def install_cursor_guard():
    """Android has no OS cursors: turn pygame.mouse.set_cursor into a no-op."""
    if not IS_ANDROID:
        return
    import pygame

    pygame.mouse.set_cursor = lambda *args, **kwargs: None
    pygame.mouse.set_visible = lambda *args, **kwargs: None


def install_quit_on_back_button():
    """Android back button arrives as a key/quit event; keep pygame alive."""
    if not IS_ANDROID:
        return
    try:
        os.environ.setdefault("SDL_ANDROID_BLOCK_ON_PAUSE", "1")
    except Exception:
        pass


SIZE_HINT = (1400, 800)
