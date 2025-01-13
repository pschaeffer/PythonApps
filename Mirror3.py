import math 
import numpy as np
import sys
import time

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
  # returned value is the length of the line which is always greater
  # than or equal to zero. The second returned value is the polar angle 
  # (sometime called the elevation). The range for this value is 
  # 0 <= φ <= π. The third returned value is the azimuthal angle. 
  # The range for this value is 0 <= θ <= 2π.
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
    if phi < 0.0:
      phi += math.pi * 2
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
    l1Tm = l1.newLine(1.0)
    l2Tm = l2.newLine(1.0)
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

# The MirrorPosition3D class is used to manage the pan
# and tilt of a mirror. The caller pass two values. They
# are floating-poing values and are in radians (not degrees).
class MirrorPosition3D(object): 
  # The __init__ method creates an instance of the class  
  def __init__(self, panValue = 0.0, tiltValue = 0.0):
    self.pan = panValue
    self.tilt = tiltValue
  # The getPan method returns the pan value   
  def getPan(self):
    return self.pan
  # The getTilt method returns the tilt value   
  def getTilt(self):
    return self.tilt

# The Point2D class is used to manage 2D points. Each point exists 
# in a 2 dimensional space with an x, and y coordinates. The x, and 
# y coordinates can be negative, zero, or positive. They are 
# floating point values. 
class Point2D(object): 
  # The __init__ method creates an instance of the class  
  def __init__(self, xLoc = 0.0, yLoc = 0.0):
    self.x = xLoc
    self.y = yLoc
  # The next method returns the absolute distance between 
  # two points. This value is always zero or positive. It
  # can never be negative.
  @staticmethod
  def distance(start, end):
    deltaX = start.getX() - end.getX()
    deltaY = start.getY() - end.getY()
    deltaSquared = deltaX**2 + deltaY**2
    return math.sqrt(deltaSquared)
  # The getX method returns the x coordinate   
  def getX(self):
    return self.x
  # The getY method returns the y coordinate   
  def getY(self):
    return self.y

# The Point3D class is used to manage 3D points. Each point exists 
# in a 3 dimensional space with an x, y, and z coordinates. The x, y,
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
  # The getZ method returns the z coordinate   
  def getZ(self):
    return self.z
  # The next method returns the Z angle between two points in 
  # degrees
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

# Build a set of 3D points that are equally (not really) distributed
# over a sphere. The points are not really equally distributed, but
# they are reasonably close to equally distributed. This algorithm
# come from "Evenly distributing n points on a sphere" in stack 
# overflow. This is sometimes called the "The golden spiral method".
def buildSpherePoints(numberPoints):
  # Define the return value which is a list of 3D points
  rv = []
  # Build the points using NumPy 
  indices = np.arange(0, numberPoints, dtype=float) + 0.5
  thetaArray = np.arccos(1 - 2 * indices/numberPoints)
  phiArray = np.pi * (1 + 5**0.5) * indices
  xArray, yArray, zArray = np.cos(phiArray) * np.sin(thetaArray), np.sin(phiArray) * np.sin(thetaArray), np.cos(thetaArray)
  # Get the x, y, and z values of each point
  for i in range(0, numberPoints):
    x, y, z = xArray[i], yArray[i], zArray[i]
    newPoint = Point3D(x, y, z)
    rv.append(newPoint)
  return rv

# Convert degrees to radians
def convertDegreesRadians(deg):
  return deg * math.pi / 180.0  

# Get each of the sum values and convert it to an absolute
# value. Then add the sum values
def getAbsSum2D(xLoc, yLoc, ap1, ap2, ap3):
  # Get the raw sum values (which may be negative)
  sumP1 = getSumP12D(xLoc, yLoc, ap1, ap2)
  sumP3 = getSumP32D(xLoc, yLoc, ap2, ap3)
  # Convert each of the sum values to an absolute value
  sumP1 = abs(sumP1)
  sumP3 = abs(sumP3)
  return sumP1 + sumP3

# Get the calulated pan value
def getCp12D(xLoc, yLoc):
  cp1 = (math.atan2(yLoc, (xLoc+1.0)) + math.atan2(yLoc, xLoc))/2 + math.pi/2
  return cp1
