import pytest
import pony

test_case_files = (
	('input.txt', 'output.txt'),
	('C-small-practice.in', 'C-small-practice.out'),
	('C-large-practice.in', 'C-large-practice.out'),
	)

def ingest_google_test_cases(fpath):
	
	with open(fpath) as input:
		
		test_cases = []
		
		T = int(input.readline())
		for tc in range(T):
			
			nr_cities, nr_queries = map(int, input.readline().split())
			
			horses = []
			for i in range(nr_cities):
				horses.append(tuple(map(int, input.readline().split())))
			
			map_edges = []
			for i in range(nr_cities):
				map_edges.append(list(map(int, input.readline().split())))
			
			queries = []
			for nr_queries in range(nr_queries):
				queries.append(tuple(map(int, input.readline().split())))
			
			test_cases. append(dict(id='%s:%d' % (fpath, tc), horses=horses, map_edges=map_edges, queries=queries)
	return test_cases
	
def ingest_google_test_case_output(fpath):
	with open(fpath) as input:
		
		answers = {}
		case_nr = 1
		for line in input.readlines():
			if 'Case' not in line:
				continue
			a = line.split(':')[1]
			a = a.split()
			a = tuple(map(float, a))
			answers['%s:%d' % (fpath, case_nr)] = a
			case_nr += 1
			
	return answers
	
tc = []
for i, o in test_case_files:
	_tc = ingest_google_test_cases(i))
	
	tc.append(_tc)
	
print(tc)

answers = {}
for f in test_case_output_files:
	answers.update(ingest_google_test_case_output(f))
	
print(answers)
