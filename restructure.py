import difflib
#from nis import cat
import sys
import pandas as pd
import numpy as np
import openpyxl
import glob

import os
import mysql.connector
from pymysql import NULL
import copy

from sql_object import CheckedMail, Country, ValidCertificate

import datetime
from datetime import date, datetime
from datetime import timedelta

import send_mail
from send_mail import *
#from send_mail import send_mail
#

fehler = ""

try: 

    # Falls mal ein Tag nicht verschoben wurde

    #actual_dateTime_full = datetime.now().isoformat(sep=' ') #milliseconds #timespec='seconds'
    actual_dateTime = date.today().strftime("%Y-%m-%d")
    #print(a)

    mydb = mysql.connector.connect(
            host="192.168.10.21",
            user="iscc",
            password ="FZlmbnwR5S2022!$",
            database="iscc"
        )

    # Get all countries which are in the the MySQL-DB right now

    #mycursor = mydb.cursor()
    #sql_country = "SELECT Country FROM tbl_country"
    #mycursor.execute(sql_country)
    #myresult_country_all = mycursor.fetchall()
    #mydb.commit()
    #mycursor.close()

    # Jetzt auch noch ins SQL reinschreiben

    def func_dump(obj):
        """To get all items from an Object"""
        for attr in dir(obj):
            print("obj.%s = %r" % (attr, getattr(obj, attr)))

    # Define all beginning variables
    count_update = 0
    count_insert = 0
    list_update = []

    mylist = [f for f in glob.glob("*.csv")]
    #print(len(mylist))
    if (len(mylist) > 0):
        try:
                for i in mylist:
                    #print(i)
                    keepname = i.split(".")[0]
                    df = pd.read_csv(str(i), sep=",")
                    save_name = "{}.xlsx".format(keepname)
                    #save_pfad = "iscc\certificate\valid\{}".format(save_name)
                    df.to_excel(save_name, index=False)
        except:
            print("Can't convert csv to xlsx")
            fehler = "Umwandlung in xlsx nicht möglich"
    else:
        sys.exit()


    try:

        #Get all csv which are in the directory
        for i in mylist:
            df_complete_all = pd.read_csv(str(i), sep=",")
            df_complete_nan = df_complete_all.replace(r'^s*$',  np.nan, regex = True)
            #print(df_complete_nan.head())
            df_complete_empty = df_complete_nan.dropna(axis=0, how='all')
            df_complete = df_complete_empty.fillna("")
            df_complete.reset_index(inplace=True, drop=True)
            #print(df_complete)
            #print(df_complete)
            list_header = df_complete.columns.values
            #print(list_header)
            #print("----------------")
            item_country = difflib.get_close_matches("Country",list_header)
            #print(item_country)
            # Jetzt überprüfen ob, im neuen Excel ein neues Land existiert und falls ja, hinzufügen
            list_countries = list(df_complete[item_country[0]])
            #print(list_countries.index(np.nan))
            list_countries_unique = list(set(list_countries))
            #print(list_countries_unique)

            # Implement new Countries to Database
            for j in range(len(list_countries_unique)):

                country_pos_add = list_countries_unique[j]
                obj_country = Country(Country=country_pos_add)
                #print(country_pos_add)
                count_object_country = obj_country.AskCountCountry(mydb) 
                #print(count_object_country)
                # Gehe jedes Land von SQL-Database durch und und wenn eines neu ist wird es hinzugefügt          
                if(count_object_country[0][0] < 1):
                    obj_country.InsertSQLCountry(mydb)
                    #print("Insert country")
                #else:
                #    print("Bereits vorhanden")

                del obj_country
        
            # Wenn countries fertig, dann die Objekte einspielen
            #print(df_complete.iloc[6375:6380,:])
            #print(df_complete.shape)
            for k in range(df_complete.shape[0]):

                    #df_get_single_NaN = copy.copy(df_complete.loc[k])
                    #df_get_single = df_get_single_NaN
                    
                    #if(k > 6376):
                    #    print(df_complete.loc[k])


                    df_get_single = df_complete.loc[k]
                    #
                    #print(type(df_get_single))
                    
                    #try:
                    #    df_get_single = df_get_single_NaN.fillna("")
                    #except:
                    #    pass
                    
                    #print(df_get_single)
                    #item_country = difflib.get_close_matches("country",list_header)
                    #print(list_header)

                    

                    Certificate = df_get_single[list_header[0]]
                    Certificate_Holder = df_get_single[difflib.get_close_matches("Certificate_Holder",list_header)[0]]
                    CountryName = df_get_single[difflib.get_close_matches("country",list_header)[0]]
                    Scope = df_get_single[difflib.get_close_matches("scope",list_header)[0]]
                    Raw_Material = df_get_single[difflib.get_close_matches("Raw_Material",list_header)[0]]
                    Add_Ons = df_get_single[difflib.get_close_matches("add_on",list_header)[0]]
                    valid_from = df_get_single[difflib.get_close_matches("valid_from",list_header)[0]]
                    valid_until = df_get_single[difflib.get_close_matches("valid_until",list_header)[0]]
                    date_insert = actual_dateTime
                    checked = "False"
                    Issuing_CB = df_get_single[difflib.get_close_matches("issuing",list_header)[0]]
                    Products= df_get_single[difflib.get_close_matches("products",list_header)[0]]
                    RawMat_Categ= df_get_single[difflib.get_close_matches("RawMat_Categ",list_header)[0]]
                    Status= "Inactive"
                    date_changed = actual_dateTime

                    object_ValidCert = ValidCertificate(Certificate=Certificate, Certificate_Holder=Certificate_Holder, Country=CountryName, Scope=Scope,Raw_Material=Raw_Material,
                    Add_Ons=Add_Ons,valid_from=valid_from, valid_until=valid_until,date_insert=date_insert, date_changed=date_changed, Checked=checked, Issuing_CB=Issuing_CB,
                    Products=Products, RawMat_Categ=RawMat_Categ,Status=Status)



                
                    # Wenn das Certificate noch nicht in der Datenbank aufscheint -> neu hinzufügen
                    countCert = object_ValidCert.AskCountCertificate(mydb)
                    if(countCert[0][0] < 1):

                        countryID = object_ValidCert.ReturnCountryID(mydb)
                        object_ValidCert.CountryID = int(countryID)

                        checkedID = object_ValidCert.ReturnCheckedID(mydb)
                        object_ValidCert.cID = int(checkedID)

                        statusID = object_ValidCert.ReturnStatusID(mydb)
                        object_ValidCert.StatusID = int(statusID)

                        #print(func_dump(object_ValidCert))

                        object_ValidCert.InsertSQLCertificate(mydb)
                        count_insert = count_insert + 1
                    else:
                        # Zertifikat existiert bereits 
                        re_validfrom = object_ValidCert.ReturnValidFrom(mydb)
                        re_validuntil = object_ValidCert.ReturnValidUntil(mydb)


                        if(object_ValidCert.valid_from != re_validfrom or object_ValidCert.valid_until != re_validuntil ):
                            #print("Ungleich")
                            object_ValidCert.UpdateSQLCertificateValid(mydb)
                            count_update = count_update + 1
                            list_update.append(object_ValidCert.Certificate)
                            
                    del(object_ValidCert)


        print("Inserted = {},  Updated = {} ".format(count_insert, count_update))
        print("Upgedatet:")
        print(list_update)


    except:
        print("Can't integrate new File into SQL-Database")
        fehler = "Can't upload to SQL - Server"


except:
    print("Problem with the Python file")
    ## Send mail to me
    
        #t
    msg = "Problem bei Wget-Skript, oder bei {} ".format(fehler)
    #sendMail(sender="linux@muenzer.at",subject="Test", recipient=["ISCC_kaufmaennisch@muenzer.at"], username="",password="",message=msg,xlsx_files=save_name)

    send_mail.sendMail(sender="linux@muenzer.at",subject="Certificate Problems", recipient=["david.kohlfuerst@muenzer.at"], username="",password="",message=msg)

#