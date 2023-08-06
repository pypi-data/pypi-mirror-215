from datetime import datetime, timedelta
import logging
import os.path
import shelve
import tempfile
import unittest

import drakken.config as config
import drakken.rate_limit as rlimit


def get(name='default'):
    d = shelve.open(config.get('RATE_LIMIT_DB_PATH'), writeback=True)
    rd = dict(d[name])
    d.close()
    return rd


def set(**kwargs):
    d = shelve.open(config.get('RATE_LIMIT_DB_PATH'), writeback=True)
    if 'name' in kwargs:
        name = kwargs['name']
    else:
        name = 'default'
    if 'count' in kwargs:
        d[name]['count'] = kwargs['count']
    if 'start_time' in kwargs:
        d[name]['start_time'] = kwargs['start_time']
    d.close()


class TestRateLimit(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        db_path = os.path.join(self.dir.name, 'rate-limit')
        cfg = {
            'RATE_LIMIT_DB_PATH': db_path,
        }
        config.loads(cfg)

    def test_limit_reached(self):
        limit = 3

        @rlimit.rlimit(limit, 'SECOND')
        def sum(x, y):
            sum.counter += 1
            return x + y
        sum.counter = 0

        # 1
        z = sum(4, 3)
        self.assertEqual(z, 7)
        self.assertEqual(sum.counter, 1)
        # 2
        z = sum(12, 1)
        self.assertEqual(z, 13)
        self.assertEqual(sum.counter, 2)
        # 3
        z = sum(6, 2)
        self.assertEqual(z, 8)
        self.assertEqual(sum.counter, 3)

        # Function not executed, warning logged.
        with self.assertLogs(logger='drakken.rate_limit', level='INFO') as lc:
            z = sum(9, 5)
        self.assertTrue('Rate limit exceeded' in lc.output[0])
        self.assertEqual(sum.counter, 3)

    def test_time_expired(self):
        limit = 100

        @rlimit.rlimit(limit, 'SECOND')
        def sum(x, y):
            sum.counter += 1
            return x + y
        sum.counter = 0

        # Execute function.
        z = sum(4, 5)
        self.assertEqual(z, 9)
        self.assertEqual(sum.counter, 1)
        z = sum(1, 7)
        self.assertEqual(z, 8)
        self.assertEqual(sum.counter, 2)
        # Set db.start_time to expired.
        t = datetime.now() - timedelta(minutes=5)
        set(count=50, start_time=t)
        z = sum(1, 2)
        self.assertEqual(z, 3)
        self.assertEqual(sum.counter, 3)
        # Expired time limit resets counter.
        self.assertEqual(get()['count'], 1)

    def test_multiple_limiters(self):
        limit_sum = 3
        limit_upper = 5

        @rlimit.rlimit(limit_sum, 'SECOND', name='sum')
        def sum(x, y):
            sum.counter += 1
            return x + y
        sum.counter = 0

        @rlimit.rlimit(limit_upper, 'SECOND', name='upper')
        def upper(s):
            upper.counter += 1
            return s.upper()
        upper.counter = 0

        # 1
        z = sum(4, 3)
        self.assertEqual(z, 7)
        self.assertEqual(sum.counter, 1)
        # 2
        z = sum(12, 1)
        self.assertEqual(z, 13)
        self.assertEqual(sum.counter, 2)
        # 3
        z = sum(4, 5)
        self.assertEqual(z, 9)
        self.assertEqual(sum.counter, 3)

        # Function not executed, warning logged.
        with self.assertLogs(logger='drakken.rate_limit', level='INFO') as lc:
            z = sum(9, 5)
        self.assertTrue('Rate limit exceeded' in lc.output[0])
        self.assertEqual(sum.counter, 3)

        # 1
        s = upper('hello')
        self.assertEqual(s, 'HELLO')
        self.assertEqual(upper.counter, 1)
        # 2
        s = upper('goodbye')
        self.assertEqual(s, 'GOODBYE')
        self.assertEqual(upper.counter, 2)
        # 3
        s = upper('morning')
        self.assertEqual(s, 'MORNING')
        self.assertEqual(upper.counter, 3)
        # 4
        s = upper('evening')
        self.assertEqual(s, 'EVENING')
        self.assertEqual(upper.counter, 4)
        # 5
        s = upper('today')
        self.assertEqual(s, 'TODAY')
        self.assertEqual(upper.counter, 5)

        # Function not executed, warning logged.
        with self.assertLogs(logger='drakken.rate_limit', level='INFO') as lc:
            s = upper('day')
        self.assertTrue('Rate limit exceeded' in lc.output[0])
        self.assertEqual(upper.counter, 5)

    def test_one_limiter_multiple_functions(self):
        limit = 5

        @rlimit.rlimit(limit, 'SECOND')
        def sum(x, y):
            sum.counter += 1
            return x + y
        sum.counter = 0

        @rlimit.rlimit(limit, 'SECOND')
        def upper(s):
            upper.counter += 1
            return s.upper()
        upper.counter = 0

        # 1
        z = sum(4, 3)
        self.assertEqual(z, 7)
        self.assertEqual(sum.counter, 1)
        # 2
        s = upper('hello')
        self.assertEqual(s, 'HELLO')
        self.assertEqual(upper.counter, 1)
        # 3
        z = sum(4, 5)
        self.assertEqual(z, 9)
        self.assertEqual(sum.counter, 2)
        # 4
        s = upper('goodbye')
        self.assertEqual(s, 'GOODBYE')
        self.assertEqual(upper.counter, 2)
        # 5
        z = sum(4, 5)
        self.assertEqual(z, 9)
        self.assertEqual(sum.counter, 3)

        # Function not executed, warning logged.
        with self.assertLogs(logger='drakken.rate_limit', level='INFO') as lc:
            s = upper('day')
        self.assertTrue('Rate limit exceeded' in lc.output[0])
        self.assertEqual(upper.counter, 2)

    def tearDown(self):
        self.dir.cleanup()


if __name__ == '__main__':
    unittest.main()

