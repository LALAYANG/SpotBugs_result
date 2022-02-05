import csv
import os
from hashlib import md5
from bs4 import BeautifulSoup


test_before_od_csv = './all_run_hadoop.csv'
save_csv = './result_hadoop.csv'


def get_output_xml_results(testcase_name, xml_file):

    os.system('echo $(pwd)')
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
                failedconstructor = str.format("{},{},{}", t, test_result, eachtest["time"])
                break
            else:
                t = str.format("{}.{}", eachtest["classname"], eachtest["name"])
                if t in tests:
                    t = str.format("{}.{}=DUPLICATE", eachtest["classname"], eachtest["name"])
                tests.add(t)
            tout.append(str.format("{},{},{}", t, test_result, eachtest["time"]))


        if failedconstructor != "":
            return failedconstructor
        else:
            for eachtest in tout:
                print(eachtest)
                if testcase_name in eachtest:
                    return eachtest
        return 'ERROR_Parse'

def run_All_tests():
    hash_md5 = md5()
    pair_tests = open(test_before_od_csv,"r")
    pair_tests_reader = csv.reader(pair_tests)

    
    for eachline in pair_tests_reader:
        project = eachline[0]
        module = eachline[1]
        test_1st = eachline[2]
        od_test = eachline[3]
        h_md5 = hash_md5.copy()
        h_md5.update(test_1st.encode())
        h_md5.update(od_test.encode())
        md5_str = h_md5.hexdigest()

        test_1st_method = eachline[2][::-1].replace(".","#",1)[::-1]
        od_test_method = eachline[3][::-1].replace(".","#",1)[::-1]
        dir = './repos/'+project+'/'+module+'/target/surefire-reports/'

        xml_test_1st = dir +'TEST-'+'.'.join(eachline[2].split('.')[0:-1])+'.xml'
        xml_od_test = dir +'TEST-'+'.'.join(eachline[3].split('.')[0:-1])+'.xml'
        print(xml_test_1st,xml_od_test)

        os.system('sh ~/java-flaky/run_all_before_od.sh '+project+' '+module+' '+test_1st_method+' '+od_test_method+' '+md5_str)
        # print(result)

        '''
        os.system('cd repos')
        os.system('cd '+project)
        os.system('mvn -pl '+module+'test -Dsurefire.runOrder=testorder -Dtest='+test_1st_method+','+od_test_method +' | tee -a'+md5_str+'.log')
        os.system('cd ..')
        '''

        test_1st_result = get_output_xml_results(test_1st,xml_test_1st)
        test_od_result = get_output_xml_results(od_test,xml_od_test)

        os.system('mv ' + xml_test_1st +' ./xml_log/'+md5_str+'_1.xml')
        os.system('mv ' + xml_od_test +' ./xml_log/'+md5_str+'_2.xml')

        final_result = []
        for each in test_1st_result.split(','):
           final_result.append(each)
        for each in test_od_result.split(','):
           final_result.append(each)
        final_result.append(md5_str)


        print(test_1st_result,test_od_result,md5_str)

        with open(save_csv,"a",newline='') as save:
            writer = csv.writer(save)
            writer.writerow(final_result)



run_All_tests()
        

