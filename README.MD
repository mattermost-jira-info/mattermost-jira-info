Mattermost-Jira-Info
====================

This webservice can be used to receive incoming mattermost hooks. Once
configured it will check all incoming text for references to possible JIRA
ticket references.
If a possible reference is found, the configured JIRA instance will be queried
for with the possible reference and if a match is found the ticket details
will be shown in the dialog.

The idea is that this way (similar to the Hipchat connection) details will be
shown in the chat if a ticket is referenced.


Setup
-----

To configure this project, perform a clone, rename the ```settings.py.example```
to ```settings.py``` and fill-in the details for your environment.

Install dependencies via ```pip install -r requirements.txt```

Start the server via ```./runme.py```.

Mattermost setup
----------------

In mattermost configure outgoing webhooks for the channel(s) you desire. And
let them point to the server where the python code is running on port 5000 e.g.
```http://localhost:5000/```.
Is is not recommended to use any trigger keywords for the webhook, as it might
mean the the hook is not triggered on every occasion.

Hints
-----

The python code is written using Flask, so all methods available to run a Flask
instance can be applied.

Currently the port is hardcoded at 5000
