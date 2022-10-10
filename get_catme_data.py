"""
===============================================================================
ENGR 13300 Fall 2022

Program Description
    Gets a bunch of data from the catme website for reverse engineering

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

# Import selenium for web driving
from selenium import webdriver

# Import By for finding by XPath
from selenium.webdriver.common.by import By

# Helps when using try catch when trying to find an element
from selenium.common.exceptions import NoSuchElementException

# Import the stuff to download the Chrome driver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Import time for pausing
import time

# Import list for type hinting
from typing import List, Tuple

# The number of questions the catme asks
NUMBER_OF_QUESTIONS = 5

# The 1st dimension of the list are the different questions.
# The keys are the sentences that affect that question.
# The values[0] are the sum of all the ratings based on that sentence.
# The values[1] are the number of times that question has showed up.
results = [{}] * NUMBER_OF_QUESTIONS


def main():
    # Using Chrome to access web
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    # Get the results
    navigate_to_questions(driver)
    for i in range(NUMBER_OF_QUESTIONS):
        fill_out_questions(driver)
        find_reasons_and_rating(driver, i)
        go_to_next_question(driver)
    
    # print(results)

    # print the results
    for question in results:
        for key in question:
            print(key, end=' ')
            print(question[key])
        print()
    
    time.sleep(10000)

def navigate_to_questions(driver) -> None:
    # Open the website
    driver.get('https://www.catme.org/login/survey_demo_team')

    # Find and click on list of courses
    complete_activity_button = driver.find_element('name', 'action')

    complete_activity_button.click()

def fill_out_questions(driver) -> None:
    # Find and click a rating for each person
    person_1_button = driver.find_element('name', 'person0')
    person_2_button = driver.find_element('name', 'person1')
    person_3_button = driver.find_element('name', 'person2')

    person_1_button.click()
    person_2_button.click()
    person_3_button.click()

    # Find and click the reveal answers button
    reveal_answers_button = driver.find_element(By.XPATH, '//form[2]/section/table/tbody/tr/td[2]/input')

    reveal_answers_button.click()

def find_reasons_and_rating(driver, question: int) -> None:
    # the number of rows that we can choose
    NUMBER_OF_ROWS = 5

    # iterate through each row
    for i in range(NUMBER_OF_ROWS):

        # get the row
        row = driver.find_element(By.XPATH, f'//form[2]/section/div/table/tbody/tr[{i+5}]')

        # test if that row was the correct answer for any of them
        for j in range(3):
            try:
                reasons = row.find_element('id', f'info{j}{question + 1}').get_attribute('textContent')
            except NoSuchElementException:
                continue

            reasons_list, rating = get_reasons_and_rating(reasons, i)
            record_reasons_and_rating(question, reasons_list, rating)

def get_reasons_and_rating(reasons: str, row_num: int) -> Tuple[List[str], int]:
    # calculate the rating based on the current row
    rating = 5 - row_num

    # remove the unnecessary content from the text
    reasons = reasons.replace("The behaviors described in the phrase '", "")
    reasons = reasons.replace(".' should have resulted in the rating described for this factor.", "")

    # split the text into its sentences
    reasons_list = reasons.split('.')
    for i in range(len(reasons_list)):

        # remove unnecessary whitespace
        reasons_list[i] = reasons_list[i].strip()
    
    return reasons_list, rating

def record_reasons_and_rating(question: int, reasons_list: List[str], rating: int) -> None:
    # copy the corresponding dictionary (I hate that I have to do this stupidity)
    question_results = results[question].copy()

    # iterate through each reason in reasons
    for reason in reasons_list:

        # add the reason to the results dictionary
        if reason in question_results:
            question_results[reason][0] += rating
            question_results[reason][1] += 1
        else:
            question_results[reason] = [rating, 1]
    
    # add the changed dictionary back into results
    results[question] = question_results

def go_to_next_question(driver) -> None:
    # find and click the next button
    next_button = driver.find_element(By.XPATH, '//form[2]/section/table/tbody/tr/td[3]/input')

    next_button.click()

if __name__ == '__main__':
    main()