import sqlite3 as lite

con = lite.connect('dbdmtest.db')

rows = con.execute('SELECT ra, decl FROM Stars')

for row in rows: 
	print "Ra={0} Dec={1}".format(row[0], row[1])
