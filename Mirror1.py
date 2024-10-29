# The Point3D class is used to manage 3D points. Each points exists 
# in a 3 dimensional space with an x, y, and z coordinarte. The x, y,
# and z coordinates can be negative, zero, or positive. They are 
# floating point values. 

import math

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
  # the vector defined by the first two point. The new point
  # can be before the second point or after second point or 
  # exactly at the second point. One way of looking at this
  # is that the new point is on the vector that starts with
  # the first point and goes through the second point. The
  # distance from the first point to the new point will always
  # be the length passed by the caller.
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

# The Vector3D class is used to manage 3D vectors. Each vector has
# a starting point and an ending point. The points may be the same,
# in which case the vector has a length of zero. The starting and
# ending points both have x, y, and z coordinates. The x, y,and z 
# coordinates can be negative, zero, or positive. They are 
# floating point values. 
class Vector3D(object): 
  # The __init__ method creates an instance of the class  
  def __init__(self, start3D, end3D):
    self.st = start3D
    self.en = end3D
  # The next method returns the absolute length of a vector.
  # This value is always zero or positive. It can never be
  # negative.
  def distance(self): 
    deltaX = self.st.getX() - self.en.getX()
    deltaY = self.st.getY() - self.en.getY()
    deltaZ = self.st.getZ() - self.en.getZ()
    deltaSquared = deltaX**2 + deltaY**2 + deltaZ**2
    return math.sqrt(deltaSquared)
  # The next method takes two vectors as input and returns the dot product
  # of the two vectors. Both vectors must start at the origin. However, the
  # lengths of the two vectors can be different or the lengths can be the
  # same. The two input vectors can end in the same place. The output value
  # is just one number. 
  @staticmethod
  def dotProduct(v1, v2):
    # Make sure the two input vectors start at exactly the origin
    assert(v1.getStart().getX() == 0.0)
    assert(v1.getStart().getY() == 0.0)
    assert(v1.getStart().getZ() == 0.0)
    assert(v2.getStart().getX() == 0.0)
    assert(v2.getStart().getY() == 0.0)
    assert(v2.getStart().getZ() == 0.0)
    # Get the x, y, and z locations of the ending points of the 
    # two input vectors
    v1X = v1.getEnd().getX()
    v1Y = v1.getEnd().getY()
    v1Z = v1.getEnd().getZ()
    v2X = v2.getEnd().getX()
    v2Y = v2.getEnd().getY()
    v2Z = v2.getEnd().getZ()
    # Return the dot product of the two vectors
    return v1X*v2X + v1Y*v2Y + v1Z*v2Z
  # The next method takes two vectors as input and returns the angle between
  # the two vectors. Both vectors must start at the exact same point. However, 
  # they do not need to start at the origin. The lengths of the two vectors 
  # can be different or the lengths can be the same. The two input vectors 
  # can end in the same place. The output value is just one number in radians. 
  @staticmethod
  def getAngle(v1, v2):
    # Make sure the two input vectors start at exactly the same point
    assert(v1.getStart().getX() == v2.getStart().getX())
    assert(v1.getStart().getY() == v2.getStart().getY())
    assert(v1.getStart().getZ() == v2.getStart().getZ())
    # Create two temporary vectors that start at the origin from the
    # two input vectors
    v1Tm = v1.moveOrigin() 
    v2Tm = v2.moveOrigin()
    # Get the dot product of the two temporary vectors
    dot = Vector3D.dotProduct(v1Tm, v2Tm)
    # Get the lengths of the two temporary vectors
    v1Ln = v1Tm.distance()
    v2Ln = v2Tm.distance()
    # Return the angle (in radians) between the two vectors
    return math.acos(dot / (v1Ln * v2Ln))
  # The getEnd method returns the ending point    
  def getEnd(self):
    return self.en
  # The next method returns the polar coordinates of a vector. The
  # starting point of the vector are assumed to be at the origin.
  # In other words, the vector is effectively (but not actually)
  # moved so that its starting point is the origin (x, y, and z
  # values of zero) and the ending point is moved exactly as much
  # as the starting point. In other words, the relative position 
  # of the ending point is not changed.
  #
  # The returned values use the ISO pysics conventions. Each angle
  # value is in radians, not degrees. A value in degrees can be
  # obtained by multiplying the radians value by 180/Pi. The first
  # returned value is the length of the vector. The second returned
  # value is the polar angle. The third returned value is the azimuthal
  # angle. 
  def getPolar(self):
    # Get the x, y, and z locations of the starting and ending 
    # points of the vector
    stX = self.getStart().getX()
    stY = self.getStart().getY()
    stZ = self.getStart().getZ()
    enX = self.getEnd().getX()
    enY = self.getEnd().getY()
    enZ = self.getEnd().getZ()
    # Get the x, y, and z deltas between the starting and ending
    # points of the vector 
    dlX = enX - stX
    dlY = enY - stY
    dlZ = enZ - stZ
    # Get the radial distance (length) of the vector
    r = math.sqrt(dlX**2 + dlY**2 + dlZ**2)
    theta = math.acos(dlZ/r)
    phi = math.atan2(dlY, dlX)
    return r, theta, phi
  # The getStart method returns the starting point    
  def getStart(self):
    return self.st
  # The next method takes two vectors as input and returns a vector that
  # is exactly halfway between the two input vectors. The two input vectors 
  # must start at exactly the same point. The lengths of the two vectors 
  # can be the same or they can be different. The output vector will be 
  # exactly halfway between the input vectors in angular terms. The length
  # of the output vector is undefined. The end points of the two input 
  # vectors can be anywhere. They can even be at the same location.
  @staticmethod
  def halfVector(v1, v2):
    # Make sure the two input vectors start at exactly the same point
    assert(v1.getStart().getX() == v2.getStart().getX())
    assert(v1.getStart().getY() == v2.getStart().getY())
    assert(v1.getStart().getZ() == v2.getStart().getZ())
    # Create two temporary vectors from the input vectors with standard
    # lengths. The temporary vectors are used to build the final output
    # vector below.
    v1Tm = v1.newVector(1.0)
    v2Tm = v2.newVector(1.0)
    # Get the x, y, and z locations of the ending points of the 
    # two temporary vectors
    v1X = v1Tm.getEnd().getX()
    v1Y = v1Tm.getEnd().getY()
    v1Z = v1Tm.getEnd().getZ()
    v2X = v2Tm.getEnd().getX()
    v2Y = v2Tm.getEnd().getY()
    v2Z = v2Tm.getEnd().getZ()
    # Get the new x, y, and z locations of the new point at the
    # end of the new output vector
    nwX = (v1X + v2X)/2.0
    nwY = (v1Y + v2Y)/2.0
    nwZ = (v1Z + v2Z)/2.0
    return Vector3D(v1.getStart(), Point3D(nwX, nwY, nwZ))
  # The next method takes two vectors as input and returns the vector
  # exactly halfway between the two vectors. The two vectors must start
  # at exactly the same point. The lengths of the two vectors must be
  # exactly the same. The end points of the two vectors can be anywhere.
  # They can even be at the same location.
  @staticmethod
  def halfway(v1, v2):
    # Make sure the two input vectors start at exactly the same point
    assert(v1.getStart().getX() == v2.getStart().getX())
    assert(v1.getStart().getY() == v2.getStart().getY())
    assert(v1.getStart().getZ() == v2.getStart().getZ())
    # Get the lengths of the input vectors and make sure they are the
    # same. Since the lengths are floating-point values they may differ
    # to a very small extent. This is OK. 
    v1Length = v1.distance()
    v2Length = v2.distance()
    v1v2Length = math.fabs(v1Length - v2Length)
    assert(v1v2Length < 1.0e-15)
    # Get the x, y, and z locations of the ending points of the 
    # two vectors
    v1X = v1.getEnd().getX()
    v1Y = v1.getEnd().getY()
    v1Z = v1.getEnd().getZ()
    v2X = v2.getEnd().getX()
    v2Y = v2.getEnd().getY()
    v2Z = v2.getEnd().getZ()
    # Get the new x, y, and z locations of the new point at the
    # end of the new vector
    nwX = (v1X + v2X)/2.0
    nwY = (v1Y + v2Y)/2.0
    nwZ = (v1Z + v2Z)/2.0
    return Vector3D(v1.getStart(), Point3D(nwX, nwY, nwZ))
  # The next method takes an input vector and moves it to the
  # origin. The input vector is not actually changed at all. 
  # A new vector is created that starts at the origin. The new
  # vector is returned to the caller. The direction of the new
  # vector is exactly the same as the input vector. The length
  # of the new vector is exactly the same as the input vector.
  def moveOrigin(self):
    # Get the x, y, and z locations of the starting and ending 
    # points of the input vector
    stX = self.getStart().getX()
    stY = self.getStart().getY()
    stZ = self.getStart().getZ()
    enX = self.getEnd().getX()
    enY = self.getEnd().getY()
    enZ = self.getEnd().getZ()
    # Get the x, y, and z deltas between the starting and ending
    # points of the vector 
    dlX = enX - stX
    dlY = enY - stY
    dlZ = enZ - stZ
    # Build an output vector that starts at the origin and has
    # the correct endpoint
    return Vector3D(Point3D(0.0, 0.0, 0.0), Point3D(dlX, dlY, dlZ))
  # The next method takes a vector and a length as input 
  # and returns a new vector as output. The new vector will 
  # exactly match the input vector in direction and will have
  # exactly the same starting point. However, the length of 
  # the new vector will always be equal to the length passed
  # by the caller. 
  def newVector(self, len = 1.0):
    # Get the length of the current vector 
    dist = self.distance()
    # Get a multiplier for adjusting lengths between the first point
    # of the old (input) vector and the second point of the old (input)
    # vector
    mult = len/dist
    # Get the x, y, and z locations of the starting and ending 
    # points of the old (input) vector
    stX = self.st.getX()
    stY = self.st.getY()
    stZ = self.st.getZ()
    enX = self.en.getX()
    enY = self.en.getY()
    enZ = self.en.getZ()
    # Get the x, y, and z deltas between the starting and ending
    # points of the old (input) vector
    dlX = enX - stX
    dlY = enY - stY
    dlZ = enZ - stZ
    # Get the new x, y, and z locations of the new point at the 
    # end of the new vector
    nwX = stX + dlX * mult
    nwY = stY + dlY * mult
    nwZ = stZ + dlZ * mult
    return Vector3D(self.st, Point3D(nwX, nwY, nwZ))

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
  v12 = Vector3D(x1, x2)
  v13 = Vector3D(x1, x3)
  vNw12 = v12.newVector(1.0)
  vNw13 = v13.newVector(1.0)
  vNwH = Vector3D.halfway(vNw12, vNw13)
  r, theta, phi = vNwH.getPolar()
  theta *= 180/math.pi
  phi *= 180/math.pi

  print(r, theta, phi)
  print(vNwH)
    
  # Third version of the code
  x3 = Point3D(0.0, 0.0, 0.0)
  x1 = Point3D(-2.0, 2.0, 1.0)
  x2 = Point3D(1.0, 4.0, 2.5)
  v12 = Vector3D(x1, x2)
  v13 = Vector3D(x1, x3)
  vNwH = Vector3D.halfVector(v12, v13)
  r, theta, phi = vNwH.getPolar()
  theta *= 180/math.pi
  phi *= 180/math.pi

  print(r, theta, phi)
  print(90-theta)
  print(vNwH)


# Actual starting point
if __name__ == "__main__":
  main()