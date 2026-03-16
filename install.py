#!/usr/bin/env python3
"""One-command installer for google-workspace-cli Claude Code skill.

Usage:
    python3 install.py YOUR_EMAIL
    python3 install.py YOUR_EMAIL --client-id ID --client-secret SECRET
"""

import os, sys, platform, urllib.request

GW_PY_URL = "https://raw.githubusercontent.com/tolmme/google-workspace-cli/main/gw.py"

def home():
    return os.path.expanduser("~")

def skill_dir():
    return os.path.join(home(), ".claude", "skills", "google-workspace")

def scripts_dir():
    return os.path.join(skill_dir(), "scripts")

def gw_py_path():
    return os.path.join(scripts_dir(), "gw.py")

def config_dir():
    if platform.system() == "Windows":
        base = os.environ.get("APPDATA", home())
        return os.path.join(base, "google-workspace-cli")
    return os.path.join(home(), ".google-workspace-cli")

def env_file_path():
    if platform.system() == "Windows":
        return os.path.join(config_dir(), ".env")
    return os.path.join(home(), ".google-workspace-cli.env")

def download_gw_py():
    d = scripts_dir()
    os.makedirs(d, exist_ok=True)
    path = gw_py_path()
    print(f"  Downloading gw.py ...")
    urllib.request.urlretrieve(GW_PY_URL, path)
    if platform.system() != "Windows":
        os.chmod(path, 0o755)
    print(f"  Saved to {path}")

def create_skill_md(email):
    path = os.path.join(skill_dir(), "SKILL.md")
    py = gw_py_path().replace("\\", "/")
    content = f"""---
name: google-workspace
description: "Google Workspace API: Calendar, Sheets, Drive, Gmail, Docs, Contacts, Tasks. Use for ANY Google service task."
allowed-tools: Bash(python3 {py} *)
---

# Google Workspace

Direct Google REST API calls. Zero dependencies.

## Calling pattern

```bash
python3 {py} <command> '{{"email":"{email}", ...}}'
python3 {py} cal_events '{{"time_min":"2026-01-01T00:00:00Z","time_max":"2026-12-31T00:00:00Z"}}'
```

Default email: `{email}` (omit `email` param to use default).

All {49} tools: `python3 {py} --help`
"""
    with open(path, "w") as f:
        f.write(content)
    print(f"  Skill created at {path}")

def create_env_file(email, client_id=None, client_secret=None):
    path = env_file_path()
    if os.path.exists(path):
        print(f"  Env file already exists at {path} — skipping")
        return

    os.makedirs(os.path.dirname(path) if os.path.dirname(path) else ".", exist_ok=True)

    cid = client_id or "PASTE_YOUR_CLIENT_ID_HERE"
    cs = client_secret or "PASTE_YOUR_CLIENT_SECRET_HERE"

    with open(path, "w") as f:
        f.write(f"GOOGLE_OAUTH_CLIENT_ID={cid}\n")
        f.write(f"GOOGLE_OAUTH_CLIENT_SECRET={cs}\n")
        f.write(f"DEFAULT_EMAIL={email}\n")
        f.write(f"DEFAULT_TIMEZONE=UTC\n")

    if platform.system() != "Windows":
        try:
            os.chmod(path, 0o600)
        except OSError:
            pass

    if client_id and client_secret:
        print(f"  Credentials saved to {path}")
    else:
        print(f"  Template created at {path}")
        print(f"  >>> EDIT THIS FILE and paste your Google OAuth Client ID & Secret <<<")

def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print("Usage: python3 install.py YOUR_EMAIL [--client-id ID --client-secret SECRET]")
        print()
        print("Installs google-workspace-cli as a Claude Code skill:")
        print("  1. Downloads gw.py")
        print("  2. Creates Claude Code skill definition")
        print("  3. Creates env file template for Google OAuth credentials")
        print()
        print("After install, follow the README to set up Google Cloud OAuth:")
        print("  https://github.com/tolmme/google-workspace-cli#google-cloud-setup-one-time-5-minutes")
        sys.exit(0)

    email = sys.argv[1]

    client_id = None
    client_secret = None
    if "--client-id" in sys.argv:
        idx = sys.argv.index("--client-id")
        if idx + 1 < len(sys.argv):
            client_id = sys.argv[idx + 1]
    if "--client-secret" in sys.argv:
        idx = sys.argv.index("--client-secret")
        if idx + 1 < len(sys.argv):
            client_secret = sys.argv[idx + 1]

    print("Installing google-workspace-cli skill...")
    print()

    download_gw_py()
    create_skill_md(email)
    create_env_file(email, client_id, client_secret)

    print()
    if client_id and client_secret:
        print("Done! Run this to authorize:")
        print(f"  python3 {gw_py_path()} auth {email}")
    else:
        print("Almost done! Next steps:")
        print(f"  1. Set up Google Cloud OAuth (see README)")
        print(f"  2. Edit {env_file_path()} with your Client ID & Secret")
        print(f"  3. Run: python3 {gw_py_path()} auth {email}")
    print()
    print("Then restart Claude Code to pick up the new skill.")

if __name__ == "__main__":
    main()
