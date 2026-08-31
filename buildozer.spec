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

# Android

android.api = 33
android.minapi = 21

android.ndk = 25b
android.ndk_api = 21

android.archs = arm64-v8a,armeabi-v7a

android.private_storage = True
android.allow_backup = True

android.accept_sdk_license = True

# Python-for-Android

p4a.bootstrap = sdl2

# Output

android.debug_artifact = apk
android.release_artifact = aab

[buildozer]

log_level = 2
warn_on_root = 0
