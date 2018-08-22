# -*- coding: utf-8 -*-

from ast import literal_eval
from collections import OrderedDict
import re


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


def parse_value(raw):
    # Ref.
    # https://www.postgresql.org/docs/current/static/config-setting.html#CONFIG-SETTING-NAMES-VALUES
    if raw.startswith("'"):
        raw = literal_eval(raw)

    if raw.startswith('0'):
        return int(raw, base=8)
    elif raw.endswith('B'):
        mul = MEMORY_MULTIPLIERS[raw[-2:]]
        return int(raw[:-2]) * mul
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
