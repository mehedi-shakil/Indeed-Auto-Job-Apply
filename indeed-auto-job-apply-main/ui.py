from tkinter import *
from apply_job import apply_job
import re


def start_apply():

    # print(job_title.get(), no_of_job.get(), location.get(), email.get(), password.get())

    email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if not re.fullmatch(email_regex, email.get()):
        msg_entry['text'] = "Email is invalid"

    else:
        msg_entry['text'] = "Applying Job..."
        msg_entry.pack()
        
        apply_job(email.get(), password.get(), job_title.get(), location.get(), no_of_job.get())
        
        msg_entry['text'] = "Apply Job Completed"
        msg_entry.pack()

def main():
    global job_title, no_of_job, location, email, password, msg_entry
    #Create an instance of Tkinter frame
    win= Tk()

    #Set the geometry of Tkinter frame
    win.title("Indeed Auto Job Apply")
    win.geometry("750x500")


        
    #Initialize a Label to display the User Input
    # label.pack()

    #User Email
    Label(win, text="Indeed email address:", font=("Courier 14")).pack()
    email= Entry(win, width= 40)
    email.pack()

    #User password
    Label(win, text="Indeed password:", font=("Courier 14")).pack()
    password= Entry(win, width= 40)
    password.pack()

    #Job Title/keyword
    Label(win, text="Job title, keyword:", font=("Courier 14")).pack()
    job_title= Entry(win, width= 40)
    job_title.pack()

    #Job Location
    Label(win, text="Job location:", font=("Courier 14")).pack()
    location= Entry(win, width= 40)
    location.pack()

    #Number of jobs
    Label(win, text="How many jobs to apply:", font=("Courier 14")).pack()
    no_of_job= Entry(win, width= 40)
    no_of_job.pack()


    #Response
    msg_entry = Label(win, text="", font=("Courier 14"))
    msg_entry.pack()

    #Submit Button
    Button(win, text="Submit",width=20, command=start_apply).pack(pady=20)

    win.mainloop()

if __name__ == "__main__":
    main()