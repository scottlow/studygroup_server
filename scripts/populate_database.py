from server.models import Course, University, Student
from datetime import datetime


u = University(name="University of Victoria")
c = Course(name="CSc 110", start_date=datetime(2014, 5, 1), end_date=datetime(2014, 8, 31), university=u)
c.save()