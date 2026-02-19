#!/bin/bash
# Creates a portable backup ZIP of the HR Chatbot project (excludes venv, chroma_db)
# Run from inside hr-chatbot folder: bash create_backup.sh

cd "$(dirname "$0")"
BACKUP_NAME="HRChatBot-backup-$(date +%Y%m%d).zip"
zip -r "$BACKUP_NAME" . \
  -x ".venv/*" \
  -x "chroma_db/*" \
  -x "__pycache__/*" \
  -x "*/__pycache__/*" \
  -x "*.DS_Store" \
  -x ".env" \
  -x "*.zip"
echo ""
echo "Created: $(pwd)/$BACKUP_NAME"
echo "Save this ZIP to Google Drive, Dropbox, OneDrive, or USB."
