from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

# Initialize Chrome WebDriver
driver = webdriver.Chrome()

# Step 1: Open the quiz website
quiz_url = "https://lms2.ai.saveetha.in/mod/quiz/view.php?id=2563"
driver.get(quiz_url)

# Step 2: Handle authentication
# Verify these selectors are correct; update if needed
username_field = driver.find_element(By.ID, "username")
username_field.send_keys("23002539")
password_field = driver.find_element(By.ID, "password")
password_field.send_keys("jjj")
login_button = driver.find_element(By.ID, "loginbtn")
login_button.click()

# Wait for quiz page to load
# Using XPath for "Attempt quiz" button (adjust text if different)
try:
    attempt_quiz_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Attempt quiz')]"))
    )
except TimeoutException:
    print("Timeout: Could not find the 'Attempt quiz' button. Check the page load or button text.")
    driver.save_screenshot("attempt_error.png")
    print(driver.page_source)
    driver.quit()
    exit()

# Step 3: Access the quiz
attempt_quiz_button.click()

# Step 4: Open Grok in a new tab
# Replace with the actual Grok URL (https://chatgpt.com/ was incorrect)
grok_url = "https://chatgpt.com/"  # Update with actual Grok URL
driver.execute_script(f"window.open('{grok_url}', '_blank');")

# Store window handles
quiz_window = driver.window_handles[0]
grok_window = driver.window_handles[1]

# Switch back to quiz window
driver.switch_to.window(quiz_window)

# Step 5: Process each question
while True:
    # Wait for question to load
    # Replace "qtext" with the actual class or ID of the question text element
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "qtext")))
    except TimeoutException:
        print("Timeout: Could not find question text element. Check the selector.")
        driver.save_screenshot("question_error.png")
        print(driver.page_source)
        break

    # Extract question text
    question_elem = driver.find_element(By.CLASS_NAME, "qtext")
    question_text = question_elem.text
    print(f"Question: {question_text}")  # Debug: Verify question text

    # Switch to Grok window
    driver.switch_to.window(grok_window)

    # Send question to Grok
    # Replace "prompt-input" with the actual ID or selector of Grok's input field
    try:
        grok_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "prompt-input"))
        )
        grok_input.clear()
        grok_input.send_keys(question_text)
        grok_input.send_keys(Keys.RETURN)
    except TimeoutException:
        print("Timeout: Could not find Grok input field. Check the selector.")
        driver.save_screenshot("grok_input_error.png")
        break

    # Wait for Grok's response
    # Replace "response" with the actual class or ID of Grok's response element
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "response")))
        answer_elem = driver.find_element(By.CLASS_NAME, "response")
        answer = answer_elem.text.strip().lower()  # Assuming answer is "a", "b", "c", or "d"
        print(f"Grok Answer: {answer}")  # Debug: Verify answer
    except TimeoutException:
        print("Timeout: Could not find Grok response. Check the selector.")
        driver.save_screenshot("grok_response_error.png")
        break

    # Switch back to quiz window
    driver.switch_to.window(quiz_window)

    # Select the answer
    try:
        radio = driver.find_element(By.XPATH, f"//input[@type='radio' and @value='{answer}']")
        radio.click()
    except:
        print(f"Could not find radio button '{answer}' for question: {question_text}")

    # Click "Next" button if present
    # Replace "mod_quiz-next-nav" with the actual ID of the "Next" button
    next_buttons = driver.find_elements(By.ID, "mod_quiz-next-nav")
    if next_buttons:
        next_buttons[0].click()
        # Wait for the next question
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "qtext")))
    else:
        break

# Step 6: Submit the quiz
# Using XPath for "Submit all and finish" button
try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Submit all and finish')]"))
    )
    submit_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Submit all and finish')]")
    submit_button.click()
except TimeoutException:
    print("Timeout: Could not find the 'Submit all and finish' button. Check the selector.")
    driver.save_screenshot("submit_error.png")
    driver.quit()
    exit()

# Close the browser
driver.quit()
