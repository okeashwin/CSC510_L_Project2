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
cur.execute("""CREATE TABLE IF NOT EXISTS issue (id INTEGER, name VARCHAR(128),
        createtime DATETIME NOT NULL,closedtime DATETIME NOT NULL ,milestone_id INTEGER,
        assignee_id INTEGER,label_str VARCHAR(1024),labels_count INTEGER,
        CONSTRAINT pk_issue PRIMARY KEY (id) );""")
cur.execute("""CREATE TABLE IF NOT EXISTS milestone(id INTEGER, title VARCHAR(128), description VARCHAR(1024),
        created_at DATETIME, due_at DATETIME, closed_at DATETIME, user VARCHAR(128), identifier INTEGER,
        CONSTRAINT pk_milestone PRIMARY KEY(id));""")
cur.execute("""CREATE TABLE IF NOT EXISTS event(issueID INTEGER NOT NULL, time DATETIME NOT NULL, action VARCHAR(128),
        label VARCHAR(128), user VARCHAR(128), milestone INTEGER, identifier INTEGER,
        CONSTRAINT pk_event PRIMARY KEY (issueID, time, action, label),
        CONSTRAINT fk_event_issue FOREIGN KEY (issueID) REFERENCES issue(id),
        CONSTRAINT fk_event_milestone FOREIGN KEY (milestone) REFERENCES milestone(id));""")
cur.execute("""CREATE TABLE IF NOT EXISTS comment(issueID INTEGER NOT NULL, user VARCHAR(128), createtime DATETIME NOT NULL,
        updatetime DATETIME, text VARCHAR(1024), identifier INTEGER,
        CONSTRAINT pk_comment PRIMARY KEY (issueID, user, createtime),
        CONSTRAINT fk_comment_issue FOREIGN KEY (issueID) REFERENCES issue(id));""")
cur.execute("""CREATE TABLE IF NOT EXISTS commits(id INTEGER NOT NULL, time DATETIME NOT NULL, sha VARCHAR(128),
        user VARCHAR(128), message VARCHAR(128),
        CONSTRAINT pk_commits PRIMARY KEY (id));""")

db.close()