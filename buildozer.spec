[app]

# ============================================================
# MONEY TRACKER — ANDROID BUILD CONFIGURATION
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

android.build_tools_version = 33.0.2

android.archs = arm64-v8a,armeabi-v7a

android.allow_backup = True


# ============================================================
# PYTHON-FOR-ANDROID
# ============================================================

p4a.branch = stable


# ============================================================
# BACKUP
# ============================================================

android.backup_rules = backup_rules.xml


# ============================================================
# BUILDOZER
# ============================================================

[buildozer]

log_level = 2

warn_on_root = 1
