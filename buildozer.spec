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
android.api = 33
android.minapi = 21
android.ndk = 25b
android.build_tools_version = 33.0.2
android.gradle_dependencies =
p4a.branch = master
android.archs = arm64-v8a,armeabi-v7a
android.allow_backup = True
android.backup_rules = backup_rules.xml

[buildozer]
log_level = 2
warn_on_root = 1

[android]
android.permissions = INTERNET

[buildozer:android]
# Build with: buildozer -v android debug
