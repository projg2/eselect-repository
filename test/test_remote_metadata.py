def test_remote_metadata(repositories_xml, repos_conf, runner):
    repos_conf.write(f'''
[foo]
location = /tmp/foo

[frobnicate]
location = /tmp/frobnicate
''')
    repos_conf.close()

    assert (
        runner(repositories_xml, repos_conf.name,
               ['remote-metadata', 'foo', 'bar', 'frobnicate', 'noexist',
                'weird-source']) ==
        (0, b'foo enabled /tmp/foo\n'
            b'bar remote git git@example.com:bar.git\n'
            b'frobnicate enabled /tmp/frobnicate\n'
            b'noexist not-exist\n'
            b'weird-source unsupported\n'))

