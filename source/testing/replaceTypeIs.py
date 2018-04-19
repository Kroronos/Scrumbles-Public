import re
pattern = r'^( *\w+ )type\((\w+)\) *== *ScrumblesObjects\.(User|Sprint|Comment|Project):$'

out = ''

lines = open('test.py','r').read().splitlines()

for line in lines:
	result = re.match(pattern,line)
	if result:
		groups = result.groups()
		out += "{}repr({}) == \"<class 'data.ScrumblesObjects.{}'>\":\n".format(groups[0],groups[1],groups[2])
	else:
		out += line+'\n'

open('test.py','w').write(out)