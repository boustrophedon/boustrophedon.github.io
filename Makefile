all:
	pelican
publish:
	pelican -s publishconf.py
clean:
	rm -rf {tmp/,out/}*
