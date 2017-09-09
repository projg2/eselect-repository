PREFIX = /usr/local
# used to locate repos.conf
SYSCONFDIR = /etc
# used for the default storage path
SHAREDSTATEDIR = /var
# used to keep downloaded repositories.xml
CACHEDIR = $(SHAREDSTATEDIR)/cache/eselect-repo
# install location for the Python helper
HELPERDIR = $(PREFIX)/lib/eselect-repo
# install location for the module
ESELECTDIR = /usr/share/eselect/modules

all: repository.eselect

repository.eselect: repository.eselect.in Makefile
	rm -f $@ $@.tmp
	sed \
		-e '/^CACHEDIR=/s^=.*$$^=$(CACHEDIR)^' \
		-e '/^SYSCONFDIR=/s^=.*$$^=$(SYSCONFDIR)^' \
		-e '/^SHAREDSTATEDIR=/s^=.*$$^=$(SHAREDSTATEDIR)^' \
		-e '/^HELPER=/s^=.*$$^=$(HELPERDIR)/eselect-repo-helper^' \
		$< > $@.tmp
	chmod a+r $@.tmp
	mv $@.tmp $@

clean:
	rm -f repository.eselect

install: repository.eselect
	install -d $(DESTDIR)$(HELPERDIR)
	install -m0755 eselect-repo-helper $(DESTDIR)$(HELPERDIR)/
	install -d $(DESTDIR)$(ESELECTDIR)
	install -m0644 repository.eselect $(DESTDIR)$(ESELECTDIR)/

.PHONY: all clean install
