import re
import os
pattern = r'^( *\w+ )type\((\w+)\) *== *ScrumblesObjects\.(User|Sprint|Comment|Project):$'

out = ''

paths = ['../data/','../frames/','../styling/','../testing/','../views/' ]

files = []

for path in paths:
    for filename in os.listdir(path):
        files.append(path+filename)


for file in files:
    lines = open(file, 'r').read().splitlines()
    for line in lines:
        result = re.match(pattern,line)
        if result:
            groups = result.groups()
            out += "{}repr({}) == \"<class 'data.ScrumblesObjects.{}'>\":\n".format(groups[0],groups[1],groups[2])
        else:
            out += line+'\n'

    open(file,'w').write(out)