import requests 

server = 'https://osamers.atlassian.net/rest/api/2/issue/CA-229'
# r = requests.get('https: // osamers.atlassian.net/rest/api/2/search?jql = project = %22CA % 22',
#                  auth=('dphamanh45@gmail.com', 'dung4597'))
r = requests.get(server,auth=('dphamanh45@gmail.com', 'dung4597'))

x=r.json()

dod=x['fields']['customfield_10053']

print(dod)


