# Import for type hinting
from typing import List, Dict, Tuple

# Import for reading csv file easier
import csv

def calculate_answers(descriptions: Tuple[int]) -> Tuple[Tuple[int]]:
    NUMBER_OF_QUESTIONS = 5

    answers = []

    # Calculate the answers for each of the descriptions
    for description in descriptions:
        description = format_description(description)
        answers.append(calculate_paragraph_ratings(description, NUMBER_OF_QUESTIONS))
    
    # Make it so then the tuple that we return is tuple[n][m], where n is the question and m is the person 
    return tuple(zip(*answers[::]))

def format_description(description: str) -> List[str]:
    # Split the description into sentences
    description = description.strip('. ').lower().split('.')

    # Remove unnecessary whitespace
    for i in range(len(description)):
        description[i] = description[i].strip()
    
    return description

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