l=["A","B","C","D"]

f=open("k.txt","w")
 
f.writelines(l)
f.close()

l=["A","B","C","D"]
 
f=open("k.txt","a")
 
for line in l:
    f.write(line+'\n')
f.close()

f = open("demofile3.txt", "a")
f.writelines(["\nSee you soon! \t Over and out.", "\n"])
f.close()

f=open("k.txt","a")
f.writelines(["Block Size\t", str(5), "\n"])
f.writelines(["Block Size", "\t", str(6), "\n"])
f.close()
