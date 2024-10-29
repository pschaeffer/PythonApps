import math

# The Point3D class is used to manage 3D points. Each points exists 
# in a 3 dimensional space with an x, y, and z coordinarte. The x, y,
# and z coordinates can be negative, zero, or positive. They are 
# floating point values. 
class Point3D(object): 
  # The __init__ method creates an instance of the class  
  def __init__(self, xLoc = 0.0, yLoc = 0.0, zLoc = 0.0):
    self.x = xLoc
    self.y = yLoc
    self.z = zLoc
  # The next method returns the absolute distance between 
  # two points. This value is always zero or positive. It
  # can never be negative.
  @staticmethod
  def distance(start, end):
    deltaX = start.getX() - end.getX()
    deltaY = start.getY() - end.getY()
    deltaZ = start.getZ() - end.getZ()
    deltaSquared = deltaX**2 + deltaY**2 + deltaZ**2
    return math.sqrt(deltaSquared)
  # The getX method returns the x coordinate   
  def getX(self):
    return self.x
  # The getY method returns the y coordinate   
  def getY(self):
    return self.y
  # The getZ method returns the z coordinate   
  def getZ(self):
    return self.z
  # The next method returns the Y angle between two points
  @staticmethod
  def getYAngle(start, end):
    # Get the x, y, and z locations of the starting and ending 
    # points passed by the caller
    stX = start.getX()
    stY = start.getY()
    stZ = start.getZ()
    enX = end.getX()
    enY = end.getY()
    enZ = end.getZ()
    # Get the x, y, and z deltas between the starting and ending
    # points passed by the caller
    dlX = enX - stX
    dlY = enY - stY
    dlZ = enZ - stZ
    return math.atan2(dlY, dlX) * 180/math.pi
  # The next method returns the Z angle between two points
  @staticmethod
  def getZAngle(start, end):
    # Get the x, y, and z locations of the starting and ending 
    # points passed by the caller
    stX = start.getX()
    stY = start.getY()
    stZ = start.getZ()
    enX = end.getX()
    enY = end.getY()
    enZ = end.getZ()
    # Get the x, y, and z deltas between the starting and ending
    # points passed by the caller
    dlX = enX - stX
    dlY = enY - stY
    dlXY = math.sqrt(dlX**2 + dlY**2)
    dlZ = enZ - stZ
    return math.atan2(dlZ, dlXY) * 180/math.pi
  # The next method takes two points as input and returns the point
  # exactly halfway between the two points. Of course, the points can
  # be anywhere. They can even be at the same location.
  @staticmethod
  def halfway(start, end):
    # Get the x, y, and z locations of the starting and ending 
    # points passed by the caller
    stX = start.getX()
    stY = start.getY()
    stZ = start.getZ()
    enX = end.getX()
    enY = end.getY()
    enZ = end.getZ()
    # Get the new x, y, and z locations of the new point
    nwX = (stX + enX)/2.0
    nwY = (stY + enY)/2.0
    nwZ = (stZ + enZ)/2.0
    return Point3D(nwX, nwY, nwZ) 
  # The next method takes two points and a length as input
  # and returns a new point as output. The new point is on
  # the line (or perhaps after the line) defined by the 
  # first two points. The new point can be before the second
  # point or after second point or exactly at the second point.
  # One way of looking at this is that the new point is on the
  # vector that starts with the first point and goes through 
  # the second point. The distance from the first point to the
  # new point will always be the length passed by the caller.
  @staticmethod
  def newPoint(start, end, len = 1.0):
    # Get the distance between the two points passed by the
    # caller
    dist = Point3D.distance(start, end)
    # Get a multiplier for adjusting lengths between the first
    # old point and the second old point
    mult = len/dist
    # Get the x, y, and z locations of the starting and ending 
    # points passed by the caller
    stX = start.getX()
    stY = start.getY()
    stZ = start.getZ()
    enX = end.getX()
    enY = end.getY()
    enZ = end.getZ()
    # Get the x, y, and z deltas between the starting and ending
    # points passed by the caller
    dlX = enX - stX
    dlY = enY - stY
    dlZ = enZ - stZ
    # Get the new x, y, and z locations of the new point
    nwX = stX + dlX * mult
    nwY = stY + dlY * mult
    nwZ = stZ + dlZ * mult
    return Point3D(nwX, nwY, nwZ) 