# Get the calulated pan value
def getCp22D(xLoc, yLoc):
  cp2 = (math.atan2(yLoc, (xLoc+0.0)) + math.atan2(yLoc, xLoc))/2 + math.pi/2
  return cp2
# Get the calulated pan value
def getCp32D(xLoc, yLoc):
  cp3 = (math.atan2(yLoc, (xLoc-1.0)) + math.atan2(yLoc, xLoc))/2 + math.pi/2
  return cp3

# Get a few sum values
def getSumP12D(xLoc, yLoc, ap1, ap2):
  cp1 = getCp12D(xLoc, yLoc)
  cp2 = getCp22D(xLoc, yLoc)
  sum = cp1 - ap1 - cp2 + ap2
  return sum
# Get a few sum values
def getSumP32D(xLoc, yLoc, ap2, ap3):
  cp3 = getCp32D(xLoc, yLoc)
  cp2 = getCp22D(xLoc, yLoc)
  sum = cp3 - ap3 - cp2 + ap2
  return sum

# Get the angle from the x axis to the point. this is 
# a 2D function, not a 3D function.
def getAngle2D(start, end):
  deltaX = end.getX() - start.getX()
  deltaY = end.getY() - start.getY()
  return math.atan2(deltaY, deltaX)

# Get the actual location and a pan adjustment value using
# a set of inputs. The inputs are a suggested location, and
# a set of actual pan values.
def getLocation2D(sugX, sugY, ap1, ap2, ap3):
  # Define a few arrays for plotting
  xArray = []
  yArray = []
  moveFactor = 0.01
  loopCount = 0
  while True:
    # Increment the loop counter
    loopCount += 1
    if loopCount > 5:
      break
    # Start at the old suggested location and get a new suggested
    # location
    [sugX, sugY] = getLocationMove2D(sugX, sugY, moveFactor, ap1, ap2, ap3, xArray, yArray)
    moveFactor /= 10.0
  # We now have x and y values that are very close to correct
  cp1 = getCp12D(sugX, sugY)
  panAjustment = cp1 - ap1
  plt.plot(xArray, yArray) 
  plt.show()
  return [sugX, sugY, panAjustment]

# Get the actual 3D location and a mirror adjustment value 
# (pan and tilt adjustments) using a set of inputs. The 
# inputs are a suggested 3D location, and a set of actual 
# mirror (pan and tilt) values.
def getLocation3D(point3DStart, actualMirror1, actualMirror2, actualMirror3):
  testCount = 100
  spherePoints = buildSpherePoints(testCount)
  # Build the first suggested location
  point3DSug = Point3D(point3DStart.getX(), point3DStart.getY(), point3DStart.getZ())
  # Declare and define a few values for use later
  moveFactor = 0.01
  loopCount = 0
  while True:
    # Increment the loop counter
    loopCount += 1
    if loopCount > 10:
      break
    # Start at the old suggested location and get a new suggested
    # location
    point3DSug = getLocationMove3D(point3DSug, moveFactor, spherePoints,
                                   actualMirror1, actualMirror2, actualMirror3)
    moveFactor /= 10.0
  # We now have x, y, and z values that are very close to correct.
  # Define a few 3D points for use later. These are standard 3D points.
  point3D1 = Point3D(0.0, -1.0, 0.0)
  point3D2 = Point3D(0.0, 0.0, 0.0)
  point3D3 = Point3D(0.0, 0.0, 1.0)
  point3D4 = Point3D(0.0, 0.0, 2.0)
  # Get each of the mirror positions
  mirrorPosition1 = getMirrorPosition(point3D4, point3DSug, point3D1)
  mirrorPosition2 = getMirrorPosition(point3D4, point3DSug, point3D2)
  mirrorPosition3 = getMirrorPosition(point3D4, point3DSug, point3D3)
  # Get the pan and tilt value for each of the actual mirror positions
  aMPan1 = actualMirror1.getPan()
  aMPan2 = actualMirror2.getPan()
  aMPan3 = actualMirror3.getPan()
  aMTilt1 = actualMirror1.getTilt()
  aMTilt2 = actualMirror2.getTilt()
  aMTilt3 = actualMirror3.getTilt()
  # Get the pan and tilt value for each of the calculated mirror positions
  mP1Pan = mirrorPosition1.getPan()
  mP2Pan = mirrorPosition2.getPan()
  mP3Pan = mirrorPosition3.getPan()
  mP1Tilt = mirrorPosition1.getTilt()
  mP2Tilt = mirrorPosition2.getTilt()
  mP3Tilt = mirrorPosition3.getTilt()
  # Deterine each of the adjustment factors
  aF1Pan = aMPan1 - mP1Pan
  aF2Pan = aMPan2 - mP2Pan
  aF3Pan = aMPan3 - mP3Pan
  aF1Tilt = aMTilt1 - mP1Tilt
  aF2Tilt = aMTilt2 - mP2Tilt
  aF3Tilt = aMTilt3 - mP3Tilt  
  # Build a mirror position instance with the adjustment values
  mirrorAdjustments = MirrorPosition3D(aF1Pan, aF1Tilt)
  # The code below (that is not in use) plots the path to the 
  # final value
  # mpl.rcParams['legend.fontsize'] = 10
  # fig = plt.figure()
  # ax = fig.gca(projection='3d') 
  # ax.plot(xArray, yArray, zArray)
  # plt.show()
  return [mirrorAdjustments, point3DSug]

