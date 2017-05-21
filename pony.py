''' Pony Express Solver

Usage:
	pony.py [options] <input>

-h, --help
-v, --verbose
'''
import docopt
import logging
from itertools import product

def main():

	args = docopt.docopt(__doc__, version='Pony Express Solver 1.0')
	input = open(args['<input>'])

	if args['--verbose']:
		logging.basicConfig(level=logging.DEBUG)
	
	tc = ingest_google_test_cases(args['<input>'])
	pprint(tc)
	sys.exit(0)
	
	T = int(input.readline())
	lines = []
	for tc in range(T):
		
		N, Q = map(int, input.readline().split())
		E = []
		S = []
		
		for n in range(N):
			ei, si = map(int, input.readline().split())
			E.append(ei)
			S.append(si)
		D = []
		for n in range(N):
			D.append(list(map(int, input.readline().split())))
		
		route_lookup = solve_fastest_routes(E,S,D)
		s = 'Case #%d:' % (tc+1)
		
		U = []
		K = []
		
		for q in range(Q):
			Ui, Ki = map(int, input.readline().split())
			s += ' %f' % route_lookup[Ui-1][Ki-1]
			U.append(Ui)
			K.append(Ki)
		s += '\n'
		print(s)

def solve_fastest_routes(E,S,D):
	logging.debug('solve_fastest_routes:')
	logging.debug('Max Distance: ', E)
	logging.debug('Speed       : ', S)
	
	V = len(D)
	
	INF = float('inf')

	# Initialize the matrix, diagonals are 0 weight
	# -1 translate to infinite cost
	for i,j in product(range(V), repeat=2):
		if i == j:
			D[i][j] = 0
		elif D[i][j] == -1:
			D[i][j] = INF
	#City Map 
	
	# Floyd-Warshal for Shortest routes for all edge combinations
	for k, i, j in product(range(V), repeat=3):
		if(D[i][j] > D[i][k] + D[k][j]):
			D[i][j] = D[i][k] + D[k][j]
	#Shortest Distance
	
	# Translate all shortest routes from SRC -> DST to TIME in hours
	# Drop out routes that are infeasible using SRC horse
	for i,j in product(range(V), repeat=2):	
		if E[i] >= D[i][j]: #If the horse is capable			
			D[i][j] /= (1.0 * S[i])
			logging.debug('%d -> %d: %f' % (i,j,D[i][j]))
		else:
			D[i][j] = INF
	#Distance converted to time
	
	for k, i, j in product(range(V), repeat=3):	
		if(D[i][j] > D[i][k] + D[k][j]):
			D[i][j] = D[i][k] + D[k][j]
	#SOLVED LOOKUP TABLE
	
	return D
	
if __name__ == '__main__':
	main()