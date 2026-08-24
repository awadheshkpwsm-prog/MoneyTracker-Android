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


# ---------------------------------------------------------
# ANDROID
# ---------------------------------------------------------

android.api = 33

android.minapi = 21

android.ndk = 25b

android.build_tools_version = 33.0.2

android.archs = arm64-v8a,armeabi-v7a

android.permissions = INTERNET

android.allow_backup = True

android.backup_rules = backup_rules.xml


# ---------------------------------------------------------
# PYTHON-FOR-ANDROID
# ---------------------------------------------------------

p4a.fork = kivy

p4a.branch = develop


# ---------------------------------------------------------
# BUILD
# ---------------------------------------------------------

[buildozer]

log_level = 2

warn_on_root = 0

On Tue, Aug 25, 2026, 4:32 AM Pandey G Official <awadheshkpwsm@gmail.com> wrote:
name: Build Android APK

on:
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-22.04

    env:
      ANDROID_HOME: ${{ github.workspace }}/android-sdk
      ANDROID_SDK_ROOT: ${{ github.workspace }}/android-sdk
      BUILDOZER_WARN_ON_ROOT: "0"

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Java
        uses: actions/setup-java@v4
        with:
          distribution: temurin
          java-version: "17"

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install Linux Dependencies
        run: |
          sudo apt-get update
          sudo apt-get install -y \
            git \
            zip \
            unzip \
            autoconf \
            automake \
            libtool \
            pkg-config \
            zlib1g-dev \
            libffi-dev \
            libssl-dev \
            cmake

      - name: Setup Android SDK
        uses: android-actions/setup-android@v3

      - name: Configure Android SDK
        run: |
          mkdir -p "$ANDROID_HOME/cmdline-tools/latest"

          echo "ANDROID_HOME=$ANDROID_HOME"
          echo "ANDROID_SDK_ROOT=$ANDROID_SDK_ROOT"

          yes | sdkmanager --sdk_root="$ANDROID_HOME" --licenses || true

      - name: Install Required Android SDK
        run: |
          sdkmanager --sdk_root="$ANDROID_HOME" \
            "platform-tools" \
            "platforms;android-33" \
            "build-tools;33.0.2"

      - name: Verify Android SDK
        run: |
          echo "Installed platforms:"
          ls -la "$ANDROID_HOME/platforms" || true

          echo "Installed build-tools:"
          ls -la "$ANDROID_HOME/build-tools" || true

          echo "SDK packages:"
          sdkmanager --sdk_root="$ANDROID_HOME" --list_installed || true

          echo "AIDL:"
          "$ANDROID_HOME/build-tools/33.0.2/aidl" --version

      - name: Install Python Dependencies
        run: |
          python -m pip install --upgrade pip setuptools wheel
          pip install "Cython<3"
          pip install buildozer==1.5.0

      - name: Clean Build Cache
        run: |
          rm -rf .buildozer
          rm -rf bin

      - name: Accept Android Licenses
        run: |
          mkdir -p ~/.android
          touch ~/.android/repositories.cfg

          yes | sdkmanager \
            --sdk_root="$ANDROID_HOME" \
            --licenses || true

      - name: Build APK
        run: |
          buildozer -v android debug

      - name: Show Build Output
        if: always()
        run: |
          echo "===== BIN DIRECTORY ====="
          ls -lah bin || true

      - name: Upload APK
        uses: actions/upload-artifact@v4
        with:
          name: MoneyTracker-APK
          path: bin/*.apk
          if-no-files-found: error