# Get a proposed location using a set of inputs. The inputs are
# a suggested location, a move factor, and a set of actual pan 
# values.
def getLocationMove2D(sugX, sugY, moveFactor, ap1, ap2, ap3, xArray, yArray):
  xLoc = sugX
  yLoc = sugY
  # The loop below moves the x and y locations until the new
  # value is not an improvement over the old value
  xyLength = math.sqrt(xLoc**2 + yLoc**2)
  xyMove = xyLength * moveFactor
  loopCount = 0
  while True:
    # Increment the loop counter
    loopCount += 1
    # Check if this loop has run too many times
    if loopCount > 10000: 
      raise RuntimeError("Loop inside getLocationMove2D did not converge") 
    # Add the current values for x and y to x and y arrays
    xArray.append(xLoc)
    yArray.append(yLoc)
    # Get the old sum of sums value
    oldSum = getAbsSum2D(xLoc, yLoc, ap1, ap2, ap3)
    # We now to try and move in many directions to see what
    # direction works best
    testCount = 100
    # Set the starting angle and the current angle
    startAngle = 0.0
    curAngle = startAngle
    # Get the angle adjustment each time this loop executes
    angleAdjust = (2*math.pi)/testCount
    # We need to find the direction with the lowest sum of sums
    lowestSum = float('inf')
    lowestDirection = 0.0
    lowestX = 0.0
    lowestY = 0.0
    for i in range(0, testCount):
      # Get the Sine and Cosine values
      curSin = math.sin(curAngle)
      curCos = math.cos(curAngle)      
      # Get a new temporary location
      xTmp = xLoc + moveFactor * curSin
      yTmp = yLoc + moveFactor * curCos
      # Get the temporary sum of sums value
      tmpSum = getAbsSum2D(xTmp, yTmp, ap1, ap2, ap3)    
      # Check if we have a new low
      if tmpSum < lowestSum:
        lowestSum = tmpSum
        lowestDirection = curAngle
        lowestX = xTmp
        lowestY = yTmp
      curAngle += angleAdjust
    # We can now reset our location and determine a new sum of sums
    newSum = getAbsSum2D(lowestX, lowestY, ap1, ap2, ap3)
    # Check if we are done. We are done when the new location
    # is no longer better than the old location
    if newSum >= oldSum:
      break
    # Move to the new location
    xLoc = lowestX
    yLoc = lowestY
  return [xLoc, yLoc]

