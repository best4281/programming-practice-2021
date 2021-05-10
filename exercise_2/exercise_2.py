#Task 0
class Party:

    #Task 0.1
    def __init__(self):
        self.info_attendees = {}
        self.detailed_info_attendees = {}
    
    #Task 0.2
    def add_attendees(self, family_name, number_of_attendees):
        self.info_attendees[family_name] = number_of_attendees
    
    #Task 1.1
    def detailed_attendees(self, family_names, adult_attendees, child_attendees):
        for index, fam in enumerate(family_names):
            #{'name' : [adult_attendees, child_attendees, default_priority = 0]}
            self.detailed_info_attendees[fam] = [adult_attendees[index], child_attendees[index], 0]
    
    #Task 1.2 - I use detailed_info_attendees as a reference, so info_attendees will change accordingly.
    def check_and_resolve(self):
        for i in self.detailed_info_attendees:
            self.info_attendees[i] = self.detailed_info_attendees[i][0] + self.detailed_info_attendees[i][1]
        for j in self.info_attendees.keys() - self.detailed_info_attendees.keys():
            del(self.info_attendees[j])
    
    #Task 2.1
    def get_total_attendees(self):
        self.check_and_resolve()
        return sum(self.info_attendees.values())

    #Task 2.2
    def filter_attendees(self):
        self.filtered_family = []
        for i in self.detailed_info_attendees:
            if self.info_attendees[i] > 2:
                self.filtered_family.append(i)
            elif self.detailed_info_attendees[i][1] >= 1:
                self.filtered_family.append(i)
        return self.filtered_family

    #Task 3 ???
    def covid_changes(self):
        limit = 50
        if self.get_total_attendees() <= limit:
            print("Total number of attendees is not over " + str(limit) + " people, no need to change the detail of attendees.")
        else:
            print(*self.filter_attendees(), sep = ", ")
            print("Please bring only up to two adult family members to the party. Children are not allowed.")

    #Task 4.1
    def include_priority(self, family_names, priorities):
        for i,name in enumerate(family_names):
            try:
                self.detailed_info_attendees[name][2] = priorities[i]
            except:
                pass
    
    #Task 4.2
    def filter_priorities(self, priority):
        prioritized_family = []
        for i in self.detailed_info_attendees:
            if self.detailed_info_attendees[i][2] <= priority:
                prioritized_family.append(i)
        return prioritized_family

'''### INPUT ###
family = ["John","Edward"]
total = [4,2]
adult = [3,1]
child = [0,0]
priorities = [5,1]

p1 = Party()
for i,name in enumerate(family):
    p1.add_attendees(name, total[i])
p1.detailed_attendees(family, adult, child)
p1.check_and_resolve()
print(p1.get_total_attendees())
print(p1.filter_attendees())
p1.covid_changes()
p1.include_priority(family,priorities)
print(p1.filter_priorities(4))'''

def exercise_2(inputs): # DO NOT CHANGE THIS LINE
    """
    Output should be the name of the class.
    """
    output = Party

    return output       # DO NOT CHANGE THIS LINE

#p = exercise_2(1)()
#print(p)
