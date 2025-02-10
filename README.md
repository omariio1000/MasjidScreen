# Masjid Display - Developed for ICCH

## How to Run:

- `GUI.bat` - Runs the main program
- `GUI_Ramadan.bat` - Runs Ramadan mode with trivia
- Can also be run by changing directory to the `code` folder and running: `python masjid_display.py`. There are the following options:
  - `-h` - Display help dialog
  - `-r` - Ramadan mode
  - `-t` - Test mode  (must be combined with `-r`)

## Required:

1. Python (Developed and tested on 3.12.8)
2. The following python libraries:
   - pillow
   - openpyxl
   - gspread
   - oauth2client
   - pandas 
   - google-api-python-client
   - google-auth-httplib2
   - google-auth-oauthlib
   - qrcode
   - Or run the `install_libs.bat` script

## Customizing:

To customize for any masjid links, open the `config.json` file. Modify the following values:
- `flyers` - Local location on Desktop for flyer images
- `socials` - Link to social media accounts (linktree is used by ICCH)
- `donate` - Link to donate to masjid
- `website` - Link to masjid website

## Required for Trivia:

 - `service_account.json`
 - `trivia_details.json`
 - `email_credentials.json`
 - `amazon_codes.txt`

## Help Scripts

- `authenticate_email.bat` - Tests sending emails from a local gmail account
- `install_libs.bat` - Installs needed libraries
- `update_files` - Updates to latest repository changes and displays git status