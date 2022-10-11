"""
===============================================================================
ENGR 13300 Fall 2022

Program Description
    Prompts the user for the 3 descriptions and then generates the correct
    answers for each of the questions

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

# import for type hinting
from typing import List, Dict, Tuple

# import for reading csv file easier
import csv

def main():
    description_names = ['first', 'second', 'third']

    data = interpret_data()

    descriptions = []

    for name in description_names:
        descriptions.append(input(f'Enter the {name} description:\n'))

    answers = calculate_answers(descriptions, data)

    print(answers)

def calculate_answers(descriptions: Tuple[int], data: Dict[str, List[Tuple[int, int]]]) -> Tuple[Tuple[int]]:
    NUMBER_OF_QUESTIONS = 5

    answers = []

    for description in descriptions:
        description = format_description(description)
        answers.append(calculate_paragraph_ratings(description, data, NUMBER_OF_QUESTIONS))
    
    # make it so then in answers[n][m], n is the question and m is the person 
    return tuple(zip(*answers[::]))

def format_description(description: str) -> List[str]:
    # split the description into sentences
    description = description.strip('. ').lower().split('.')

    # remove unnecessary whitespace
    for i in range(len(description)):
        description[i] = description[i].strip()
    
    return description

# returns a dictionary with
# the keys being the sentences
# the indexes of the values are how we store the different tuples (if the sentence affects more than one question we need to have more than one tuple)
# the first index of the tuple being the question number
# the second index of the tuple being what rating the sentence corresponds to
def interpret_data() -> Dict[str, List[Tuple[int, int]]]:
    data = {}
    with open('results.csv', 'r') as file:
        # skip the first line
        file.readline()

        # open the file with csv.reader to make it easier to separate data into columns
        csv_reader = csv.reader(file)

        for line in csv_reader:
            # give all the data names
            question_num = int(line[0])
            sentence = line[1].lower()
            summation = int(line[2])
            frequency = int(line[3])
            rating = calculate_sentence_rating(summation, frequency)

            # add the data to the data dictionary
            if sentence in data:
                data[sentence].append((question_num, rating))
            else:
                data[sentence] = [(question_num, rating)]
    
    return data

def calculate_sentence_rating(summation: int, frequency: int) -> int:
    ratio = summation / frequency # in python we don't have to worry about integer division lol
    if ratio >= 4:
        return 5
    if ratio == 4:
        return 4
    if ratio > 2:
        return 3
    if ratio == 2:
        return 2
    return 1

def calculate_paragraph_ratings(description: List[str], data: Dict[str, List[Tuple[int, int]]], NUMBER_OF_QUESTIONS: int) -> List[int]:
    # the answer for each question from 1-5
    paragraph_ratings = [0] * NUMBER_OF_QUESTIONS
    for sentence in description:
        if sentence not in data:
            raise RuntimeError(f'sentence: {sentence} could not found in the data')
        for result in data[sentence]:
            # give the data names
            (question_num, rating) = result

            if paragraph_ratings[question_num] == 0: # if no other sentence has been found yet that affects the answer to that question
                paragraph_ratings[question_num] = rating
                continue
            
            rating_sum = paragraph_ratings[question_num] + rating

            # we only need to change the paragraph rating if the sentence ratings are 1 and 3 or 3 and 5
            if rating_sum == 8:
                paragraph_ratings[question_num] = 4
            elif rating_sum == 4:
                paragraph_ratings[question_num] = 2
    
    return paragraph_ratings

if __name__ == '__main__':
    main()