# The Line3D class is used to manage 3D lines. Each line has
# a starting point and an ending point. The points may be the same,
# in which case the line has a length of zero. The starting and
# ending points both have x, y, and z coordinates. The x, y,and z 
# coordinates can be negative, zero, or positive. They are 
# floating-point values. 
class Line3D(object): 
  # The __init__ method creates an instance of the class  
  def __init__(self, start3D, end3D):
    self.st = start3D
    self.en = end3D
  # The next method returns the absolute length of a line.
  # This value is always zero or positive. It can never be
  # negative.
  def distance(self): 
    deltaX = self.st.getX() - self.en.getX()
    deltaY = self.st.getY() - self.en.getY()
    deltaZ = self.st.getZ() - self.en.getZ()
    deltaSquared = deltaX**2 + deltaY**2 + deltaZ**2
    return math.sqrt(deltaSquared)
  # The next method takes two lines as input and returns the dot product
  # of the two lines. Both lines must start at the origin. However, the
  # lengths of the two lines can be different or the lengths can be the
  # same. The two input lines can end in the same place. The output value
  # is just one number. 
  @staticmethod
  def dotProduct(line1, line2):
    # Make sure the two input lines start at exactly the origin
    assert(line1.getStart().getX() == 0.0)
    assert(line1.getStart().getY() == 0.0)
    assert(line1.getStart().getZ() == 0.0)
    assert(line2.getStart().getX() == 0.0)
    assert(line2.getStart().getY() == 0.0)
    assert(line2.getStart().getZ() == 0.0)
    # Get the x, y, and z locations of the ending points of the 
    # two input lines
    line1X = line1.getEnd().getX()
    line1Y = line1.getEnd().getY()
    line1Z = line1.getEnd().getZ()
    line2X = line2.getEnd().getX()
    line2Y = line2.getEnd().getY()
    line2Z = line2.getEnd().getZ()
    # Return the dot product of the two lines
    return line1X*line2X + line1Y*line2Y + line1Z*line2Z
  # The next method takes two lines as input and returns the angle between
  # the two lines. Both lines must start at the exact same point. However, 
  # they do not need to start at the origin. The lengths of the two lines 
  # can be different or the lengths can be the same. The two input lines 
  # can end in the same place. The output value is just one number in radians. 
  @staticmethod
  def getAngle(line1, line2):
    # Make sure the two input lines start at exactly the same point
    assert(line1.getStart().getX() == line2.getStart().getX())
    assert(line1.getStart().getY() == line2.getStart().getY())
    assert(line1.getStart().getZ() == line2.getStart().getZ())
    # Create two temporary lines that start at the origin from the
    # two input lines
    line1Tm = line1.moveOrigin() 
    line2Tm = line2.moveOrigin()
    # Get the dot product of the two temporary lines
    dot = Line3D.dotProduct(line1Tm, line2Tm)
    # Get the lengths of the two temporary lines
    line1Ln = line1Tm.distance()
    line2Ln = line2Tm.distance()
    # Return the angle (in radians) between the two lines
    return math.acos(dot / (line1Ln * line2Ln))
  # The getEnd method returns the ending point    
  def getEnd(self):
    return self.en
  # The next method returns the polar coordinates of a line. The
  # starting point of the line is assumed to be at the origin.
  # In other words, the line is effectively (but not actually)
  # moved so that its starting point is the origin (x, y, and z
  # values of zero) and the ending point is moved exactly as much
  # as the starting point. In other words, the relative position 
  # of the ending point is not changed.
  #
  # The returned values use the ISO physics conventions. Each angle
  # value is in radians, not degrees. A value in degrees can be
  # obtained by multiplying the radians value by 180/Pi. The first
  # returned value is the length of the line. The second returned
  # value is the polar angle. The third returned value is the azimuthal
  # angle. 
  def getPolar(self):
    # Get the x, y, and z locations of the starting and ending 
    # points of the line
    stX = self.getStart().getX()
    stY = self.getStart().getY()
    stZ = self.getStart().getZ()
    enX = self.getEnd().getX()
    enY = self.getEnd().getY()
    enZ = self.getEnd().getZ()
    # Get the x, y, and z deltas between the starting and ending
    # points of the line 
    dlX = enX - stX
    dlY = enY - stY
    dlZ = enZ - stZ
    # Get the radial distance (length) of the line
    r = math.sqrt(dlX**2 + dlY**2 + dlZ**2)
    theta = math.acos(dlZ/r)
    phi = math.atan2(dlY, dlX)
    return r, theta, phi
  # The getStart method returns the starting point    
  def getStart(self):
    return self.st
  # The next method takes two lines as input and returns a line that
  # is exactly halfway between the two input lines. The two input lines 
  # must start at exactly the same point. The lengths of the two lines 
  # can be the same or they can be different. The output line will be 
  # exactly halfway between the input lines in angular terms. The length
  # of the output line is undefined. The end points of the two input 
  # lines can be anywhere. They can even be at the same location.
  @staticmethod
  def halfLine(l1, l2):
    # Make sure the two input lines start at exactly the same point
    assert(l1.getStart().getX() == l2.getStart().getX())
    assert(l1.getStart().getY() == l2.getStart().getY())
    assert(l1.getStart().getZ() == l2.getStart().getZ())
    # Create two temporary lines from the input lines with standard
    # lengths. The temporary lines are used to build the final output
    # line below.
    l1Tm = l1.newline(1.0)
    l2Tm = l2.newline(1.0)
    # Get the x, y, and z locations of the ending points of the 
    # two temporary lines
    l1X = l1Tm.getEnd().getX()
    l1Y = l1Tm.getEnd().getY()
    l1Z = l1Tm.getEnd().getZ()
    l2X = l2Tm.getEnd().getX()
    l2Y = l2Tm.getEnd().getY()
    l2Z = l2Tm.getEnd().getZ()
    # Get the new x, y, and z locations of the new point at the
    # end of the new output line
    nwX = (l1X + l2X)/2.0
    nwY = (l1Y + l2Y)/2.0
    nwZ = (l1Z + l2Z)/2.0
    return Line3D(l1.getStart(), Point3D(nwX, nwY, nwZ))
  # The next method takes two lines as input and returns the line
  # exactly halfway between the two lines. The two lines must start
  # at exactly the same point. The lengths of the two lines must be
  # exactly the same. The end points of the two lines can be anywhere.
  # They can even be at the same location.
  @staticmethod
  def halfway(line1, line2):
    # Make sure the two input lines start at exactly the same point
    assert(line1.getStart().getX() == line2.getStart().getX())
    assert(line1.getStart().getY() == line2.getStart().getY())
    assert(line1.getStart().getZ() == line2.getStart().getZ())
    # Get the lengths of the input lines and make sure they are the
    # same. Since the lengths are floating-point values they may differ
    # to a very small extent. This is OK. 
    line1Length = line1.distance()
    line2Length = line2.distance()
    line1line2Length = math.fabs(line1Length - line2Length)
    assert(line1line2Length < 1.0e-15)
    # Get the x, y, and z locations of the ending points of the 
    # two lines
    line1X = line1.getEnd().getX()
    line1Y = line1.getEnd().getY()
    line1Z = line1.getEnd().getZ()
    line2X = line2.getEnd().getX()
    line2Y = line2.getEnd().getY()
    line2Z = line2.getEnd().getZ()
    # Get the new x, y, and z locations of the new point at the
    # end of the new line
    nwX = (line1X + line2X)/2.0
    nwY = (line1Y + line2Y)/2.0
    nwZ = (line1Z + line2Z)/2.0
    return Line3D(line1.getStart(), Point3D(nwX, nwY, nwZ))
  # The next method takes an input line and moves it to the
  # origin. The input line is not actually changed at all. 
  # A new line is created that starts at the origin. The new
  # line is returned to the caller. The direction of the new
  # line is exactly the same as the input line. The length
  # of the new line is exactly the same as the input line.
  def moveOrigin(self):
    # Get the x, y, and z locations of the starting and ending 
    # points of the input line
    stX = self.getStart().getX()
    stY = self.getStart().getY()
    stZ = self.getStart().getZ()
    enX = self.getEnd().getX()
    enY = self.getEnd().getY()
    enZ = self.getEnd().getZ()
    # Get the x, y, and z deltas between the starting and ending
    # points of the line 
    dlX = enX - stX
    dlY = enY - stY
    dlZ = enZ - stZ
    # Build an output line that starts at the origin and has
    # the correct endpoint
    return Line3D(Point3D(0.0, 0.0, 0.0), Point3D(dlX, dlY, dlZ))
  # The next method takes a line and a length as input 
  # and returns a new line as output. The new line will 
  # exactly match the input line in direction and will have
  # exactly the same starting point. However, the length of 
  # the new line will always be equal to the length passed
  # by the caller. 
  def newLine(self, len = 1.0):
    # Get the length of the current line 
    dist = self.distance()
    # Get a multiplier for adjusting lengths between the first point
    # of the old (input) line and the second point of the old (input)
    # line
    mult = len/dist
    # Get the x, y, and z locations of the starting and ending 
    # points of the old (input) line
    stX = self.st.getX()
    stY = self.st.getY()
    stZ = self.st.getZ()
    enX = self.en.getX()
    enY = self.en.getY()
    enZ = self.en.getZ()
    # Get the x, y, and z deltas between the starting and ending
    # points of the old (input) line
    dlX = enX - stX
    dlY = enY - stY
    dlZ = enZ - stZ
    # Get the new x, y, and z locations of the new point at the 
    # end of the new line
    nwX = stX + dlX * mult
    nwY = stY + dlY * mult
    nwZ = stZ + dlZ * mult
    return Line3D(self.st, Point3D(nwX, nwY, nwZ))

