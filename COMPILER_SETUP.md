# Compiler Installation Guide

The Coding Challenge module allows you to execute code in various languages. However, since the code runs locally on your machine, you must have the necessary compilers installed.

## Current Status of Your System

| Language | Requirement | Status |
| :--- | :--- | :--- |
| **Python** | Python 3 | ✅ Installed |
| **JavaScript** | Node.js | ✅ Installed |
| **Java** | JDK (javac) | ✅ Installed |
| **C / C++** | GCC (MinGW) | ❌ **Missing** |

## How to Install GCC (for C and C++)

To run C or C++ code, you need to install GCC. The easiest way on Windows is via **WinLibs** or **TDM-GCC**.

### Option 1: WinLibs (Recommended)
1.  Download the **Zip** archive from [winlibs.com](https://winlibs.com/). (Look for "UCRT runtime" version).
2.  Extract the zip file to `C:\MinGW`.
3.  Add `C:\MinGW\bin` to your **System Path**:
    *   Press `Win` key, type "env", and select **Edit the system environment variables**.
    *   Click **Environment Variables**.
    *   Under "System variables", find **Path** and click **Edit**.
    *   Click **New** and paste `C:\MinGW\bin`.
    *   Click **OK** on all dialogs.
4.  Restart your terminal/command prompt.

### Option 2: TDM-GCC (Installer)
1.  Download the [TDM-GCC Installer](https://jmeubank.github.io/tdm-gcc/).
2.  Run the installer and follow the prompts.
3.  Ensure "Add to Path" is checked.
4.  Restart your terminal.

## Verification
After installing, run this command in a new terminal to verify:
```powershell
gcc --version
```
If successful, the Coding Challenge page will automatically be able to run C and C++ code.
