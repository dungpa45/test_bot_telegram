from jira import JIRA
import json, codecs

jira_server = 'https://osamers.atlassian.net'

jira_servers = {'server': jira_server}

jira = JIRA(options=jira_servers,basic_auth=('dphamanh45@gmail.com','dung4597'))

search = jira.search_issues(
    'DOD is EMPTY AND status != Done AND status != "To Do" AND Sprint in (89, 105) ORDER BY priority DESC', maxResults=50)
print(len(search))
dic={}
ls=[]
stt = 0
if len(search)==0:
    print("Tasks already has DOD")
else:
    for iss in search:

        tieude = iss.fields.summary
        ten = iss.fields.reporter.displayName
        trangthai = iss.fields.status.name
        # print(trangthai)
        # dic[tieude] = trangthai
        dic[tieude] = ten
        ls.append(trangthai)
    # print(dic)
    # print(ls)
    k = []
    index = 0
    # print(dic.values())
    for j in dic:
        stt += 1
        # print(j.keys())
        k.append(str(stt)+': '+ j + ' - ' + dic[j] +' - '+ ls[index])
        index +=1
        # print(j)
    # print(k)

    # for i in range(len(k)):
    #     k[i] += [ls[i]]
    # print(k)

    z = "\n".join(k)
    print(z)
  



