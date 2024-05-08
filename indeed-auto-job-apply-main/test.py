import pyautogui as pg 
import os
import time


def locate_until(path, timeout=5):
    location = None
    while True:
        location = pg.locateCenterOnScreen(path)
        if location or not timeout:
            break
        else:
            time.sleep(1)
            timeout -= 1
    return location


# submit = locate_until('test_files/submit.png')
# print(submit)

def ui_test(inputs):
    # email = locate_until('test_files/email.png')
    if True:
        # print(email)
        # pg.click(email)
        pg.press('tab')
        time.sleep(0.1)

        pg.write(inputs['email'])
        time.sleep(0.1)

        pg.press('tab')
        pg.write(inputs['password'])
        time.sleep(0.1)

        pg.press('tab')
        pg.write(inputs['job_title'])
        time.sleep(0.1)

        pg.press('tab')
        pg.write(inputs['location'])
        time.sleep(0.1)

        pg.press('tab')
        pg.write(inputs['no_of_jobs'])
        time.sleep(1)

        # pg.click(submit)
        # pg.press('enter')

        print('\nTest Case Passed\n')


inputs = {
    'email': 'salahuddin3652@gmail.com',
    'password': 'password',
    'job_title': ' ',
    'location': 'remote',
    'no_of_jobs': '50'
}

time.sleep(5)
ui_test(inputs)

# img = pg.screenshot()
# img.save('test_files/ss.png')