# Get a proposed location using a set of inputs. The inputs are
# a suggested location, a move factor, and a set of actual pan 
# values.
def getLocationMove3D(point3DSug, moveFactor, spherePoints, 
                      actualMirror1, actualMirror2, actualMirror3):
  # Get the x, y, and z values for the current suggested point
  xLoc = point3DSug.getX()
  yLoc = point3DSug.getY()
  zLoc = point3DSug.getZ()
  # The loop below moves the x, y and z locations until the new
  # value is not an improvement over the old value
  xyzLength = math.sqrt(xLoc**2 + yLoc**2 + zLoc**2)
  xyzMove = xyzLength * moveFactor
  loopCount = 0   
  while True: 
    print(xLoc, yLoc, zLoc)
    # Increment the loop counter
    loopCount += 1
    # Check if this loop has run too many times
    if loopCount > 10000: 
      raise RuntimeError("Loop inside getLocationMove3D did not converge") 
    # Get the old sum value
    point3DSug = Point3D(xLoc, yLoc, zLoc)
    oldSum = testLocation3D(point3DSug, actualMirror1, actualMirror2, actualMirror3)
    # We now to try and move in many directions to see what
    # direction works best
    testCount = len(spherePoints)
    # We need to find the direction with the lowest sum value
    lowestSum = float('inf')
    lowestDirection = -1
    lowestX = 0.0
    lowestY = 0.0
    lowestZ = 0.0
    for i in range(0, testCount):     
      # Get a new temporary location
      xValue = spherePoints[i].getX()
      xTmp = xLoc + xyzMove * xValue
      yValue = spherePoints[i].getY()
      yTmp = yLoc + xyzMove * yValue
      zValue = spherePoints[i].getZ()
      zTmp = zLoc + xyzMove * zValue
      # Get the temporary sum value
      point3DTmp = Point3D(xTmp, yTmp, zTmp)
      tmpSum = testLocation3D(point3DTmp, actualMirror1, actualMirror2, actualMirror3)   
      # Check if we have a new low
      if tmpSum < lowestSum:
        lowestSum = tmpSum
        lowestDirection = i
        lowestX = xTmp
        lowestY = yTmp 
        lowestZ = zTmp 
    # We can now reset our location and determine a new sum value
    newSum = lowestSum
    # Check if we are done. We are done when the new location
    # is no longer better than the old location
    if newSum >= oldSum:
      break
    # Move to the new location
    xLoc = lowestX
    yLoc = lowestY
    zLoc = lowestZ
  point3DSug = Point3D(xLoc, yLoc, zLoc)
  return point3DSug

# This routine returns the correct mirror position for a set
# of points. The points are the laser source, the mirror (the 
# center of the mirror), and the target point. The correct 
# mirror position will exactly reflect the laser source to 
# target point. 
def getMirrorPosition(laserPos, mirrorPos, targetPos):  
  piOver2 = math.pi / 2
  # Get some 3D lines. Note that all of the lines start at
  # the mirror point, but end in various places.
  lineMirrorLaser = Line3D(mirrorPos, laserPos)
  lineMirrorTarget = Line3D(mirrorPos, targetPos)
  # Get one 3D line that is exactly (in angular terms) 
  # halfway between the lines from the laser source (p4)
  # to the mirror (the mirror location) and the target
  # point.
  halfLaserMirrorTarget = Line3D.halfLine(lineMirrorLaser, lineMirrorTarget)
  # Get the polar coordinates for the line 
  polarLaserMirrorTarget = Line3D.getPolar(halfLaserMirrorTarget)
  # Extract all of the values from the polar coordinates
  radiusLMT = polarLaserMirrorTarget[0]
  thetaLMT = polarLaserMirrorTarget[1]
  phiLMT = polarLaserMirrorTarget[2]
  mirrorPosition = MirrorPosition3D(phiLMT - math.pi, thetaLMT - piOver2)
  return mirrorPosition

# Handle startup 
def startup():
  return

