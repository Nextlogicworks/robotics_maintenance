import requests

response = requests.get(
    "http://127.0.0.1:8000/factory",
    timeout=10
)

response.raise_for_status()

factory_data = response.json()

print(type(factory_data))



robot_1 = {'ID':'R-301','Parts':540,'Defects':9,'Temperature':69.5,'Power':22.5}
robot_2 = {'ID':'R-302','Parts':615,'Defects':28,'Temperature':82.4,'Power':31.8}
robot_3 = {'ID':'R-303','Parts':470,'Defects':12,'Temperature':76.8,'Power':27.4}
robot_4 = {'ID':'R-304','Parts':590,'Defects':7,'Temperature':67.2,'Power':20.9}
robot_5 = {'ID':'R-305','Parts':650,'Defects':35,'Temperature':88.6,'Power':36.2}
robot_6 = {'ID':'R-306','Parts':505,'Defects':18,'Temperature':79.1,'Power':29.7}
robot_7 = {'ID':'R-307','Parts':625,'Defects':10,'Temperature':71.4,'Power':24.6}
robot_8 = {'ID':'R-308','Parts':560,'Defects':24,'Temperature':85.3,'Power':33.1}

robots = [robot_1,robot_2,robot_3,robot_4,robot_5,robot_6,robot_7,robot_8]

robots = factory_data['robots']

def calculation( parts,defects):
    good_parts = parts - defects
    defect_percentage = (defects/parts) * 100
    if defect_percentage < 2:
        defect_per_status = 'Excellent'
    elif 2 <= defect_percentage <= 4:
        defect_per_status = 'Normal'
    else:
        defect_per_status = 'Check Robot'
    return good_parts,defect_percentage,defect_per_status

def cal(temperature):
    if temperature < 70:
        temp_status = 'Normal'
    elif 70 <= temperature < 85:
        temp_status = 'Warning'
    else:
        temp_status = 'Critical'
    return temp_status

total_good_parts = 0
total_defect_per = 0
total_temperature = 0
total_power = 0
robot_count = 0

count_excellent = 0
count_normal = 0
count_check_robot = 0

count_normal_temp = 0
count_warning_temp = 0
count_critical_temp = 0

highest_defect_per = None
highest_defect_id = 0
highest_defect_pos = 0

highest_power_con = None
highest_power_id = 0
highest_power_pos = 0

highest_attention_defect_per = None
highest_attention_id = 0
highest_attention_tem = 0
highest_attention_production_status = 0
highest_attention_temperature_status = 0
highest_attention_pos = 0


for number,robot in enumerate(robots):

    good_parts,defect_percentage,defect_per_status = calculation(robot['Parts'],robot['Defects'])

    temp_status = cal(robot['Temperature'])       

    robot['Good Parts'] = good_parts

    robot['Defect Percentage'] = defect_percentage
    robot['Defect Percentage'] = round(robot['Defect Percentage'],3)

    robot['Production Status'] = defect_per_status

    robot['Temperature Status'] = temp_status

    robot_count += 1

    total_good_parts += good_parts

    total_defect_per += defect_percentage

    total_temperature += robot['Temperature']

    total_power += robot['Power']

    if defect_per_status == 'Excellent':
        count_excellent += 1

    if defect_per_status == 'Normal':
        count_normal += 1

    if defect_per_status == 'Check Robot':
        count_check_robot += 1

    if temp_status == 'Normal':
        count_normal_temp += 1

    if temp_status == 'Warning':
        count_warning_temp += 1

    if temp_status == 'Critical':
        count_critical_temp += 1

    if highest_defect_per is None or defect_percentage > highest_defect_per:
        highest_defect_per = defect_percentage
        highest_defect_id = robot ['ID']
        highest_defect_pos = number +1

    if highest_power_con is None or robot['Power'] > highest_power_con:
        highest_power_con = robot['Power']
        highest_power_id = robot['ID']
        highest_power_pos = number +1

    if defect_per_status == 'Check Robot' or temp_status == 'Critical':
       if highest_attention_defect_per is None or defect_percentage > highest_attention_defect_per :
           highest_attention_defect_per = defect_percentage
           highest_attention_id = robot['ID']
           highest_attention_tem = robot['Temperature']
           highest_attention_production_status = defect_per_status
           highest_attention_temperature_status = temp_status
           highest_attention_pos = number +1

    
average_defect_per = total_defect_per / robot_count

average_temperature = total_temperature / robot_count

average_power = total_power / robot_count

for robot in robots:
    print(robot)


