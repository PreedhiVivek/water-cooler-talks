all: jitsi-listener jitsi-listener.service
.PHONY: all jitsi-listener install uninstall
lib_dir = /usr/local/lib/jitsi_listener
conf_dir = /usr/local/etc/jitsi_listener
service_dir = /etc/systemd/system
venv = $(lib_dir)/venv_listener

install: $(service_dir) jitsi-listener.service
	@echo Installing the service file...
	cp jitsi-listener.service $(service_dir)
	chown root:root $(service_dir)/jitsi-listener.service
	chmod 644 $(service_dir)/jitsi-listener.service

	@echo Installing library files...
	mkdir -p $(lib_dir)
	cp jitsi_listener.py $(lib_dir)
	chown root:root $(lib_dir)/*
	chmod 644 $(lib_dir)/*

	@echo Installing configuration files...
	mkdir -p $(conf_dir)
	cp jitsi_listener.env $(conf_dir)
	chown root:root $(conf_dir)/*
	chmod 644 $(conf_dir)/*

	@echo Creating python virtual environment and Installing packages...
	python3 -m venv $(venv)
	$(venv)/bin/pip3 install -r requirements.txt

	@echo Installation done.

startservice:
	-systemctl start jitsi-listener.service
	@echo Service status...
	-systemctl status jitsi-listener.service

uninstall:
	-systemctl stop jitsi-listener.service
	-systemctl disable jitsi-listener.service
	-rm -r $(lib_dir)
	-rm -r $(conf_dir)
	-rm -r $(service_dir)/jitsi-listener.service
	@echo Uninstall done.