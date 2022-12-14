"""
===============================================================================
ENGR 13300 Fall 2022

Program Description
    Tests if calculate_answers.py is actually correct by filling out
    TIMES_TO_RUN Catme surveys

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

# Import the stuff to download the Chrome driver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Import By for finding by XPath
from selenium.webdriver.common.by import By

# Helps when using try catch when trying to find an element
from selenium.common.exceptions import NoSuchElementException

# Import for pausing
import time

# Import for type hinting
from typing import List

# Import our algorithm for calculating the correct answers
import calculate_answers

current_test_failed = False
failed_tests = 0

NUMBER_OF_QUESTIONS = 5

def main():
    TIMES_TO_RUN = 10000

    # Using Chrome to access web
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    for i in range(TIMES_TO_RUN):
        print(f'running: {i + 1} / {TIMES_TO_RUN}')
        test_algorithm(driver)

# Fills out the correct answers for 1 Catme survey
def test_algorithm(driver) -> None:
    global current_test_failed
    current_test_failed = False
    navigate_to_descriptions(driver)
    descriptions = get_descriptions(driver)
    answers = calculate_answers.calculate_answers(descriptions)
    navigate_to_questions(driver)

    # Fill out each of the questions
    for i in range(NUMBER_OF_QUESTIONS):
        fill_out_questions(driver, answers[i])
        go_to_next_question(driver)
    
    try:
        if get_score(driver) < 30:
            print('we made a mistake somewhere')
            time.sleep(9999999)
    except ValueError:
        # Move to next test
        print('ran into ValueError, moving on to next test')
        failed_tests += 1
        current_test_failed = True
    

# Go to the first page of the Catme survey (which lists the descriptions)
def navigate_to_descriptions(driver) -> None:
    # Open the website
    driver.get('https://www.catme.org/login/survey_demo_team')

# Return the descriptions for each person
def get_descriptions(driver) -> List[str]:
    NUMBER_OF_DESCRIPTIONS = 3

    # Get the descriptions and fill the list
    descriptions = []
    for i in range(NUMBER_OF_DESCRIPTIONS):
        description = find_element(driver, By.XPATH, f'//section/dl/dd[{i + 1}]').get_attribute('textContent')
        if current_test_failed: return
        descriptions.append(description)
    
    return descriptions

# Presses the "complete activity" button to get to the questions
def navigate_to_questions(driver) -> None:
    global current_test_failed
    # Find and click on list of courses
    complete_activity_button = find_element(driver, 'name', 'action')
    if current_test_failed: return

    complete_activity_button.click()

# Given the correct answers as a parameter, it chooses the correct answer for each person
def fill_out_questions(driver, answers: List[int]) -> None:
    NUMBER_OF_ROWS = 5
    # Find and click a rating for each person
    for i in range(len(answers)):
        person_i_button = find_element(driver, By.XPATH, f'//form[2]/section/div/table/tbody/tr[{(NUMBER_OF_ROWS - answers[i]) + 5}]/td[{i + 1}]/input')
        if current_test_failed: return

        person_i_button.click()

# Clicks the next button to go to the next question in the Catme survey
def go_to_next_question(driver) -> None:
    # Find and click the next button
    next_button = find_element(driver, By.XPATH, '//form[2]/section/table/tbody/tr/td[3]/input')
    if current_test_failed: return

    next_button.click()

# Reads the text of the results page to see what score out of 30 we got
def get_score(driver) -> int:
    # Find the header with the score
    header = find_element(driver, 'id', 'page_title_h1_lbl').text
    return int(header.replace('Practice Scenario Results: Score ', '').replace(' of 30.', ''))

# A version of driver.find_element that will signal the program to move on to the
# next test instead of throwing an error (now that I think about it I could've just surrounded)
# lines 67 - 68 with try catch and it would've been so much easier)
def find_element(driver, find_method, method_value: str):
    global current_test_failed, failed_tests
    if current_test_failed: return
    try:
        return driver.find_element(find_method, method_value)
    except NoSuchElementException:
        # Move to next test
        print('ran into NoSuchElementException, moving on to next test')
        failed_tests += 1
        current_test_failed = True

if __name__ == '__main__':
    main()