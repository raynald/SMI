from launchpadlib.launchpad import Launchpad

launchpad = Launchpad.login_anonymously('just testing', 'production', version = 'devel')
pro_name = 'neutron'
my_project = launchpad.projects(pro_name)
specifications = my_project.all_specifications
with open('yash/' + pro_name + '.csv', 'a') as f:
    f.write('Priority,Blueprint,Design,Delivery,Assignee,Email,Series\n')
    for blueprints in specifications:
        priority = blueprints.priority
        blueprint = blueprints.name
        design = blueprints.definition_status
        delivery = blueprints.implementation_status
        assignee = blueprints.assignee
        name = ''
        if assignee != None:
            name = assignee.display_name
        milestone = blueprints.milestone
        series = ''
        if milestone != None:
            series = milestone.code_name
        content = priority + ',' + blueprint + ',' + design + ',' + delivery + ',' + name + ',' + series + '\n'
        f.write(content.encode('utf-8'))

