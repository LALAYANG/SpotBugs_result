import csv

all_tests_csv = './all_tests.csv'
od_tests_csv = './allod.csv'

save_result= './query.csv'
all = []
od = []

def generate_final_data():
    final = []
    all_tests = open(all_tests_csv,"r")
    all_tests_reader = csv.reader(all_tests)

    od_tests = open(od_tests_csv,"r")
    od_tests_reader = csv.reader(od_tests)


    for each_od in od_tests_reader:
        od.append(each_od)
    for each_test in all_tests_reader:
        all.append(each_test)

    print(len(od),len(all))

    for o in od:
        for a in all:
            if o[0].split('/')[-1]+o[2] == a[0]+a[1]:
                temp = a[0:3]
                temp.append(o[3])
                temp.append(o[4])
                final.append(temp)
                
    print(len(final))
    num=0
    with open(save_result,"w",newline='') as result_csv:
        writer = csv.writer(result_csv)
        for each in final:
            if each[1] == 'querydsl-hibernate-search':
                writer.writerow(each)
                num+=1
    print(num)

generate_final_data()