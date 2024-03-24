import csv
import subprocess
import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

#Creating and configure logging
logging.basicConfig(filename="attendancefile.log", format='%(asctime)s %(message)s', filemode='w', level=logging.INFO)

def get_data():
    filename = open('Names.csv', 'r', encoding='utf-8-sig')

    file = csv.DictReader(filename)

    #empty list to store names
    student = []

    for row in file:
        student.append(row)

    print(student)
    return student

def get_ssid():
    results = subprocess.check_output(["netsh", "wlan", "show", "network"])
    results = results.decode("ascii")
    results = results.replace("\r", "")
    ls = results.split("\n")
    ls = ls[4:]
    ssids = []

    for line in ls:
        if line.startswith("SSID"):
            ssid = line.split(":")[1].strip()
            ssids.append(ssid)
    
    print(ssids)
    return ssids 

def compare_lists(list1, list2):
    try:
        iCount = 0
        list1_names = [row['Name']for row in list1]

        for item in list2:
            if item in list1_names:
                logging.info(f"Present : {item}")
                print("present", item)
                iCount +=1
                print("Present Student count :",iCount)
        
        logging.info(f"Present Student count : {iCount}")

    except Exception as e:
        logging.error(f"Error in compare_lists function : {e}")

def send_log():
    my_address = "gangurdemaitreya@gmail.com"
    my_password = "----------------"

    sobj = smtplib.SMTP(host = "smtp.gmail.com", port=587)
    sobj.starttls()
    sobj.login(my_address, my_password)

    msg = MIMEMultipart()
    msg['From'] = my_address
    msg['To'] = "maitreyagangurde@gmail.com"
    msg['Subject'] = "Today's Attendance of class BE-A"
    message = "Python Automation Script for Attendance"
    msg.attach(MIMEText(message, 'plain'))
    with open('attendancefile.log', 'rb') as file:
        msg.attach(MIMEApplication(file.read(), Name = "attendance.log"))

    sobj.send_message(msg)
            
def main():
    try:
        student = get_data()
        ssids = get_ssid()
        compare_lists(student,ssids)
        send_log()

    except Exception as e:
        logging.error(f"Error in Main function : {e}")

if __name__ =="__main__":
    main()