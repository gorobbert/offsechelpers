# Offsec Helpers

Small webbased tool to assist with quickly creating reverse shell payloads. Comes with a small collection of frequently used payloads and encoding methods. The tool is easy to extend by just creating or editing the files in the payloads directory.


## How to use
On RHEL based systems, `podman.sh` can be used to quickly setup the environment.
Otherwise, use the following commands to start the webapp:

```console
[user@system:~/OffsecHelpers]$ python3 -m venv venv
[user@system:~/OffsecHelpers]$ source venv/bin/activate
[user@system:~/OffsecHelpers]$ cd src
[user@system:~/OffsecHelpers]$ pip install -r requirements.txt
[user@system:~/OffsecHelpers]$ uvicorn main:app --host 0.0.0.0 --reload
```
