'''
Examples:

Run for 15 seconds maxing out all processors:
  stress.py 15

Run for 15 seconds with each subprocess sleeping for 0.01s every 100,000 cycles across all processors (on my machine it's about a 50% duty cycle):
  stress.py 15 0.01 100000

Run for 15 seconds, sleep 0.01s every 100,000 cycles, but only use a max of 8 processors:
  stress.py 15 0.01 100000 8
'''

import time, sys, random, requests, json
from itertools import repeat
from multiprocessing import Pool, cpu_count


def stress_cpu(x, runtime=1, busycycles=100000):
	timeout = time.time() + runtime
	cnt = 0

	while True:

		# Define a random amount of time to let the CPU rest after certain cycles of stress
		stress_sleeptime = random.randrange(0, 4)

		# Make it 40% possible to get a 0
		if stress_sleeptime == 4: 
			stress_sleeptime = 0

		# Break the loop after the defined runtime's over
		if time.time() > timeout:
			break

		# Let the processor rest after a certain number of busycycles
		if stress_sleeptime and cnt % busycycles == 0:
			print(f'Resting for {stress_sleeptime} seconds')
			time.sleep(stress_sleeptime)

		# Stress the processes
		x*x
		cnt += 1


def api_call():
	url = "https://rickandmortyapi.com/api/character/17"

	payload = ""
	headers = {}

	response = requests.request("GET", url, headers=headers, data=payload)

	print(response.text)

if __name__ == '__main__':
	while(True):
		sleeptime = random.randrange(1, 1200)

		runtime = random.randrange(60, 600)                 if len(sys.argv) <= 1 else float(sys.argv[1])
		busycycles = random.randrange(4000000, 9000000)	    if len(sys.argv) <= 2 else float(sys.argv[2])
		processes = cpu_count()                             if len(sys.argv) <= 3 else int(sys.argv[4])     if 0 < int(sys.argv[3]) <= cpu_count() else cpu_count()
		
		print(f'Running for {runtime}s with sleep time of {sleeptime} seconds. CPU will rest every {busycycles} cycles, utilizing {processes} cores')

		# Stress
		pool = Pool(processes)
		pool.starmap(stress_cpu, zip(range(processes), repeat(runtime), repeat(busycycles)))

		# Call an API and sleep our code
		print(f"Finished stressing. Calling an API")
		api_call()
		print(f"Sleeping for {sleeptime} seconds")
		time.sleep(sleeptime)