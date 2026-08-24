# Money Tracker — Android APK Build Project

This project uses the saved modular Money Tracker backend as `mt/` and adds a Kivy Android UI in `main.py`.

## Google Colab build

1. Upload this ZIP to Colab and extract it.
2. Run:

```bash
!apt-get update -qq
!apt-get install -y -qq git zip unzip openjdk-17-jdk autoconf automake libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev cmake libffi-dev libssl-dev
!pip install -q buildozer cython==0.29.37
%cd MoneyTracker_Android
!buildozer -v android debug
```

3. The APK will be in `bin/`.

## Important

The original modular Python project is kept under `mt/`. The Android adapter only changes the data path so JSON data is stored in Android's writable app data directory.
