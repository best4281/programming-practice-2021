from exercise_0.exercise_0 import exercise_0
from exercise_1.exercise_1 import exercise_1
from exercise_2.exercise_2 import exercise_2

# Tests for Exercise 0

if exercise_0(2) == 4:
	print("Successful")
else:
	raise Exception("Unsuccessful")


# Tests for Exercise 1

p =  ['t101', 't102', 't103']
q = ['s101', 's102', 's103']
r = {
        'l101':['t101': ['s101', 's102']], 
        'l102': ['t102', ['s101', 's102', 's103']]
 }


try: 
	class_person, class_teacher, class_student, class_lecture = exercise_1([p, q, r])
	print("Exercise 1 Attempted")
except:
	raise Exception("Not Attempted")

try:
	p = class_person()
	raise Exception("Unsuccessful")
except:
	print("Task 1 Successful")

try:
	t = class_teacher()
	raise Exception("Unsuccessful")
except:
	print("Task 2.1 Successful")

try:
	s = class_student()
	raise Exception("Unsuccessful")
except:
	print("Task 2.2 Successful")

try:
	l = class_lecture()
	raise Exception("Unsuccessful")
except:
	print("Task 3 Successful")

try:
	_ = l + s
	raise Exception("Unsuccessful")
except:
	print("Task 5 Successful")

