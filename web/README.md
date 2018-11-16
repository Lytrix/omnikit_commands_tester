# Omnikit Commands Tester #

Small upload and test site to evaluate Omnikit commands. 

### Usage ###

Upload a text file recorded with:
- [rtlomni](https://github.com/openaps/openomni) as a .omni file
- Debugger Xcode log of [Loop](https://github.com/LoopKit/Loop) as a Markdown (.md) file

Hit process and it will:
1. Show all list of all recorded temp basal commands.
2. Check for mismatches for each temp basal command with the recorded PDM commands using this markdown file: 

https://github.com/openaps/openomni/wiki/All-Temp-basal-units-for-0.5h

### Install procedure ###

```
git clone https://github.com/Lytrix/omnikit_commands_tester.git 
cd omnikit_commands_tester
```

Create a local environment and activate it:
```
virtualenv --python=$(which python3) venv
source venv/bin/activate
```

Install the packages 
```
pip install -r ./web/requirements.txt
```

You can run the website locally with using:
```
./web/manage.py runserver
```

The site can be found on http://localhost:8000</br>
