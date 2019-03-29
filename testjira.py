from jira import JIRA
import requests

jira_server = "https://osamers.atlassian.net"
jira_user = "dphamanh45@gmail.com"
jira_pass = "dung4597"

jira_servers = {'server': jira_server}
jira = JIRA(options=jira_servers, basic_auth=(jira_user, jira_pass))

project = jira.project('CA')
# print(issue.fields.project.key)
# print(issue.fields.issuetype.name)
# print(issue.fields.reporter.displayName)
# # get fields of DoD
# print(issue.fields.customfield_10053)
# print(issue.fields.created)
# print(project.lead.displayName)
for i in jira.search_issues('project = CA AND created >= -2d ORDER BY created DESC', maxResults=10):
    print('{} - Name: {}'.format(i.fields.summary, i.fields.reporter.displayName))
    print('DoD:  {}'.format(i.fields.customfield_10053))
# for issue in jira.search_issues('reporter = currentUser() order by created desc', maxResults=50):
#     print('{}: {}'.format(issue.key, issue.fields.summary))
    # print('DoD: ''{}'.format(issue.fields.customfield_10053))



