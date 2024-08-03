ls
cd data/
ls
cd db/
ls
exit
ls
cd data/
ls
cd db/
ls
/Users/brandonblackwell/Desktop/Software-Engineering/database_development/dev_env/bin/python /Users/brandonblackwell/Desktop/Software-Engineering/database_development/main.py
quit
exit
ls
cd data/
ls
cd db/
ls
cat healthcare_dataset.csv 
exit
exit
ls
cd da
cd data/
ls
cd db
ls
cat healthcare_dataset.csv 
pwd
ls
cd ..
cd ..
pwd
cd ..
pwd
exit
mongoimport -d dev_dummy -c healthcare -type=csv -file=/data/db/healthcare_dataset.csv -columnsHaveTypes -fields="Name.string(), Age.int32(), Gender.string(), Blood Type.string(), Medical Condition.string(), Date of Admission.auto(), Doctor.auto(), Hospital.auto(), Insurance Provider.auto(), Billing Amount.auto(), Room Number.auto(), Admission Type.auto(), Disharge Date.auto(), Medication.auto(), Test Results.auto()"
mongoimport --help
clear
mongoimport -d dev_dummy -c healthcare --type=csv --file=/data/db/healthcare_dataset.csv --columnsHaveTypes --fields="Name.string(), Age.int32(), Gender.string(), Blood Type.string(), Medical Condition.string(), Date of Admission.auto(), Doctor.auto(), Hospital.auto(), Insurance Provider.auto(), Billing Amount.auto(), Room Number.auto(), Admission Type.auto(), Disharge Date.auto(), Medication.auto(), Test Results.auto()"
mongoimport -d dev_dummy -c healthcare --type=csv --file=/data/db/healthcare_dataset.csv --columnsHaveTypes --fields="Name.string(), Age.auto(), Gender.string(), Blood Type.string(), Medical Condition.string(), Date of Admission.auto(), Doctor.auto(), Hospital.auto(), Insurance Provider.auto(), Billing Amount.auto(), Room Number.auto(), Admission Type.auto(), Disharge Date.auto(), Medication.auto(), Test Results.auto()"
exit
