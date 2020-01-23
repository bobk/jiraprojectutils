
# http://github.com/bobk/jiraprojectutils
#
#   list_roles-groups-users.py
#   lists all roles in a project, along with the groups (expanded to users) and users in those roles
#

from jira import JIRA
import time
from datetime import datetime
import os 

#   get our login and server data from env vars
server   = os.environ['JIRA_SERVER']
project  = os.environ['JIRA_PROJECT']
username = os.environ['JIRA_USERNAME']
password = os.environ['JIRA_PASSWORD']

#   connect to Jira
options = { "server" : server }
jira = JIRA(options, basic_auth=(username, password))

#   get all the roles in the project
roles = jira.project_roles(project)
print(f"project = {project}")

#   for each role, get the role name
for rolename in roles:
    roleid = roles[rolename]['id']
    role = jira.project_role(project, roleid)
    roledescription = role.description or "<role description missing>"
    print(f"   role = {rolename} ({roleid}, {roledescription})")

#   then look in that role's members, either groups or users or both
    for actor in role.actors:
        actorid = actor.id
        actorname = actor.name
        actordisplayname = actor.displayName
        actortype = actor.type
        actortype_display = "UNKNOWN"

#   if it's a user, then print the user's data
        if (actortype == "atlassian-user-role-actor"): 
            actortype_display = "USER"
            print(f"      role member = {actorname} {actortype_display} ({actorid})")
            print(f"         member name = {actordisplayname}")

#   if it's a group, then print the basic group info, then iterate through the members
        if (actortype == "atlassian-group-role-actor"): 
            actortype_display = "GROUP"
            print(f"      role member = {actorname} {actortype_display} ({actorid}, {actordisplayname})")
            groupmembers = jira.group_members(actorname)
            for groupmember in groupmembers:
                groupmemberfullname = groupmembers[groupmember]['fullname']
                print(f"         member name = {groupmemberfullname}")

