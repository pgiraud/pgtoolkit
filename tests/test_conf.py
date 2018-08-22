from textwrap import dedent


def test_parse_value():
    from pgtoolkit.conf import parse_value

    # Booleans
    assert parse_value('on') is True
    assert parse_value('off') is False
    assert parse_value('true') is True
    assert parse_value('false') is False
    assert parse_value('yes') is True
    assert parse_value("'no'") is False

    # Numbers
    assert 10 == parse_value('10')
    assert 8 == parse_value('010')
    assert 8 == parse_value("'010'")
    assert 1.4 == parse_value('1.4')

    # Strings
    assert 'esc\'aped string' == parse_value(r"'esc\'aped string'")

    # Memory
    assert 1024 == parse_value('1kB')
    assert 1024 * 1024 * 512 == parse_value('512MB')
    assert 1024 * 1024 * 1024 * 64 == parse_value('64GB')
    assert 1024 * 1024 * 1024 * 1024 * 5 == parse_value('5TB')

    # Time
    delta = parse_value('24s')
    assert 24 == delta.seconds
    delta = parse_value('2 h')
    assert 120 == delta.seconds

    # Enums
    assert 'md5' == parse_value('md5')


def test_parser():
    from pgtoolkit.conf import parse

    lines = dedent("""\
    # - Connection Settings -
    listen_addresses = '*'                  # comma-separated list of addresses;
                            # defaults to 'localhost'; use '*' for all
                            # (change requires restart)
    port = 5432
    bonjour 'without equals'
    shared_buffers = 248MB
    """).splitlines(True)  # noqa

    conf = parse(lines)

    assert '*' == conf.listen_addresses
    assert 5432 == conf.port
    assert 'without equals' == conf.bonjour
