from bs4 import BeautifulSoup
import httplib2
import csv
import time

# Variables
course_vals = []
csvfile = open('courses.csv', 'wb')
csv_writer = csv.writer(csvfile, delimiter='|', quotechar='|', quoting=csv.QUOTE_MINIMAL)

# Get course keys
url = "https://www.uvic.ca/BAN2P/bwckgens.p_proc_term_date"
params = "p_calling_proc=bwckschd.p_disp_dyn_sched&p_term=201405"

h = httplib2.Http()

resp, page = h.request(url, "POST", params)

soup = BeautifulSoup(page)
select = soup.find(id='subj_id')
courses = select.find_all('option')

for course in courses:
	course_vals.append(course.attrs['value'])

# print course_vals

# Start making proper requests
url = "https://www.uvic.ca/BAN2P/bwckschd.p_get_crse_unsec"
params_tmpl = "term_in=201405&sel_subj=dummy&sel_day=dummy&sel_schd=dummy&sel_insm=dummy&sel_camp=dummy&sel_levl=dummy&sel_sess=dummy&sel_instr=dummy&sel_ptrm=dummy&sel_attr=dummy&sel_subj={0}&sel_crse=&sel_title=&sel_schd=%25&sel_insm=%25&sel_from_cred=&sel_to_cred=&sel_camp=%25&sel_levl=%25&sel_ptrm=%25&sel_instr=%25&begin_hh=0&begin_mi=0&begin_ap=a&end_hh=0&end_mi=0&end_ap=a"

for j in range(0, len(course_vals)):
	title_text = []
	date_text = []

	params = params_tmpl.format(course_vals[j])
	resp, page = h.request(url, "POST", params)

	soup = BeautifulSoup(page)
	titles = soup.find_all(class_='ddtitle')

	for title in titles:
		c = title.find('a').string.split('-')
		title_text.append([c[2].strip(), c[0].strip().title(), c[3].strip()])

	big_data_table = soup.find(class_='datadisplaytable')
	data_tables = big_data_table.find_all(class_='datadisplaytable')

	for table in data_tables:
		entries = table.find_all(class_='dddefault')
		date = entries[4].string
		split_date = date.split(' - ')
		date_text.append([split_date[0], split_date[1]])

	# print title_text
	# print len(title_text)

	# print date_text
	# print len(date_text)

	for i in range(0, len(title_text)):
		try:
			if('A01' in title_text[i][2]):
				if(' 5' not in title_text[i][0] and ' 6' not in title_text[i][0]):
					csv_writer.writerow([title_text[i][0] + ' - ' + title_text[i][1]] + date_text[i])
				else:
					csv_writer.writerow([title_text[i][0] + ' - ' + title_text[i][1]] + ['null', 'null'])
		except IndexError:
			csv_writer.writerow([title_text[i][0] + ' - ' + title_text[i][1]] + ['null', 'null'])