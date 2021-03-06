import time
import Pyro4
import server

def run(jobs):
	dispatcher = server.dispatcher_setup()
	[dispatcher.putWork((i,jobs[i])) for i in range(len(jobs))]

	while dispatcher.resultQueueSize() < len(jobs):
		time.sleep(1)

	results = []
	[results.append(dispatcher.getResult()) for i in range(len(jobs))]

	#ensure results are returned in the same order they're put into the queue
	return [y[1] for y in sorted(results,key=lambda x: x[0])]

def poison():
	dispatcher = server.dispatcher_setup()
	dispatcher.Poison()

if __name__ == "__main__":
	jobs = range(10)
	results = run(jobs)
	poison()
	for r in results:
		print r