print('\nFactory Summary')
print('\nTotal Good Parts:',total_good_parts)
print('Average defect percentage:',round(average_defect_per,3))
print('Average Temperature:',round(average_temperature,2))
print('Average Power:',round(average_power,2))
print('Excellent Robot:',count_excellent)
print('Normal Robot:',count_normal)
print('Check Robot:',count_check_robot)
print('Normal Temperature Robots:',count_normal_temp)
print('Warning Temperature Robots:',count_warning_temp)
print('Critical Temperature Robots:',count_critical_temp)
print('Highest Defects Percentage:', ' ID:',highest_defect_id,' Defect Percentage:',round(highest_defect_per,2),' Position:',highest_defect_pos)
print('Highest Power Consunmption:', ' ID:',highest_power_id,' Power Consumption:',highest_power_con,' Position:',highest_power_pos )
print('Most Attention Robot:'' ID:',highest_attention_id,' Defect Percentage:',highest_attention_defect_per,' Temperature:',highest_attention_tem, ' Production Status:',highest_attention_production_status,' Temperature Status:',highest_attention_temperature_status,' Position:',highest_attention_pos)


def maintenance(production,temperature):
    if production =='Check Robot'  and temperature == 'Critical' :
        maintenance_priority = 'Urgent'
    elif production == 'Check Robot'  or temperature == 'Critical' :
        maintenance_priority = 'High'
    elif production == 'Normal' or temperature == 'Warning':
        maintenance_priority = 'Medium'
    else:
        maintenance_priority = 'Low'
    return maintenance_priority

count_maintenance_urgent = 0
count_maintenance_high = 0
count_maintenance_medium = 0
count_maintenance_low = 0
highest_defect_percentage_maintenance = None
highest_defect_percentage_maintenance_id = 0
highest_defect_percentage_maintenance_temp = 0
highest_defect_percentage_maintenance_pos = 0


for number,robot in enumerate(robots):

    maintenance_priority = maintenance(robot['Production Status'],robot['Temperature Status'])

    robot ['Maintenance Priority'] = maintenance_priority

    if maintenance_priority == 'Urgent':
        count_maintenance_urgent += 1
        if highest_defect_percentage_maintenance is None or robot['Defect Percentage'] > highest_defect_percentage_maintenance:
            highest_defect_percentage_maintenance = robot['Defect Percentage'] 
            highest_defect_percentage_maintenance = round(highest_defect_percentage_maintenance,2)
            highest_defect_percentage_maintenance_id = robot ['ID']
            highest_defect_percentage_maintenance_temp = robot ['Temperature']
            highest_defect_percentage_maintenance_pos = number +1

    if maintenance_priority == 'High':
        count_maintenance_high += 1

    if maintenance_priority == 'Medium':
        count_maintenance_medium += 1

    if maintenance_priority == 'Low':
        count_maintenance_low += 1

    print('\nRobot:' '\tID:',robot[ 'ID'], '\tProdution Status :',robot['Production Status'],'\t\tTemperature:',robot['Temperature Status'],' \t\tMaintenance Priority:',robot['Maintenance Priority'])



print('\nMaintenance Priority Robots:' ' Urgent:',count_maintenance_urgent, ' High:',count_maintenance_high, ' Medium:',count_maintenance_medium, ' Low:',count_maintenance_low)
print( '\nHigthest Defect Maintenance Priority:' ' ID:',highest_defect_percentage_maintenance_id, ' Defect Percentage:',highest_defect_percentage_maintenance,' Temperature:',highest_defect_percentage_maintenance_temp, 'Position:',highest_defect_percentage_maintenance_pos)

def maintenance_action(main_prio):
    if main_prio == 'Urgent':
        main_action = 'Stop and inspect'
    elif main_prio == 'High':
        main_action = 'Inspect before next shift'
    elif main_prio == 'Medium':
        main_action = 'Schedule routine inspection'
    elif main_prio == 'Low':
        main_action = 'Continue operation'
    return main_action

robot_urgent_high_count = 0
robot_continue_count = 0
robot_continue_good_parts = 0
robot_urgent_high_power_cos = None
robot_urgent_high_power_id = 0
robot_urgent_high_power_pos = 0
robot_urgent_high_power_prio = 0
stop_now_count = 0
before_next_shift = 0
allowed_to_continue_count = 0
good_parts_allowed_continue = 0
highest_power_robot_attention = 0