# Handle startup 
def startup():
  return
   
# Main program
def main():
  # First version of the code
  x3 = Point3D(0.0, 0.0, 0.0)
  x1 = Point3D(-2.0, 2.0, 1.0)
  x2 = Point3D(1.0, 4.0, 2.5)

  nwX2 = Point3D.newPoint(x1, x2, 1.0)
  nwX3 = Point3D.newPoint(x1, x3, 1.0)
  nwH = Point3D.halfway(nwX2, nwX3)

  print(Point3D.distance(nwH, nwX2))
  print(Point3D.distance(nwH, nwX3))
  print(Point3D.getYAngle(x1, nwH))
  print(Point3D.getZAngle(x1, nwH))

  # Second version of the code
  x3 = Point3D(0.0, 0.0, 0.0)
  x1 = Point3D(-2.0, 2.0, 1.0)
  x2 = Point3D(1.0, 4.0, 2.5)
  line12 = Line3D(x1, x2)
  line13 = Line3D(x1, x3)
  lNw12 = line12.newLine(1.0)
  lNw13 = line13.newLine(1.0)
  lNwH = Line3D.halfway(lNw12, lNw13)
  r, theta, phi = lNwH.getPolar()
  theta *= 180/math.pi
  phi *= 180/math.pi

  print(r, theta, phi)
  print(lNwH)
    
  # Third version of the code
  x3 = Point3D(0.0, 0.0, 0.0)
  x1 = Point3D(-2.0, 2.0, 1.0)
  x2 = Point3D(1.0, 4.0, 2.5)
  line12 = Line3D(x1, x2)
  line13 = Line3D(x1, x3)
  lNwH = Line3D.halfLine(line12, line13)
  r, theta, phi = lNwH.getPolar()
  theta *= 180/math.pi
  phi *= 180/math.pi

  print(r, theta, phi)
  print(90-theta)
  print(lNwH)


# Actual starting point
if __name__ == "__main__":
  main()