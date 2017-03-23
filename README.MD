Mattermost-Jira-Info
====================

This webservice can be used to to query Jira for issue details. Once
configured you can use a slash command to attach issue details to Jira issues mentioned in your text.
If a possible reference is found, the configured JIRA instance will be queried
for with the possible reference and if a match is found the ticket details
will be attached to your message.

The idea is that you want to mention a issue in your text. Because, for security reasons it is not possible to parse alle the messages all the time, you have to hit a configured slash(/) together with the text mentioning a Jira issue.
The bot will post your message in your name (+BOT) and with your avatar and attach the details of the Jira issues.

What you write in Mattermost
----------------------------
![What you write in Mattermost](/doc/mattermost-jira-info-allChannels-input.png)
What all users will see
-----------------------
![What all users will see](/doc/mattermost-jira-info-allChannels-output.png)

Features
--------

* Replaces all issues in your text with propper links to Jira
* Attaches details of each valid Jira issue you mentioned
* Shows Title, Description, Issue-Type (with icon), Issue-Status (with icon) and Assignee
* Highlights the attachment with a color matching the status of the issue (configurable)
* Replaces complete issue URLs with the issue ID as a link
* Can be used in all channels and private messages
* Returns error messages in case of failure (only visible to sender)


Setup
-----

To configure this project, perform a clone, rename the ```settings.py.example```
to ```settings.py``` and fill-in the details for your environment.

Install dependencies via ```pip install -r requirements.txt```

Start the server via ```./runme.py```.

## Start as service:
copy the mattermost-jira-info.conf into /etc/init/
edit the "Path to mattermost-jira-info installation" within the file
```sudo start mattermost-jira-info```

Mattermost setup
----------------

In mattermost configure a slash(/) command of your choice and
let it point to the server where the python code is running on the port you defined (default: 5000) e.g.
*http://localhost:5000/*.

Requires Mattermost Server 3.6 (fixed attachments working for slash-commands)

Hints
-----

The python code is written using Flask, so all methods available to run a Flask
instance can be applied.
