class CheckedMail:

    species = "Checked Mail"
    def __inti__(self, Checked):
        self.checked = Checked
    def __del__(self):
        pass


#class GetStatus:#

#    species = "Status"
#    def __inti__(self, Status):
#        self.Status = Status
#    def __del__(self):
#        pass


class Country:
    species = "Country"

    def __init__(self, Country):
        self.Country = Country

    def AskCountCountry(self, connector):
        mycursor = connector.cursor()
        
        sql_country = "SELECT COUNT(*) FROM tbl_country WHERE Country =%s"
        val_country = (self.Country,)
        mycursor.execute(sql_country,val_country)
        myresult_country = mycursor.fetchall()
        connector.commit()
        mycursor.close()
        return(myresult_country)

    def InsertSQLCountry(self,connector):
        mycursor = connector.cursor()
        sql = "INSERT INTO tbl_country (Country) VALUES (%s)"
        val = (self.Country,)
        mycursor.execute(sql,val)
        connector.commit()
        mycursor.close()

    def __del__(self):
        pass


class ValidCertificate:
    species = "Valid Certificate"

    def __init__(self, Certificate,Certificate_Holder,Country,Scope,Raw_Material,Add_Ons,
    valid_from,valid_until,date_insert,Checked,Issuing_CB,Products,RawMat_Categ,Status,date_changed):
        self.Certificate = Certificate
        self.Certificate_Holder = Certificate_Holder
        self.Country = Country
        self.CountryID = ""
        self.Scope = Scope
        self.Raw_Material = Raw_Material
        self.Add_Ons=Add_Ons
        self.valid_from=valid_from
        self.valid_until = valid_until
        self.date_insert = date_insert
        self.Checked = Checked
        self.cID = ""
        self.Issuing_CB = Issuing_CB
        self.Products=Products
        self.RawMat_Categ = RawMat_Categ
        self.Status = Status
        self.StatusID = ""
        self.date_changed = date_changed

    # Get Country ID from table for connection
    def ReturnCountryID(self,connector):
        mycursor = connector.cursor()

        sql_type = "SELECT ID_country FROM tbl_country WHERE Country=%s"
        val_type = (self.Country,)
        mycursor.execute(sql_type,val_type)
        myresult_CouID = mycursor.fetchall()
        connector.commit()
        mycursor.close()
        return(myresult_CouID[0][0])

    # Get CheckedID from table for connection, at the beginning, everything is False if first inserted
    
    def ReturnCheckedID(self,connector):
        mycursor = connector.cursor()

        sql_cid = "SELECT ID_checked FROM tbl_checked WHERE Checked=%s"
        val_cid = (self.Checked,)
        mycursor.execute(sql_cid,val_cid)
        myresult_CID = mycursor.fetchall()
        connector.commit()
        mycursor.close()
        return(myresult_CID[0][0])

    # Get Status ID from table for connection, Status is determined by Date, therefore THIS IS NOT needed here
    def ReturnStatusID(self,connector):
        mycursor = connector.cursor()

        sql_Sid = "SELECT Status_ID FROM tbl_status WHERE Status=%s"
        val_Sid = (self.Status,)
        mycursor.execute(sql_Sid,val_Sid)
        myresult_SID = mycursor.fetchall()
        connector.commit()
        mycursor.close()
        return(myresult_SID[0][0])


    def ReturnValidFrom(self,connector):
        mycursor = connector.cursor()

        sql_VF = "SELECT valid_from FROM tbl_valid_certificate WHERE Certificate=%s"
        val_VF = (self.Certificate,)
        mycursor.execute(sql_VF,val_VF)
        myresult_VF_full = mycursor.fetchall()
        connector.commit()
        mycursor.close()
        myresult_VF_value = myresult_VF_full[0][0]
        myresult_VF = myresult_VF_value.strftime("%Y-%m-%d")
        return(myresult_VF)

    def ReturnValidUntil(self,connector):
        mycursor = connector.cursor()

        sql_VU = "SELECT valid_until FROM tbl_valid_certificate WHERE Certificate=%s"
        val_VU = (self.Certificate,)
        mycursor.execute(sql_VU,val_VU)
        myresult_VU_full = mycursor.fetchall()
        connector.commit()
        mycursor.close()
        myresult_VU_value = myresult_VU_full[0][0]
        myresult_VU = myresult_VU_value.strftime("%Y-%m-%d")
        return(myresult_VU)

    # To look, if the Certificate already exist, if not -> insert, else update if needed
    def AskCountCertificate(self, connector):
        mycursor = connector.cursor()
        
        sql = "SELECT COUNT(*) FROM tbl_valid_certificate WHERE Certificate = %s"
        val = (self.Certificate,)
        mycursor.execute(sql,val)
        myresult_cert = mycursor.fetchall()
        connector.commit()
        mycursor.close()
        return(myresult_cert)


    def InsertSQLCertificate(self,connector):

        mycursor = connector.cursor()
        sql = "INSERT INTO tbl_valid_certificate (Certificate,Certificate_Holder,CountryID,Scope,Raw_Material,Add_Ons,valid_from,valid_until,date_insert,cID,Issuing_CB,Products,RawMat_Categ,StatusID,date_changed) VALUES(%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s,%s,%s,%s,%s)"
        #self.date_changed = self.date_insert
        val = (self.Certificate, self.Certificate_Holder, self.CountryID, self.Scope, self.Raw_Material, self.Add_Ons, self.valid_from, self.valid_until, 
        self.date_insert, self.cID, self.Issuing_CB, self.Products,self.RawMat_Categ,self.StatusID,self.date_changed)
        mycursor.execute(sql,val)
        connector.commit()
        mycursor.close()
 

    #def UpdateSQLCertificate(self,connector):

    #    mycursor = connector.cursor()
    #    sql = "UPDATE tbl_valid_certificate SET Certificate_Holder=%s,CountryID=%s,Scope=%s,Raw_Material=%s,Add_Ons=%s,valid_from=%s,valid_until=%s,cID=%s,Issuing_CB=%s,Products=%s, RawMat_Categ=%s, Status=%s, date_changed=%s  WHERE Certificate=%s"
    #    val = (self.Certificate_Holder, self.CountryID,self.Scope,self.Raw_Material,self.Add_Ons,self.valid_from, 
    #    self.valid_until,self.cID,self.Issuing_CB,self.Products,self.RawMat_Categ,self.Status, self.date_changed, self.Certificate)
    #    mycursor.execute(sql,val)
    #    connector.commit()
    #    mycursor.close()

    def UpdateSQLCertificateValid(self,connector):

        mycursor = connector.cursor()
        sql = "UPDATE tbl_valid_certificate SET valid_from=%s,valid_until=%s,date_changed=%s  WHERE Certificate=%s"
        val = (self.valid_from, self.valid_until, self.date_changed, self.Certificate)
        mycursor.execute(sql,val)
        connector.commit()
        mycursor.close()

    def __del__(self):
        pass
        #Deconstrutor
     