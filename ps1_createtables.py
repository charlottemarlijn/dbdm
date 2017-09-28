import sqlite3 as lite
import numpy as np
import sys

def createtables(con):
	
	with con: 
		cur = con.cursor()
		
		#Drop if they already exist so we can run this function again
		#if something went wrong:
		cur.execute('DROP TABLE IF EXISTS MagTable')
		cur.execute('DROP TABLE IF EXISTS PhysTable')
		
		#Table creation commands
		create_mag_table =  "CREATE TABLE IF NOT EXISTS MagTable \
							(Name STRING, ra STRING, dec STRING, \
							B DOUBLE, R DOUBLE, UNIQUE(Name), \
							PRIMARY KEY(Name))"
		create_phys_table = "CREATE TABLE IF NOT EXISTS PhysTable \
							(Name STRING, T_eff INT, FeH FLOAT, \
							UNIQUE(Name), PRIMARY KEY(Name))"
	
		#Execute the commands to create the tables
		cur.execute(create_mag_table)
		cur.execute(create_phys_table)
		
		#Fill the tables using the .dat files
		with open('magtable.dat', 'r') as tab:
			for row in tab:
				data = row.split(",")
				#print data
				command = "INSERT INTO MagTable VALUES('%s', '%s', '%s', %s, %s)"%(data[0],data[1],data[2],data[3],data[4])
				print command
				cur.execute(command)
		
		with open('phystable.dat', 'r') as tab:
			for row in tab:
				data = row.split(",")
				#print data
				command = "INSERT INTO PhysTable VALUES('%s', %s, %s)"%(data[0],data[1],data[2])
				print command
				cur.execute(command)
	


con = lite.connect('ps1_createtables.db')

#Creating the tables (commented because I've already done it)
#createtables(con)

#a) Find the Ra & Dec of all objects with B > 16:
print '\n'
radec = con.execute('SELECT ra, dec FROM MagTable WHERE B > 16')
print 'a) Ra and Dec of all objects with B > 16:' 
for row in radec: #forloop over the found values
	print "Ra=%s Dec=%s"%(row[0], row[1])
print '\n'

#b) Output B, R, T_eff and FeH for all stars (I guess this question is not 
#   well defined because T_eff & FeH are not available for all stars in MagTable)
#   (& maybe other reasons?)
name_and_BR = con.execute('SELECT Name, B, R FROM MagTable')
name_and_TF = con.execute('SELECT Name, T_eff, FeH FROM PhysTable')
name_and_TF_array = np.array(name_and_TF.fetchall())
print 'b) B, R for all stars and T_eff and FeH where possible:'
for row in name_and_BR:
	name = row[0]
	TFidx = np.where(name_and_TF_array[:,0] == name)
	if len(TFidx[0])>0:
		print "Name=%s, B=%g, R=%g, T_eff=%s K, FeH=%s"%(row[0], row[1], row[2],
														name_and_TF_array[TFidx[0][0],1],
														name_and_TF_array[TFidx[0][0],2])
	else: print "Name=%s, B=%g, R=%g"%(row[0], row[1], row[2])
print '\n'

#c) Output the same for all objects with FeH > 0
# Let's try joining tables now and selecting only FeH > 0 stars
tab = con.execute("SELECT m.Name, m.B, m.R, p.T_eff, p.FeH\
					FROM MagTable as m \
					JOIN PhysTable as p \
					ON m.Name = p.Name \
					WHERE FeH > 0")
#Print the data for which FeH > 0
print 'c) B, R, T_eff and FeH for all stars with FeH > 0'					
for row in tab:
	print "Name=%s, B=%s, R=%g, T_eff=%g K, FeH=%g"%(row[0],row[1],row[2],row[3],row[4])
print '\n'

#d) Create a table with the B-R colour (commented)

#with con:
#	cur = con.cursor()
#
#	create_BR_table =  "CREATE TABLE IF NOT EXISTS BRTable \
#								(Name STRING, BR double, UNIQUE(Name), \
#								PRIMARY KEY(Name))"
#	cur.execute(create_BR_table)						
#	BRcolour = con.execute("SELECT Name, B-R as BR FROM MagTable")
#	BRcolour = np.array(BRcolour.fetchall())
#	for i in range(len(BRcolour[:,0])):
#		cur.execute("INSERT INTO BRTable VALUES('%s', %g)"%(BRcolour[i,0],float(BRcolour[i,1])))

	
#Check if it actually worked: 
BRtab = con.execute("SELECT Name, BR FROM BRTable")
print "d) This is what's in the table with B-R colour"
for rowj in BRtab:
	print "Name=%s, B-R=%g"%(rowj[0],rowj[1])


	

