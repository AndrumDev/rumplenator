[![Build Status](https://www.travis-ci.com/AndrumDev/rumplenator.svg?branch=main)](https://www.travis-ci.com/AndrumDev/rumplenator)

# rumplenator
Code for the twitch chatbot on andrumpleteazer's stream ( twitch.tv/andrumpleteazer )

# local setup

1. In the root folder, create a virtual environment

```
virtualenv venv
```

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

4. Run the tests: (pass `-s` to prevent stdout from being suppressed):

```
python -m pytest 
```

5. Set local environment variables by copying `.example.env` to a new file named `.env`, and setting `TMI_TOKEN` and `CLIENT_ID`.

6. Run the bot locally:

```
python -m main.py
```
