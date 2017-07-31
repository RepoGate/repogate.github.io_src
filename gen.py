# Copyright 2017 Sean Kelleher. All rights reserved.

#!/usr/bin/env python

import sys
import collections

Line = collections.namedtuple('Line', ['text', 'indent', 'kids'])

sections = []
with open(sys.argv[1]) as f:
    cur_sect_path = [Line(None, -1, sections)]

    for line in f:
        line = line[:-1]

        if len(line) == 0:
            continue

        indent = 0
        for c in line:
            if c == ' ':
                indent += 1
            else:
                break

        line = line[indent:]

        while indent <= cur_sect_path[-1].indent:
            cur_sect_path.pop()

        cur_sect_path[-1].kids.append(Line(line, indent, []))

        if indent != cur_sect_path[-1].indent:
            cur_sect_path.append(cur_sect_path[-1].kids[-1])

template = ''
with open('template.html') as f:
    template = ''.join(line for line in f)
nav = '\n'

pages = [section.text.split()[0].lower()+'.html' for section in sections]
pages[0] = 'index.html'
for i in range(1, len(sections)):
    nav += '<li><a href="'+pages[i]+'">'+sections[i].text+'</a></li>\n'
template = template.replace('<!-- nav -->', nav)

def render_section(lv, section):
    if len(section.kids) == 0:
        return section.text + '\n'
    else:
        kids = ''
        for kid in section.kids:
            kids += render_section(lv+1, kid)
        return \
            '<h'+str(lv)+'>'+section.text+'</h'+str(lv)+'>\n'+\
            '\n'+\
            '<section>\n'+\
            kids+\
            '</section>\n'

for i in range(len(sections)):
    with open('build/'+pages[i], 'w') as f:
        section = render_section(2, sections[i])
        f.write(template.replace('<!-- sections -->', section))
