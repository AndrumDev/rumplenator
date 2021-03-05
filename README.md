[![Build Status](https://www.travis-ci.com/AndrumDev/rumplenator.svg?branch=main)](https://www.travis-ci.com/AndrumDev/rumplenator)

# rumplenator
Code for the twitch chatbot on andrumpleteazer's stream ( twitch.tv/andrumpleteazer )

# local setup

1. In the root folder, create a virtual environment

On mac/linux:

```
virtualenv venv
```

On windows:

See: [https://docs.python.org/3/library/venv.html](https://docs.python.org/3/library/venv.html)

2. Activate the virtual environment

On mac/linux:
```
source venv/bin/activate
```

On windows:
```
venv\Scripts\activate
```

3. Install the requirements:

```
pip install -r requirements.txt
```

4. Run the tests  (pass `-s` to prevent stdout from being suppressed):

```
python -m pytest -s
```

on windows, the dyson tests will fail. Run:

```
python -m pytest -s --ignore-glob="*dyson*"
```

5. Set local environment variables by copying `.example.env` to a new file named `.env`, and setting `TMI_TOKEN` and `CLIENT_ID`.

6. Run the bot locally:

```
python -m main.py
```


# setup notes if you need to run the docker container on windows

- install docker desktop
- install wsl and the kernel update
- run PowerShell ISE as an administrator
- if the docker daemon complains about needing elevated privileges, run `& 'C:\Program Files\Docker\Docker\DockerCli.exe' -SwitchDaemon`
- making scripts executable: https://www.scivision.dev/git-windows-chmod-executable/
