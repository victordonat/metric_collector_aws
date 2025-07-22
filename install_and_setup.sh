#!/bin/bash -e

# Requirements: cron, Python and pip with access to:
# boto3, psutil, pytz, python-dotenv

# Variables
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/main.py"
LOG_FILE="$SCRIPT_DIR/cron.log"
SOURCE_PY="$(which python3)"

echo "🐍 Python version: $("$SOURCE_PY" --version)"

# Check if pip is available
if "$SOURCE_PY" -m pip --version > /dev/null 2>&1; then
  echo "📦 Pip is available: $("$SOURCE_PY" -m pip --version)"
else
  echo "❌ pip no está instalado para $SOURCE_PY"
  exit 1
fi

echo "🔧 Installing dependencies..."
"$SOURCE_PY" -m pip install --user boto3 psutil pytz python-dotenv

# Check that the Python script exists
if [ ! -f "$PYTHON_SCRIPT" ]; then
  echo "❌ Python script not found: $PYTHON_SCRIPT"
  exit 1
fi

echo "🕒 Setting up cron to run every 5 minutes..."

# Clean previous entries and add a new one
( (crontab -l 2>/dev/null || true) | grep -v "$PYTHON_SCRIPT" ; echo "*/5 * * * * $SOURCE_PY $PYTHON_SCRIPT > $LOG_FILE 2>&1" ) | crontab -

echo "✅ Done. The script will run every 5 minutes."
