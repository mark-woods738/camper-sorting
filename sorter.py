import random

class Sorter:
    def __init__(self, campers, activities, numBlocks):
        self.campers = campers
        self.activities = activities
        self.numBlocks = numBlocks

    def getMatchingActivity(self, preference, activities):
        for activity in activities:
            if preference == activity.name:
                return activity
        # print(len(activities))
        choice = random.choice(activities)
        # print("Random choice: ", choice.name)
        return choice
    
    def getBlockActivites(self, block):
        activities = []
        for activity in self.activities:
            if activity.block == block:
                activities.append(activity)
        return activities

    def sortCampers(self, oldCampers):
        newCampers = []
        length = len(oldCampers)
        score = 0
        while len(newCampers) != length:
            for camper in oldCampers:
                if camper.calculateScore() == score:
                    newCampers.append(camper)
            score += 1
        return newCampers
    
    def reset(self):
        for camper in self.campers:
            camper.reset()
        for activity in self.activities:
            activity.reset()
        
    def sort(self):
        for block in range(1, self.numBlocks):
            blockActivities = self.getBlockActivites(block)
    
            for camper in self.campers:
                selected = False
                offset = 0
                retryCount = 0
                while selected == False:
                    # print("Retry Count: ", retryCount)
                    preference = camper.getNextPreference(offset)
                    # print(camper.name)
                    # print("Batch: ", block)
                    # print("Preference: ", preference)
                    activity = self.getMatchingActivity(preference, blockActivities)
                    # print("Activity: ", activity.name)
                    if(len(activity.participants) - activity.capacity == 0):
                        offset += 1
                    else:
                        if camper.addActivity(activity):
                            selected = True
                        else: 
                            offset += 1
                    
                    if retryCount >= len(blockActivities)*5:
                        # print("++++++EXCEPTION++++++")
                        raise Exception("no valid activity found")
                    
                    retryCount += 1

            self.campers = self.sortCampers(self.campers)
        return self.campers

