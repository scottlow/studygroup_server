from server.models import Course
from server.models import University
from datetime import datetime

u = University.objects.get(name="University of Victoria")
c = Course(name="CSc 111", start_date=datetime(2014, 5, 1), end_date=datetime(2014, 8, 31), university=u)
c.save()