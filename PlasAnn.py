#!/usr/bin/python
'''
DESCRIPTION: PlasAnn takes in a fasta csv file and runs annotation pipeline for each plasmid
fasta in the csv file
'''
import os
import csv
import sys

def main(run_all):
	os.chdir("./scripts")
	fastas=os.listdir("./../fastas")

	with open("./../fasta.csv", 'w') as csvfile:
		write=csv.writer(csvfile, delimiter='\t')
		for fasta in fastas:
			write.writerow([fasta[0:len(fasta)-6]])

	if int(run_all)==0:
		print("\nWould you like to re-annotate any already annotated plasmids?")
		print("0-Do not re-annotate already annotated plasmids")
		print("1-Re-annotate already annotated plasmids")
		print("STOP-STOP PROGRAM\n")
		process=-1
		run=True
		while run==True:
			try:
				process=input("Type your answer: ")
				if int(process)!=0 and int(process)!=1:
					print("\nPlease type valid binary number!")
				else:
					run=False
			except:
				if str(process) in "STOP":
					print("STOP DETECTED: EXITING PROGRAM")
					sys.exit()
				else:
					print("\nPlease type valid binary number!")


		plasmids=[]
		with open("./../fasta.csv", 'r') as csvfile:
			read=csv.reader(csvfile, delimiter='\t')
			for plasmid in read:
				plasmids.append(plasmid[0])

		rerun_pls=[]
		if int(process)==1:
			print("\nPlease enter the names of already annotated plasmids that you'd like reannotated")
			print("Press ENTER every time you type a plasmid name! Only press ENTER when you're done")
			print("Type ALL if all plasmids need to be reannotated")
			print("Type STOP to STOP PROGRAM")
			pls="-"
			while len(pls)!=0:
				try:
					pls=str(input("\nPlasmid Name: "))
					if pls in "STOP" or pls in "^C":
						sys.exit()
					if pls in "ALL":
						rerun_pls=plasmids
						pls=""
						break
					elif pls not in plasmids:
						print("INVALID Plasmid Name!")
					else:
						rerun_pls.append(pls)
				except SystemExit:
					print("STOP DETECTED: EXITING PROGRAM")
				except:
					print("Enter valid string input only!")


		print("\n=== PLAS ANN ===")
		for plasmid in plasmids:
			exists=os.path.exists("./output/plasmids/" + plasmid + "/final.tsv")
			if exists:
				print("---------------------------------------------------")
				print("Annotating Plasmid " + plasmid)
				print("---------------------------------------------------")
				os.system("/bin/bash bgbm.sh " + plasmid)
			elif len(rerun_pls)>0 and plasmid in rerun_pls:
				print("---------------------------------------------------")
				print("Re-annotating " + plasmid)
				print("---------------------------------------------------")
				os.system("/bin/bash bgbm.sh " + plasmid)
			else:
				print("---------------------------------------------------")
				print("Plasmid " + plasmid + " has already been annotated!")
				print("---------------------------------------------------")

	print("\nLINEAR REGRESSION RUNNING")
	os.system("python lr_file_AL.py")
	os.system("python linear_regression.py")
	os.chdir("./../")

if __name__=="__main__":
	print("*******************")
	print("=== PLAS ANN ===")
	print("*******************\n")
	print("Select running option: ")
	print("0-Run entire program")
	print("1-Run linear regression ONLY (make sure you have all necessary files)")
	print("STOP-STOP PROGRAM")
	run_all=-1
	while True:
		try:
			run_all=input("Type your answer: ")
			if int(run_all)!=0 and int(run_all)!=1:
				print("\nPlease type valid binary number!")
			else:
				break
		except:
			if str(run_all) in "STOP" or str(run_all) in "^C":
				print("STOP DETECTED: EXITING PROGRAM")
				sys.exit()
			else:
				print("\nPlease type valid binary number!")
	main(run_all)
