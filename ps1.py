import sqlite3 as lite
import numpy as np
import sys

#Starting up

con = lite.connect('dbdmtest.db')
#cur = con.cursor()

rows = con.execute('SELECT ra, decl FROM Stars')
#print rows #just prints the object
#print rows.next() #gives you the next object
#print rows.fetchall() #gives you all remaining objects

for row in rows: #forloop also works for some reason
	print "Ra={0} Dec={1}".format(row[0], row[1])

#Two extra questions:

#4. Where is the FITS image stored for star S5?
print 
print 'Question 4'
query4 = "SELECT FieldID FROM Stars WHERE Star = 'S5'"
fieldID = con.execute(query4).fetchall()[0][0]
print 'FieldID of star S5:', fieldID
print 'Star S5 is stored at', con.execute("SELECT WhereStored FROM \
											Observations WHERE \
											ID = %i"%(fieldID)).fetchall()[0][0]

#5. Give me a list of all stars obseved with the same FieldID
print 
print 'Question 5'
fieldquery = 'SELECT FieldID FROM Stars'
fieldID  = con.execute(fieldquery)
fieldIDs = np.array(fieldID.fetchall())
fieldIDs = np.unique(fieldIDs)
for ID in fieldIDs:
	print 'Stars with fieldID', ID
	query5 =  "SELECT Star FROM Stars WHERE FieldID = %i"%(ID)
	print con.execute(query5).fetchall()

