def process():
    name = []
    family = []
    num = []

    f1=open("S1.txt","r")
    lines=f1.readlines()
    f1.close()

    for line in lines:
        if line.strip():
            part=line.split()
            if len(part)==3:
                first_name=part[0]
                last_name=part[1]
                phone_number=part[2]
                if len(phone_number) == 11 and phone_number.isdigit() and phone_number.startswith("09"):
                    name.append(first_name)
                    family.append(last_name)
                    num.append(phone_number)

    output = "output file.txt"
    f2 = open(output,"w")
    f2.write("Names: "+" ".join(name)+"\n")
    f2.write("Surnames: "+" ".join(family)+"\n")
    f2.write("Numbers: "+" ".join(num))
    f2.close()

    print("completed!")

process()