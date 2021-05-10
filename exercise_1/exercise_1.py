from abc import ABC, abstractmethod

#Example input
p = ['Teacher Andy', 'Teacher Blake', 'Teacher Canon']
q = ['Student Alex', 'Student Bethany', 'Student Carlson', 'Student Daniel']
r = {
    'l101': ['Teacher Blake', ['Student Alex', 'Student Bethany']], 
    'l102': ['Teacher Andy', ['Student Bethany', 'Student Carlson']],
    'l103': ['Teacher Canon', ['Student Bethany', 'Student Alex']],
    'l104': ['Teacher Andy', ['Student Bethany', 'Student Daniel']],
    'l105': ['A',['B']]
}
inp = [p, q, r]

#Task 6 - done
studentnum = 0
teachernum = 0

#Task 1 - without natural error
class Person(ABC):

    name = ''

    @abstractmethod
    def get_attributes(self):
        pass

#Task 2.1 - done
class Student(Person):

    def __init__(self, name):
        self.name = name
        self.lecture_enrolled = set()
        #Task 6.1 - assigning student_id on the go
        global studentnum
        studentnum += 1
        self.student_id = "S" + str(studentnum + 1000)
    
    #Task 5.2
    def __add__(self,other):
        print("Please assign new student to lecture using \"lecture + new_student\" instead.")
        return other

    def get_attributes(self):
        try:
            return { student_id : lecture_enrolled }
        except:
            return

#Task 2.2 - done
class Teacher(Person):

    def __init__(self, name):
        self.name = name
        self.lecture_taught = ""
        #Task 6.2 - assigning teacher_id on the go
        global teachernum
        teachernum += 1
        self.teacher_id = "T" + str(teachernum + 2000)
    
    def get_attributes(self):
        try:
            return { teacher_id : lecture_taught }
        except:
            return

#Task 3 - done
class Lecture:

    def __init__(self, lecid):
        self.lecture_id = lecid
        self.students = set()

    def assign_teacher(self, lecturer):
        if lecturer.lecture_taught == "":
            self.lecturer = lecturer
            lecturer.lecture_taught = self.lecture_id
        else:
            #Task 4.1 - done
            print(lecturer.name, "cannot be assigned to teach", self.lecture_id)
            print("Reason:", lecturer.name, "is already assigned to", lecturer.lecture_taught, "\n")

    def get_teacher(self):
        #print("Lecturer name:",self.lecturer)
        try:
            return self.lecturer.name
        except:
            return "no lecturer assigned."
    
    def assign_students(self, stu):
        if len(stu.lecture_enrolled) < 3:
            self.students.add(stu)
            stu.lecture_enrolled.add(self.lecture_id)
        else:
            #Task 4.2 - done
            print(stu.name, "cannot enroll to", self.lecture_id)
            print("Reason:", stu.name, "already enrolled to maximum of 3 lectures\n")
    
    def get_students(self):
        if len(self.students) != 0:
            return self.students
        else:
            return False
    
    #Task 5.1
    def __add__(self, new_student):
        self.assign_students(new_student)
        return self

def exercise_1(inputs): # DO NOT CHANGE THIS LINE
    """
    This functions receives the input in the parameter 'inputs'. 
    Change the code, so that the output is sqaure of the given input.
    
    p, q, r = inputs
    
    p => ['t101', 't102', 't103']
    q => ['s101', 's102', 's103']
    r => {
        'l101':['t101': ['s101', 's102']], 
        'l102': ['s101', 's102', 's103']]
    }
    
    p = Person()
    s = Student()
    t = Teacher()
    l = Lecture()
    
    output = {
        1: [Person, p], 
        2: [Teacher, Student, t, s], 
        3: [Lecture, l], 
        4: [Lecture, l], 
        5: [Lecture, Student, l, s], 
        6: [Teacher, Student, t, s]
    }
    """
    #Creating dictionary of instances of student, with students' name as keys
    stu = {}
    for x in inputs[1]:
        stu[x] = Student(x)

    #Creating dictionary of instances of teacher, with teachers' name as keys
    tea = {}
    for x in inputs[0]:
       tea[x] = Teacher(x)

    #Creating dictionary of instances of lecture, with lecture ID as keys
    lec = {}
    for x in inputs[2]:
        lec[x] = Lecture(x)
        try:
           lec[x].assign_teacher(tea[inputs[2][x][0]])
        except:
            print("No teacher with name", inputs[2][x][0], "in this system")
        for y in inputs[2][x][1]:
            try:
                #lec[x].assign_students(stu[y])
                lec[x] = lec[x] + stu[y]
            except:
                print("No student with name", y, "in this system")

    #Code for debugging each variable (stu,tea,lec)
    print()
    for x in lec:
        print("Lecture code",lec[x].lecture_id, "has", lec[x].get_teacher())
        print("Lecture participant(s):")
        if not lec[x].get_students():
            print("No student enrolled to this lecture.")
        else:
            for y in lec[x].get_students():
                print(">", y.name)
        print()

    print()
    for x in stu:
        print(stu[x].name, "has enrolled in lecture:", *sorted(stu[x].lecture_enrolled))

    print()
    for x in tea:
        print(tea[x].name, "is in charge of lecture", tea[x].lecture_taught)
 
    output = {
        1: [Person], 
        2: [Teacher, Student, tea, stu], 
        3: [Lecture, lec], 
        4: [Lecture, lec], 
        5: [Lecture, Student, lec, stu],
        6: [Teacher, Student, tea, stu]
    }

    return output       # DO NOT CHANGE THIS LINE

#exercise_1(inp)
