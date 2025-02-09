# Masjid Display - Developed for ICCH

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

 - service_account.json
 - trivia_details.json
 - email_credentials.json
 - amazon_codes.txt