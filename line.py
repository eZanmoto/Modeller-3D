def compute_slope( a, b ):
    x1, y1 = a
    x2, y2 = b
    under = x2 - x1
    return 0.0001 if under == 0 else ( y2 - y1 ) / under

class Line:
    """Immutable"""

    def __init__( self, point1, slope ):
        self._point = point1
        self._slope = slope

    @classmethod
    def from_point( self, point1, point2 ):
        return self( point1, compute_slope( point1, point2 ) )

    @classmethod
    def from_slope( self, point1, slope ):
        return self( point1, slope )

    def intersection( self, line ):
        x1, y1 = self._point
        x2, y2 = line._point
        x = ( y2 - y1 + self._slope * x1 - line._slope * x2 ) / ( self._slope - line._slope )
        y = y1 + self._slope * ( x - x1 )
        return ( x, y )

    def __str__( self ):
        x, y = self._point
        y_intersept = y - self._slope * x
        return "y = %dx - %d" % ( self._slope, y_intersept )

tests_passed = 0
tests_failed = 0

def assert_intersection( lines, intersection ):
    global tests_passed
    global tests_failed
    a, b = lines[ -1 ], lines[ -2 ]
    result = a.intersection( b )
    if result == intersection:
        print "PASSED: [%s] intersection [%s] = %s" % ( a, b, intersection )
        tests_passed += 1
    else:
        print "FAILED: [%s] intersection [%s] : expected %s, got %s" % ( a, b, intersection, result )
        tests_failed += 1

if '__main__' == __name__:
    lines = [ ]
    lines.append( Line.from_slope( ( 0, 0 ),  1 ) )
    lines.append( Line.from_slope( ( 0, 0 ), -1 ) )
    assert_intersection( lines, ( 0, 0 ) )
    lines.append( Line.from_point( ( -1, -1 ), ( 1, 1 ) ) )
    lines.append( Line.from_point( ( -1, 1 ), ( 1, -1 ) ) )
    assert_intersection( lines, ( 0, 0 ) )
    lines.append( Line.from_point( ( 0, 2 ), ( 2, 0 ) ) )
    lines.append( Line.from_point( ( 0, 0 ), ( 2, 2 ) ) )
    assert_intersection( lines, ( 1, 1 ) )
    if tests_failed == 0:
        print "All %d tests passed." % ( tests_passed )
    else:
        print "%d/%d tests passed." % ( tests_passed, tests_passed + tests_failed )
