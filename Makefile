init:
	pip3 install -r requirements.txt

run:
	python3 -m sectograph

rcc:
	/usr/local/Cellar/qt/6.0.2/bin/rcc -binary sectograph/resources/rc.qrc -o sectograph/resources/rc.rcc

format:
	black launcher.py sectograph

.PHONY: init run rcc format
