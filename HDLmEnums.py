# The enum below defines the types of host names supported
# by this code. Several quite different kinds of host names
# exist. This code has an enum value for each of them. Of 
# course, other types of enums also exist. They are defined
# by the code below.
#
# In a few cases, the appropriate enum name causes conflicts
# with Python. In those names 'Enum' (without the quotes) has
# been added to the enum name to avoid the conflicts. The suffix
# must be removed in a few cases. 

import enum

# The enum below defines the types of editors this code can be 
#	used for. This code can be used to build and run a modifications
#	editor, an authentication editor, and ignore-lists editor,
#	and a store (stored value) editor. All six (or more) types
#	of editors are valid.
#	 
#	This code can also be used to run the pass-through mechanism.
#	The pass-through mechanism is not generally an editor (with 
#	at least one exception). However, the editor machinery is used
#	to display rules.		
#	  
#	This code was originally used to build and run the 
#	different types of editors. A global value is used to control 
#	the current editor type in the JavaScript code (but not in the
#	Java code). The Python code stores the current editor type in
# a special object.
class HDLmEditorTypes(enum.Enum):
  none     = 0
  auth     = 1
  config   = 2
  ignore   = 3 
  mod      = 4
  passEnum = 5
  proxy    = 6
  store    = 7
  popup    = 8
  simple   = 9 
  gem      = 10
  gxe      = 11
# The enum below defines the types of hosts supported by
# this code. Note that the first type is none which means
# that the host type has not been specified. 
class HDLmHostTypes(enum.Enum):
  none     = 0
  ipv4     = 1
  ipv6     = 2
  standard = 3
# The enum below defines the types of modifications supported by
# this code. Note that the first type is none which means that 
# the modification type has not been specified.   
class HDLmModTypes(enum.Enum):
  none         = 0
  attribute    = 1 
  changeattrs  = 2 
  changenodes  = 3
  extract      = 4
  fontcolor    = 5
  fontfamily   = 6
  fontkerning  = 7
  fontsize     = 8
  fontstyle    = 9
  fontweight   = 10
  height       = 11
  image        = 12
  modify       = 13
  notify       = 14
  order        = 15
  remove       = 16
  replace      = 17 
  script       = 18
  style        = 19
  text         = 20
  textchecked  = 21
  title        = 22
  visit        = 23
  width        = 24
  # The entries below are not valid rule types. However, some instances 
  # of HDLmMod (actually the classes that extend HDLmMod) are not used 
  # for rules. These types are for the other uses of HDLmMod extensions.
  # The entries below were actually taken from the tree types.  
  company      = 24
  data         = 25
  lists        = 26
  reports      = 27
  rules        = 28
# The enum below defines the values for node identifier tracing. 
# We generally don't trace node identifier processing. However, 
# we can trace node identifier processing. These values control 
# what is traced and under what circumstances. */ 
class HDLmNodeIdenTracing(enum.Enum): 
	none  = 0    
	off   = 1
	error = 2
	all   = 3
# The enum below defines the types of tokens supported by the
# tokenizer. An integer is a sequence of numeric digits. A 
# number may or may not have a decimal point. Note that the 
# end type is used as a sentinel to mark the end of the token 
# array. 
# 
# The standard tokenizer never # returns tokens with a type 
# of number. However, other code might combine lower-level 
# tokens to create number tokens.
class HDLmTokenTypes(enum.Enum): 
  none       = 0
  identifier = 1
  operator   = 2
  quoted     = 3
  integer    = 4
  number     = 5
  space      = 6
  unknown    = 7
  end        = 8 
# The enum below defines the types of nodes supported by this
# code. Many types of nodes are supported. We have one and
# only one top-level node. Of course, we can have many
# company, division, site, and modification level nodes. 
# Note that the enum value for modification level nodes 
# is mod, not modification. 
class HDLmTreeTypes(enum.Enum):  
  none      = 0
  top       = 1
  company   = 2
  division  = 3
  site      = 4
  mod       = 5
  config    = 6
  store     = 7
  listEnum  = 8
  ignore    = 9
  reports   = 10
  report    = 11
  line      = 12
  lines     = 13
  lists     = 14
  companies = 15
  rules     = 16
  data      = 17
  value     = 18