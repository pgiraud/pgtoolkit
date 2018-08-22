# -*- coding: utf-8 -*-

from ast import literal_eval
from collections import OrderedDict
import re
from datetime import timedelta


def parse(fo):
    conf = Configuration()
    conf.parse(fo)
    return conf


MEMORY_MULTIPLIERS = {
    'kB': 1024,
    'MB': 1024 * 1024,
    'GB': 1024 * 1024 * 1024,
    'TB': 1024 * 1024 * 1024 * 1024,
}
_memory_re = re.compile(r'^\s*(?P<number>\d+)\s*(?P<unit>[kMGT]B)\s*$')
TIMEDELTA_ARGNAME = {
    'ms': 'milliseconds',
    's': 'seconds',
    'min': 'minutes',
    'h': 'hours',
    'd': 'days',
}
_timedelta_re = re.compile(r'^\s*(?P<number>\d+)\s*(?P<unit>ms|s|min|h|d)\s*$')


def parse_value(raw):
    # Ref.
    # https://www.postgresql.org/docs/current/static/config-setting.html#CONFIG-SETTING-NAMES-VALUES

    if raw.startswith("'"):
        try:
            raw = literal_eval(raw)
        except SyntaxError as e:
            raise ValueError(str(e))

    if raw.startswith('0'):
        try:
            return int(raw, base=8)
        except ValueError:
            pass

    m = _memory_re.match(raw)
    if m:
        unit = m.group('unit')
        mul = MEMORY_MULTIPLIERS[unit]
        return int(m.group('number')) * mul

    m = _timedelta_re.match(raw)
    if m:
        unit = m.group('unit')
        arg = TIMEDELTA_ARGNAME[unit]
        kwargs = {arg: int(m.group('number'))}
        return timedelta(**kwargs)

    elif raw in ('true', 'yes', 'on'):
        return True
    elif raw in ('false', 'no', 'off'):
        return False
    else:
        try:
            return int(raw)
        except ValueError:
            try:
                return float(raw)
            except ValueError:
                return raw


class Configuration(object):
    _parameter_re = re.compile(
        r'^(?P<name>[a-z_]+)(?: +(?!=)| *= *)(?P<value>.*?)'
        '[\s\t]*'
        r'(?P<comment>#.*)$'
    )

    def __init__(self):
        self.lines = []
        self.entries = OrderedDict()

    def parse(self, fo):
        for raw_line in fo:
            self.lines.append(raw_line)
            line = raw_line.strip()
            if line.startswith('#'):
                continue

            m = self._parameter_re.match(line)
            if not m:
                raise ValueError("Bad line: %s." % raw_line)
            entry = m.groupdict()
            entry['value'] = parse_value(entry['value'])

            import pdb; pdb.set_trace()
