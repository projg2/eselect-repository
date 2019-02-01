PREFIX = /usr/local
# used to locate repos.conf
SYSCONFDIR = /etc
# used for the default storage path
SHAREDSTATEDIR = /var
# used for the default manpage path
MANPAGEDIR = $(PREFIX)/share/man

# used for the default cache path (for repositories.xml)
CACHEDIR = $(SHAREDSTATEDIR)/cache
# used to keep the configuration file
CONFIGDIR = $(SYSCONFDIR)/eselect
# install location for the Python helper
HELPERDIR = $(PREFIX)/lib/eselect-repo
# install location for the module
ESELECTDIR = /usr/share/eselect/modules

CONFIG = $(CONFIGDIR)/repository.conf
HELPER = $(HELPERDIR)/eselect-repo-helper

all: repository.eselect

repository.eselect: repository.eselect.in Makefile
	rm -f $@ $@.tmp
	sed \
		-e '/^CACHEDIR=/s^=.*$$^=$(CACHEDIR)^' \
		-e '/^SYSCONFDIR=/s^=.*$$^=$(SYSCONFDIR)^' \
		-e '/^SHAREDSTATEDIR=/s^=.*$$^=$(SHAREDSTATEDIR)^' \
		-e '/^HELPER=/s^=.*$$^=$(HELPER)^' \
		-e '/^CONFIG=/s^=.*$$^=$(CONFIG)^' \
		$< > $@.tmp
	chmod a+r $@.tmp
	mv $@.tmp $@

repository.eselect.5: repository.eselect.5.in
	rm -f $@.tmp
	sed 's=/etc/eselect/repository.conf=$(CONFIG)=' $< > $@.tmp
	chmod a+r $@.tmp
	mv $@.tmp $@

clean:
	rm -f repository.eselect

install: repository.eselect repository.eselect.5
	install -d $(DESTDIR)$(HELPERDIR)
	install -m0755 eselect-repo-helper $(DESTDIR)$(HELPER)
	install -d $(DESTDIR)$(ESELECTDIR)
	install -m0644 repository.eselect $(DESTDIR)$(ESELECTDIR)/
	install -d $(DESTDIR)$(CONFIGDIR)
	install -m0644 eselect-repo.conf $(DESTDIR)$(CONFIG)
	install -d $(DESTDIR)$(MANPAGEDIR)/man5/
	install -m0644 repository.eselect.5 $(DESTDIR)$(MANPAGEDIR)/man5/

.PHONY: all clean install
