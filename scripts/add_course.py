from server.models import Course
from server.models import University
from datetime import datetime
import csv

u = University.objects.get(name="University of Victoria")
#c = Course(name="CSC 111", start_date=datetime(2014, 5, 1), end_date=datetime(2014, 8, 31), university=u)
#c.save()

month = dict()
month['Jan'] = 1
month['Feb'] = 2
month['Mar'] = 3
month['Apr'] = 4
month['May'] = 5
month['Jun'] = 6
month['Jul'] = 7
month['Aug'] = 8
month['Sep'] = 9
month['Oct'] = 10
month['Nov'] = 11
month['Dec'] = 12

# read courses from file and save in database
csvfile = open('./scripts/courses.csv','rt')
print 'csvfile'
reader = csv.reader(csvfile, delimiter='|')   
for row in reader:
    print "row: ", row[0], row[1][8:12], row[1][:3], row[1][4:6]
    # check dates
    if (len(row[1])==4):
        sd = None
    else:
        sd=datetime(int(row[1][8:12]), month[row[1][:3]], int(row[1][4:6]))
        
    if (len(row[2])==4):
        ed = None
    else:
        ed = datetime(int(row[2][8:12]), month[row[2][:3]], int(row[2][4:6]))
        
    c = Course(name=row[0], start_date=sd, end_date=ed, university=u)
    c.save()
     
        
