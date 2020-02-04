import requests

r = requests.post('http://127.0.0.1:5000', json={"jobs": {"unigue_job_name": {"date": "3.2.2020", 'printer': 'Test_printer',
                                                                              'print_job': "Job that do it all", 'page_format': 'A4', 'number_of_pages': 12, 'ip': '4.4.4.4'}}})
r = requests.post('http://127.0.0.1:5000', json={"jobs": {"unigue_job_nameľ": {"date": "3.2.2020", 'printer': 'Test_printer',
                                                                              'print_job': "Job that do it all", 'page_format': 'A4', 'number_of_pages': '12', 'ip': '4.4.4.4'}}})
# r = requests.post('http://127.0.0.1:5000', json={"jobs": {"test2": "Test"}})
# r = requests.post('http://127.0.0.1:5000', json={"jobs": {"test3": "Test"}})
# r = requests.post('http://127.0.0.1:5000', json={"jobs": {"test4": "Test"}})
# r = requests.post('http://127.0.0.1:5000', json={"jobs": {"test15": "Test"}})
# r = requests.post('http://127.0.0.1:5000', json={"jobs": {"test6": "Test"}})
# r = requests.post('http://127.0.0.1:5000', json={"jobs": {"test7": "Test"}})

# json={"jobs": {print_job: date + " " + printer + " " + username + " " + print_job + " " + paper_format + " " + number_of_pages + " " + ip}})