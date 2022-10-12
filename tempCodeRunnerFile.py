def go_to_next_question(driver) -> None:
    global current_test_failed
    if current_test_failed: return
    # find and click the next button
    next_button = find_element(driver, By.XPATH, '//form[2]/section/table/tbody/tr/td[3]/input')
    if current_test_failed: return

    next_button.click()