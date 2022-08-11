import pymsteams


myTeamsMessage = pymsteams.connectorcard(
    "https://computerconceptslimited.webhook.office.com/webhookb2/07857eba-f3da-4913-89a7-95b56d26b075@341602ea-596a-4091-92a0-ded5cbc504a9/IncomingWebhook/be38e1ab06b64bfe8cd97f5d947af8a2/830c2b63-cf57-4151-b3f2-674eca3297b9")
# myTeamsMessage.text(errordisable_port.to_string())
myTeamsMessage.title("PR: Ansible-prod | TEST")
myTeamsMessage.addLinkButton(" Pull reqeuest",
                             "https://grafana.otago.ac.nz")

myTeamsMessage.text(
    'Ops! a new pull reqest at xx comming.')
myTeamsMessage.printme()
#myTeamsMessage.send()
print("sent successful!!")



