import requests

BASE = "http://127.0.0.1:5000/"

response = requests.get(BASE + "batch_jobs?filter[max_nodes]=20")
print("Batch records with max nodes of 20 is the following:\n")
print(response.json())
print('\n\n\n')

response = requests.get(BASE + "batch_jobs?filter[min_nodes]=15000")
print("Batch records with min nodes of 15000 is the following:\n")
print(response.json())

print('\n\n\n')

response = requests.get(BASE + "batch_jobs?filter[submitted_after]='2018-03-04T23:45:37+00:00'")
print("Batch records submitted after 2018-03-04T23:45:37+00:00 is the following:\n")
print(response.json())

print('\n\n\n')

response = requests.get(BASE + "batch_jobs?filter[submitted_before]='2018-02-28T00:07:13+00:00'")
print("Batch records submitted before 2018-02-28T00:07:13+00:00 is the following:\n")
print(response.json())

print('\n\n\n')

response = requests.get(BASE + "batch_jobs?filter[submitted_after]='2018-03-04T18:57:37+00:00'&filter[submitted_before]='2018-03-04T20:24:01+00:00'&filter[min_nodes]=100&filter[max_nodes]=1900")
print("Batch records submitted before 2018-03-04T20:24:01+00:00 and submitted after 2018-03-04T18:57:37+00:00 that uses between 100 and 1900 nodes (inclusive) is the following:\n")
print(response.json())

print('\n\n\n')
