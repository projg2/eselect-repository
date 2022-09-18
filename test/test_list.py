import pytest


def test_repos_conf_empty(repositories_xml, repos_conf, runner):
    assert (
        runner(repositories_xml, repos_conf.name, ['list']) ==
        (0, b'bar disabled https://example.com/bar\n'
            b'foo disabled https://example.com/foo\n'
            b'no-homepage disabled \n'
            b'weird-source disabled \n'))


@pytest.mark.parametrize('uri', ['https://example.com/foo.git',
                                 'git@example.com:foo.git'])
def test_repos_conf_match(uri, repositories_xml, repos_conf, runner):
    repos_conf.write(f'''
[foo]
location = /tmp/foo
sync-type = git
sync-uri = {uri}
''')
    repos_conf.close()

    assert (
        runner(repositories_xml, repos_conf.name, ['list']) ==
        (0, b'bar disabled https://example.com/bar\n'
            b'foo enabled https://example.com/foo\n'
            b'no-homepage disabled \n'
            b'weird-source disabled \n'))


@pytest.mark.parametrize(
    'proto,uri',
    [('git', 'https://example.com/bar.git'),
     ('hg', 'https://example.com/foo.git'),
     ])
def test_repos_conf_mismatch(proto, uri, repositories_xml, repos_conf,
                             runner):
    repos_conf.write(f'''
[foo]
location = /tmp/foo
sync-type = {proto}
sync-uri = {uri}
''')
    repos_conf.close()

    assert (
        runner(repositories_xml, repos_conf.name, ['list']) ==
        (0, b'bar disabled https://example.com/bar\n'
            b'foo need-update https://example.com/foo\n'
            b'no-homepage disabled \n'
            b'weird-source disabled \n'))


def test_repos_conf_no_uri(repositories_xml, repos_conf, runner):
    repos_conf.write('''
[foo]
location = /tmp/foo
''')
    repos_conf.close()

    assert (
        runner(repositories_xml, repos_conf.name, ['list']) ==
        (0, b'bar disabled https://example.com/bar\n'
            b'foo need-update https://example.com/foo\n'
            b'no-homepage disabled \n'
            b'weird-source disabled \n'))


def test_local(repositories_xml, repos_conf, runner):
    repos_conf.write('''
[frobnicate]
location = /tmp/frobnicate
sync-type = git
sync-uri = https://example.com/frobnicate.git
''')
    repos_conf.close()

    assert (
        runner(repositories_xml, repos_conf.name, ['list']) ==
        (0, b'bar disabled https://example.com/bar\n'
            b'foo disabled https://example.com/foo\n'
            b'frobnicate local \n'
            b'no-homepage disabled \n'
            b'weird-source disabled \n'))
