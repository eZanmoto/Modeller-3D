class Point:
    """Immutable"""
    def __init__( self, x, y, z ):
        self.x = x
        self.y = y
        self.z = z

    def as_tuple( self ):
        return ( self.x, self.y, self.z )

    def rel_to( self, point ):
        x = self.move( point.z, point.x, self.z, self.x )
        y = self.move( point.z, point.y, self.z, self.y )
        return ( x, y )

    def move( self, viewer_d, displacement, object_d, object_h ):
        over  = object_h * ( viewer_d * -1 ) + object_d * displacement
        under = object_d - viewer_d
        return over / ( 0.1 if 0 == under else under )

    def move_up( self, n ):
        return Point( self.x, self.y - n, self.z )

    def move_right( self, n ):
        return Point( self.x + n, self.y, self.z )

    def move_down( self, n ):
        return Point( self.x, self.y + n, self.z )

    def move_left( self, n ):
        return Point( self.x - n, self.y, self.z )

    def move_forward( self, n ):
        return Point( self.x, self.y, self.z + n )

    def move_back( self, n ):
        return Point( self.x, self.y, self.z - n )

    def __str__( self ):
        return "(%d, %d, %d)" % ( self.x, self.y, self.z )

    def __eq__( self, other ):
        return other != None and self.x == other.x and self.y == other.y and self.z == other.z

    def __ne__( self, other ):
        return not ( self == other )