# This routine tests a proposed location (3D). A single floating-point
# value shows how 'good' or 'bad' the proposed location. The returned
# value will always be zero or positive.
def testLocation3D(testLocation, actualMirror1, actualMirror2, actualMirror3): 
  piOver2 = math.pi / 2
  # Define a few 3D points
  point3D1 = Point3D(0.0, -1.0, 0.0)
  point3D2 = Point3D(0.0, 0.0, 0.0)
  point3D3 = Point3D(0.0, 0.0, 1.0)
  point3D4 = Point3D(0.0, 0.0, 2.0)
  # Get some 3D lines. Note that all of the lines start at
  # the mirror point (the test location) but end in various 
  # places
  ltlp43D = Line3D(testLocation, point3D4)
  ltlp13D = Line3D(testLocation, point3D1)
  ltlp23D = Line3D(testLocation, point3D2)
  ltlp33D = Line3D(testLocation, point3D3)
  # Get some 3D lines that are exactly (in angular terms) 
  # halfway between the lines from the laser source (p4)
  # to the mirror (the test location) and the designated points 
  hp4tlp1 = Line3D.halfLine(ltlp43D, ltlp13D)
  hp4tlp2 = Line3D.halfLine(ltlp43D, ltlp23D)
  hp4tlp3 = Line3D.halfLine(ltlp43D, ltlp33D) 
  # Get the polar coordinates for each line 
  polarP4tlp1 = Line3D.getPolar(hp4tlp1)
  polarP4tlp2 = Line3D.getPolar(hp4tlp2)
  polarP4tlp3 = Line3D.getPolar(hp4tlp3)  
  # Extract all of the values from the polar coordinates
  radiusP4tlp1 = polarP4tlp1[0]
  thetaP4tlp1 = polarP4tlp1[1]
  phiP4tlp1 = polarP4tlp1[2]
  radiusP4tlp2 = polarP4tlp2[0]
  thetaP4tlp2 = polarP4tlp2[1]
  phiP4tlp2 = polarP4tlp2[2]
  radiusP4tlp3 = polarP4tlp3[0]
  thetaP4tlp3 = polarP4tlp3[1]
  phiP4tlp3 = polarP4tlp3[2]
  # Get the calculated pan and tilt values for each 
  # of the designated points 
  calculatedPanP4tlp1 = phiP4tlp1 - math.pi 
  calculatedTiltP4tlp1 = thetaP4tlp1 - piOver2
  calculatedPanP4tlp2 = phiP4tlp2 - math.pi 
  calculatedTiltP4tlp2 = thetaP4tlp2 - piOver2
  calculatedPanP4tlp3 = phiP4tlp3 - math.pi 
  calculatedTiltP4tlp3 = thetaP4tlp3 - piOver2 
  # Calculate the pan and tilt adjustments for each
  # of the designationed points
  adjustmentPanP4tlp1 = calculatedPanP4tlp1 - actualMirror1.getPan()
  adjustmentTiltP4tlp1 = calculatedTiltP4tlp1 - actualMirror1.getTilt()
  adjustmentPanP4tlp2 = calculatedPanP4tlp2 - actualMirror2.getPan()
  adjustmentTiltP4tlp2 = calculatedTiltP4tlp2 - actualMirror2.getTilt()
  adjustmentPanP4tlp3 = calculatedPanP4tlp3 - actualMirror3.getPan()
  adjustmentTiltP4tlp3 = calculatedTiltP4tlp3 - actualMirror3.getTilt()
  # Get the average adjustment values
  adjustmentPanAverage = (adjustmentPanP4tlp1 + adjustmentPanP4tlp2 + adjustmentPanP4tlp3)/3.0
  adjustmentTiltAverage = (adjustmentTiltP4tlp1 + adjustmentTiltP4tlp2 + adjustmentTiltP4tlp3)/3.0 
  # get sum of the differences between the pan and tilt values
  sum = 0.0
  sum += (adjustmentPanP4tlp1 - adjustmentPanAverage)**2  
  sum += (adjustmentPanP4tlp2 - adjustmentPanAverage)**2 
  sum += (adjustmentPanP4tlp3 - adjustmentPanAverage)**2 
  sum += (adjustmentTiltP4tlp1 - adjustmentTiltAverage)**2  
  sum += (adjustmentTiltP4tlp2 - adjustmentTiltAverage)**2 
  sum += (adjustmentTiltP4tlp3 - adjustmentTiltAverage)**2 
  return sum
  # Get the pan and tilt adjustment values for each 
  # of the designated points
  adjustedPanP4tlp1 = calculatedPanP4tlp1 - actualMirror1.getPan()
  adjustedTiltP4tlp1 = calculatedTiltP4tlp1 - actualMirror1.getTilt()
  # Get the pan and tilt values for the second point
  adjustedPanP4tlp2 = calculatedPanP4tlp2 - actualMirror2.getPan()
  adjustedTiltP4tlp2 = calculatedTiltP4tlp2 - actualMirror2.getTilt()
  # Get the pan and tilt values for the third point
  adjustedPanP4tlp3 = calculatedPanP4tlp3 - actualMirror3.getPan()
  adjustedTiltP4tlp3 = calculatedTiltP4tlp3 - actualMirror3.getTilt()
  # Get the sum of the differences between the pan and tilt values  
  sum = 0
  sum += (adjustedPanP4tlp2 - adjustedPanP4tlp1)**2
  sum += (adjustedPanP4tlp3 - adjustedPanP4tlp1)**2
  sum += (adjustedTiltP4tlp2 - adjustedTiltP4tlp1)**2
  sum += (adjustedTiltP4tlp3 - adjustedTiltP4tlp1)**2
  return sum
   
