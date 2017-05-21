''' Pony Express Solver

Usage:
	pony.py [options] <input>

-h, --help
-v, --verbose
'''
import docopt
import logging
from itertools import product
import collections

Horse = collections.namedtuple('Horse', 'max_distance, speed')

def ingest_google_test_cases(fpath):
	
	with open(fpath) as input:
		
		test_cases = []
		
		T = int(input.readline())
		for tc in range(T):
			
			nr_cities, nr_queries = map(int, input.readline().split())
			
			horses = []
			for i in range(nr_cities):
				horses.append(Horse(*map(int, input.readline().split())))
			
			map_edges = []
			for i in range(nr_cities):
				map_edges.append(list(map(int, input.readline().split())))
			
			queries = []
			for nr_queries in range(nr_queries):
				queries.append(tuple(map(int, input.readline().split())))
			
			test_cases.append(dict(
				id='%s:%d' % (fpath, tc),
				horses=horses, 
				map_edges=map_edges, 
				queries=queries,
				))
	return test_cases

def main():

	args = docopt.docopt(__doc__, version='Pony Express Solver 1.0')
	input = open(args['<input>'])

	if args['--verbose']:
		logging.basicConfig(level=logging.DEBUG)
	
	tc = ingest_google_test_cases(args['<input>'])
	
	for i, test_case in enumerate(tc):
		route_lookup = solve_fastest_routes(test_case)
		answers = [route_lookup[src-1][dst-1] for src, dst in test_case['queries']]		
		print('Case #%d:' % (i+1), ' '.join(('%f' % x for x in answers)))

def solve_fastest_routes(test_case):
	horses = test_case['horses']
	D = test_case['map_edges']
	
	V = len(D)
	
	INF = float('inf')

	# Initialize the matrix, diagonals are 0 weight
	# -1 translate to infinite cost
	for i,j in product(range(V), repeat=2):
		if i == j:
			D[i][j] = 0
		elif D[i][j] == -1:
			D[i][j] = float('inf')
	#City Map 
	
	# Floyd-Warshal for Shortest routes for all edge combinations
	for k, i, j in product(range(V), repeat=3):
		if(D[i][j] > D[i][k] + D[k][j]):
			D[i][j] = D[i][k] + D[k][j]
	#Shortest Distance
	
	# Translate all shortest routes from SRC -> DST to TIME in hours
	# Drop out routes that are infeasible using SRC horse
	for i,j in product(range(V), repeat=2):	
		if horses[i][0] >= D[i][j]: #If the horse is capable			
			D[i][j] /= (1.0 * horses[i][1])
			logging.debug('%d -> %d: %f' % (i,j,D[i][j]))
		else:
			D[i][j] = float('inf')
	#Distance converted to time
	
	for k, i, j in product(range(V), repeat=3):	
		if(D[i][j] > D[i][k] + D[k][j]):
			D[i][j] = D[i][k] + D[k][j]
	#SOLVED LOOKUP TABLE
	
	return D
	
if __name__ == '__main__':
	main()