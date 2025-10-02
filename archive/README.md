# Archive - Original Email Senders

This directory contains the original email sender scripts that were used for the CSAC conference project. These files are preserved for historical reference and memory.

## Files

### `archive_original_sender.py`
- **Original version** of the email sender
- Single sender email account
- Basic retry logic (3 attempts with 61-second delays)
- Simple error handling
- Used environment variables: `SENDER_EMAIL`, `SENDER_PASSWORD`, `SMTP_SERVER`, `SMTP_PORT`, `CSV_FILENAME`

### `archive_improved_sender.py` 
- **Improved version** with multiple sender accounts
- Support for rotating between multiple sender emails
- Better retry logic (2 attempts with 10-second delays)
- Enhanced error handling and logging
- Email counter for tracking progress
- Used environment variables: `SENDER_EMAILS` (comma-separated), `SENDER_PASSWORD`, `SMTP_SERVER`, `SMTP_PORT`, `CSV_FILENAME`

## Key Differences

| Feature | Original | Improved |
|---------|----------|----------|
| Sender Accounts | Single | Multiple (rotation) |
| Retry Logic | 3 attempts, 61s delay | 2 attempts, 10s delay |
| Error Handling | Basic | Enhanced with logging |
| Progress Tracking | None | Email counter |
| Email Content | Same CSAC conference template | Same CSAC conference template |

## Historical Context

These scripts were created for sending conference invitations for the Computer Science Advancements Conference (CSAC) in October 2024. They represent the evolution of the email sending functionality:

1. **Original**: Basic single-sender approach
2. **Improved**: Multi-sender approach to handle rate limits
3. **Current**: General-purpose tool (`email_sender.py`) for any email campaign

## Note

These files are preserved for reference only. For current email sending needs, use the main `email_sender.py` tool which is more flexible and feature-complete.
