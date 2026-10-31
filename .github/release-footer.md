
---

## Downloads

| System | File |
| --- | --- |
| Mac with Apple Silicon (M1 and newer) | `pyobd-…-macos-apple-silicon.zip` |
| Mac with Intel processor | `pyobd-…-macos-intel.zip` |
| Windows 10 / 11 | `pyobd-…-windows.zip` |
| Linux (x86_64) | `pyobd-…-linux.tar.gz` |

## Opening the app for the first time

The app isn't signed with a paid certificate yet, so your system will warn you the first time you open it. This only happens once.

**macOS:** unzip the file and move `pyobd.app` to Applications, then try to open it. When macOS says it can't be opened, go to **System Settings → Privacy & Security**, scroll down and click **Open Anyway**.
Or run this once in Terminal:
```bash
xattr -dr com.apple.quarantine /Applications/pyobd.app
```

**Windows:** unzip the file and run `pyobd.exe` inside the `pyobd` folder. If you see "Windows protected your PC", click **More info → Run anyway**. Some antivirus programs wrongly flag apps built with PyInstaller. If yours does, you can [run pyOBD from source](https://github.com/aidan846/pyobd#installation) instead.

**Linux:** extract the file and run `./pyobd/pyobd`. You may need to add your user to the `dialout` group first; see the [README](https://github.com/aidan846/pyobd#linux).
