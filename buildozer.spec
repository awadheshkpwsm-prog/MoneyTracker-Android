[app]

title = Money Tracker

package.name = moneytracker
package.domain = org.moneytracker

source.dir = .

source.include_exts = py,png,jpg,jpeg,kv,json,txt

version = 1.0

requirements = python3,kivy

orientation = portrait

fullscreen = 0

android.api = 33
android.minapi = 21

android.ndk = 25b
android.ndk_api = 21

android.archs = arm64-v8a, armeabi-v7a

android.accept_sdk_license = True

android.private_storage = True

android.allow_backup = True

android.debug_artifact = apk

p4a.bootstrap = sdl2

log_level = 2

[buildozer]

warn_on_root = 0
