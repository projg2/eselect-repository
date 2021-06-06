import subprocess

import pytest


REPOS_XML = b'''<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE repositories SYSTEM "http://www.gentoo.org/dtd/repositories.dtd">
<repositories xmlns="" version="1.0">
  <repo quality="experimental" status="unofficial">
    <name>foo</name>
    <description lang="en">test foo repository</description>
    <homepage>https://example.com/foo</homepage>
    <owner type="person">
      <email>fooowner@example.com</email>
      <name>Owner of Foo</name>
    </owner>
    <source type="git">https://example.com/foo.git</source>
    <source type="git">git@example.com:foo.git</source>
    <feed>https://example.com/foo/atom.xml</feed>
  </repo>
  <repo quality="experimental" status="unofficial">
    <name>bar</name>
    <description lang="en">test bar repository</description>
    <homepage>https://example.com/bar</homepage>
    <owner type="person">
      <email>barowner@example.com</email>
      <name>Owner of Bar</name>
    </owner>
    <source type="git">git@example.com:bar.git</source>
    <source type="git">https://example.com/bar.git</source>
    <feed>https://example.com/bar/atom.xml</feed>
  </repo>
  <repo quality="experimental" status="unofficial">
    <name>no-homepage</name>
    <description lang="en">i don't have a home :-(</description>
    <owner type="person">
      <email>nohomeowner@example.com</email>
      <name>Owner of Nohome</name>
    </owner>
    <source type="git">git@example.com:nohome.git</source>
    <source type="git">https://example.com/nohome.git</source>
  </repo>
  <repo quality="experimental" status="unofficial">
    <name>weird-source</name>
    <description lang="en">this one's got custom syncer</description>
    <owner type="person">
      <email>weirdowner@example.com</email>
      <name>Owner of Weird</name>
    </owner>
    <source type="weird-thing">https://example.com/weird-source</source>
  </repo>
</repositories>
'''


@pytest.fixture
def repositories_xml(tmp_path):
    path = tmp_path / 'repositories.xml'
    with open(path, 'wb') as f:
        f.write(REPOS_XML)
    return path


@pytest.fixture
def repos_conf(tmp_path):
    path = tmp_path / 'repos.conf'
    return open(path, 'w')


class Runner:
    def __call__(self, repositories_xml, repos_conf, args):
        subp = subprocess.Popen(
            ['./eselect-repo-helper',
             '--repositories-xml', repositories_xml,
             '--repos-conf', repos_conf,
             *args],
            stdout=subprocess.PIPE)
        sout, _ = subp.communicate()
        return subp.returncode, sout


@pytest.fixture
def runner():
    return Runner()
