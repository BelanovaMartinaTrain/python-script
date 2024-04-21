# Cleaning helper scripts

These scripts were created for my team to help with great amount of data we needed to comb through during the process of "cleaning" public IP addresses.
It needed to workaround the lack of automation in within teams so the output data are prepared in the most suitable format.

Because it was created for my work it utilises a lot of slovak language words :)

## How it works

-   it filters .csv file obtained from our database team and creates a list of customers from selected IP subnet and other selectors
-   it checks gateway routers and status of PPPoE sessions according to obtained filtered data
-   it creates new groups according to the PPPoE session status and other selectors
-   based on the group you new private/public IP is assigned from IP subnet selected

-   after the IPs are updated on the radius server with the commands outputted from these scripts it connects to gateway routers and clean the sessions

-   it creates several outputs for our tema and other teams to keep our records updated in a suitable form considering the lack of automation services available

## Installation

You need PYTHON 3.

See [pip](https://pip.pypa.io/en/stable/) to install required modules:

```bash
pip install paramiko
pip install csv
pip install getpass4
```

## Usage

### SKRIPT hlavny_skript.py

```
- in cmd: "python hlavny_skript.py arg1 arg2"
- arg1 is input file -> .csv
- arg2 is output file
```
