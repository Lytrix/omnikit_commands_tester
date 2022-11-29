# Omnikit Commands Tester #

Small upload and test site to evaluate Omnikit commands.

Working online version can be found here:
https://omnikit-commands-tester.herokuapp.com

### Usage ###

Upload a text file recorded with:
- [rtlomni](https://github.com/openaps/openomni) as a .omni file
- Debugger Xcode log of [Loop](https://github.com/LoopKit/Loop) as a Markdown (.md) file

Hit process and it will:
1. Extracts a list of all recorded temp basal commands.
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
pip install -r requirements.txt
```

You can run the website locally with using:
```
python manage.py runserver
```

The site can be found on http://localhost:8000</br>

You can also run tester commands in the terminal for example like this:
```
cd omnikit_commands_tester/issuereports
python set_insulin_comands_tester.py filename.md
```

