import os
import sys

def runQueries(repoID,targetDir):
	os.chdir(targetDir)
	queries=[line.rstrip('\n') for line in open('../Queries.txt')]
	queryID=0
	for query in queries:
		os.system("sqlite3 -csv group"+str(repoID)+".db \""+query+"\" > ./result_"+str(queryID)+".csv")
		queryID+=1
	os.chdir("../")

def pushData(repoID):
	targetDir="./Group"+str(repoID)+"Data"
	dataDir="../Group"+str(repoID)+"Results"
	os.mkdir(targetDir)
	os.chdir(targetDir)

	#issue dump
	print("sqlite3 -header -csv "+dataDir+"/group"+str(repoID)+".db \"select * from issue;\" > issues.csv")
	os.system("sqlite3 -header -csv "+dataDir+"/group"+str(repoID)+".db \"select * from issue;\" > issues.csv")
	#milestone dump
	os.system("sqlite3 -header -csv "+dataDir+"/group"+str(repoID)+".db \"select * from milestone;\" > milestones.csv")
	#labels dump
	os.system("sqlite3 -header -csv "+dataDir+"/group"+str(repoID)+".db \"select * from labels;\" > labels.csv")
	#event
	os.system("sqlite3 -header -csv "+dataDir+"/group"+str(repoID)+".db \"select * from event;\" > event.csv")
	# commits dump
	os.system("sqlite3 -header -csv "+dataDir+"/group"+str(repoID)+".db \"select * from commits;\" > commits.csv")

	os.chdir("../")

def execute():
	if os.path.isfile("./repos.conf"):
		repos = [line.rstrip('\n') for line in open('./repos.conf')]
	else:
		print("repos.conf not found")
		sys.exit()

	if os.path.isfile("./Queries.txt") == False:
		print("Queries.txt not found")
		sys.exit()

	print(str(len(repos))+" repos found in the file")

	if os.path.isfile("./group1.db"):
		os.remove("./group1.db")
	if os.path.isfile("./group2.db"):
		os.remove("./group2.db")
	if os.path.isfile("./group3.db"):
		os.remove("./group3.db")

	os.system("rm -rf ./Group1Results")
	os.system("rm -rf ./Group2Results")
	os.system("rm -rf ./Group3Results")
	os.system("rm -rf ./Group1Data")
	os.system("rm -rf ./Group2Data")
	os.system("rm -rf ./Group3Data")
	os.mkdir("./Group1Results")
	os.mkdir("./Group2Results")
	os.mkdir("./Group3Results")
	repoID=1
	for repo in repos:
		returnValue=os.system("python gitable-sql.py "+repo+" group"+str(repoID))
		filename="group"+str(repoID)+".db"
		targetDir="Group"+str(repoID)+"Results"
		os.system("mv "+filename+" ./"+targetDir+"/"+filename)
		if returnValue==0:
			print("------- Succeeded for Group "+str(repoID)+"---------")
		else:
			print("Failed with exit code : "+str(returnValue))
			print("------- Failed for Group "+str(repoID)+"---------")

		pushData(repoID)
		runQueries(repoID,targetDir)
		repoID+=1


execute()