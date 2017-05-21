import pytest
import pony

test_case_files = (
	('input.txt', 'output.txt'),
	('C-small-practice.in', 'C-small-practice.out'),
	('C-large-practice.in', 'C-large-practice.out'),
	)

def ingest_google_test_case_output(fpath):
	with open(fpath) as input:
		
		answers = []
		case_nr = 1
		for line in input.readlines():
			if 'Case' not in line:
				continue
			a = line.split(':')[1]
			a = a.split()
			a = tuple(map(float, a))
			answers.append(a)
	return answers
	
tc = []
for i, o in test_case_files:
	_tc = pony.ingest_google_test_cases(i)
	answers = ingest_google_test_case_output(o)
	assert(len(_tc) == len(answers))
	for x in range(len(_tc)):
		_tc[x]['answers'] = answers[x]
	tc.extend(_tc)
	
import pprint; pprint.pprint(tc)
	
@pytest.mark.parametrize('tc', tc)
def test_fastest_routes(tc):
	route_lookup = pony.solve_fastest_routes(tc)
	answers = [route_lookup[src-1][dst-1] for src, dst in tc['queries']]		
	for x in range(len(answers)):
		assert pytest.approx(answers[x], abs=1e-6, rel=1e-6) == tc['answers'][x]
	#assert answers == pytest.approx(tc['answers'])