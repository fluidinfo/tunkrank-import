#!/usr/bin/env python

from dateutil.parser import parse
from getpass import getpass
from fom.session import Fluid
from fom.errors import FluidError
import csv
import sys
import time


def checkCompatible(header):
    """Check that the input is compatible with expectations."""
    assert header[1] == 'ScreenName'
    assert header[8] == 'RawTunkRankScore'
    assert header[9] == 'TunkRankScore'
    assert header[10] == 'TunkRankComputedAt'

if __name__ == '__main__':
    fdb = Fluid()
    password = getpass('Enter the tunkrank.com Fluidinfo user password: ')
    fdb.login('tunkrank.com', password)

    reader = csv.reader(sys.stdin)

    # Check that the first (header) line of input looks good.
    checkCompatible(reader.next())

    totalTime = 0.0

    for i, row in enumerate(reader):
        screenName = row[1]
        rawTunkRankScore = float(row[8])
        tunkRankScore = float(row[9])
        tunkRankComputedAt = time.mktime(parse(row[10]).utctimetuple())

        about = '@%s' % screenName.lower()

        start = time.time()
        response = fdb.objects.post(about=about)
        objectId = response.value['id']
        try:
            fdb.values.put(
                query='fluiddb/id="%s"' % objectId,
                values={
                    'tunkrank.com/raw-score': {'value': rawTunkRankScore},
                    'tunkrank.com/score': {'value': tunkRankScore},
                    'tunkrank.com/computed-at': {'value': tunkRankComputedAt},
                    })
        except FluidError, e:
            print 'Error processing %s' % screenName
            print e.args[0].response
            raise
        else:
            elapsed = time.time() - start
            print 'Processed %d: %s (%.3f)' % (i + 1, screenName, elapsed)
            totalTime += elapsed
    av = totalTime / (i + 1)
    print 'Average time per user: %.3f' % av
    lines = 1561613  # The number of users Jason Adams sent us data for.
    print 'Estimated number of days to process %d users: %.3f' % (
        lines, lines * av / 60 / 60 / 24)
