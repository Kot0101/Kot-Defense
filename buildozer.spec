[app]

# -----------------------------------------------------------------------------
# Kot Defense - Pocket Edition (Android)
# -----------------------------------------------------------------------------
title = Kot Defense
package.name = kotdefense
package.domain = org.kotdefense

source.dir = .
source.include_exts = py,png,jpg,jpeg,ttf,otf,json,mp3,ogg,wav,txt,md
source.exclude_dirs = .git,.github,tools,bin,.buildozer,__pycache__,.idea,.vscode,saves
source.exclude_patterns = _smoke_test.py,compiler.py,start.bat,output_project.md,*.psd,*.pyc

# Версия APK. Меняй при каждой сборке, если ставишь поверх старой.
version = 1.5.0

# pygame-ce на десктопе, но python-for-android собирает upstream pygame
# (рецепт "pygame"). 2.5.2 - ближайшая версия к pygame-ce 2.5.7 по API:
# игра использует только общий API (gfxdraw, smoothscale, BLEND_RGBA_MULT).
# cython обязателен: архив pygame с GitHub не содержит сгенерированных .c
# файлов, и setup.py пытается собрать их на месте. Рецепт cython у p4a
# ставится и в hostpython (install_in_hostpython = True), без него сборка
# падает с "You need cython".
requirements = python3,cython,pygame==2.5.2

icon.filename = %(source.dir)s/Data/textures/icon.png
presplash.filename = %(source.dir)s/Data/textures/loading.png

orientation = landscape
fullscreen = 1

# --- Android ----------------------------------------------------------------
android.api = 34
android.minapi = 24
android.ndk = 25b
android.ndk_api = 24

# arm64-v8a - все телефоны с 2017 года. Если нужна поддержка старых 32-битных
# устройств, допиши сюда armeabi-v7a (сборка станет примерно в 2 раза дольше).
android.archs = arm64-v8a

android.accept_sdk_license = True
android.private_storage = True
android.allow_backup = True

# Игре не нужен интернет и файлы вне приватной папки приложения.
android.permissions =

# Датапаки и сохранения живут в приватной папке приложения (ANDROID_PRIVATE),
# поэтому доступ к внешней памяти не запрашивается.
p4a.bootstrap = sdl2

[buildozer]

log_level = 2
warn_on_root = 0
