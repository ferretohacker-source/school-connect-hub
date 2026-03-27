"""Create a Windows startup .bat file so Ferreto starts at login."""

from pathlib import Path
import os
import sys


BAT_TEMPLATE = """@echo off
cd /d "{project_dir}"
"{python_exe}" "{project_dir}\\main.py"
"""


def main() -> None:
    appdata = os.environ.get("APPDATA")
    if not appdata:
        print("This script is intended for Windows with APPDATA available.")
        sys.exit(1)

    startup_dir = Path(appdata) / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup"
    startup_dir.mkdir(parents=True, exist_ok=True)

    project_dir = Path(__file__).resolve().parent
    bat_path = startup_dir / "FerretoAIStartup.bat"

    content = BAT_TEMPLATE.format(project_dir=str(project_dir), python_exe=sys.executable)
    bat_path.write_text(content, encoding="utf-8")

    print(f"Startup file created: {bat_path}")


if __name__ == "__main__":
    main()
