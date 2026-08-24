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

aandroid.api = 33
android.minapi = 21
android.ndk = 25b
android.build_tools_version = 33.0.2
p4a.branch = stable

android.archs = arm64-v8a,armeabi-v7a

[buildozer]
log_level = 2
warn_on_root = 1
