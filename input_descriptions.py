"""
===============================================================================
ENGR 13300 Fall 2022

Program Description
    Prompts the user for the 3 descriptions and then generates the correct
    answers for each of them

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

import calculate_answers


def main():
    description_names = ['first', 'second', 'third']

    descriptions = []

    # Prompt the user for the descriptions
    for name in description_names:
        descriptions.append(input(f'Enter the {name} description:\n'))

    answers = calculate_answers.calculate_answers(descriptions)

    print(answers)

if __name__ == '__main__':
    main()


