import MySQLdb

db = MySQLdb.connect(host="us-cdbr-iron-east-03.cleardb.net",    # your host, usually localhost
                     user="b4041f462a1916",         # your username
                     passwd="a842671f",  # your password
                     db="heroku_7061d9f68bcc51c")        # name of the data base

print "Connected to the target mysql server"

cur = db.cursor()

# Test query
cur.execute("SELECT * FROM expense_sharing_expenses")
print "Connection verified"

# DDL statements for different tables go here
cur.execute("""CREATE TABLE Issues ( issue_id varchar(100), issue_text varchar(255), 
			user varchar(50), commit_flag varchar(10), milestone_flag varchar(10), state varchar(10),
			primary key(issue_id) );""")

db.close()