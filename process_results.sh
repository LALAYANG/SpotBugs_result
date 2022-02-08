# This script generates:
# (1) all_results.csv which contains all of the execution results from all projects/modules of the one-by-one experiments done by Yang
# (2) new-victims.txt which contains the fully qualified names of the newly found victims
# (3) new-polluters.txt which contains the fully qualified names of the newly found polluters
# To run the script invoke the following in this directory (the directory that contains result-*.csv files)
# bash process_results.sh

cat result_* > all_results.csv

# for each suspected victim remove all NIO runs
for g in $(for f in $(cut -d, -f4,5 all_results.csv | grep -v ,pass ); do grep ",$f," result_*; done | grep ,pass, | cut -d, -f4 | sort -u); do
    num=$(grep -n  "^$g,.*,.*,$g," all_results.csv | cut -d':' -f1)
    sed -i "${num}d" all_results.csv
done

# look for victims by first searching for tests that did not pass when run second but yet the first test passed. The second part gets only tests that passed when it is run first (to filter out tests that always fail)
victims=$(comm -12 <( for f in $(cut -d, -f4,5 all_results.csv | grep -v ,pass ); do grep ",$f," all_results.csv; done | grep ,pass, | cut -d, -f4 | sort -u) <( cut -d, -f-2 all_results.csv | grep ,pass$ | cut -d, -f1 | sort -u ) )

# save the newly found victims
echo "$victims" > new-victims.txt

# save the new polluters by finding, for each of the victims, the rows where the victim failed but the first test passed
for g in $(echo "$victims"); do cut -d, -f-5 all_results.csv | grep ",${g},failure\|,${g},error$"; done | grep "^.*,pass," | cut -d, -f1 | sort -u > new-polluters.txt

# comm -23 <( cat new-polluters.txt ) <( cat ../known-polluters.txt ) | wc -l
# comm -23 <( cat new-victims.txt ) <( cat ../known-victims.txt ) | wc -l
