def test_metadata(repositories_xml, repos_conf, runner):
    repos_conf.write(f'''
[foo]
location = /tmp/foo

[frobnicate]
location = /tmp/frobnicate

[bar]
location = /tmp/bar
sync-type = git
sync-uri = https://example.com/bar.git

[nolocation]
sync-type = hg
sync-uri = https://example.com/noloc
''')
    repos_conf.close()

    assert (
        runner(repositories_xml, repos_conf.name,
               ['metadata', 'noexist', 'foo', 'bar', 'frobnicate',
                'nolocation']) ==
        (0, b'noexist not-exist\n'
            b'foo no-sync-uri /tmp/foo\n'
            b'bar remote /tmp/bar\n'
            b'frobnicate local /tmp/frobnicate\n'
            b'nolocation local \n'))