for number,robot in enumerate(robots):

    maintenance_priority = maintenance(robot['Production Status'],robot['Temperature Status'])
    
    main_action = maintenance_action(maintenance_priority)

    good_parts,defect_percentage,defect_per_status = calculation(robot['Parts'],robot['Defects'])

    robot['Maintenance Action'] = main_action

    #counting robots in priority 'urgent' and action 'inpect before next shift'
    if robot ['Maintenance Priority'] == 'Urgent' or robot['Maintenance Action'] == 'Inspect before next shift': 
        robot_urgent_high_count += 1
        if robot_urgent_high_power_cos is None or robot['Power'] > robot_urgent_high_power_cos:
            robot_urgent_high_power_cos = robot['Power']
            robot_urgent_high_power_id = robot ['ID']
            robot_urgent_high_power_pos = number +1
            robot_urgent_high_power_prio = maintenance_priority
            

    if robot ['Maintenance Priority'] == 'Medium' or robot['Maintenance Priority'] == 'Low':
        robot_continue_count += 1
        robot_continue_good_parts += robot['Good Parts']

    if robot['Maintenance Action'] == 'Stop and inspect':
        stop_now_count += 1

    if robot ['Maintenance Action'] == 'Inspect before next shift':
        before_next_shift += 1

    if robot['Maintenance Action'] == 'Schedule routine inspection' or robot['Maintenance Action'] == 'Continue operation':
        allowed_to_continue_count += 1
        good_parts_allowed_continue += robot['Good Parts']
    
    print('Robot ID:',robot['ID'],'\tMaintenance Priority:',robot['Maintenance Priority'],'  \tMaintenance Action:',robot['Maintenance Action'])
    
print('\nUrgent and High robots:',robot_urgent_high_count)
print('\nRobots allowed to continue:',robot_continue_count)
print('\nRobots allowed to continue good Parts:', robot_continue_good_parts)
print('\nAmong Urgent and High highest Power:' '\tID:',robot_urgent_high_power_id,'\tPosition:',robot_urgent_high_power_pos,'\tPriority:',robot_urgent_high_power_prio,'\tPower:',robot_urgent_high_power_cos)
print('\nSUPERVISOR SUMMARY')
print('\nStop now Robots:',stop_now_count)
print('Inpect before next shift:',  before_next_shift)
print('Allowed to continue Robots:',allowed_to_continue_count)
print('Good Parts from continue Robots:',good_parts_allowed_continue)
print('Highest Power attention Robot:',robot_urgent_high_power_cos)


robot_stop_and_inspect_id = 0
robot_stop_and_inspect_priority = 0
robot_stop_and_inspect_action = 0
robot_stop_and_inspect_power_con = 0
robot_stop_and_inspect_total_power_con = 0
robot_stop_and_inspect_highest_power_con = None
robot_stop_and_inspect_highest_power_id = 0
robot_stop_and_inspect_highest_power_priority = 0
number_count = 0

print('\nSupervisor Attention Report:')


for robot in robots:

    if robot['Maintenance Action'] == 'Stop and inspect' or robot['Maintenance Action'] == 'Inspect before next shift':
        robot_stop_and_inspect_id = robot['ID']
        robot_stop_and_inspect_priority = robot ['Maintenance Priority']
        robot_stop_and_inspect_action = robot ['Maintenance Action']
        robot_stop_and_inspect_power_con = robot['Power']
        robot_stop_and_inspect_total_power_con += robot['Power']
        number_count += 1
        if robot_stop_and_inspect_highest_power_con is None or robot['Power'] > robot_stop_and_inspect_highest_power_con:
            robot_stop_and_inspect_highest_power_con = robot ['Power']
            robot_stop_and_inspect_highest_power_id = robot ['ID']
            robot_stop_and_inspect_highest_power_priority = robot ['Maintenance Priority']

    


    
        print('Maintenance with high action:' '\tID:',robot_stop_and_inspect_id, '\tMaintenance Priority:' ,robot_stop_and_inspect_priority,'\˝Maintenance Action:',robot_stop_and_inspect_action,'\tPower consumption:',robot_stop_and_inspect_power_con )

if number_count == 0:
    print('No robots require attention:',number_count)
print('\nTotal Power Consumption of the robot above:',robot_stop_and_inspect_total_power_con)
print('\nHighest Power Consumption of the robot above:' '\tID:',robot_stop_and_inspect_highest_power_id ,'\tPower Consumption:',robot_stop_and_inspect_highest_power_con,'\tMaintenance Priority:',robot_stop_and_inspect_highest_power_priority)
print('\nNumber of Robots requiring Attention:',number_count)

webhook_url = "https://sert333.app.n8n.cloud/webhook/32ff7ec8-5c95-4034-aa51-60c155135cae"
dashboard_webhook_url = "https://sert333.app.n8n.cloud/webhook/d7992127-5b0d-4bab-9c79-952a936e80ba"

responds = requests.post(webhook_url, json = robots)

dashboard_responds = requests.post(dashboard_webhook_url, json = robots)