from sys import exit
import os
import random
import time
from selenium.webdriver.common.keys import Keys

from helpers.scraper import Scraper
from helpers.utility import formatted_time, data_countdown, countdown, execution_time
from helpers.files import read_csv, read_txt, write_to_csv, write_to_txt, read_txt_in_dict, pd_read_csv
from helpers.numbers import formatted_number_with_comma, numbers_within_str, str_to_int

def search():
    job_keyword, job_location = keyword['job_keyword'], keyword['job_location']
    # d.sleep(1, 3)
    d.element_send_keys(job_keyword, '#text-input-what')

    if job_location:
        d.element_send_keys(job_location, '#text-input-where')

    # Search job button
    d.sleep(0.3, 1.0)
    d.element_click('.yosegi-InlineWhatWhere-primaryButton')


def get_ans(q, type):
    
    for data in q_ans:
        # print(data[1])
        if str(data[1]).lower().strip() in q.lower().strip():
            ans = data[2].strip()
            break
    else:
        print('Cannot answer this question,')
        print('Question:', q)
        ans = input('Your Answer: ')
        
        # Add question to database
        q_ans.append([type, q.strip(), ans.strip()])
        write_to_csv(q_ans, ['type','keyword','answer'], 'inputs/q_ans.csv')
    
    return ans

def handle_question(type, q_div):
    
    if type == 'text' or type == 'textarea':
        quesn = d.find_element('label', ref_element=q_div).text
        ans = get_ans(quesn, type)
        if ans:
            if type == 'textarea':
                d.element_send_keys(ans, 'textarea', ref_element=q_div)
            else:
                d.element_send_keys(ans, 'input', ref_element=q_div)
    elif type == 'radio':
        quesn = d.find_element('legend', ref_element=q_div).text
        ans = get_ans(quesn, type)
        if ans:
            options = d.find_elements('label', ref_element=q_div)
            for op in options:
                if ans.lower() in op.text.lower():
                    op.click()
                    break
    elif type == 'select':
        quesn = d.find_element('label', ref_element=q_div).text
        ans = get_ans(quesn, type)
        if ans:
            options = d.find_elements('option', ref_element=q_div)
            for op in options:
                value = op.text
                if ans.lower() in value.lower():
                    d.select_dropdown('select', text=value, ref_element=q_div)
                    break
    elif type == 'unknown':
        quesn = d.find_element('label', ref_element=q_div).text
        if '(optional)' in quesn.lower():
            pass
        else:
            input('Cannot determine the type of the question: ', quesn)
            
def loop_questions(questions_div):
    for q in questions_div:
        input_box = d.find_element_no_wait('input', ref_element=q, exit_on_missing_element=False)
        if input_box:
            input_type = input_box.get_attribute('type')
            if input_type == 'text' or input_type == 'number':
                handle_question(type='text', q_div=q)
            elif input_type == 'radio':
                handle_question(type='radio', q_div=q)
            else:
                handle_question(type='unknown', q_div=q)            
        elif d.find_element_no_wait('select', ref_element=q, exit_on_missing_element=False):
            handle_question(type='select', q_div=q)
        elif d.find_element_no_wait('textarea', ref_element=q, exit_on_missing_element=False):
            handle_question(type='textarea', q_div=q)
        else:
            handle_question(type='unknown', q_div=q)
        
def apply_on_current_job():

    phone_number = keyword['phone_number']
    d.switch_to_tab(1)
    if d.element_send_keys(phone_number, '#input-phoneNumber', exit_on_missing_element=False):
        d.element_click('button[class*="continue"]')
    
    #Select resume
    d.element_click('#resume-display-buttonHeader', exit_on_missing_element=False)
    d.sleep(1, 2)
    d.element_click('button[class*="continue"]')
    
    # Answer questions
    d.sleep(8, 10, True)
    questions_div = d.find_elements('div[id^="q_"]')
    loop_questions(questions_div)
    
    # Continue
    d.sleep(2, 3, True)
    d.element_click('button[class*="continue"]')

    # Answer questions
    d.sleep(5, 7)
    questions_div = d.find_elements('div[id^="q_"]')
    if questions_div:
        loop_questions(questions_div)
    
    # Continue
    d.sleep(2, 3, True)
    d.element_click('button[class*="continue"]', exit_on_missing_element=False)
    d.sleep(2, 3)
    
    # Review and submit button
    d.sleep(2, 3, True)
    d.element_click('button[class*="continue"]', exit_on_missing_element=False)
    
    # Success confirmation
    d.sleep(1, 2)
    success = d.find_element('div[class*="ia-BasePage-component"] h1', exit_on_missing_element=False)
    if success and success.text == 'Your application has been submitted!':
        return True
    return False

def apply_job(email, password, title, location, no_of_job):
    global keyword, q_ans, d
    keyword = {'job_keyword': title, 'job_location': location, 'phone_number' : '3143129164'}
    no_of_job = int(no_of_job)

    q_ans = read_csv('inputs/q_ans.csv')

    url = 'https://www.indeed.com'
    d = Scraper(url, exit_on_missing_element=False, profile="indeed")
    # d.print_executable_path()
    
    d.go_to_page(url)
    d.add_login_functionality('#AccountMenu')
    print('Logged in')
    
    if title:
        search()
    
    #job results
    count = 0
    while count <= no_of_job:
        d.sleep(3, 4)
        jobs = d.find_elements('a[id^="job_"]')
        print('\nLen of jobs: ', len(jobs))
        for job in jobs:
            d.element_click(element=job)
                
            iframe = d.find_element('iframe[title="Selected Job Details"]')
            d.driver.switch_to.frame(iframe)
            apply_btn = d.find_element('#indeedApplyButton', exit_on_missing_element=False, wait_element_time=0.1)
            if apply_btn:
                d.element_click(element=apply_btn)
                success = apply_on_current_job()
                if success:
                    count += 1
                    data_countdown(f'{count} job applied')
                    time.sleep(1)
                d.close_tab_and_back_homepage()
            else:
                d.driver.switch_to.default_content()

        # Go to next page
        if d.element_click('a[aria-label="Next Page"]') == None:
            break
    
    d.driver.quit()


# apply_job()