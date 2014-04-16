from server.models import Course, University, Student
from datetime import datetime

u = University(name="University of Victoria", latitude="48.4630959", longitude="-123.3121053")
u.save()