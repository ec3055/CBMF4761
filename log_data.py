import sys

f = open("log.txt", "a")

f.write("------log---------\n"+str(sys.argv[1])+"\n")
f.close()