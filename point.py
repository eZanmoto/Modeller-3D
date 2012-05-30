class Point:
    """Immutable"""
    def __init__( self, x, y, z ):
        self.x = x
        self.y = y
        self.z = z

    def rel_to( self, point ):
        x = self.move( point.z, point.x, self.z, self.x )
        y = self.move( point.z, point.y, self.z, self.y )
        return ( x, y )

    def move( self, viewer_d, displacement, object_d, object_h ):
        over  = object_h * viewer_d + object_d * displacement
        under = object_d + viewer_d + 1
        return over / under

    def __str__( self ):
        return "(%d, %d, %d)" % ( self.x, self.y, self.z )

    def __eq__( self, other ):
        return other != None and self.x == other.x and self.y == other.y and self.z == other.z

    def __ne__( self, other ):
        return not ( self == other )
