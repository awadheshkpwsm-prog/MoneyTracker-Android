[app]

# ============================================================
# APPLICATION
# ============================================================

title = Money Tracker

package.name = moneytracker

package.domain = org.moneytracker

source.dir = .

source.include_exts = py,json,txt,png,jpg,kv

version = 1.0.0

requirements = python3,kivy

orientation = portrait

fullscreen = 0


# ============================================================
# ANDROID
# ============================================================

android.api = 33

android.minapi = 21

android.ndk = 28c

android.ndk_api = 21

android.build_tools_version = 33.0.2

android.archs = arm64-v8a,armeabi-v7a


# ============================================================
# USE RUNNER'S EXISTING ANDROID SDK
#
# IMPORTANT:
# Do NOT let Buildozer download another SDK.
# ============================================================

android.sdk_path = /usr/local/lib/android/sdk

android.ndk_path = /usr/local/lib/android/sdk/ndk/28.2.13676358

android.skip_update = True


# ============================================================
# ANDROID STORAGE / BACKUP
# ============================================================

android.private_storage = True

android.allow_backup = True


# ============================================================
# PYTHON-FOR-ANDROID
# ============================================================

p4a.fork = kivy

p4a.branch = master

p4a.bootstrap = sdl2


# ============================================================
# DEBUG / RELEASE ARTIFACT
# ============================================================

android.debug_artifact = apk

android.release_artifact = aab


# ============================================================
# BUILDOZER
# ============================================================

[buildozer]

log_level = 2

warn_on_root = 1