# Main program
def main():
  piOver2 = math.pi / 2
  twoPi = math.pi * 2
  # Define the test pan and tilt adjustments
  panAdjustDeg = 11.27
  panAdjustRad = convertDegreesRadians(panAdjustDeg)
  tiltAdjustDeg = -5.66 
  tiltAdjustRad = convertDegreesRadians(tiltAdjustDeg)
  # Define a few 2D points
  point2D1x = -1.0
  point2D1y = 0.0
  point2D1 = Point2D(point2D1x, point2D1y)
  point2D2x = 0.0
  point2D2y = 0.0
  point2D2 = Point2D(point2D2x, point2D2y)
  point2D3x = 1.0
  point2D3y = 0.0
  point2D3 = Point2D(point2D3x, point2D3y)
  # The 2D test point follows  
  point2D4x = -0.5
  point2D4y = -2.0
  point2D4 = Point2D(point2D4x, point2D4y)
  # Get some 2D angles 
  ap12D = getAngle2D(point2D1, point2D4)
  ap22D = getAngle2D(point2D2, point2D4)
  ap32D = getAngle2D(point2D3, point2D4)
  # Get some reflection angles. The leading 'r'
  # (without the quotes) is for reflection
  rp1p22D = (ap12D + ap22D)/2.0
  rp2p22D = (ap22D + ap22D)/2.0
  rp3p22D = (ap32D + ap22D)/2.0
  # Get some 2D pan values 
  pp1p22D = rp1p22D + piOver2
  pp2p22D = rp2p22D + piOver2  
  pp3p22D = rp3p22D + piOver2
  # Add the adjustment factor to the 2D pan values
  ap1p22D = pp1p22D + panAdjustRad
  ap2p22D = pp2p22D + panAdjustRad
  ap3p22D = pp3p22D + panAdjustRad
  # Try to find the location
  # [xLoc, yLoc, calculatedPan] = getLocation2D(-1.0, -1.0, ap1p22D, ap2p22D, ap3p22D)
  # Define a few 3D points
  point3D1 = Point3D(0.0, -1.0, 0.0)
  point3D2 = Point3D(0.0, 0.0, 0.0)
  point3D3 = Point3D(0.0, 0.0, 1.0)
  point3D4 = Point3D(0.0, 0.0, 2.0)
  point3D5 = Point3D(2.0, -0.5, 1.5)
  point3DStart = Point3D(1.7, -0.3, 1.3)
  # Get some 3D lines. Note that all of the lines start
  # at the mirror point but end in various places
  lp5p43D = Line3D(point3D5, point3D4)
  lp5p13D = Line3D(point3D5, point3D1)
  lp5p23D = Line3D(point3D5, point3D2)
  lp5p33D = Line3D(point3D5, point3D3)
  # Get some 3D lines that are exactly (in angular terms) 
  # halfway between the lines from the laser source (p4)
  # to the mirror (p5) and the designated points 
  hp4p5p1 = Line3D.halfLine(lp5p43D, lp5p13D)
  hp4p5p2 = Line3D.halfLine(lp5p43D, lp5p23D)
  hp4p5p3 = Line3D.halfLine(lp5p43D, lp5p33D) 
  # Get the polar coordinates for each line 
  polarP4p5p1 = Line3D.getPolar(hp4p5p1)
  polarP4p5p2 = Line3D.getPolar(hp4p5p2)
  polarP4p5p3 = Line3D.getPolar(hp4p5p3)  
  # Extract all of the values from the polar coordinates
  radiusP4p5p1 = polarP4p5p1[0]
  thetaP4p5p1 = polarP4p5p1[1]
  phiP4p5p1 = polarP4p5p1[2]
  radiusP4p5p2 = polarP4p5p2[0]
  thetaP4p5p2 = polarP4p5p2[1]
  phiP4p5p2 = polarP4p5p2[2]
  radiusP4p5p3 = polarP4p5p3[0]
  thetaP4p5p3 = polarP4p5p3[1]
  phiP4p5p3 = polarP4p5p3[2]
  # Get the calculated pan and tilt values for each 
  # of the designated points
  calculatedPanP4p5p1 = phiP4p5p1 - math.pi
  calculatedTiltP4p5p1 = thetaP4p5p1 - piOver2
  calculatedPanP4p5p2 = phiP4p5p2 - math.pi
  calculatedTiltP4p5p2 = thetaP4p5p2 - piOver2
  calculatedPanP4p5p3 = phiP4p5p3 - math.pi
  calculatedTiltP4p5p3 = thetaP4p5p3 - piOver2
  # Get the adjusted pan and tilt values for each 
  # of the designated points
  adjustedPanP4p5p1 = calculatedPanP4p5p1 + panAdjustRad
  adjustedTiltP4p5p1 = calculatedTiltP4p5p1 + tiltAdjustRad
  mpP4p5p1 = MirrorPosition3D(adjustedPanP4p5p1, adjustedTiltP4p5p1)
  adjustedPanP4p5p2 = calculatedPanP4p5p2 + panAdjustRad
  adjustedTiltP4p5p2 = calculatedTiltP4p5p2 + tiltAdjustRad
  mpP4p5p2 = MirrorPosition3D(adjustedPanP4p5p2, adjustedTiltP4p5p2)
  adjustedPanP4p5p3 = calculatedPanP4p5p3 + panAdjustRad
  adjustedTiltP4p5p3 = calculatedTiltP4p5p3 + tiltAdjustRad
  mpP4p5p3 = MirrorPosition3D(adjustedPanP4p5p3, adjustedTiltP4p5p3)
  # Try to find the location of the mirror
  # [mirrorPoint, mirrorPosition] = getLocation3D(point3DStart, mpP4p5p1, mpP4p5p2, mpP4p5p3)
  if 1 == 2:
    mpl.rcParams['legend.fontsize'] = 10
    fig = plt.figure()
    ax = fig.gca(projection='3d')
  # The code below produces a 3D parametric spiral. It is 
  # commented out for now.
  if 1 == 2:
    theta = np.linspace(-4 * np.pi, 4 * np.pi, 100)
    z = np.linspace(-2, 2, 100)
    r = z**2 + 1
    x = r * np.sin(theta)
    y = r * np.cos(theta)
    ax.plot(x, y, z, label='parametric curve')
    ax.legend()
    plt.show()
  # Data for a three-dimensional line
  if 1 == 2:
    zline = np.linspace(0, 15, 1000)
    xline = np.sin(zline)
    yline = np.cos(zline)
    ax.plot3D(xline, yline, zline, 'gray')
  # Data for three-dimensional scattered points
  if 1 == 2:
    zdata = 15 * np.random.random(100)
    xdata = np.sin(zdata) + 0.1 * np.random.randn(100)
    ydata = np.cos(zdata) + 0.1 * np.random.randn(100)
    ax.scatter3D(xdata, ydata, zdata, c=zdata, cmap='Greens')
  # A 3D contour plot
  if 1 == 2:
    def f(x, y):
      return np.sin(np.sqrt(x ** 2 + y ** 2))
    x = np.linspace(-6, 6, 30)
    y = np.linspace(-6, 6, 30)
    X, Y = np.meshgrid(x, y)
    Z = f(X, Y)
  # Another 3D contour plot
  if 1 == 2:
    ax.contour3D(X, Y, Z, 50, cmap='binary')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
  # Another 3D contour plot
  if 1 == 2:
    ax.plot_wireframe(X, Y, Z, color='black')
    ax.set_title('wireframe')
  # Another 3D contour plot
  if 1 == 2:
    ax.plot_surface(X, Y, Z, rstride=1, cstride=1,
                    cmap='viridis', edgecolor='none')
    ax.set_title('surface')
  # Another 3D contour plot
  if 1 == 2:
    def f(x, y):
      return np.sin(np.sqrt(x ** 2 + y ** 2))
    r = np.linspace(0, 6, 20)
    theta = np.linspace(-0.9 * np.pi, 0.8 * np.pi, 40)
    r, theta = np.meshgrid(r, theta)
    X = r * np.sin(theta)
    Y = r * np.cos(theta)
    Z = f(X, Y) 
    ax.plot_surface(X, Y, Z, rstride=1, cstride=1,
                    cmap='viridis', edgecolor='none')
  # Plot the 3D surface
  if 1 == 2:
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)
    x = 10 * np.outer(np.cos(u), np.sin(v))
    y = 10 * np.outer(np.sin(u), np.sin(v))
    z = 10 * np.outer(np.ones(np.size(u)), np.cos(v))
    ax.plot_surface(x, y, z, color='b')
  # Actually display the 3D plot
  if 1 == 2:
    # ax.view_init(60, 35)
    ax.legend()
    plt.show()
  # Actually display the 2D plot
  if 1 == 2:
    num_pts = 1000
    indices = np.arange(0, num_pts, dtype=float) + 0.5
    r = np.sqrt(indices/num_pts)
    theta = np.pi * (1 + 5**0.5) * indices
    plt.scatter(r*np.cos(theta), r*np.sin(theta))
    plt.show()
  # Create a sphere
  if 1 == 2:
    r = 1
    pi = np.pi
    cos = np.cos
    sin = np.sin
    phi, theta = np.mgrid[0.0:pi:100j, 0.0:2.0*pi:100j]
    x = r*sin(phi)*cos(theta)
    y = r*sin(phi)*sin(theta)
    z = r*cos(phi)
    # Set colours and render
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(x, y, z,  rstride=1, cstride=1, color='c', alpha=0.6, linewidth=0)
    # plt_axes.plot_trisurf(x, y, z, shade=False, color='blue', cmap='Blues', zorder=0)
    # plt_axes.plot(x, y, z, marker='.', linestyle='None', label='Label', color='red', zorder=10)
    plt.show()
  # Scatter plot of generated points
  if 1 == 2:
    num_pts = 100
    indices = np.arange(0, num_pts, dtype=float) + 0.5
    phi = np.arccos(1 - 2*indices/num_pts)
    theta = np.pi * (1 + 5**0.5) * indices
    x, y, z = np.cos(theta) * np.sin(phi), np.sin(theta) * np.sin(phi), np.cos(phi) 
    plt.figure().add_subplot(111, projection='3d').scatter(x, y, z)
    plt.show()
  # Scatter plot of generated points
  if 1 == 2:
    num_pts = 1000
    indices = np.arange(0, num_pts, dtype=float) + 0.5
    theta = np.arccos(1 - 2*indices/num_pts)
    phi = np.pi * (1 + 5**0.5) * indices
    x, y, z = np.cos(phi) * np.sin(theta), np.sin(phi) * np.sin(theta), np.cos(theta) 
    plt.figure().add_subplot(111, projection='3d').scatter(x, y, z)
    plt.show()
  # Build the sphere points used later
  if 1 == 2:
    spherePoints = buildSpherePoints(100)
  # Check the sum value for a known location
  if 1 == 2:
    sum = testLocation3D(point3D5, mpP4p5p1, mpP4p5p2, mpP4p5p3)
    print(sum)
  # Try to find a known location
  if 1 == 1:
    actualMirror1 = mpP4p5p1
    actualMirror2 = mpP4p5p2
    actualMirror3 = mpP4p5p3
    mirrorAdjustments, sugPoint = getLocation3D(point3DStart, actualMirror1, actualMirror2, actualMirror3)
    sum = testLocation3D(sugPoint, mpP4p5p1, mpP4p5p2, mpP4p5p3)
    print(sum)
  # Run some timing code
  if 1 == 2:
    print(time.time())
    start, times = time.perf_counter(), {}
    print("hello")
    times["print"] = time.perf_counter() 
    time.sleep(1.60)
    times["sleep"] = time.perf_counter()
    a = [n**2 for n in range(1000000)]
    times["pow"] = time.perf_counter()
    print(times)

# Actual starting point
if __name__ == "__main__":
  main()