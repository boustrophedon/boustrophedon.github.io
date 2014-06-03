all:
	pelican
publish:
	pelican -s publishconf.py
clean:
	rm -r {tmp/,out/}drafts
	rm -r {tmp/,out/}category
	rm -r {tmp/,out/}feeds
	rm -r {tmp/,out/}tag
	rm -r {tmp/,out/}theme
	rm -r {tmp/,out/}images
	rm -r {tmp/,out/}author
	rm {tmp/,out/}*.html
