# Exercise 1 - Playing with Classes

Task 1 - Create an abstract class `Person` with only an attribute `name` (string) and an abstract method `get_attributes` which returns an natural error if it is not overriden by inherited class

Task 2.1 - Create a concrete class `Student` with attributes `student_id` (string) and `lectures_enrolled` (list of strings), it inherits the class Person.  
Task 2.2 - Create a concrete class `Teacher` with attributes `teacher_id` (string) and `lecture_taught` (string), it also inherits the class Person. 

Task 3 - Create a class `Lecture` which has an attribute `lecture_id` (string). 
		 It has a function `assign_teacher` which takes an instance of `Teacher` and assigns it to a variable `lecturer`, and a counter function `get_teacher` which returns the name of the teacher of the lecture. 
		 It also has a function `assign_students` which takes an instance of `Student` and adds to a variable `students`, and a counter function `get_students` which returns the name of the students in the lecture.

Task 4.1 - Return a natural error when two or more teachers are assigned a common lecture. 
Task 4.2 - Return a natural error when any students takes more than 3 lectures. 

Task 5.1 - Allow assigning students to the lecture with `+` operator. Example: `lecture + new_student`
Task 5.2 - Return a natural error for Task 5 when `+` is abused as `new_student + lecture`.

Task 6 - Assign the student_id and teacher_id, on the go with one to one assignment. 


You will receive a list of names of teachers and a list of names of students, and a dictionary with keys as lectures and a values is a 2 element list whose first element is name of teacher and second element is list of students in the class. 
Outputs shoud be a dictionary with key value as int of the task, and values should be class and class instances involved in the task.
