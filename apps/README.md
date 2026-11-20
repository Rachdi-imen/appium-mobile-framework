# apps/

This folder holds the app binaries under test. They are **not versioned** (see `.gitignore`).

## Android

1. Download `mda-2.3.0-27.apk` from the
   [My Demo App releases](https://github.com/saucelabs/my-demo-app-android/releases).
2. Save it here as `android-mydemoapp.apk`.

## iOS

Download the iOS build from the
[My Demo App iOS releases](https://github.com/saucelabs/my-demo-app-ios/releases)
and save it here as `ios-mydemoapp.zip` (local simulator) or upload it to your cloud provider.

The file names above must match `ANDROID_APP_PATH` / `IOS_APP_PATH` in your `.env`.