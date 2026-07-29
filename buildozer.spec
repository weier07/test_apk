[app]

title = Моё приложение
package.name = myfirstapp
package.domain = org.student

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,json

version = 0.1

requirements = python3,kivy

orientation = portrait
fullscreen = 0

android.archs = arm64-v8a
android.accept_sdk_license = True

[buildozer]

log_level = 2
warn_on_root = 1
