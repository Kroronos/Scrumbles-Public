import re
import os
pattern = r'^( *\w+ )type\((\w+)\) *== *ScrumblesObjects\.(User|Sprint|Comment|Project):$'



paths = ['../data/','../frames/','../styling/','../testing/','../views/' ]

files = []

for path in paths:
    for filename in os.listdir(path):
        files.append(path+filename)


for file in files:
    out = ''
    try:
        lines = open(file, 'r').read().splitlines()
    except:
        print('Could not open file {}'.format(file))
    for line in lines:
        result = re.match(pattern,line)
        if result:
            print('found {}\n in file: {}'.format(line,file))
            groups = result.groups()
            out += "{}repr({}) == \"<class 'data.ScrumblesObjects.{}'>\":\n".format(groups[0],groups[1],groups[2])
        else:
            out += line+'\n'
    try:
        open(file,'w').write(out)
    except:
        print('Could not open file {}'.format(file))