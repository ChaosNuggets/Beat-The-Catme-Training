"""
===============================================================================
ENGR 13300 Fall 2022

Program Description
    Has a bunch of functions that help calculate what the correct answers are

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

# Import for type hinting
from typing import List, Dict, Tuple

# Import for reading csv file easier
import csv

# Takes in a list of descriptions as the argument and returns the answers
def calculate_answers(descriptions: Tuple[int]) -> Tuple[Tuple[int]]:
    NUMBER_OF_QUESTIONS = 5

    answers = []

    # Calculate the answers for each of the descriptions
    for description in descriptions:
        description = format_description(description)
        answers.append(calculate_paragraph_ratings(description, NUMBER_OF_QUESTIONS))
    
    # Make it so then the tuple that we return is tuple[n][m], where n is the question and m is the person 
    return tuple(zip(*answers[::]))

# Splits a description into a list of sentences
def format_description(description: str) -> List[str]:
    # Split the description into sentences
    description = description.strip('. ').lower().split('.')

    # Remove unnecessary whitespace
    for i in range(len(description)):
        description[i] = description[i].strip()
    
    return description

# Interprets the data in results.csv.
# Returns a dictionary with
# the keys being the sentences
# the indexes of the values are how we store the different tuples (if the sentence affects more than one question we need to have more than one tuple)
# the first index of the tuple being the question number
# the second index of the tuple being what rating the sentence corresponds to
def interpret_data() -> Dict[str, List[Tuple[int, int]]]:
    data = {}
    with open('results.csv', 'r') as file:
        # Skip the first line
        file.readline()

        # Open the file with csv.reader to make it easier to separate data into columns
        csv_reader = csv.reader(file)

        for line in csv_reader:
            # Give all the data names
            question_num = int(line[0])
            sentence = line[1].lower()
            summation = int(line[2])
            frequency = int(line[3])
            rating = calculate_sentence_rating(summation, frequency)

            # Add the data to the data dictionary
            if sentence in data:
                data[sentence].append((question_num, rating))
            else:
                data[sentence] = [(question_num, rating)]
    
    return data

# Given the sum of all the ratings and the amount of times that sentence appeared in the surveys,
# return the rating for that sentence.
def calculate_sentence_rating(summation: int, frequency: int) -> int:
    ratio = summation / frequency # In python we don't have to worry about integer division lol
    if ratio > 4:
        return 5
    if ratio == 4:
        return 4
    if ratio > 2:
        return 3
    if ratio == 2:
        return 2
    return 1

# Given one description, calculate the answer to each question
def calculate_paragraph_ratings(description: List[str], NUMBER_OF_QUESTIONS: int) -> List[int]:
    # The answer for each question from 1-5
    paragraph_ratings = [0] * NUMBER_OF_QUESTIONS
    for sentence in description:
        if sentence not in data:
            raise RuntimeError(f'sentence "{sentence}" could not be found in the data')
        for result in data[sentence]:
            # Give the data names
            (question_num, rating) = result

            if paragraph_ratings[question_num] == 0: # if no other sentence has been found yet that affects the answer to that question
                paragraph_ratings[question_num] = rating
                continue
            
            rating_sum = paragraph_ratings[question_num] + rating

            # Change the paragraph rating to the correct thing
            if 6 < rating_sum < 10:
                paragraph_ratings[question_num] = 4
            elif 2 < rating_sum < 6:
                paragraph_ratings[question_num] = 2
    
    return paragraph_ratings

# Interpret and organize the data
data = interpret_data()

# data_str = str(data)
# print(data_str.replace(')], ', ')],\n'))