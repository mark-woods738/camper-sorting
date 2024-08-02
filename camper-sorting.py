import random
import copy
import csv

class Camper:
    def __init__(self, name, preferences):
        self.name = name
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
            if(activity.name == self.preferences[0]):
                score = score + 3
            if(activity.name == self.preferences[1]):
                score = score + 2
            if(activity.name == self.preferences[2]):
                score = score + 1
        return score

    def getNextPreference(self, offset):
        index = 0 + offset
        while index < 3:
            if (self.remainingPreferences[index] != "") & (self.selectedActivites.count(self.remainingPreferences[index]) == 0):
                return self.preferences[index]
            else:
                index += 1
        return "any"
        
class Activity:
    participants = []

    def __init__(self, name, capacity, block):
        self.name = name
        self.capacity = capacity
        self.block = block
        self.participants = []

def getMatchingActivity(preference, activities):
    for activity in activities:
        if preference == activity.name:
            return activity
    print(len(activites))
    choice = random.choice(activities)
    print("Random choice: ", choice.name)
    return choice
        
    
def getBlockActivites(block, allActivities):
    activities = []
    for activity in allActivities:
        if activity.block == block:
            activities.append(activity)
    return activities

def sortCampers(oldCampers):
    newCampers = []
    length = len(oldCampers)
    score = 0
    while len(newCampers) != length:
        for camper in oldCampers:
            if camper.calculateScore() == score:
                newCampers.append(camper)
        score += 1
    return newCampers

# TODO load data
with open('./camper-selections.csv', 'r') as csvfile:
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

for block in range(1, 4):
    activites = getBlockActivites(block, allActivities)
    
    for camper in campers:
        selected = False
        offset = 0
        while selected == False:
            preference = camper.getNextPreference(offset)
            # print("Batch: ", block)
            print("Preference: ", preference)
            activity = getMatchingActivity(preference, activites)
            # print("Activity: ", activity.name)
            if(len(activity.participants) - activity.capacity == 0):
                offset += 1
            else:
                if camper.addActivity(activity):
                    selected = True
                else: 
                    offset += 1

    campers = sortCampers(campers)

# Print result
for activity in allActivities:
    print(activity.name, activity.block)
    print("=====")
    for person in activity.participants:
        print(person)
    print("")

for camper in campers:
    print(camper.name +" (Score: "+ str(camper.calculateScore())+")")
    print("=====")
    print("Block 1: "+camper.selectedActivites[0].name)
    print("Block 2: "+camper.selectedActivites[1].name)
    print("Block 3: "+camper.selectedActivites[2].name)
    print("");

# TODO add writing to file

        