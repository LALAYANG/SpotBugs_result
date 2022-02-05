project=$1
module=$2
test_one=$3
test_two=$4
md5_str=$5


cd repos
cd $project
mvn -pl $module test -Dsurefire.runOrder=testorder -Dtest=$test_one,$test_two | tee -a $md5_str.log
cd ..
