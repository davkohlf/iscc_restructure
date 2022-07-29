import difflib
import pandas as pd
import numpy as np
import openpyxl
import glob
import certifi
import os
import mysql.connector
from pymysql import NULL
import copy

from sql_object import CheckedMail, Country, ValidCertificate

import datetime
from datetime import date, datetime
from datetime import timedelta

import webdav3
from webdav3.client import Client

from send_mail import *

try:
    #actual_dateTime_full = datetime.now().isoformat(sep=' ') #milliseconds #timespec='seconds'
    actual_dateTime = date.today().strftime("%Y-%m-%d")

    mydb = mysql.connector.connect(
            host="192.168.10.21",
            user="iscc",
            password ="FZlmbnwR5S2022!$",
            database="iscc"
        )



    ############################################################################
    #########                   Abfrage nach noch nicht gesendeten 

    #################################################################################
    #print("Now starting with the control of sending Mails and checking if a certificate is still valid")

    # Get all countries which are in the the MySQL-DB right now

    #######  Get Date and the correct Format #######
    today_date = date.today()

    # Look for entries which are younger than the last 7 days. So if something is new we save those Certificates into a Excel File
    day_max = 7
    #d1 = today_date.strftime("%Y_%m_%d")
    day_single_max = today_date.strftime("%Y_%m_%d")
    past_eight_date = today_date - timedelta(days = day_max)
    #print(past_eight_date)



    #mycursor = mydb.cursor()
    #sql_cert = "SELECT * FROM tbl_valid_certificate"
    #sql_cert = "select * from tbl_valid_certificate where date_insert >= Convert(datetime, %s )"

    #mycursor.execute(sql_cert)
    #myresult_Certificate = mycursor.fetchall()
    #mydb.commit()
    #mycursor.close()


    mycursor = mydb.cursor()
    #sql = "SELECT * FROM tbl_valid_certificate WHERE >= Convert(datetime, %s )"
    sql = "SELECT * FROM tbl_valid_certificate WHERE date_insert >= %s"
    val = (past_eight_date,)
    mycursor.execute(sql,val)
    myresult_Cert = mycursor.fetchall()
    mydb.commit()
    mycursor.close()

    df_allresult = pd.DataFrame(myresult_Cert)
    #print(df_allresult)

    #print(myresult_Certificate[0][0])

    #a = myresult_Cert[0][0]

    pfad = "C:\Multimedia_Arbeit\Python_Projects\Iscc"
    save_name = "{}\{}_new_certificates.xlsx".format(pfad,day_single_max)


    list_header_sql = []
    for i in range(len(mycursor.description)):
        item = (mycursor.description[i][0])
        list_header_sql.append(item)

    #print(list_header_sql)

    df_allresult.columns = list_header_sql

    df_allresult.to_excel(save_name, index=False)

    """
    #######################################################         NICHT LÖSCHEN     ##################################################################
    ## Jetzt noch auto E-Mail verschicken
    import smtplib #nur für versand, das email muss zuvor noch aufgebaut werden
    import email.mime.text
    from email.mime.text import MIMEText
    from email.message import EmailMessage
    #from email.mime.base import MIMEBase



    import os, smtplib, traceback
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.application import MIMEApplication

    #https://stackoverflow.com/questions/16968758/sending-email-to-a-microsoft-exchange-group-using-python
    #

    #testt

    def sendMail(sender,
                subject,
                recipient,
                username,
                password,
                message=None,
                xlsx_files=None):

        msg = MIMEMultipart()
        msg["Subject"] = subject
        msg["From"] = sender
        if type(recipient) == list:
            msg["To"] = ", ".join(recipient)
        else:
            msg["To"] = recipient
        message_text = MIMEText(message, 'html')
        msg.attach(message_text)

        if xlsx_files:
            #for f in xlsx_files:
            #    attachment = open(f, 'rb')
            #    file_name = os.path.basename(f)
            #    part = MIMEApplication(attachment.read(), _subtype='xlsx')
            #    part.add_header('Content-Disposition', 'attachment', filename=file_name)
            #    msg.attach(part)
            attachment = open(xlsx_files, 'rb')
            #print(attachment)
            file_name = os.path.basename(xlsx_files)
            #print(file_name)
            part = MIMEApplication(attachment.read(), _subtype='xlsx')
            part.add_header('Content-Disposition', 'attachment', filename=file_name)
            msg.attach(part)
        try:
            #server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server = smtplib.SMTP("192.168.10.250",port=25) #SMTP Object bekommt server daten + Port
            server.connect("192.168.10.250",25)
            server.ehlo()
            server.starttls()
            server.ehlo()
            #server.login(username, password)
            server.sendmail(sender, recipient, msg.as_string())
            server.close()
        except Exception as e:
            error = traceback.format_exc()
            #print(error)
            #print(e)

    """


    msg = "Im Anhang befindet sich das neue Excel-File "
    #sendMail(sender="linux@muenzer.at",subject="Test", recipient=["ISCC_kaufmaennisch@muenzer.at"], username="",password="",message=msg,xlsx_files=save_name)

    sendMail(sender="linux@muenzer.at",subject="Test", recipient=["david.kohlfuerst@muenzer.at"], username="",password="",message=msg,xlsx_files=save_name)

    #["david.kohlfuerst@muenzer.at","selina.edelsbrunner@muenzer.at","patrick.seyer@muenzer.at"

    #print(save_name)
except:
    msg_ST = "Problem with Stefano-Group sending Mails hat Probleme"
    sendMail(sender="linux@muenzer.at",subject="Stefano Group sending mail", recipient=["david.kohlfuerst@muenzer.at"], username="",password="",message=msg_ST)



