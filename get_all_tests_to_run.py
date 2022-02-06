from bs4 import BeautifulSoup
import os
import sys
import csv

dirs = [
    './repos/querydsl/querydsl-hibernate-search/target/surefire-reports'
]
#dir = 'D:/java-flaky'

all_tests_save_csv='./all_tests_query.csv'

all_results=[]

def get_all_xml(dirs):

    for each_dir in dirs:
        files = os.listdir(each_dir)
        project=each_dir.split('/')[2]
        module = '/'.join(each_dir.split('/')[3:-2])
        for eachfile in files:
            file_path = os.path.join(each_dir, eachfile)
            if ".xml" in file_path:
                print(file_path)
                get_all_tests(project, module, file_path)


def get_all_tests(project,module,xml_file):
    with open(xml_file) as fp:
        xml_content = BeautifulSoup(fp, features="xml")
        tout = []
        failedconstructor = ""
        tests = set()
        for eachtest in xml_content.testsuite.findAll("testcase"):
            test_result = "unknown"

            if eachtest.find('failure'):
                test_result = "failure"
            elif eachtest.find('error'):
                test_result = "error"
            else:
                test_result = "pass"

            if eachtest["name"] == eachtest["classname"] or eachtest["name"] == "":
                t = xml_file[3]
                failedconstructor = str.format("{},{},{},{},{}", project, module, t, test_result, eachtest["time"])
                break
            else:
                t = str.format("{}.{}", eachtest["classname"], eachtest["name"])
                if t in tests:
                    t = str.format("{}.{}=DUPLICATE", eachtest["classname"], eachtest["name"])
                tests.add(t)

            tout.append(str.format("{},{},{},{},{}", project, module, t, test_result, eachtest["time"]))

        if failedconstructor != "":
            print(failedconstructor)
            all_results.append(failedconstructor)
        else:
            for eachtest in tout:
                print(eachtest)
                all_results.append(eachtest)

    with open(all_tests_save_csv,"w",newline='') as tests_csv:
        writer = csv.writer(tests_csv)
        for each in all_results:
            writer.writerow(each.split(','))

get_all_xml(dirs)