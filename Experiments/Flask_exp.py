# -*- coding: utf-8 -*-
"""
Created on Tue May 24 11:20:38 2022

@author: tonum
"""

# Importing pdfplumber library which can be used to Extract data from a PDF file
import pdfplumber

# Importing MySQL Connector used to work with Databases
import mysql.connector

# Connecting Database and assigning it to db variable
db = mysql.connector.connect(
    host = "LOCALHOST",       # Enter Your Database Host
    user = "YOURUSERNAME",    # Enter Your Database User name
    password = "YOURPASSWORD" # Enter Your Database Password
)

# Using cursor function to have control over Database
cursor = db.cursor()

# I'm creating a database called Bank and started using it
cursor.execute("CREATE DATABASE Bank;")
cursor.execute("USE Bank;")
 
#Opening the PDF file using the pdfplumber library
with pdfplumber.open('(Bank Statement).pdf') as pdf:
    #Assuming that the bank statement PDF has only one page
    #Extracting the first page data and assign it to the variable Extract
    Extract = (pdf.pages[0]).extract_text()

# Spliting lines of the Extracted data
Extracted_lines = Extract.splitlines()

# MySQL query to Create a table called bank_statement and adding fields
Query="CREATE TABLE bank_statement ( Date VARCHAR(12), Description VARCHAR(20), Deposit FLOAT, Withdraw FLOAT, Balance FLOAT );"

# Executing the CREATE TABLE Query
cursor.execute( Query )

# Removing the Heading texts from the Extrcted data
Extracted_lines.pop(0)

# Initial Balance
Balance = 5000.0

# Looping every lines of the Extracted text
for lines in Extracted_lines:
    Entries = lines.split()

    # Removing amount's commas
    for i in range(2,4):
        Entries[i] = float(Entries[i].replace(",",''))
    
    # Conditional statements for checking the amount as Deposit
    if ( Entries[2]+Balance == Entries[3] ):
        Entries.append(Entries[3]) 
        Entries[3] = 0
        Balance = Entries[4]

    # Conditional statements for checking the amount as Withdraw
    elif ( Balance-Entries[2] == Entries[3] ):
        Entries.append(Entries[3])
        Entries[3] = Entries[2]
        Entries[2] = 0
        Balance = Entries[4]
        
    # MySQL query to Insert datas into table bank_statement 
    Query = "INSERT INTO bank_statement ( Date, Description, Deposit, Withdraw, Balance ) VALUES ( %s, %s, %s, %s, %s );"

    # Executing the INSERT Query
    cursor.execute( Query, Entries )

    # commit method used to commit changes to the Database
    db.commit()