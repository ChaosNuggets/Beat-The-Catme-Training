"""
===============================================================================
ENGR 13300 Fall 2022

Program Description
    The user enters the 3 descriptions as arguments and then this program
    prints the correct answers for each of them

Assignment Information
    Assignment:     Individual project
    Author:         Stanley So, sos@purdue.edu
    Team ID:        LC4 - 12

Contributor:    Name, login@purdue [repeat for each]
    My contributor(s) helped me:
    [ ] understand the assignment expectations without
        telling me how they will approach it.
    [ ] understand different ways to think about a solution
        without helping me plan my solution.
    [ ] think through the meaning of a specific error or
        bug present in my code without looking at my code.
    Note that if you helped somebody else with their code, you
    have to list that person as a contributor here as well.
    
ACADEMIC INTEGRITY STATEMENT
I have not used source code obtained from any other unauthorized
source, either modified or unmodified. Neither have I provided
access to my code to another. The project I am submitting
is my own original work.
===============================================================================
"""

import sys
import calculate_answers

def main():
    # get the descriptions from the command line arguments
    descriptions = sys.argv[1:]

    # remove the blank strings
    for argument in sys.argv[1:]:
        if argument == '':
            descriptions.remove(argument)

    # check if the user entered at least 1 description
    if len(descriptions) == 0:
        print('Please enter at least 1 description')
        return
    
    # check if the description is valid
    try:
        answers = calculate_answers.calculate_answers(descriptions)
    except RuntimeError as error:
        print(f'Error: {error}')
        return

    # print the description
    for i in range(len(answers)):
        for j in range(len(answers[0])):
            # print a comma and a space if there is another element to print
            if j < len(answers[0]) - 1:
                endstr = ', '
            else:
                endstr = ''
            
            # print a question mark if there was not enough data in the description to determine the rating
            if answers[i][j] == 0:
                thing_to_print = "idk"
            else:
                thing_to_print = str(answers[i][j])
            
            print(thing_to_print, end=endstr)
        
        # print a newline if there is another tuple to print
        if i < len(answers) - 1:
            print()

if __name__ == '__main__':
    main()


