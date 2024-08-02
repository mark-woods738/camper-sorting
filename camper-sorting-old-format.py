import random
import copy
import csv
from sorter import Sorter

# TODO 
# + check that there are enough spaces possible for all the campers
# - test it works for any number of preferences
# + all a 10 times retry to the program if it doesn't solve within time limit
# - check for tent allocations
# - print in tent groups
# - branch intakes from old and new csv formats
# - write the readme file
# - intake data validation

# TODO output formats:
# - by tent
# - by block
# - by tent
# - campers alphabetically

class Camper:
    def __init__(self, name, preferences):
        self.name = name
        self.tent = None
        self.preferences = preferences
        self.remainingPreferences = copy.deepcopy(preferences)
        self.selectedActivites = []
    
    def addActivity(self, activity):
        for existingActivity in self.selectedActivites:
            if existingActivity.name == activity.name:
                return False
        else:
            if self.remainingPreferences.count(activity.name) != 0:
                self.remainingPreferences[self.remainingPreferences.index(activity.name)] = ""
            self.selectedActivites.append(activity)
            activity.participants.append(self.name)
            return True
    
    def calculateScore(self):
        score = 0
        for activity in self.selectedActivites:            
            numPreferences = len(self.preferences)
            for i in range(0, numPreferences):
                if(activity.name == self.preferences[i]):
                    score = score + (numPreferences - i)
        return score
            
    def getNextPreference(self, offset):
        index = 0 + offset
        while index < 3:
            if (self.remainingPreferences[index] != "") & (self.selectedActivites.count(self.remainingPreferences[index]) == 0):
                return self.preferences[index]
            else:
                index += 1
        return "any"
    
    def reset(self):
        self.remainingPreferences = copy.deepcopy(preferences)
        self.selectedActivites = []
    
    def display(self):
        outstring = self.name +" (Score: "+ str(camper.calculateScore())+")" +"\n"
        underlineLength = len(outstring)
        for i in range(0,underlineLength):
            outstring += "="
        outstring += "\n"
        for i in range(0, len(self.selectedActivites)):
            outstring += "Block " +str(i+1) +": " +self.selectedActivites[i].name +"\n"
        print(outstring)
        
class Activity:
    participants = []

    def __init__(self, name, capacity, block):
        self.name = name
        self.capacity = capacity
        self.block = block
        self.participants = []

    def reset(self):
        self.participants = []

    def display(self):
        outstring = str.title(self.name) +"     Activity Block: " +str(self.block) +"     Total Campers: " +str(len(self.participants))+"\n"
        outstring = underlineString(outstring)
        for camper in self.participants:
            outstring += camper +"\n"
        print(outstring)

def underlineString(s):
    underlineLength = len(s)
    outstring = s
    for i in range(0,underlineLength):
        outstring += "="
    outstring += "\n"
    return outstring

# TODO load data
with open('./example.csv', 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')

    # load headers as activity names
    headers = next(reader, None)
    activityNames = []
    for i in range(3, len(headers)):
        activityNames.append(headers[i].strip().lower())

    # load campers
    campers = []
    for line in reader:
        name = line[0] + line[1]
        name = name[1:(len(name)-1)]
        preferences = ['', '', '']
        for x in range(4, len(line)):
            if line[x].strip() == '1':
                preferences[0] = activityNames[x-4]
            elif line[x].strip() == '2':
                preferences[1] = activityNames[x-4]
            elif line[x].strip() == '3':
                preferences[2] = activityNames[x-4]
        campers.append(Camper(name, preferences))

# load activites 
with open('./activity-details.csv', 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    nLine = 1;
    allActivities = []
    for line in reader:
        for x in range(0, len(line)):
            if x%2 == 1:
                allActivities.append(Activity(line[x-1].strip().lower(), int(line[x].strip()), nLine))
        nLine += 1


# print campers
for camper in campers:
    print(camper.name, camper.preferences[0], camper.preferences[1], camper.preferences[2])

# print activities
for activity in allActivities:
    print(activity.name, activity.capacity)

sorter = Sorter(campers, allActivities, 4)

complete = False
retryCount = 0
while (complete == False):
    try:
        sorter.sort()
        complete = True
    except:
        sorter.reset()
        retryCount += 1
        print(retryCount)
        if retryCount == 10:
            # TODO test this more
            raise Exception("There aren't enough activity spaces for the number of campers") 


# Print result
for activity in allActivities:
    activity.display()

for camper in campers:
    camper.display()

# TODO add writing to file

        