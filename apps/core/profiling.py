import os
from time import time

from django.conf import settings
from django.db import connection


def terminal_width():
    """Function to compute the terminal width."""
    width = 0
    try:
        import struct, fcntl, termios
        s = struct.pack('HHHH', 0, 0, 0, 0)
        x = fcntl.ioctl(1, termios.TIOCGWINSZ, s)
        width = struct.unpack('HHHH', x)[1]
    except:
        pass
    if width <= 0:
        try:
            width = int(os.environ['COLUMNS'])
        except:
            pass
    if width <= 0:
        width = 80
    return width


class ProfilingMiddleware:
    """Middleware which prints out a list of all SQL queries done for each view
        that is processed. This is only useful for debugging.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time()
        response = self.get_response(request)
        end_time = time() - start_time
        indentation = 2
        if settings.DEBUG and len(connection.queries) > 0:
            width = terminal_width()
            total_time = 0.0
            for query in connection.queries:
                nice_sql = query['sql'].replace('"', '').replace(',', ', ')
                sql = "Query: %s\nTime: %s" % (nice_sql, query['time'])
                total_time = total_time + float(query['time'])
                while len(sql) > width-indentation:
                    print("%s%s" % (" "*indentation, sql[:width-indentation]))
                    sql = sql[width-indentation:]
                print("%s%s\n" % (" "*indentation, sql))
            replace_tuple = (" "*indentation, str(total_time),
                             len(connection.queries))
            print("%sTotal SQL time: %s seconds. Queries: %s." % replace_tuple)
        print("  Total time: %s seconds." % end_time)
        return response
