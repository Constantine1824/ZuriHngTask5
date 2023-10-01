#!/usr/bin/env bash
# exit on error
set -o errexit

pip install --upgrade pip
pip install --upgrade setuptools wheel

poetry install

# Create a temporary crontab file
CRONTAB_FILE=$(mktemp)

# Add the cron job to the temporary crontab file
echo "*/2 * * * * /usr/bin/python3 tasks.py" >> "$CRONTAB_FILE"

# Install the temporary crontab file
crontab "$CRONTAB_FILE"

# Clean up the temporary crontab file
rm "$CRONTAB_FILE"

echo "Cron job to run $PYTHON_SCRIPT every two minutes has been set up."

python manage.py collectstatic --no-input
