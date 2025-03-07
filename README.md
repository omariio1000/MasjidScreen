# Masjid Display - Developed for ICCH

## How to Run:

- `GUI.bat` - Runs the main program
- `Ramadan_GUI.bat` - Runs Ramadan mode with trivia
  - This mode requires extra files that are mentioned below
- Can also be run by changing directory to the `code` folder and running: `python masjid_display.py`. There are the following options:
  - `-h` - Display help dialog
  - `-r` - Ramadan mode
  - `-t` - Trivia test mode  (must be combined with `-r`)

## Required:

1. Python (Developed and tested on 3.12.8)
2. The following python libraries:
   - pillow
   - openpyxl
   - pandas 
   - qrcode
3. These libraries are needed for the Ramadan mode (`-r`):
   - oauth2client
   - google-api-python-client
   - google-auth-httplib2
   - google-auth-oauthlib
   - Or run the `install_libs.bat` script

## Customizing:

To customize for any masjid links, open the `config.json` file. Modify the following values:
- `flyers` - Local location on Desktop for flyer images
- `socials` - Link to social media accounts (linktree is used by ICCH)
- `donate` - Link to donate to masjid
- `website` - Link to masjid website

## Required for Trivia:

Trivia requires Google Cloud integration and a service account. It also needs a file for trivia details and codes to send to winners by email.

 - `service_account.json`
 - `email_credentials.json`
 - `trivia_details.json`
 - `amazon_codes.txt`

## Help Scripts

- `authenticate_email.bat` - Tests sending emails from a local gmail account
- `install_libs.bat` - Installs needed libraries
- `update_files.bat` - Updates to latest repository changes and displays git status
