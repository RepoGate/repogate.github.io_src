# Copyright 2017 Sean Kelleher. All rights reserved.

TGTDIR=build

all: \
	$(TGTDIR)/index.html \
	$(TGTDIR)/index.css

$(TGTDIR)/index.html: sections.txt template.html gen.py
	python gen.py $<

$(TGTDIR)/index.css: index.css
	cp $< $@
