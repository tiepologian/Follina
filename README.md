# Follina Proof of Concept (CVE-2022-30190)

Quick and easy "proof of concept" for the Follina RCE that affects Microsoft Office/365 products. This POC supports both the one-click exploit and the zero-click exploit through RTF files.  
Running the script will generate an `infected.zip` archive that contains two files:
* A `zero-click.rtf` file that allows you to test the RCE without opening the file (*simply previewing the file will trigger the exploit*)
* A `one-click.doc` file that triggers the exploit when opened

# Usage
1. Edit `follina.py` and set `COMMAND` to execute (*defaults to calc*), `INTERFACE` (*defaults to eth0*) and `PORT` (*defaults to 8000*)
2. Run `./follina.py`
3. Copy and extract the `infected.zip` on the target machine
4. From the target machine, open `one-click.doc` or simply preview `zero-click.rtf`

<img src="https://i.ibb.co/FH0M3cC/follina-01.png" width="500" />
