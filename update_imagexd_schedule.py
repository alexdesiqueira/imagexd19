"""

Some references:
  [1] https://stackoverflow.com/questions/4823468/comments-in-markdown
  [2] https://www.geeksforgeeks.org/python-list-index/

"""

from urllib.request import urlopen
import yaml

README = 'README.md'
SCHEDULE_SECTION = '## Schedule\n'
TABLE_HEAD = '| Time | Slot | Presenter |\n'
TABLE_SEP = '| ---- | ---- | --------- |\n'
URL = 'https://raw.githubusercontent.com/xd-con/imagexd-2019/master/site/config.yml'

STARTING_LINE = '<!-- begin schedule -->\n'
ENDING_LINE = '<!-- end schedule -->\n'

FOOD_TIME = ['Check-in / Breakfast',
             'Breakfast',
             'Lunch',
             'Tea break']

TUTORIALS_ADDRESSES = {'Stéfan' : 'https://github.com/BIDS/imagexd19/blob/master',
                       'Dani' : 'https://github.com/BIDS/ISVC2019',
                       'Ariel' : 'https://github.com/arokem/conv-nets',
                       'Maryana' : 'https://github.com/BIDS/imagexd19/blob/master',
                       'Loic' : 'https://github.com/BIDS/imagexd19/blob/master',
                       'Carolyn' : 'https://github.com/BIDS/imagexd19/blob/master'
}


with open(README) as readme_file:
    readme = readme_file.readlines()

data_url = urlopen(URL)
data = yaml.safe_load(data_url)

new_schedule = ['\n', SCHEDULE_SECTION]

for schedule in data['params']['Schedule']:
    first_line_schedule = '### ' + schedule['day'] + '\n'
    new_schedule.extend(('\n', first_line_schedule))
    day_slots = schedule['slots']
    new_schedule.extend(('\n', TABLE_HEAD, TABLE_SEP))

    for slot in day_slots:
        aux_name = slot.get('name', '')
        aux_pres = slot.get('presenter', '')

        if aux_name in FOOD_TIME:  # if it is food time, it doesn't need an URL
            event_name = aux_name
        else:  # if not, get a link for the materials
            aux_url = ''
            for pres, url in TUTORIALS_ADDRESSES.items():
                if pres in aux_pres:
                    aux_url = url

            event_name = '[' + aux_name + '](' + aux_url + ')'
        line_schedule = '| ' + slot.get('time', '') + ' | ' + event_name + ' | ' + aux_pres + ' |\n'
        new_schedule.append(line_schedule)

# replacing old schedule (between STARTING_LINE and ENDING_LINE) by the new one
readme[readme.index(STARTING_LINE)+1: readme.index(ENDING_LINE)] = new_schedule

with open(README, 'w') as readme_file:
    readme_file.writelines(readme)

readme_file.close()
