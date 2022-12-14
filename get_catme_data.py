"""
===============================================================================
ENGR 13300 Fall 2022

Program Description
    Gets a bunch of data from the Catme website for reverse engineering

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

# Import for type hinting
from typing import List, Tuple

# The number of questions the catme asks
NUMBER_OF_QUESTIONS = 5

# Seconds to wait before trying to locate an element again
TRY_AGAIN_TIME = 5

# The 1st dimension of the list are the different questions.
# The keys are the sentences that affect that question.
# The values[0] are the sum of all the ratings based on that sentence.
# The values[1] are the number of times that question has showed up.
results = [{}] * NUMBER_OF_QUESTIONS

# The number of failed tests
failed_tests = 0

# Whether or not the current test has failed
current_test_failed = False

def main():
    global current_test_failed
    TIMES_TO_RUN = 1000

    # Using Chrome to access web
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    for i in range(TIMES_TO_RUN):
        current_test_failed = False
        print(f'Running: {i + 1} / {TIMES_TO_RUN}')
        get_results(driver)

    write_results()

    print(f'Done! ({failed_tests} / {TIMES_TO_RUN} tests failed)')

# Fills out one Catme survey and gets its data
def get_results(driver) -> None:
    global current_test_failed
    navigate_to_questions(driver)

    # Fill out each of the questions
    for i in range(NUMBER_OF_QUESTIONS):
        fill_out_question(driver)
        go_to_next_question(driver)
    
    # Get the results
    for i in range(NUMBER_OF_QUESTIONS):
        find_reasons_and_rating(driver, i)

# Presses the "complete activity" button to get to the questions
def navigate_to_questions(driver) -> None:
    global current_test_failed
    # Open the website
    driver.get('https://www.catme.org/login/survey_demo_team')

    # Find and click on list of courses
    complete_activity_button = find_element(driver, 'name', 'action')
    if current_test_failed: return

    complete_activity_button.click()

# Chooses an arbitrary answer for each person
def fill_out_question(driver) -> None:
    global current_test_failed
    # Find and click a rating for each person
    person_1_button = find_element(driver, 'name', 'person0')
    if current_test_failed: return
    person_2_button = find_element(driver, 'name', 'person1')
    if current_test_failed: return
    person_3_button = find_element(driver, 'name', 'person2')
    if current_test_failed: return

    person_1_button.click()
    person_2_button.click()
    person_3_button.click()

# Finds out what the correct answer was for each person
def find_reasons_and_rating(driver, question: int) -> None:
    global current_test_failed, failed_tests
    # The number of rows that we can choose
    NUMBER_OF_ROWS = 5

    # The people we still haven't found the correct answer for yet
    not_found_yet = [0, 1, 2]

    # Iterate through each row
    for i in range(NUMBER_OF_ROWS):
        # Create a temporary not_found_yet because removing elements from the actual not_found_yet
        # List while still in the for loop will cause weird stuff to happen
        temp_not_found_yet = not_found_yet.copy()

        # Get the row
        row = find_element(driver, By.XPATH, f'//section/div/table[{question + 1}]/tbody/tr[{i+5}]')
        if current_test_failed: return

        # Test if that row was the correct answer for any of them
        for j in not_found_yet:
            
            # Test if the correct answer is in that row
            try:
                reasons = row.find_element('id', f'info{j}{question + 1}').get_attribute('textContent')
            except NoSuchElementException:
                continue

            # Do these if the correct answer is in that row
            temp_not_found_yet.remove(j)
            reasons_list, rating = get_reasons_and_rating(reasons, i)
            record_reasons_and_rating(question, reasons_list, rating)
        
        # Make the changes
        not_found_yet = temp_not_found_yet.copy()

        # If we've found everything (the not_found_yet list is empty), then we can return
        if not not_found_yet:
            return
    
    print("couldn't find correct answer, moving on to next test")
    failed_tests += 1
    current_test_failed = True

# Returns a list of the reasons why that choice should have been the correct answer
# (Catme tells you what sentences should've affected your answer for each question)
def get_reasons_and_rating(reasons: str, row_num: int) -> Tuple[List[str], int]:
    # Calculate the rating based on the current row
    rating = 5 - row_num

    # Remove the unnecessary content from the text
    reasons = reasons.replace("The behaviors described in the phrase '", "")
    reasons = reasons.replace(".' should have resulted in the rating described for this factor.", "")

    # Split the text into its sentences
    reasons_list = reasons.split('.')
    for i in range(len(reasons_list)):

        # Remove unnecessary whitespace
        reasons_list[i] = reasons_list[i].strip()
    
    return reasons_list, rating

# Saves the results into the results list (a global variable defined near the top of this program)
def record_reasons_and_rating(question: int, reasons_list: List[str], rating: int) -> None:
    # Copy the corresponding dictionary (I hate that I have to do this stupidity)
    question_results = results[question].copy()

    # Iterate through each reason in reasons
    for reason in reasons_list:

        # Add the reason to the results dictionary
        if reason in question_results:
            question_results[reason][0] += rating
            question_results[reason][1] += 1
        else:
            question_results[reason] = [rating, 1]
    
    # Add the changed dictionary back into results
    results[question] = question_results

# Presses the next button to go to the next question.
def go_to_next_question(driver) -> None:
    global current_test_failed
    # Find and click the next button
    next_button = find_element(driver, By.XPATH, '//form[2]/section/table/tbody/tr/td[3]/input')
    if current_test_failed: return

    next_button.click()

# A version of driver.find_element that will signal the program to move on to the
# next test instead of throwing an error (now that I think about it I could've just surrounded)
# lines 74 - 76 with try catch and it would've been so much easier)
def find_element(driver, find_method, method_value: str):
    global current_test_failed, failed_tests
    if current_test_failed: return
    try:
        return driver.find_element(find_method, method_value)
    except NoSuchElementException:
        # Print the error and move on
        print('ran into NoSuchElementException, moving on to next test')
        failed_tests += 1
        current_test_failed = True

# Saves the results to results.csv
def write_results() -> None:
    with open('results.csv', 'w') as file:
        file.write('Question Number,Reason,Sum,Frequency\n')
        for i in range(len(results)):
            for key in results[i]:
                file.write(f'{i},')
                file.write(f'"{key}",')
                file.write(f'{results[i][key][0]},')
                file.write(f'{results[i][key][1]}\n')

if __name__ == '__main__':
    main()