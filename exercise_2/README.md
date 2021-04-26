# Exercise 2 - Playing with Data Structures

You were about to throw a party, however you realise there are many people to invite.
To keep a track of people you have invited and know the estimated number of attendees you create a program to keep a track of it.

Task 0.1: Create a class `Party` to keep track of the information about the party. It has one attribute a dictionary `info_attendees` which has family name as key and estimated number of attendees of the family as the value.
Task 0.2: Create a function `add_attendees` which takes `family_name` and `number_of_attendees` as parameters and add it to the attribute `info_attendees`.

Task 1.1: However, you decide to keep a special food and beverages for the kids. You can your invitees and ask them if they are bringing any kids with them. Create a function `detailed_attendees` which takes three lists `family_names`, `adult_attendees` and `child_attendees` and create a new attribute `detailed_info_attendees` which convert this information into a dictionary.
Task 1.2: You notice that after the re-enquiry there is some discrepancy in your two dictionaries `info_attendees` and `detailed_info_attendees`. Create a function, `check_and_resolve` which checks for any discrepancy and resolves it using comprehension.

Task 2.1: However, the number of COVID-19 cases has surged in your county and local administration has decided that any gathering in the county cannot have more than 50 people and to be cautious no children are allowed in the gathering. Create a function `get_total_attendees` which returns the estimated total number of attendees which you have invited both including adults and kids.
Task 2.2: You notice that the number of people you have invited is well above the permitted limit. To restrict the number of attendees, you decide that you will invite only 2 members per family and ask them to not bring anhy children with them. Create a function `filter_attendees` which return the names of families which have  either more than 2 members or if they are bringing atleast a child to the party using comprehension.

Task 3: Using your program you decide to call these families and let them know about the changes in situation and ask them to kindly bring only upto two adult family members to the party. Create a function `covid_changes` which does the same using comprehension.

Task 4.1: Even after this you notice that the number of attendees is more than 50. You then try to prioritise the families on a scale 0-5. Create a function `include_priority` which takes two lists `family_names` and `priorities` and add this information to your attribute `detailed_info_attendees`.

Task 4.2: Create a function `filter_priorities` which takes a value `priority` and returns the names of the families with less than of equal to the given priority using comprehension.
