# Follina Proof of Concept (CVE-2022-30190)

Quick and easy "proof of concept" for the Follina RCE that affects Microsoft Office products.
Running the script will generate an "infected.zip" archive that contains two files:
* A zero-click.rtf file that allows you to test the RCE without opening the file (simply previewing the file will trigger the exploit)
* A one-click.doc file that triggers the exploit when it is opened
