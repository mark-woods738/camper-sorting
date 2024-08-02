import random
import copy
import csv
from sorter import Sorter

class Camper:
    def __init__(self, forename, surname, tent, preferences):
        self.forename = forename
        self.surname = surname
        self.tent = tent
        self.preferences = preferences
        self.remainingPreferences = copy.deepcopy(preferences)
        self.selectedActivites = []

    def getName(self):
        return self.forename +" " +self.surname
    
    def addActivity(self, activity):
        for existingActivity in self.selectedActivites:
            if existingActivity.name == activity.name:
                return False
        else:
            if self.remainingPreferences.count(activity.name) != 0:
                self.remainingPreferences[self.remainingPreferences.index(activity.name)] = ""
            self.selectedActivites.append(activity)
            activity.participants.append(self.getName())
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
        tent = ""
        if self.tent != None:
            tent = " Tent: " +self.tent

        outstring = self.getName() +" (Score: "+ str(camper.calculateScore())+")" +tent +"\n"
        underlineLength = len(outstring)
        for i in range(0,underlineLength):
            outstring += "="
        outstring += "\n"
        for i in range(0, len(self.selectedActivites)):
            outstring += "Block " +str(i+1) +": " +self.selectedActivites[i].name +"\n"
        print(outstring)

    def writeAsCSV(self, writer):
        if(self.tent == None):
            writer.writerow(["Name", self.getName(), "Score", self.calculateScore()])
        else:
            writer.writerow(["Name", self.getName(), "Tent", self.tent, "Score", self.calculateScore()])
        
        for i in range(0,len(self.preferences)):
            writer.writerow(["Block "+str(i+1), self.preferences[i]])
        writer.writerow([])
        
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
        outstring = str.title(self.name) +"     Activity Block: " +str(self.block) +"     Total Participants: " +str(len(self.participants))+"\n"
        outstring = underlineString(outstring)
        for camper in self.participants:
            outstring += camper +"\n"
        print(outstring)

    def writeAsCSV(self, writer):
        writer.writerow(["Activity", self.name, "Activity Block", self.block, "Total Participants", str(len(self.participants))])
        for p in self.participants:
            writer.writerow([p])
        writer.writerow([])

def underlineString(s):
    underlineLength = len(s)
    outstring = s
    for i in range(0,underlineLength):
        outstring += "="
    outstring += "\n"
    return outstring

try:
    with open('./camper-selections.csv', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')

        # detect if tent numbers are present
        tentsPresent = False
        # unused headers
        headers = next(reader, None)
        # used headers
        headers = next(reader, None)
        if headers[1].strip().lower() == "tent":
            tentsPresent = True
        
        # load campers
        campers = []
        for line in reader:
            name = line[0]
            forename = name.split(" ")[0]
            surname = name[len(forename):len(name)]
            surname = ''.join(surname).strip()

            tent = None
            offset = 0
            if tentsPresent:
                offset = 1
                tent = line[1].strip().lower()

            preferences = []
            for i in range(1+offset,len(line)):
                preferences.append(line[i].strip().lower())

            campers.append(Camper(forename, surname, tent, preferences))
except:
    raise Exception("Invalid format in the 'camper-selections.csv' file")

# load activites 
try:
    with open('./activity-details.csv', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        nLine = 1;
        allActivities = []
        for line in reader:
            for x in range(0, len(line)):
                if x%2 == 1:
                    allActivities.append(Activity(line[x-1].strip().lower(), int(line[x].strip()), nLine))
            nLine += 1
except:
    raise Exception("Invalid format in the 'activity-details.csv' file")

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
            raise Exception("There aren't enough activity spaces for the number of campers") 

# Print result
for activity in allActivities:
    activity.display()

for camper in campers:
    camper.display()

# By camper name file
with open('./output/groups-by-camper-name.csv', 'w') as csvfile: 
    w = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for camper in campers:
        camper.writeAsCSV(w)

# By camper tent
if tentsPresent:
    with open('./output/groups-by-tent.csv', 'w') as csvfile:
        w = csv.writer(csvfile, delimiter=',', quotechar="|", quoting=csv.QUOTE_MINIMAL)
        completeTents = []
        for camper in campers:
            if completeTents.count(camper.tent) == 0:
                for c in campers:
                    if c.tent == camper.tent:
                        c.writeAsCSV(w)
                completeTents.append(camper.tent)

# By activity
with open('./output/groups-by-activity.csv', 'w') as csvfile:
    w = csv.writer(csvfile, delimiter=',', quotechar="|", quoting=csv.QUOTE_MINIMAL)
    completeActivities = []
    for activity in allActivities:
        if completeActivities.count(activity.name) == 0:
            for a in allActivities:
                if a.name == activity.name:
                    a.writeAsCSV(w)
            completeActivities.append(activity.name)

# By activity block
with open('./output/groups-by-activity-block.csv', 'w') as csvfile:
    w = csv.writer(csvfile, delimiter=',', quotechar="|", quoting=csv.QUOTE_MINIMAL)

    # find highest block
    maxBlock = -1
    for activity in allActivities:
        if activity.block > maxBlock:
            maxBlock = activity.block
    
    for i in range(1,maxBlock+1):
        w.writerow(["Block "+ str(i)])
        for activity in allActivities:
            if activity.block == i:
                activity.writeAsCSV(w)