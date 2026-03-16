# google-workspace-cli

Single-file Google Workspace API client. Zero dependencies. Python 3.7+.

49 commands covering Calendar, Sheets, Drive, Gmail, Docs, Contacts, and Tasks.

**Platform:** Developed and tested on macOS. Works on Linux. Windows users may need to adapt credential file permissions (see [Windows Notes](#windows-notes)).

## Install

Paste this into Claude Code:

```
Install the google-workspace-cli skill: download https://raw.githubusercontent.com/tolmme/google-workspace-cli/main/install.py and run it with my email: YOUR_EMAIL
```

Or manually:

```bash
# macOS / Linux
python3 <(curl -s https://raw.githubusercontent.com/tolmme/google-workspace-cli/main/install.py) YOUR_EMAIL

# Windows (PowerShell)
curl -o install.py https://raw.githubusercontent.com/tolmme/google-workspace-cli/main/install.py; python install.py YOUR_EMAIL; del install.py
```

The installer downloads `gw.py`, creates the Claude Code skill, and prompts you to set up Google Cloud credentials.

## Google Cloud Setup (one-time, ~5 minutes)

You need to create an OAuth app in Google Cloud Console to get a Client ID and Client Secret.

### Step 1: Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click the project dropdown (top bar) > **New Project**
3. Name it anything (e.g. "Workspace CLI") > **Create**
4. Make sure the new project is selected in the dropdown

### Step 2: Enable APIs

Go to **APIs & Services > Library** and enable these APIs (click each, then "Enable"):

- Google Calendar API
- Google Sheets API
- Google Drive API
- Gmail API
- Google Docs API
- People API (for Contacts)
- Tasks API

Or use gcloud CLI:

```bash
gcloud services enable calendar-json.googleapis.com sheets.googleapis.com drive.googleapis.com gmail.googleapis.com docs.googleapis.com people.googleapis.com tasks.googleapis.com
```

### Step 3: Configure OAuth Consent Screen

1. Go to **APIs & Services > OAuth consent screen**
2. Select **External** > **Create**
3. Fill in:
   - App name: anything (e.g. "My Workspace CLI")
   - User support email: your email
   - Developer contact email: your email
4. Click **Save and Continue**
5. **Scopes** page: click **Add or remove scopes**, add these:
   - `https://www.googleapis.com/auth/calendar`
   - `https://www.googleapis.com/auth/drive`
   - `https://www.googleapis.com/auth/gmail.modify`
   - `https://www.googleapis.com/auth/gmail.send`
   - `https://www.googleapis.com/auth/spreadsheets`
   - `https://www.googleapis.com/auth/documents`
   - `https://www.googleapis.com/auth/contacts`
   - `https://www.googleapis.com/auth/tasks`

   (Or just check "Select all" — the app only uses what it needs)
6. Click **Save and Continue**
7. **Test users** page: click **Add users** and add your Gmail address
8. **Save and Continue** > **Back to Dashboard**

### Step 4: Create OAuth Client ID

1. Go to **APIs & Services > Credentials**
2. Click **Create Credentials > OAuth client ID**
3. Application type: **Web application**
4. Name: anything
5. Under **Authorized redirect URIs**, add: `http://localhost:8000/oauth2callback`
6. Click **Create**
7. Copy the **Client ID** and **Client Secret**

### Step 5: Save Credentials

Create the env file:

```bash
# macOS / Linux
cat > ~/.google-workspace-cli.env << 'EOF'
GOOGLE_OAUTH_CLIENT_ID=your-client-id-here.apps.googleusercontent.com
GOOGLE_OAUTH_CLIENT_SECRET=your-client-secret-here
DEFAULT_EMAIL=you@gmail.com
DEFAULT_TIMEZONE=America/New_York
EOF
chmod 600 ~/.google-workspace-cli.env
```

```powershell
# Windows (PowerShell)
$dir = "$env:APPDATA\google-workspace-cli"
New-Item -ItemType Directory -Force -Path $dir | Out-Null
@"
GOOGLE_OAUTH_CLIENT_ID=your-client-id-here.apps.googleusercontent.com
GOOGLE_OAUTH_CLIENT_SECRET=your-client-secret-here
DEFAULT_EMAIL=you@gmail.com
DEFAULT_TIMEZONE=America/New_York
"@ | Set-Content "$dir\.env"
```

### Step 6: Authorize

```bash
python3 gw.py auth you@gmail.com
```

This opens your browser. Sign in with your Google account and grant access. The OAuth token is saved locally and auto-refreshes.

### Adding Test Users

While your app is in "Testing" mode (not published), only users listed as test users can authorize. To add team members:

1. Go to **APIs & Services > OAuth consent screen**
2. Scroll to **Test users** > **Add users**
3. Enter their Gmail addresses
4. They can now use the same Client ID/Secret (share the env file)

To remove the test user limit, publish the app (Google may require verification for sensitive scopes like Gmail).

## Usage

```bash
python3 gw.py <command> '<json_args>'

# List upcoming calendar events
python3 gw.py cal_events '{"time_min":"2026-03-01T00:00:00Z","time_max":"2026-03-31T00:00:00Z"}'

# Create a calendar event
python3 gw.py cal_create '{"summary":"Team sync","start_time":"2026-03-20T10:00:00+03:00","end_time":"2026-03-20T11:00:00+03:00"}'

# Read a spreadsheet
python3 gw.py sheets_read '{"spreadsheet_id":"YOUR_ID","range":"Sheet1!A1:Z50"}'

# Search Gmail
python3 gw.py gmail_search '{"query":"from:boss@company.com is:unread"}'

# Search Drive
python3 gw.py drive_search '{"query":"name contains '\''report'\''"}'

# Use stdin for complex JSON
python3 gw.py sheets_write - <<'ARGS'
{"spreadsheet_id":"ID","range":"Sheet1!A1","values":[["Name","Score"],["Alice",95],["Bob",87]]}
ARGS
```

### Multiple Accounts

Pass `email` in the JSON args to use a different account:

```bash
python3 gw.py cal_events '{"email":"work@company.com","time_min":"2026-03-01T00:00:00Z"}'
```

Each account needs to be authorized once (`gw.py auth work@company.com`).

## All 49 Commands

**Calendar (8):** `cal_list`, `cal_events`, `cal_create`, `cal_update`, `cal_delete`, `cal_get`, `cal_quick_add`, `cal_freebusy`

**Sheets (11):** `sheets_read`, `sheets_write`, `sheets_append`, `sheets_info`, `sheets_list`, `sheets_create`, `sheets_add_sheet`, `sheets_delete_sheet`, `sheets_clear`, `sheets_batch_read`, `sheets_format`

**Drive (9):** `drive_list`, `drive_search`, `drive_get`, `drive_create_folder`, `drive_copy`, `drive_delete`, `drive_move`, `drive_share`, `drive_get_meta`

**Gmail (9):** `gmail_search`, `gmail_get`, `gmail_send`, `gmail_draft`, `gmail_labels`, `gmail_reply`, `gmail_modify`, `gmail_delete`, `gmail_thread`

**Docs (3):** `docs_get`, `docs_create`, `docs_append`

**Contacts (3):** `contacts_list`, `contacts_search`, `contacts_create`

**Tasks (6):** `tasks_lists`, `tasks_list`, `tasks_get`, `tasks_create`, `tasks_complete`, `tasks_delete`

Run `python3 gw.py --help` for the full list with descriptions.

## Parameter Reference

### Calendar

| Tool | Required | Optional |
|------|----------|----------|
| `cal_list` | -- | -- |
| `cal_events` | -- | `time_min`, `time_max` (RFC3339), `calendar_id`, `max_results`, `q` |
| `cal_create` | `summary`, `start_time`, `end_time` | `description`, `location`, `timezone`, `calendar_id`, `attendees` |
| `cal_update` | `event_id` | `summary`, `start_time`, `end_time`, `description`, `location`, `timezone`, `calendar_id` |
| `cal_delete` | `event_id` | `calendar_id` |
| `cal_get` | `event_id` | `calendar_id` |
| `cal_quick_add` | `text` | `calendar_id` |
| `cal_freebusy` | `time_min`, `time_max` | `calendar_ids` (list) |

Time format: `2026-03-10T15:00:00+03:00` (RFC3339 with timezone offset).

### Sheets

| Tool | Required | Optional |
|------|----------|----------|
| `sheets_read` | `spreadsheet_id`, `range` | -- |
| `sheets_write` | `spreadsheet_id`, `range`, `values` (2D array) | `input_option` (USER_ENTERED/RAW) |
| `sheets_append` | `spreadsheet_id`, `range`, `values` | `input_option` |
| `sheets_info` | `spreadsheet_id` | -- |
| `sheets_list` | -- | `max_results` |
| `sheets_create` | `title` | `sheets` (list of tab names) |
| `sheets_add_sheet` | `spreadsheet_id`, `title` | -- |
| `sheets_delete_sheet` | `spreadsheet_id`, `sheet_id` (numeric) | -- |
| `sheets_clear` | `spreadsheet_id`, `range` | -- |
| `sheets_batch_read` | `spreadsheet_id`, `ranges` (list) | -- |
| `sheets_format` | `spreadsheet_id`, `requests` (batchUpdate array) | -- |

### Drive

| Tool | Required | Optional |
|------|----------|----------|
| `drive_list` | -- | `query`, `max_results` |
| `drive_search` | `query` | `max_results` |
| `drive_get` | `file_id` | `export_as` (mime type) |
| `drive_create_folder` | `name` | `parent_id` |
| `drive_copy` | `file_id` | `name`, `parent_id` |
| `drive_delete` | `file_id` | -- |
| `drive_move` | `file_id`, `parent_id` | -- |
| `drive_share` | `file_id` | `type`, `role`, `email`, `notify` |
| `drive_get_meta` | `file_id` | `fields` |

### Gmail

| Tool | Required | Optional |
|------|----------|----------|
| `gmail_search` | `query` | `max_results` |
| `gmail_get` | `message_id` | -- |
| `gmail_send` | `to`, `subject`, `body` | `from`, `cc` |
| `gmail_draft` | `to`, `subject`, `body` | `from` |
| `gmail_labels` | -- | -- |
| `gmail_reply` | `message_id`, `body` | `to` |
| `gmail_modify` | `message_id` | `add_labels`, `remove_labels` |
| `gmail_delete` | `message_id` | -- |
| `gmail_thread` | `thread_id` | -- |

### Docs

| Tool | Required | Optional |
|------|----------|----------|
| `docs_get` | `document_id` | -- |
| `docs_create` | `title` | -- |
| `docs_append` | `document_id`, `text` | -- |

### Contacts

| Tool | Required | Optional |
|------|----------|----------|
| `contacts_list` | -- | `max_results`, `fields` |
| `contacts_search` | `query` | `fields` |
| `contacts_create` | -- | `name`, `first_name`, `last_name`, `email`, `phone` |

### Tasks

| Tool | Required | Optional |
|------|----------|----------|
| `tasks_lists` | -- | -- |
| `tasks_list` | -- | `list_id`, `max_results`, `show_completed`, `show_hidden` |
| `tasks_get` | `task_id` | `list_id` |
| `tasks_create` | `title` | `list_id`, `notes`, `due` (RFC3339) |
| `tasks_complete` | `task_id` | `list_id` |
| `tasks_delete` | `task_id` | `list_id` |

## Windows Notes

The script is developed on macOS but should work on Windows with these caveats:

- **File permissions:** On macOS/Linux, credential files are set to `chmod 600` (owner-only). Windows doesn't support Unix permissions — credentials are stored as regular files. Keep your `%APPDATA%\google-workspace-cli\` directory secure.
- **Config paths:** On Windows, config is stored in `%APPDATA%\google-workspace-cli\` instead of `~/.google-workspace-cli/`.
- **OAuth callback:** The localhost:8000 callback server works on Windows. Make sure no firewall blocks it.

## Auth Details

- Tokens stored in `~/.google-workspace-cli/credentials/<email>.json` (or `%APPDATA%` on Windows)
- Auto-refresh: tokens refresh silently before expiry (5 min buffer)
- Auto-auth: if no token or refresh fails, browser opens for OAuth
- Manual re-auth: `gw.py auth <email>`
- Multiple accounts: each email gets its own token file

## License

MIT
