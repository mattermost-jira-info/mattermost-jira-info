#!/usr/bin/env python
# -*- coding: utf-8 -*-

import flask
import jira
import settings
import re

# some aliasses
request = flask.request
Response = flask.Response
json = flask.json

app = flask.Flask(__name__)


@app.route('/', methods=['POST'])
def receive_mattermost():
    """We only have 1 incoming hook"""
    form = request.form
    token = form.getlist('token')[0]

    if settings.MATTERMOST_TOKEN:
        if not token == settings.MATTERMOST_TOKEN:
            app.logger.error('Received wrong token, received [%s]', token)
            return ''

    ticket_id = search_token(form.getlist('text')[0])
    if ticket_id is None:
        return ''

    (icon, resp_str, project_name) = get_detail_from_jira(ticket_id)

    if resp_str is None:
        return ''

    resp = Response(
        json.dumps({'text': resp_str,
                    'icon_url': icon,
                    'username': project_name}),
        status=200)
    return resp


def search_token(text):
    """Search in the provided text for a match on the regexp, and return"""
    match = re.search('(%s)' % settings.TICKET_REGEXP, text)
    if match:
        return match.group(0)
    else:
        return None


def parse_icon_name(field):
    """Return a 'nice' formatter layout for icons and text"""
    return \
        '![](' + \
        field.iconUrl + ') ' +\
        field.name


def get_url(ticket_id):
    return '%s/browse/%s' % (settings.JIRA_URL, ticket_id)


def get_detail_from_jira(ticket_id):
    """Connect to JIRA and retrieve the details"""

    try:
        jc = jira.JIRA(server=settings.JIRA_URL,
                       basic_auth=(settings.JIRA_USER, settings.JIRA_PASS))
    except jira.JIRAError:
        print('Connection error')
        app.logger.error('Could not connect to JIRA', exc_info=True)
        return None

    try:
        issues = jc.search_issues('key=%s' % ticket_id)
    except jira.JIRAError:
        app.logger.warning('Search on JIRA failed', exc_info=True)
        return None

    if not len(issues):
        # Could not find a matching ticket
        return None
    issue = issues[0]

    ret_str = \
       '[%s - %s](%s "%s")' % (ticket_id, issue.fields.summary, get_url(ticket_id), ticket_id) \
       + '\n\n' +\
       'Reported by *%s*\n' % issue.fields.reporter.displayName + \
       'Is being worked on by: *' + \
       (issue.fields.assignee.displayName if issue.fields.assignee else 'Nobody') +\
       '*\n' +\
       'Type of the ticket: ' + parse_icon_name(issue.fields.issuetype) + '\n' +\
       'Status of the ticket: ' + parse_icon_name(issue.fields.status) + '\n' +\
       '- - -\n' +\
       '%s' % issue.fields.description

    icon = issue.fields.project.raw['avatarUrls']['32x32']
    project_name = issue.fields.project.name

    return (icon, ret_str, project_name)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
