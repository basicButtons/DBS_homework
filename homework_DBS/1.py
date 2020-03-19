import csv
with open("type.csv","w",newline="",encoding="utf-8")  as f:
    writer =csv.writer(f)
    writer.writerow(["",""])
with open("Mtype.csv",'r',newline="",encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        if len(row[1]) > 0:
            regions = row[1].split("+")
            for region in regions:
                res = [row[0],region]
                print('res = ' + str(res))
                with open("type.csv","a",newline="",encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerow(res)
        else:
            print(row)
            with open("type.csv","a",newline="",encoding="utf-8") as f:
                writer = csv.writer(f)
                print('none = ' + str([row[0],'']))
                writer.writerow([row[0],""])

