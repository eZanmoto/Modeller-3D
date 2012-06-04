from __future__ import division

class Ordering:
    LT = -1
    EQ = 0
    GT = 1

    @classmethod
    def compare( self, a, b ):
        if a < b: return self.LT
        elif a == b: return self.EQ
        else: return self.GT

def relative_to( point, line ):
    """
        None as the value of a component means that 'line' cannot be intersected
        along this axis.
    """
    x1, y1 = point
    if line.is_horizontal():
        _, y2 = Line.vertical( point ).intersection( line )
        result = ( None, Ordering.compare( y1, y2 ) )
    elif line.is_vertical():
        x2, _ = Line.horizontal( point ).intersection( line )
        result = ( Ordering.compare( x1, x2 ), None )
    else:
        _, y2 = Line.vertical( point ).intersection( line )
        x2, _ = Line.horizontal( point ).intersection( line )
        result = ( Ordering.compare( x1, x2 ), Ordering.compare( y1, y2 ) )
    return result

class Line:
    """Immutable"""

    def __init__( self, point1, slope ):
        self._point = point1
        self._slope = slope
        if self.is_vertical():
            self._y_intercept = None
        else:
            x, y = self._point
            self._y_intercept = y - self._slope * x

    @classmethod
    def from_point( self, point1, point2 ):
        x1, y1 = point1
        x2, y2 = point2
        under = x2 - x1
        return self( point1, None if under == 0 else ( y2 - y1 ) / under )

    @classmethod
    def from_slope( self, point, slope ):
        return self( point, slope )

    @classmethod
    def horizontal( self, point ):
        return self.from_slope( point, 0 )

    @classmethod
    def vertical( self, point ):
        return self.from_slope( point, None )

    def is_horizontal( self ):
        return 0 == self._slope

    def is_vertical( self ):
        return None == self._slope

    def intersection( self, line ):
        x1, y1 = self._point
        x2, y2 = line._point
        if self._slope == line._slope:
            return None
        elif self.is_horizontal():
            if line.is_vertical():
                x, y = x2, y1
            else:
                x, y = ( y1 - line._y_intercept ) / line._slope, y1
        elif self.is_vertical():
            if line.is_horizontal():
                x, y = x1, y2
            else:
                x, y = x1, line._slope * x1 + line._y_intercept
        elif line.is_horizontal():
            x, y = ( y2 - self._y_intercept ) / self._slope, y2
        elif line.is_vertical():
            x, y = x2, self._slope * x2 + self._y_intercept
        else:
            x = ( line._y_intercept - self._y_intercept ) / ( self._slope - line._slope )
            y = self._slope * x + self._y_intercept
        return ( x, y )

    def __str__( self ):
        x, y = self._point
        if self.is_horizontal():
            return "y = " + str( y )
        elif self.is_vertical():
            return "x = " + str( x )
        else:
            if self._slope == 1:
                x_ = ""
            elif self._slope == -1:
                x_ = "-"
            else:
                x_ = str( self._slope )
            if self._y_intercept == 0:
                return "y = %sx" % ( x_ )
            else:
                if self._y_intercept >= 0:
                    operator, b = "+", str( self._y_intercept )
                else:
                    operator, b = "-", str( self._y_intercept )[ 1 : ]
                return "y = %sx %s %s" % ( x_, operator, b )

tests_passed = 0
tests_failed = 0

def assert_intersection( lines, intersection ):
    global tests_passed
    global tests_failed
    a, b = lines[ -2 ], lines[ -1 ]
    result = a.intersection( b )
    if result == intersection:
        print "PASSED: [%s] intersection [%s] = %s" % ( a, b, intersection )
        tests_passed += 1
    else:
        print "FAILED: [%s] intersection [%s] : expected %s, got %s" % ( a, b, intersection, result )
        tests_failed += 1

if '__main__' == __name__:
    lines = [ ]

    print "----- Testing first  path -----"
    print "----- slopes are equal -----"
    lines.append( Line.from_point( ( -2, 4 ), ( 2, 4 ) ) )
    lines.append( Line.from_point( ( -2, 4 ), ( 2, 4 ) ) )
    assert_intersection( lines, None )

    print "\n\n----- Testing second  path -----"
    print "----- first is horizontal, second is vertical -----"
    lines.append( Line.from_point( ( -2, 4 ), ( 2, 4 ) ) )
    lines.append( Line.from_point( ( 2, 4 ), ( 2, -4 ) ) )
    assert_intersection( lines, ( 2, 4 ) )

    print "\n\n----- Testing third path -----"
    print "----- first is horizontal -----"
    lines.append( Line.from_point( ( -2, 4 ), ( 2, 4 ) ) )
    lines.append( Line.from_point( ( 2, -4 ), ( -2, 4 ) ) )
    assert_intersection( lines, ( -2, 4 ) )

    print "\n\n----- Testing fourth path -----"
    print "----- first is vertical, second is horizontal -----"
    lines.append( Line.from_point( ( 2, 4 ), ( 2, -4 ) ) )
    lines.append( Line.from_point( ( -2, 4 ), ( 2, 4 ) ) )
    assert_intersection( lines, ( 2, 4 ) )

    print "\n\n----- Testing fifth path -----"
    print "----- first is vertical -----"
    lines.append( Line.from_point( ( 2, -4 ), ( 2, 4 ) ) )
    lines.append( Line.from_point( ( 2, -4 ), ( -2, 4 ) ) )
    assert_intersection( lines, ( 2, -4 ) )

    print "\n\n----- Testing sixth path -----"
    print "----- second is horizontal -----"
    lines.append( Line.from_point( ( 2, -4 ), ( -2, 4 ) ) )
    lines.append( Line.from_point( ( 2, 4 ), ( -2, 4 ) ) )
    assert_intersection( lines, ( -2, 4 ) )

    print "\n\n----- Testing seventh path -----"
    print "----- second is vertical -----"
    lines.append( Line.from_point( ( 2, -4 ), ( -2, 4 ) ) )
    lines.append( Line.from_point( ( 2, -4 ), ( 2, 4 ) ) )
    assert_intersection( lines, ( 2, -4 ) )

    print "\n\n----- Testing eigth path -----"
    print "----- first isn't vertical or horizontal -----"
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
        print "\nAll %d tests passed." % ( tests_passed )
    else:
        print "\n%d/%d tests passed." % ( tests_passed, tests_passed + tests_failed )

    point, line = ( 0, 0 ), Line.from_slope( ( 2, 1 ), 1 )
    print "\n[%s] is %s relative to [%s]" % ( point, relative_to( point, line ), line )

    point, line = ( 0, 0 ), Line.from_slope( ( 2, 2 ), 0 )
    print "\n[%s] is %s relative to [%s]" % ( point, relative_to( point, line ), line )
