[app]

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

# Let Buildozer/p4a use the NDK requested by this project.
# Do not override this from GitHub Actions.
android.ndk = 28c
android.ndk_api = 21

# Build Tools requested by this project.
# DO NOT downgrade this to 33.x.
android.build_tools_version = 37.0.0

android.archs = arm64-v8a,armeabi-v7a


# ============================================================
# ANDROID SDK LICENSE
# ============================================================

# Required for non-interactive GitHub Actions builds.
# This allows Buildozer to accept the Google SDK licenses
# automatically instead of waiting for interactive input.
android.accept_sdk_license = True


# ============================================================
# ANDROID STORAGE / BACKUP
# ============================================================

android.private_storage = True
android.allow_backup = True


# ============================================================
# PYTHON-FOR-ANDROID
# ============================================================

p4a.bootstrap = sdl2


# ============================================================
# ARTIFACTS
# ============================================================

android.debug_artifact = apk
android.release_artifact = aab


# ============================================================
# BUILDOZER
# ============================================================

[buildozer]

log_level = 2
warn_on_root = 0