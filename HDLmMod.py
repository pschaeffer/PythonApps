# Class for building a rule. Most rules are in the node / rule tree.
# However, rules don't have to be in the node / rule tree. The word
# rule and the word modification are used interchangeably in this
# code and elsewhere.
# 
# Each instance of this class is one rule that may or may not be in
# the node / rule tree

from   HDLmDefines import *
from   HDLmGlobals import *
import jsons

# The following JSON data structure is used to build the editor
# for each type of modification. The modification type is used
# as the property name to obtain each set of modification data. 
HDLmModInfoData = \
  {
    "attribute":     { "fields":
                       [
                         {
                           "description":   "Modification Name",
                           "source":        "name",
                           "fieldtype":     "iotext",
                           "subtype":       "modificationname"
                         },
                         {
                           "description":   "Modification Path Value",
                           "source":        "pathvalue",
                           "fieldtype":     "pathvalue",
                           "subtype":       "Path Value"
                         },
                         {
                           "description":   "Comments",
                           "source":        "comments",
                           "fieldtype":     "comminfo",
                           "subtype":       "comments"
                         },
                         {
                           "description":   "Extra Information",
                           "source":        "extra",
                           "fieldtype":     "extrainfo",
                           "subtype":       "extraAttribute"
                         },
                         {
													 "description":   "Probabiltiy",
													 "source":        "probability",
													 "fieldtype":     "float",
													 "subtype":       "probability"
												 },
                         {
													 "description":   "Use Mode",
													 "source":        "usemode",
													 "fieldtype":     "usemode",
													 "subtype":       "usemode"
												 },
                         {
                           "description":   "Created",
                           "source":        "created",
                           "fieldtype":     "dateio",
                           "subtype":       "outputdate"
                         },
                         {
                           "description":   "Last Modified",
                           "source":        "lastModified",
                           "fieldtype":     "dateio",
                           "subtype":       "outputdate"
                         },
                         {
                           "description":   "CSS Selector",
                           "source":        "cssselector",
                           "fieldtype":     "cssinfo",
                           "subtype":       "cssselector"
                         },
                         {
                           "description":   "XPath Information",
                           "source":        "xpath",
                           "fieldtype":     "xpathinfo",
                           "subtype":       "xpath"
                         },
                         {
                           "description":   "Find Information",
                           "source":        "find",
                           "fieldtype":     "findinfo",
                           "subtype":       "find"
                         },
                         {
                           "description":   "Node Identifier",
                           "source":        "nodeiden",
                           "fieldtype":     "nodeiden",
                           "subtype":       "nodeiden"
                         },
                         {
                           "description":   "Modification Enabled",
                           "source":        "enabled",
                           "fieldtype":     "checkbox",
                           "subtype":       "checkbox"
                         },
                         {
                           "description":   "Modification Type",
                           "source":        "type",
                           "fieldtype":     "typelist",
                           "subtype":       "editableruletypelist"
                         }
                       ]
                     },
    "changeattrs":   { "fields":
                       [
                         {
                           "description":   "Modification Name",
                           "source":        "name",
                           "fieldtype":     "iotext",
                           "subtype":       "modificationname"
                         },
                         {
                           "description":   "Modification Path Value",
                           "source":        "pathvalue",
                           "fieldtype":     "pathvalue",
                           "subtype":       "Path Value"
                         },
                         {
                           "description":   "Comments",
                           "source":        "comments",
                           "fieldtype":     "comminfo",
                           "subtype":       "comments"
                         },
                         {
                           "description":   "Extra Information",
                           "source":        "extra",
                           "fieldtype":     "extrainfo",
                           "subtype":       "extra"
                         },
                         {
													 "description":   "Probabiltiy",
													 "source":        "probability",
													 "fieldtype":     "float",
													 "subtype":       "probability"
												 },
                         {
													 "description":   "Use Mode",
													 "source":        "usemode",
													 "fieldtype":     "usemode",
													 "subtype":       "usemode"
												 },
                         {
                           "description":   "Created",
                           "source":        "created",
                           "fieldtype":     "dateio",
                           "subtype":       "outputdate"
                         },
                         {
                           "description":   "Last Modified",
                           "source":        "lastModified",
                           "fieldtype":     "dateio",
                           "subtype":       "outputdate"
                         },
                         {
                           "description":   "CSS Selector",
                           "source":        "cssselector",
                           "fieldtype":     "cssinfo",
                           "subtype":       "cssselector"
                         },
                         {
                           "description":   "XPath Information",
                           "source":        "xpath",
                           "fieldtype":     "xpathinfo",
                           "subtype":       "xpath"
                         },
                         {
                           "description":   "Find Information",
                           "source":        "find",
                           "fieldtype":     "findinfo",
                           "subtype":       "find"
                         },
                         {
                           "description":   "Node Identifier",
                           "source":        "nodeiden",
                           "fieldtype":     "nodeiden",
                           "subtype":       "nodeiden"
                         },
                         {
                           "description":   "Modification Enabled",
                           "source":        "enabled",
                           "fieldtype":     "checkbox",
                           "subtype":       "checkbox"
                         },
                         {
                           "description":   "Parameter Number",
                           "source":        "parameter",
                           "fieldtype":     "ionumber",
                           "subtype":       "parameter"
                         },
                         {
                           "description":   "Modification Type",
                           "source":        "type",
                           "fieldtype":     "typelist",
                           "subtype":       "editableruletypelist"
                         },
                         {
                           "description":   "New Change Attributes Values",
                           "source":        "changeattrsvalues",
                           "fieldtype":     "textlist",
                           "subtype":       "changeattrs",
                           "datatype":      "array"
                         }
                       ]
                     },
    "changenodes":   { "fields":
                       [
                         {
                           "description":   "Modification Name",
                           "source":        "name",
                           "fieldtype":     "iotext",
                           "subtype":       "modificationname"
                         },
                         {
                           "description":   "Modification Path Value",
                           "source":        "pathvalue",
                           "fieldtype":     "pathvalue",
                           "subtype":       "Path Value"
                         },
                         {
                           "description":   "Comments",
                           "source":        "comments",
                           "fieldtype":     "comminfo",
                           "subtype":       "comments"
                         },
                         {
                           "description":   "Extra Information",
                           "source":        "extra",
                           "fieldtype":     "extrainfo",
                           "subtype":       "extra"
                         },
                         {
													 "description":   "Probabiltiy",
													 "source":        "probability",
													 "fieldtype":     "float",
													 "subtype":       "probability"
												 },
                         {
													 "description":   "Use Mode",
													 "source":        "usemode",
													 "fieldtype":     "usemode",
													 "subtype":       "usemode"
												 },
                         {
                           "description":   "Created",
                           "source":        "created",
                           "fieldtype":     "dateio",
                           "subtype":       "outputdate"
                         },
                         {
                           "description":   "Last Modified",
                           "source":        "lastModified",
                           "fieldtype":     "dateio",
                           "subtype":       "outputdate"
                         },
                         {
                           "description":   "CSS Selector",
                           "source":        "cssselector",
                           "fieldtype":     "cssinfo",
                           "subtype":       "cssselector"
                         },
                         {
                           "description":   "XPath Information",
                           "source":        "xpath",
                           "fieldtype":     "xpathinfo",
                           "subtype":       "xpath"
                         },
                         {
                           "description":   "Find Information",
                           "source":        "find",
                           "fieldtype":     "findinfo",
                           "subtype":       "find"
                         },
                         {
                           "description":   "Node Identifier",
                           "source":        "nodeiden",
                           "fieldtype":     "nodeiden",
                           "subtype":       "nodeiden"
                         },
                         {
                           "description":   "Modification Enabled",
                           "source":        "enabled",
                           "fieldtype":     "checkbox",
                           "subtype":       "checkbox"
                         },
                         {
                           "description":   "Parameter Number",
                           "source":        "parameter",
                           "fieldtype":     "ionumber",
                           "subtype":       "parameter"
                         },
                         {
                           "description":   "Modification Type",
                           "source":        "type",
                           "fieldtype":     "typelist",
                           "subtype":       "editableruletypelist"
                         },
                         {
                           "description":   "New Change Nodes Values",
                           "source":        "changenodesvalues",
                           "fieldtype":     "textlist",
                           "subtype":       "changenodes",
                           "datatype":      "array"
                         }
                       ]
                     },
    "extract":       { "fields":
                       [
                         {
                           "description":   "Modification Name",
                           "source":        "name",
                           "fieldtype":     "iotext",
                           "subtype":       "modificationname"
                         },
                         {
                           "description":   "Modification Path Value",
                           "source":        "pathvalue",
                           "fieldtype":     "pathvalue",
                           "subtype":       "Path Value"
                         },
                         {
                           "description":   "Comments",
                           "source":        "comments",
                           "fieldtype":     "comminfo",
                           "subtype":       "comments"
                         },
                         {
                           "description":   "Extra Information",
                           "source":        "extra",
                           "fieldtype":     "extrainfo",
                           "subtype":       "extra"
                         },
                         {
													 "description":   "Probabiltiy",
													 "source":        "probability",
													 "fieldtype":     "float",
													 "subtype":       "probability"
												 },
                         {
													 "description":   "Use Mode",
													 "source":        "usemode",
													 "fieldtype":     "usemode",
													 "subtype":       "usemode"
												 },
                         {
                           "description":   "Created",
                           "source":        "created",
                           "fieldtype":     "dateio",
                           "subtype":       "outputdate"
                         },
                         {
                           "description":   "Last Modified",
                           "source":        "lastModified",
                           "fieldtype":     "dateio",
                           "subtype":       "outputdate"
                         },
                         {
                           "description":   "CSS Selector",
                           "source":        "cssselector",
                           "fieldtype":     "cssinfo",
                           "subtype":       "cssselector"
                         },
                         {
                           "description":   "XPath Information",
                           "source":        "xpath",
                           "fieldtype":     "xpathinfo",
                           "subtype":       "xpath"
                         },
                         {
                           "description":   "Find Information",
                           "source":        "find",
                           "fieldtype":     "findinfo",
                           "subtype":       "find"
                         },
                         {
                           "description":   "Node Identifier",
                           "source":        "nodeiden",
                           "fieldtype":     "nodeiden",
                           "subtype":       "nodeiden"
                         },
                         {
                           "description":   "Modification Enabled",
                           "source":        "enabled",
                           "fieldtype":     "checkbox",
                           "subtype":       "checkbox"
                         },
                         {
                           "description":   "Modification Type",
                           "source":        "type",
                           "fieldtype":     "typelist",
                           "subtype":       "editableruletypelist"
                         }
                       ]
                     },
    "fontcolor":     { "fields":
                       [
                         {
                           "description":   "Modification Name",
                           "source":        "name",
                           "fieldtype":     "iotext",
                           "subtype":       "modificationname"
                         },
                         {
                           "description":   "Modification Path Value",
                           "source":        "pathvalue",
                           "fieldtype":     "pathvalue",
                           "subtype":       "Path Value"
                         },
                         {
                           "description":   "Comments",
                           "source":        "comments",
                           "fieldtype":     "comminfo",
                           "subtype":       "comments"
                         },
                         {
                           "description":   "Extra Information",
                           "source":        "extra",
                           "fieldtype":     "extrainfo",
                           "subtype":       "extra"
                         },
                         {
													 "description":   "Probabiltiy",
													 "source":        "probability",
													 "fieldtype":     "float",
													 "subtype":       "probability"
												 },
                         {
													 "description":   "Use Mode",
													 "source":        "usemode",
													 "fieldtype":     "usemode",
													 "subtype":       "usemode"
												 },
                         {
                           "description":   "Created",
                           "source":        "created",
                           "fieldtype":     "dateio",
                           "subtype":       "outputdate"
                         },
                         {
                           "description":   "Last Modified",
                           "source":        "lastModified",
                           "fieldtype":     "dateio",
                           "subtype":       "outputdate"
                         },
                         {
                           "description":   "CSS Selector",
                           "source":        "cssselector",
                           "fieldtype":     "cssinfo",
                           "subtype":       "cssselector"
                         },
                         {
                           "description":   "XPath Information",
                           "source":        "xpath",
                           "fieldtype":     "xpathinfo",
                           "subtype":       "xpath"
                         },
                         {
                           "description":   "Find Information",
                           "source":        "find",
                           "fieldtype":     "findinfo",
                           "subtype":       "find"
                         },
                         {
                           "description":   "Node Identifier",
                           "source":        "nodeiden",
                           "fieldtype":     "nodeiden",
                           "subtype":       "nodeiden"
                         },
                         {
                           "description":   "Modification Enabled",
                           "source":        "enabled",
                           "fieldtype":     "checkbox",
                           "subtype":       "checkbox"
                         },
                         {
                           "description":   "Parameter Number",
                           "source":        "parameter",
                           "fieldtype":     "ionumber",
                           "subtype":       "parameter"
                         },
                         {
                           "description":   "Modification Type",
                           "source":        "type",
                           "fieldtype":     "typelist",
                           "subtype":       "editableruletypelist"
                         },
                         {
                           "description":   "New Font Colors",
                           "source":        "colors",
                           "fieldtype":     "colorlist",
                           "subtype":       "colors",
                           "datatype":      "array"
                         }
                       ]
                     },
    "fontfamily":    { "fields":
                       [
                         {
                           "description":   "Modification Name",
                           "source":        "name",
                           "fieldtype":     "iotext",
                           "subtype":       "modificationname"
                         },
                         {
                           "description":   "Modification Path Value",
                           "source":        "pathvalue",
                           "fieldtype":     "pathvalue",
                           "subtype":       "Path Value"
                         },
                         {
                           "description":   "Comments",
                           "source":        "comments",
                           "fieldtype":     "comminfo",
                           "subtype":       "comments"
                         },
                         {
                           "description":   "Extra Information",
                           "source":        "extra",
                           "fieldtype":     "extrainfo",
                           "subtype":       "extra"
                         },
                         {
													 "description":   "Probabiltiy",
													 "source":        "probability",
													 "fieldtype":     "float",
													 "subtype":       "probability"
												 },
                         {
													 "description":   "Use Mode",
													 "source":        "usemode",
													 "fieldtype":     "usemode",
													 "subtype":       "usemode"
												 },
                         {
                           "description":   "Created",
                           "source":        "created",
                           "fieldtype":     "dateio",
                           "subtype":       "outputdate"
                         },
                         {
                           "description":   "Last Modified",
                           "source":        "lastModified",
                           "fieldtype":     "dateio",
                           "subtype":       "outputdate"
                         },
                         {
                           "description":   "CSS Selector",
                           "source":        "cssselector",
                           "fieldtype":     "cssinfo",
                           "subtype":       "cssselector"
                         },
                         {
                           "description":   "XPath Information",
                           "source":        "xpath",
                           "fieldtype":     "xpathinfo",
                           "subtype":       "xpath"
                         },
                         {
                           "description":   "Find Information",
                           "source":        "find",
                           "fieldtype":     "findinfo",
                           "subtype":       "find"
                         },
                         {
                           "description":   "Node Identifier",
                           "source":        "nodeiden",
                           "fieldtype":     "nodeiden",
                           "subtype":       "nodeiden"
                         },
                         {
                           "description":   "Modification Enabled",
                           "source":        "enabled",
                           "fieldtype":     "checkbox",
                           "subtype":       "checkbox"
                         },
                         {
                           "description":   "Parameter Number",
                           "source":        "parameter",
                           "fieldtype":     "ionumber",
                           "subtype":       "parameter"
                         },
                         {
                           "description":   "Modification Type",
                           "source":        "type",
                           "fieldtype":     "typelist",
                           "subtype":       "editableruletypelist"
                         },
                         {
                           "description":   "New Font Families",
                           "source":        "families",
                           "fieldtype":     "textlist",
                           "subtype":       "fontfamily",
                           "datatype":      "array"
                         }
                       ]
                     },
    "fontkerning":   { "fields":
                       [
                         {
                           "description":   "Modification Name",
                           "source":        "name",
                           "fieldtype":     "iotext",                       
                           "subtype":       "modificationname"
                         },
                         {
                           "description":   "Modification Path Value",
                           "source":        "pathvalue",
                           "fieldtype":     "pathvalue",
                           "subtype":       "Path Value"
                         },
                         {
                           "description":   "Comments",
                           "source":        "comments",
                           "fieldtype":     "comminfo",
                           "subtype":       "comments"
                         },
                         {
                           "description":   "Extra Information",
                           "source":        "extra",
                           "fieldtype":     "extrainfo",
                           "subtype":       "extra"
                         },
                         {
													 "description":   "Probabiltiy",
													 "source":        "probability",
													 "fieldtype":     "float",
													 "subtype":       "probability"
												 },
                         {
													 "description":   "Use Mode",
													 "source":        "usemode",
													 "fieldtype":     "usemode",
													 "subtype":       "usemode"
												 },
                         {
                           "description":   "Created",
                           "source":        "created",
                           "fieldtype":     "dateio",
                           "subtype":       "outputdate"
                         },
                         {
                           "description":   "Last Modified",
                           "source":        "lastModified",
                           "fieldtype":     "dateio",
                           "subtype":       "outputdate"
                         },
                         {
                           "description":   "CSS Selector",
                           "source":        "cssselector",
                           "fieldtype":     "cssinfo",
                           "subtype":       "cssselector"
                         },
                         {
                           "description":   "XPath Information",
                           "source":        "xpath",
                           "fieldtype":     "xpathinfo",
                           "subtype":       "xpath"
                         },
                         {
                           "description":   "Find Information",
                           "source":        "find",
                           "fieldtype":     "findinfo",
                           "subtype":       "find"
                         },
                         {
                           "description":   "Node Identifier",
                           "source":        "nodeiden",
                           "fieldtype":     "nodeiden",
                           "subtype":       "nodeiden"
                         },
                         {
                           "description":   "Modification Enabled",
                           "source":        "enabled",
                           "fieldtype":     "checkbox",
                           "subtype":       "checkbox"
                         },
                         {
                           "description":   "Parameter Number",
                           "source":        "parameter",
                           "fieldtype":     "ionumber",
                           "subtype":       "parameter"
                         },
                         {
                           "description":   "Modification Type",
                           "source":        "type",
                           "fieldtype":     "typelist",
                           "subtype":       "editableruletypelist"
                         },
                         {
                           "description":   "New Font Kernings",
                           "source":        "kernings",
                           "fieldtype":     "textlist",
                           "subtype":       "fontkerning",
                           "datatype":      "array"
                         }
                       ]
                     },
    "fontsize":      { "fields":
                       [
                         {
                           "description":   "Modification Name",
                           "source":        "name",
                           "fieldtype":     "iotext",
                           "subtype":       "modificationname"
                         },
                         {
                           "description":   "Modification Path Value",
                           "source":        "pathvalue",
                           "fieldtype":     "pathvalue",
                           "subtype":       "Path Value"
                         },
                         {
                           "description":   "Comments",
                           "source":        "comments",
                           "fieldtype":     "comminfo",
                           "subtype":       "comments"
                         },
                         {
                           "description":   "Extra Information",
                           "source":        "extra",
                           "fieldtype":     "extrainfo",
                           "subtype":       "extra"
                         },
                         {
													 "description":   "Probabiltiy",
													 "source":        "probability",
													 "fieldtype":     "float",
													 "subtype":       "probability"
												 },
                         {
													 "description":   "Use Mode",
													 "source":        "usemode",
													 "fieldtype":     "usemode",
													 "subtype":       "usemode"
												 },
                         {
                           "description":   "Created",
                           "source":        "created",
                           "fieldtype":     "dateio",
                           "subtype":       "outputdate"
                         },
                         {
                           "description":   "Last Modified",
                           "source":        "lastModified",
                           "fieldtype":     "dateio",
                           "subtype":       "outputdate"
                         },
                         {
                           "description":   "CSS Selector",
                           "source":        "cssselector",
                           "fieldtype":     "cssinfo",
                           "subtype":       "cssselector"
                         },
                         {
                           "description":   "XPath Information",
                           "source":        "xpath",
                           "fieldtype":     "xpathinfo",
                           "subtype":       "xpath"
                         },
                         {
                           "description":   "Find Information",
                           "source":        "find",
                           "fieldtype":     "findinfo",
                           "subtype":       "find"
                         },
                         {
                           "description":   "Node Identifier",
                           "source":        "nodeiden",
                           "fieldtype":     "nodeiden",
                           "subtype":       "nodeiden"
                         },
                         {
                           "description":   "Modification Enabled",
                           "source":        "enabled",
                           "fieldtype":     "checkbox",
                           "subtype":       "checkbox"
                         },
                         {
                           "description":   "Parameter Number",
                           "source":        "parameter",
                           "fieldtype":     "ionumber",
                           "subtype":       "parameter"
                         },
                         {
                           "description":   "Modification Type",
                           "source":        "type",
                           "fieldtype":     "typelist",
                           "subtype":       "editableruletypelist"
                         },
                         {
                           "description":   "New Font Sizes",
                           "source":        "sizes",
                           "fieldtype":     "textlist",
                           "subtype":       "fontsize",
                           "datatype":      "array"
                         }
                       ]
                     },
    "fontstyle":     { "fields":
                       [
                         {
                           "description":   "Modification Name",
                           "source":        "name",
                           "fieldtype":     "iotext",
                           "subtype":       "modificationname"
                         },
                         {
                           "description":   "Modification Path Value",
                           "source":        "pathvalue",
                           "fieldtype":     "pathvalue",
                           "subtype":       "Path Value"
                         },
                         {
                           "description":   "Comments",
                           "source":        "comments",
                           "fieldtype":     "comminfo",
                           "subtype":       "comments"
                         },
                         {
                           "description":   "Extra Information",
                           "source":        "extra",
                           "fieldtype":     "extrainfo",
                           "subtype":       "extra"
                         },
                         {
													 "description":   "Probabiltiy",
													 "source":        "probability",
													 "fieldtype":     "float",
													 "subtype":       "probability"
												 },
                         {
													 "description":   "Use Mode",
													 "source":        "usemode",
													 "fieldtype":     "usemode",
													 "subtype":       "usemode"
												 },
                         {
                           "description":   "Created",
                           "source":        "created",
                           "fieldtype":     "dateio",
                           "subtype":       "outputdate"
                         },
                         {
                           "description":   "Last Modified",
                           "source":        "lastModified",
                           "fieldtype":     "dateio",
                           "subtype":       "outputdate"
                         },
                         {
                           "description":   "CSS Selector",
                           "source":        "cssselector",
                           "fieldtype":     "cssinfo",
                           "subtype":       "cssselector"
                         },
                         {
                           "description":   "XPath Information",
                           "source":        "xpath",
                           "fieldtype":     "xpathinfo",
                           "subtype":       "xpath"
                         },
                         {
                           "description":   "Find Information",
                           "source":        "find",
                           "fieldtype":     "findinfo",
                           "subtype":       "find"
                         },
                         {
                           "description":   "Node Identifier",
                           "source":        "nodeiden",
                           "fieldtype":     "nodeiden",
                           "subtype":       "nodeiden"
                         },
                         {
                           "description":   "Modification Enabled",
                           "source":        "enabled",
                           "fieldtype":     "checkbox",
                           "subtype":       "checkbox"
                         },
                         {
                           "description":   "Parameter Number",
                           "source":        "parameter",
                           "fieldtype":     "ionumber",
                           "subtype":       "parameter"
                         },
                         {
                           "description":   "Modification Type",
                           "source":        "type",
                           "fieldtype":     "typelist",
                           "subtype":       "editableruletypelist"
                         },
                         {
                           "description":   "New Font Styles",
                           "source":        "styles",
                           "fieldtype":     "textlist",
                           "subtype":       "fontstyle",
                           "datatype":      "array" 
                         }
                       ]
                     },
    "fontweight":    { "fields":
                       [
                         {
                           "description":   "Modification Name",
                           "source":        "name",
                           "fieldtype":     "iotext",
                           "subtype":       "modificationname"
                         },
                         {
                           "description":   "Modification Path Value",
                           "source":        "pathvalue",
                           "fieldtype":     "pathvalue",
                           "subtype":       "Path Value"
                         },
                         {
                           "description":   "Comments",
                           "source":        "comments",
                           "fieldtype":     "comminfo",
                           "subtype":       "comments"
                         },
                         {
                           "description":   "Extra Information",
                           "source":        "extra",
                           "fieldtype":     "extrainfo",
                           "subtype":       "extra"
                         },
                         {
													 "description":   "Probabiltiy",
													 "source":        "probability",
													 "fieldtype":     "float",
													 "subtype":       "probability"
												 },
                         {
													 "description":   "Use Mode",
													 "source":        "usemode",
													 "fieldtype":     "usemode",
													 "subtype":       "usemode"
												 },
                         {
                           "description":   "Created",
                           "source":        "created",
                           "fieldtype":     "dateio",
                           "subtype":       "outputdate"
                         },
                         {
                           "description":   "Last Modified",
                           "source":        "lastModified",
                           "fieldtype":     "dateio",
                           "subtype":       "outputdate"
                         },
                         {
                           "description":   "CSS Selector",
                           "source":        "cssselector",
                           "fieldtype":     "cssinfo",
                           "subtype":       "cssselector"
                         },
                         {
                           "description":   "XPath Information",
                           "source":        "xpath",
                           "fieldtype":     "xpathinfo",
                           "subtype":       "xpath"
                         },
                         {
                           "description":   "Find Information",
                           "source":        "find",
                           "fieldtype":     "findinfo",
                           "subtype":       "find"
                         },
                         {
                           "description":   "Node Identifier",
                           "source":        "nodeiden",
                           "fieldtype":     "nodeiden",
                           "subtype":       "nodeiden"
                         },
                         {
                           "description":   "Modification Enabled",
                           "source":        "enabled",
                           "fieldtype":     "checkbox",
                           "subtype":       "checkbox"
                         },
                         {
                           "description":   "Parameter Number",
                           "source":        "parameter",
                           "fieldtype":     "ionumber",
                           "subtype":       "parameter"
                         },
                         {
                           "description":   "Modification Type",
                           "source":        "type",
                           "fieldtype":     "typelist",
                           "subtype":       "editableruletypelist"
                         },
                         {
                           "description":   "New Font Weights",
                           "source":        "weights",
                           "fieldtype":     "textlist",
                           "subtype":       "fontweight",
                           "datatype":      "array"
                         }
                       ]
                     },
    "height":        { "fields":
                       [
                         {
                           "description":   "Modification Name",
                           "source":        "name",
                           "fieldtype":     "iotext",
                           "subtype":       "modificationname"
                         },
                         {
                           "description":   "Modification Path Value",
                           "source":        "pathvalue",
                           "fieldtype":     "pathvalue",
                           "subtype":       "Path Value"
                         },
                         {
                           "description":   "Comments",
                           "source":        "comments",
                           "fieldtype":     "comminfo",
                           "subtype":       "comments"
                         },
                         {
                           "description":   "Extra Information",
                           "source":        "extra",
                           "fieldtype":     "extrainfo",
                           "subtype":       "extra"
                         },
                         {
													 "description":   "Probabiltiy",
													 "source":        "probability",
													 "fieldtype":     "float",
													 "subtype":       "probability"
												 },
                         {
													 "description":   "Use Mode",
													 "source":        "usemode",
													 "fieldtype":     "usemode",
													 "subtype":       "usemode"
												 },
                         {
                           "description":   "Created",
                           "source":        "created",
                           "fieldtype":     "dateio",
                           "subtype":       "outputdate"
                         },
                         {
                           "description":   "Last Modified",
                           "source":        "lastModified",
                           "fieldtype":     "dateio",
                           "subtype":       "outputdate"
                         },
                         {
                           "description":   "CSS Selector",
                           "source":        "cssselector",
                           "fieldtype":     "cssinfo",
                           "subtype":       "cssselector"
                         },
                         {
                           "description":   "XPath Information",
                           "source":        "xpath",
                           "fieldtype":     "xpathinfo",
                           "subtype":       "xpath"
                         },
                         {
                           "description":   "Find Information",
                           "source":        "find",
                           "fieldtype":     "findinfo",
                           "subtype":       "find"
                         },
                         {
                           "description":   "Node Identifier",
                           "source":        "nodeiden",
                           "fieldtype":     "nodeiden",
                           "subtype":       "nodeiden"
                         },
                         {
                           "description":   "Modification Enabled",
                           "source":        "enabled",
                           "fieldtype":     "checkbox",
                           "subtype":       "checkbox"
                         },
                         {
                           "description":   "Parameter Number",
                           "source":        "parameter",
                           "fieldtype":     "ionumber",
                           "subtype":       "parameter"
                         },
                         {
                           "description":   "Modification Type",
                           "source":        "type",
                           "fieldtype":     "typelist",
                           "subtype":       "editableruletypelist"
                         },
                         {
                           "description":   "New Heights",
                           "source":        "heights",
                           "fieldtype":     "textlist",
                           "subtype":       "height",
                           "datatype":      "array"
                         }
                       ]
                     },
    "image":         { "fields":
                       [
                         {
                           "description":   "Modification Name",
                           "source":        "name",
                           "fieldtype":     "iotext",
                           "subtype":       "modificationname"
                         },
                         {
                           "description":   "Modification Path Value",
                           "source":        "pathvalue",
                           "fieldtype":     "pathvalue",
                           "subtype":       "Path Value"
                         },
                         {
                           "description":   "Comments",
                           "source":        "comments",
                           "fieldtype":     "comminfo",
                           "subtype":       "comments"
                         },
                         {
                           "description":   "Extra Information",
                           "source":        "extra",
                           "fieldtype":     "extrainfo",
                           "subtype":       "extra"
                         },
                         {
													 "description":   "Probabiltiy",
													 "source":        "probability",
													 "fieldtype":     "float",
													 "subtype":       "probability"
												 },
                         {
													 "description":   "Use Mode",
													 "source":        "usemode",
													 "fieldtype":     "usemode",
													 "subtype":       "usemode"
												 },
                         {
                           "description":   "Created",
                           "source":        "created",
                           "fieldtype":     "dateio",
                           "subtype":       "outputdate"
                         },
                         {
                           "description":   "Last Modified",
                           "source":        "lastModified",
                           "fieldtype":     "dateio",
                           "subtype":       "outputdate"
                         },
                         {
                           "description":   "CSS Selector",
                           "source":        "cssselector",
                           "fieldtype":     "cssinfo",
                           "subtype":       "cssselector"
                         },
                         {
                           "description":   "XPath Information",
                           "source":        "xpath",
                           "fieldtype":     "xpathinfo",
                           "subtype":       "xpath"
                         },
                         {
                           "description":   "Find Information",
                           "source":        "find",
                           "fieldtype":     "findinfo",
                           "subtype":       "find"
                         },
                         {
                           "description":   "Node Identifier",
                           "source":        "nodeiden",
                           "fieldtype":     "nodeiden",
                           "subtype":       "nodeiden"
                         },
                         {
                           "description":   "Modification Enabled",
                           "source":        "enabled",
                           "fieldtype":     "checkbox",
                           "subtype":       "checkbox"
                         },
                         {
                           "description":   "Parameter Number",
                           "source":        "parameter",
                           "fieldtype":     "ionumber",
                           "subtype":       "parameter"
                         },
                         {
                           "description":   "Modification Type",
                           "source":        "type",
                           "fieldtype":     "typelist",
                           "subtype":       "editableruletypelist"
                         },
                         {
                           "description":   "New Images",
                           "source":        "images",
                           "fieldtype":     "imagelist",
                           "subtype":       "images",
                           "datatype":      "array"
                         }
                       ]
                     },
    "modify":        { "fields":
                       [
                         {
                           "description":   "Modification Name",
                           "source":        "name",
                           "fieldtype":     "iotext",
                           "subtype":       "modificationname"
                         },
                         {
                           "description":   "Modification Path Value",
                           "source":        "pathvalue",
                           "fieldtype":     "pathvalue",
                           "subtype":       "Path Value"
                         },
                         {
                           "description":   "Comments",
                           "source":        "comments",
                           "fieldtype":     "comminfo",
                           "subtype":       "comments"
                         },
                         {
                           "description":   "Extra Information",
                           "source":        "extra",
                           "fieldtype":     "extrainfo",
                           "subtype":       "extra"
                         },
                         {
													 "description":   "Probabiltiy",
													 "source":        "probability",
													 "fieldtype":     "float",
													 "subtype":       "probability"
												 },
                         {
													 "description":   "Use Mode",
													 "source":        "usemode",
													 "fieldtype":     "usemode",
													 "subtype":       "usemode"
												 },
                         {
                           "description":   "Created",
                           "source":        "created",
                           "fieldtype":     "dateio",
                           "subtype":       "outputdate"
                         },
                         {
                           "description":   "Last Modified",
                           "source":        "lastModified",
                           "fieldtype":     "dateio",
                           "subtype":       "outputdate"
                         },
                         {
                           "description":   "CSS Selector",
                           "source":        "cssselector",
                           "fieldtype":     "cssinfo",
                           "subtype":       "cssselector"
                         },
                         {
                           "description":   "XPath Information",
                           "source":        "xpath",
                           "fieldtype":     "xpathinfo",
                           "subtype":       "xpath"
                         },
                         {
                           "description":   "Find Information",
                           "source":        "find",
                           "fieldtype":     "findinfo",
                           "subtype":       "find"
                         },
                         {
                           "description":   "Node Identifier",
                           "source":        "nodeiden",
                           "fieldtype":     "nodeiden",
                           "subtype":       "nodeiden"
                         },
                         {
                           "description":   "Modification Enabled",
                           "source":        "enabled",
                           "fieldtype":     "checkbox",
                           "subtype":       "checkbox"
                         },
                         {
                           "description":   "Modification Type",
                           "source":        "type",
                           "fieldtype":     "typelist",
                           "subtype":       "editableruletypelist"
                         }
                       ]
                     },
    "newcompmod":    { "fields":
                       [
                         {
                           "description":   "Company Name",
                           "source":        "name",
                           "fieldtype":     "iotext",
                           "subtype":       "editablecompmodname"
                         }
                       ]
                     },
    "newdivision":   { "fields":
                       [
                         {
                           "description":   "Division Name",
                           "source":        "name",
                           "fieldtype":     "iotext",
                           "subtype":       "editabledivisionname"
                         }
                       ]
                     },
    "newmod":        { "fields":
                       [
                         {
                           "description":   "Modification Name",
                           "source":        "name",
                           "fieldtype":     "iotext",
                           "subtype":       "editablemodificationname"
                         },
                         {
                           "description":   "Modification Path Value",
                           "source":        "pathvalue",
                           "fieldtype":     "pathvalue",
                           "subtype":       "Path Value"
                         },
                         {
                           "description":   "Comments",
                           "source":        "comments",
                           "fieldtype":     "comminfo",
                           "subtype":       "comments"
                         },
                         {
                           "description":   "Extra Information",
                           "source":        "extra",
                           "fieldtype":     "extrainfo",
                           "subtype":       "extra"
                         },
                         {
													 "description":   "Probabiltiy",
													 "source":        "probability",
													 "fieldtype":     "float",
													 "subtype":       "probability"
												 },
                         {
													 "description":   "Use Mode",
													 "source":        "usemode",
													 "fieldtype":     "usemode",
													 "subtype":       "usemode"
												 },
                         {
                           "description":   "Created",
                           "source":        "created",
                           "fieldtype":     "dateio",
                           "subtype":       "outputdate"
                         },
                         {
                           "description":   "Last Modified",
                           "source":        "lastModified",
                           "fieldtype":     "dateio",
                           "subtype":       "outputdate"
                         },
                         {
                           "description":   "CSS Selector",
                           "source":        "cssselector",
                           "fieldtype":     "cssinfo",
                           "subtype":       "cssselector"
                         },
                         {
                           "description":   "XPath Information",
                           "source":        "xpath",
                           "fieldtype":     "xpathinfo",
                           "subtype":       "xpath"
                         },
                         {
                           "description":   "Find Information",
                           "source":        "find",
                           "fieldtype":     "findinfo",
                           "subtype":       "find"
                         },
                         {
                           "description":   "Node Identifier",
                           "source":        "nodeiden",
                           "fieldtype":     "nodeiden",
                           "subtype":       "nodeiden"
                         },
                         {
                           "description":   "Modification Enabled",
                           "source":        "enabled",
                           "fieldtype":     "checkbox",
                           "subtype":       "checkbox"
                         },
                         {
                           "description":   "Parameter Number",
                           "source":        "parameter",
                           "fieldtype":     "ionumber",
                           "subtype":       "editableparameter"
                         },
                         {
                           "description":   "Modification Type",
                           "source":        "type",
                           "fieldtype":     "typelist",
                           "subtype":       "editableruletypelist"
                         }
                       ]
                     },
    "newsite":       { "fields":
                       [
                         {
                           "description":   "Site Name",
                           "source":        "name",
                           "fieldtype":     "iotext",
                           "subtype":       "editablesitename"
                         }        
                       ]
                     },
    "newvalue":      { "fields":
                       [
                         {
                           "description":   "Data Value Name",
                           "source":        "name",
                           "fieldtype":     "iotext",
                           "subtype":       "editabledatavaluename"
                         },    
                         {
                           "description":   "Comments",
                           "source":        "comments",
                           "fieldtype":     "comminfo",
                           "subtype":       "comments"
                         },
                         {
                            "description":  "Data value",
                            "source":       "value",
                            "fieldtype":    "iotext",
                            "subtype":      "datavalue"
                         }
                       ]
                     },
    "notify":        { "fields":
                       [
                         {
                           "description":   "Modification Name",
                           "source":        "name",
                           "fieldtype":     "iotext",
                           "subtype":       "modificationname"
                         },
                         {
                           "description":   "Modification Path Value",
                           "source":        "pathvalue",
                           "fieldtype":     "pathvalue",
                           "subtype":       "Path Value"
                         },
                         {
                           "description":   "Comments",
                           "source":        "comments",
                           "fieldtype":     "comminfo",
                           "subtype":       "comments"
                         },
                         {
                           "description":   "Extra Information",
                           "source":        "extra",
                           "fieldtype":     "extrainfo",
                           "subtype":       "extra"
                         },
                         {
													 "description":   "Probabiltiy",
													 "source":        "probability",
													 "fieldtype":     "float",
													 "subtype":       "probability"
												 },
                         {
													 "description":   "Use Mode",
													 "source":        "usemode",
													 "fieldtype":     "usemode",
													 "subtype":       "usemode"
												 },
                         {
                           "description":   "Created",
                           "source":        "created",
                           "fieldtype":     "dateio",
                           "subtype":       "outputdate"
                         },
                         {
                           "description":   "Last Modified",
                           "source":        "lastModified",
                           "fieldtype":     "dateio",
                           "subtype":       "outputdate"
                         },
                         {
                           "description":   "CSS Selector",
                           "source":        "cssselector",
                           "fieldtype":     "cssinfo",
                           "subtype":       "cssselector"
                         },
                         {
                           "description":   "XPath Information",
                           "source":        "xpath",
                           "fieldtype":     "xpathinfo",
                           "subtype":       "xpath"
                         },
                         {
                           "description":   "Find Information",
                           "source":        "find",
                           "fieldtype":     "findinfo",
                           "subtype":       "find"
                         },
                         {
                           "description":   "Node Identifier",
                           "source":        "nodeiden",
                           "fieldtype":     "nodeiden",
                           "subtype":       "nodeiden"
                         },
                         {
                           "description":   "Modification Enabled",
                           "source":        "enabled",
                           "fieldtype":     "checkbox",
                           "subtype":       "checkbox"
                         },
                         {
                           "description":   "Modification Type",
                           "source":        "type",
                           "fieldtype":     "typelist",
                           "subtype":       "editableruletypelist"
                         },
                         {
                           "description":   "New Extract Targets",
                           "source":        "targets",
                           "fieldtype":     "textlist",
                           "subtype":       "target",
                           "datatype":      "array"
                         }
                       ]
                     },
    "order":         { "fields":
                       [
                         {
                           "description":   "Modification Name",
                           "source":        "name",
                           "fieldtype":     "iotext",
                           "subtype":       "modificationname"
                         },
                         {
                           "description":   "Modification Path Value",
                           "source":        "pathvalue",
                           "fieldtype":     "pathvalue",
                           "subtype":       "Path Value"
                         },
                         {
                           "description":   "Comments",
                           "source":        "comments",
                           "fieldtype":     "comminfo",
                           "subtype":       "comments"
                         },
                         {
                           "description":   "Extra Information",
                           "source":        "extra",
                           "fieldtype":     "extrainfo",
                           "subtype":       "extra"
                         },
                         {
													 "description":   "Probabiltiy",
													 "source":        "probability",
													 "fieldtype":     "float",
													 "subtype":       "probability"
												 },
                         {
													 "description":   "Use Mode",
													 "source":        "usemode",
													 "fieldtype":     "usemode",
													 "subtype":       "usemode"
												 },
                         {
                           "description":   "Created",
                           "source":        "created",
                           "fieldtype":     "dateio",
                           "subtype":       "outputdate"
                         },
                         {
                           "description":   "Last Modified",
                           "source":        "lastModified",
                           "fieldtype":     "dateio",
                           "subtype":       "outputdate"
                         },
                         {
                           "description":   "CSS Selector",
                           "source":        "cssselector",
                           "fieldtype":     "cssinfo",
                           "subtype":       "cssselector"
                         },
                         {
                           "description":   "XPath Information",
                           "source":        "xpath",
                           "fieldtype":     "xpathinfo",
                           "subtype":       "xpath"
                         },
                         {
                           "description":   "Find Information",
                           "source":        "find",
                           "fieldtype":     "findinfo",
                           "subtype":       "find"
                         },
                         {
                           "description":   "Node Identifier",
                           "source":        "nodeiden",
                           "fieldtype":     "nodeiden",
                           "subtype":       "nodeiden"
                         },
                         {
                           "description":   "Modification Enabled",
                           "source":        "enabled",
                           "fieldtype":     "checkbox",
                           "subtype":       "checkbox"
                         },
                         {
                           "description":   "Parameter Number",
                           "source":        "parameter",
                           "fieldtype":     "ionumber",
                           "subtype":       "parameter"
                         },
                         {
                           "description":   "Modification Type",
                           "source":        "type",
                           "fieldtype":     "typelist",
                           "subtype":       "editableruletypelist"
                         },
                         {
                           "description":   "New Order Information",
                           "source":        "orders",
                           "fieldtype":     "textlist",
                           "subtype":       "order",
                           "datatype":      "array"
                         }
                       ]
                     },    
    "remove":        { "fields":
                       [
                         {
                           "description":   "Modification Name",
                           "source":        "name",
                           "fieldtype":     "iotext",
                           "subtype":       "modificationname"
                         },
                         {
                           "description":   "Modification Path Value",
                           "source":        "pathvalue",
                           "fieldtype":     "pathvalue",
                           "subtype":       "Path Value"
                         },
                         {
                           "description":   "Comments",
                           "source":        "comments",
                           "fieldtype":     "comminfo",
                           "subtype":       "comments"
                         },
                         {
                           "description":   "Extra Information",
                           "source":        "extra",
                           "fieldtype":     "extrainfo",
                           "subtype":       "extra"
                         },
                         {
													 "description":   "Probabiltiy",
													 "source":        "probability",
													 "fieldtype":     "float",
													 "subtype":       "probability"
												 },
                         {
													 "description":   "Use Mode",
													 "source":        "usemode",
													 "fieldtype":     "usemode",
													 "subtype":       "usemode"
												 },
                         {
                           "description":   "Created",
                           "source":        "created",
                           "fieldtype":     "dateio",
                           "subtype":       "outputdate"
                         },
                         {
                           "description":   "Last Modified",
                           "source":        "lastModified",
                           "fieldtype":     "dateio",
                           "subtype":       "outputdate"
                         },
                         {
                           "description":   "CSS Selector",
                           "source":        "cssselector",
                           "fieldtype":     "cssinfo",
                           "subtype":       "cssselector"
                         },
                         {
                           "description":   "XPath Information",
                           "source":        "xpath",
                           "fieldtype":     "xpathinfo",
                           "subtype":       "xpath"
                         },
                         {
                           "description":   "Find Information",
                           "source":        "find",
                           "fieldtype":     "findinfo",
                           "subtype":       "find"
                         },
                         {
                           "description":   "Node Identifier",
                           "source":        "nodeiden",
                           "fieldtype":     "nodeiden",
                           "subtype":       "nodeiden"
                         },
                         {
                           "description":   "Modification Enabled",
                           "source":        "enabled",
                           "fieldtype":     "checkbox",
                           "subtype":       "checkbox"
                         },
                         {
                           "description":   "Parameter Number",
                           "source":        "parameter",
                           "fieldtype":     "ionumber",
                           "subtype":       "parameter"
                         },
                         {
                           "description":   "Modification Type",
                           "source":        "type",
                           "fieldtype":     "typelist",
                           "subtype":       "editableruletypelist"
                         },
                         {
                           "description":   "New Remove Values",
                           "source":        "removevalues",
                           "fieldtype":     "textlist",
                           "subtype":       "remove",
                           "datatype":      "array"
                         }
                       ]     
                     },
    "replace":       { "fields":
                       [
                         {
                           "description":   "Modification Name",
                           "source":        "name",
                           "fieldtype":     "iotext",
                           "subtype":       "modificationname"
                         },
                         {
                           "description":   "Modification Path Value",
                           "source":        "pathvalue",
                           "fieldtype":     "pathvalue",
                           "subtype":       "Path Value"
                         },
                         {
                           "description":   "Comments",
                           "source":        "comments",
                           "fieldtype":     "comminfo",
                           "subtype":       "comments"
                         },
                         {
                           "description":   "Extra Information",
                           "source":        "extra",
                           "fieldtype":     "extrainfo",
                           "subtype":       "extra"
                         },
                         {
													 "description":   "Probabiltiy",
													 "source":        "probability",
													 "fieldtype":     "float",
													 "subtype":       "probability"
												 },
                         {
													 "description":   "Use Mode",
													 "source":        "usemode",
													 "fieldtype":     "usemode",
													 "subtype":       "usemode"
												 },
                         {
                           "description":   "Created",
                           "source":        "created",
                           "fieldtype":     "dateio",
                           "subtype":       "outputdate"
                         },
                         {
                           "description":   "Last Modified",
                           "source":        "lastModified",
                           "fieldtype":     "dateio",
                           "subtype":       "outputdate"
                         },
                         {
                           "description":   "CSS Selector",
                           "source":        "cssselector",
                           "fieldtype":     "cssinfo",
                           "subtype":       "cssselector"
                         },
                         {
                           "description":   "XPath Information",
                           "source":        "xpath",
                           "fieldtype":     "xpathinfo",
                           "subtype":       "xpath"
                         },
                         {
                           "description":   "Find Information",
                           "source":        "find",
                           "fieldtype":     "findinfo",
                           "subtype":       "find"
                         },
                         {
                           "description":   "Node Identifier",
                           "source":        "nodeiden",
                           "fieldtype":     "nodeiden",
                           "subtype":       "nodeiden"
                         },
                         {
                           "description":   "Modification Enabled",
                           "source":        "enabled",
                           "fieldtype":     "checkbox",
                           "subtype":       "checkbox"
                         },
                         {
                           "description":   "Parameter Number",
                           "source":        "parameter",
                           "fieldtype":     "ionumber",
                           "subtype":       "parameter"
                         },
                         {
                           "description":   "Modification Type",
                           "source":        "type",
                           "fieldtype":     "typelist",
                           "subtype":       "editableruletypelist"
                         },
                         {
                           "description":   "New Replace Values",
                           "source":        "replacevalues",
                           "fieldtype":     "textlist",
                           "subtype":       "replace",
                           "datatype":      "array"
                         }
                       ]
                     },
  "script":          { "fields":
                       [
                         {
                           "description":   "Modification Name",
                           "source":        "name",
                           "fieldtype":     "iotext",
                           "subtype":       "modificationname"
                         },
                         {
                           "description":   "Modification Path Value",
                           "source":        "pathvalue",
                           "fieldtype":     "pathvalue",
                           "subtype":       "Path Value"
                         },
                         {
                           "description":   "Comments",
                           "source":        "comments",
                           "fieldtype":     "comminfo",
                           "subtype":       "comments"
                         },
                         {
                           "description":   "Extra Information",
                           "source":        "extra",
                           "fieldtype":     "extrainfo",
                           "subtype":       "extra"
                         },
                         {
													 "description":   "Probabiltiy",
													 "source":        "probability",
													 "fieldtype":     "float",
													 "subtype":       "probability"
												 },
                         {
													 "description":   "Use Mode",
													 "source":        "usemode",
													 "fieldtype":     "usemode",
													 "subtype":       "usemode"
												 },
                         {
                           "description":   "Created",
                           "source":        "created",
                           "fieldtype":     "dateio",
                           "subtype":       "outputdate"
                         },
                         {
                           "description":   "Last Modified",
                           "source":        "lastModified",
                           "fieldtype":     "dateio",
                           "subtype":       "outputdate"
                         },
                         {
                           "description":   "CSS Selector",
                           "source":        "cssselector",
                           "fieldtype":     "cssinfo",
                           "subtype":       "cssselector"
                         },
                         {
                           "description":   "XPath Information",
                           "source":        "xpath",
                           "fieldtype":     "xpathinfo",
                           "subtype":       "xpath"
                         },
                         {
                           "description":   "Find Information",
                           "source":        "find",
                           "fieldtype":     "findinfo",
                           "subtype":       "find"
                         },
                         {
                           "description":   "Node Identifier",
                           "source":        "nodeiden",
                           "fieldtype":     "nodeiden",
                           "subtype":       "nodeiden"
                         },
                         {
                           "description":   "Modification Enabled",
                           "source":        "enabled",
                           "fieldtype":     "checkbox",
                           "subtype":       "checkbox"
                         },
                         {
                           "description":   "Parameter Number",
                           "source":        "parameter",
                           "fieldtype":     "ionumber",
                           "subtype":       "parameter"
                         },
                         {
                           "description":   "Modification Type",
                           "source":        "type",
                           "fieldtype":     "typelist",
                           "subtype":       "editableruletypelist"
                         },
                         {
                           "description":   "New JS Scripts",
                           "source":        "scripts",
                           "fieldtype":     "textlist",
                           "subtype":       "script",
                           "datatype":      "array"
                         }
                       ]
                     },
    "style":         { "fields":
                       [
                         {
                           "description":   "Modification Name",
                           "source":        "name",
                           "fieldtype":     "iotext",
                           "subtype":       "modificationname"
                         },
                         {
                           "description":   "Modification Path Value",
                           "source":        "pathvalue",
                           "fieldtype":     "pathvalue",
                           "subtype":       "Path Value"
                         },
                         {
                           "description":   "Comments",
                           "source":        "comments",
                           "fieldtype":     "comminfo",
                           "subtype":       "comments"
                         },
                         {
                           "description":   "Extra Information",
                           "source":        "extra",
                           "fieldtype":     "extrainfo",
                           "subtype":       "extraStyle"
                         },
                         {
													 "description":   "Probabiltiy",
													 "source":        "probability",
													 "fieldtype":     "float",
													 "subtype":       "probability"
												 },
                         {
													 "description":   "Use Mode",
													 "source":        "usemode",
													 "fieldtype":     "usemode",
													 "subtype":       "usemode"
												 },
                         {
                           "description":   "Created",
                           "source":        "created",
                           "fieldtype":     "dateio",
                           "subtype":       "outputdate"
                         },
                         {
                           "description":   "Last Modified",
                           "source":        "lastModified",
                           "fieldtype":     "dateio",
                           "subtype":       "outputdate"
                         },
                         {
                           "description":   "CSS Selector",
                           "source":        "cssselector",
                           "fieldtype":     "cssinfo",
                           "subtype":       "cssselector"
                         },
                         {
                           "description":   "XPath Information",
                           "source":        "xpath",
                           "fieldtype":     "xpathinfo",
                           "subtype":       "xpath"
                         },
                         {
                           "description":   "Find Information",
                           "source":        "find",
                           "fieldtype":     "findinfo",
                           "subtype":       "find"
                         },
                         {
                           "description":   "Node Identifier",
                           "source":        "nodeiden",
                           "fieldtype":     "nodeiden",
                           "subtype":       "nodeiden"
                         },
                         {
                           "description":   "Modification Enabled",
                           "source":        "enabled",
                           "fieldtype":     "checkbox",
                           "subtype":       "checkbox"
                         },
                         {
                           "description":   "Parameter Number",
                           "source":        "parameter",
                           "fieldtype":     "ionumber",
                           "subtype":       "parameter"
                         },
                         {
                           "description":   "Modification Type",
                           "source":        "type",
                           "fieldtype":     "typelist",
                           "subtype":       "editableruletypelist"
                         },
                         {
                           "description":   "New Style Information",
                           "source":        "styles",
                           "fieldtype":     "textlist",
                           "subtype":       "style",
                           "datatype":      "array"
                         }
                       ]
                     },
    "text":          { "fields":
                       [
                         {
                           "description":   "Modification Name",
                           "source":        "name",
                           "fieldtype":     "iotext",
                           "subtype":       "modificationname"
                         },
                         {
                           "description":   "Modification Path Value",
                           "source":        "pathvalue",
                           "fieldtype":     "pathvalue",
                           "subtype":       "Path Value"
                         },
                         {
                           "description":   "Comments",
                           "source":        "comments",
                           "fieldtype":     "comminfo",
                           "subtype":       "comments"
                         },
                         {
                           "description":   "Extra Information",
                           "source":        "extra",
                           "fieldtype":     "extrainfo",
                           "subtype":       "extra"
                         },
                         {
													 "description":   "Probabiltiy",
													 "source":        "probability",
													 "fieldtype":     "float",
													 "subtype":       "probability"
												 },
                         {
													 "description":   "Use Mode",
													 "source":        "usemode",
													 "fieldtype":     "usemode",
													 "subtype":       "usemode"
												 },
                         {
                           "description":   "Created",
                           "source":        "created",
                           "fieldtype":     "dateio",
                           "subtype":       "outputdate"
                         },
                         {
                           "description":   "Last Modified",
                           "source":        "lastModified",
                           "fieldtype":     "dateio",
                           "subtype":       "outputdate"
                         },
                         {
                           "description":   "CSS Selector",
                           "source":        "cssselector",
                           "fieldtype":     "cssinfo",
                           "subtype":       "cssselector"
                         },
                         {
                           "description":   "XPath Information",
                           "source":        "xpath",
                           "fieldtype":     "xpathinfo",
                           "subtype":       "xpath"
                         },
                         {
                           "description":   "Find Information",
                           "source":        "find",
                           "fieldtype":     "findinfo",
                           "subtype":       "find"
                         },
                         {
                           "description":   "Node Identifier",
                           "source":        "nodeiden",
                           "fieldtype":     "nodeiden",
                           "subtype":       "nodeiden"
                         },
                         {
                           "description":   "Modification Enabled",
                           "source":        "enabled",
                           "fieldtype":     "checkbox",
                           "subtype":       "checkbox"
                         },
                         {
                           "description":   "Parameter Number",
                           "source":        "parameter",
                           "fieldtype":     "ionumber",
                           "subtype":       "parameter"
                         },
                         {
                           "description":   "Modification Type",
                           "source":        "type",
                           "fieldtype":     "typelist",
                           "subtype":       "editableruletypelist"
                         },
                         {
                           "description":   "New Texts",
                           "source":        "newtexts",
                           "fieldtype":     "textlist",
                           "subtype":       "text",
                           "datatype":      "array"
                         }
                       ]
                     },
    "textchecked":   { "fields":
                       [
                         {
                           "description":   "Modification Name",
                           "source":        "name",
                           "fieldtype":     "iotext",
                           "subtype":       "modificationname"
                         },
                         {
                           "description":   "Modification Path Value",
                           "source":        "pathvalue",
                           "fieldtype":     "pathvalue",
                           "subtype":       "Path Value"
                         },
                         {
                           "description":   "Comments",
                           "source":        "comments",
                           "fieldtype":     "comminfo",
                           "subtype":       "comments"
                         },
                         {
                           "description":   "Extra Information",
                           "source":        "extra",
                           "fieldtype":     "extrainfo",
                           "subtype":       "extra"
                         },
                         {
													 "description":   "Probabiltiy",
													 "source":        "probability",
													 "fieldtype":     "float",
													 "subtype":       "probability"
												 },
                         {
													 "description":   "Use Mode",
													 "source":        "usemode",
													 "fieldtype":     "usemode",
													 "subtype":       "usemode"
												 },
                         {
                           "description":   "Created",
                           "source":        "created",
                           "fieldtype":     "dateio",
                           "subtype":       "outputdate"
                         },
                         {
                           "description":   "Last Modified",
                           "source":        "lastModified",
                           "fieldtype":     "dateio",
                           "subtype":       "outputdate"
                         },
                         {
                           "description":   "CSS Selector",
                           "source":        "cssselector",
                           "fieldtype":     "cssinfo",
                           "subtype":       "cssselector"
                         },
                         {
                           "description":   "XPath Information",
                           "source":        "xpath",
                           "fieldtype":     "xpathinfo",
                           "subtype":       "xpath"
                         },
                         {
                           "description":   "Find Information",
                           "source":        "find",
                           "fieldtype":     "findinfo",
                           "subtype":       "find"
                         },
                         {
                           "description":   "Node Identifier",
                           "source":        "nodeiden",
                           "fieldtype":     "nodeiden",
                           "subtype":       "nodeiden"
                         },
                         {
                           "description":   "Modification Enabled",
                           "source":        "enabled",
                           "fieldtype":     "checkbox",
                           "subtype":       "checkbox"
                         },
                         {
                           "description":   "Parameter Number",
                           "source":        "parameter",
                           "fieldtype":     "ionumber",
                           "subtype":       "parameter"
                         },
                         {
                           "description":   "Modification Type",
                           "source":        "type",
                           "fieldtype":     "typelist",
                           "subtype":       "editableruletypelist"
                         },
                         {
                           "description":   "New Texts",
                           "source":        "newtexts",
                           "fieldtype":     "textlist",
                           "subtype":       "textchecked",
                           "datatype":      "array"
                         }
                       ]
                     },
    "title":         { "fields":
                       [
                         {
                           "description":   "Modification Name",
                           "source":        "name",
                           "fieldtype":     "iotext",
                           "subtype":       "modificationname"
                         },
                         {
                           "description":   "Modification Path Value",
                           "source":        "pathvalue",
                           "fieldtype":     "pathvalue",
                           "subtype":       "Path Value"
                         },
                         {
                           "description":   "Comments",
                           "source":        "comments",
                           "fieldtype":     "comminfo",
                           "subtype":       "comments"
                         },
                         {
                           "description":   "Extra Information",
                           "source":        "extra",
                           "fieldtype":     "extrainfo",
                           "subtype":       "extra"
                         },
                         {
													 "description":   "Probabiltiy",
													 "source":        "probability",
													 "fieldtype":     "float",
													 "subtype":       "probability"
												 },
                         {
													 "description":   "Use Mode",
													 "source":        "usemode",
													 "fieldtype":     "usemode",
													 "subtype":       "usemode"
												 },
                         {
                           "description":   "Created",
                           "source":        "created",
                           "fieldtype":     "dateio",
                           "subtype":       "outputdate"
                         },
                         {
                           "description":   "Last Modified",
                           "source":        "lastModified",
                           "fieldtype":     "dateio",
                           "subtype":       "outputdate"
                         },
                         {
                           "description":   "CSS Selector",
                           "source":        "cssselector",
                           "fieldtype":     "cssinfo",
                           "subtype":       "cssselector"
                         },
                         {
                           "description":   "XPath Information",
                           "source":        "xpath",
                           "fieldtype":     "xpathinfo",
                           "subtype":       "xpath"
                         },
                         {
                           "description":   "Find Information",
                           "source":        "find",
                           "fieldtype":     "findinfo",
                           "subtype":       "find"
                         },
                         {
                           "description":   "Node Identifier",
                           "source":        "nodeiden",
                           "fieldtype":     "nodeiden",
                           "subtype":       "nodeiden"
                         },
                         {
                           "description":   "Modification Enabled",
                           "source":        "enabled",
                           "fieldtype":     "checkbox",
                           "subtype":       "checkbox"
                         },
                         {
                           "description":   "Parameter Number",
                           "source":        "parameter",
                           "fieldtype":     "ionumber",
                           "subtype":       "parameter"
                         },
                         {
                           "description":   "Modification Type",
                           "source":        "type",
                           "fieldtype":     "typelist",
                           "subtype":       "editableruletypelist"
                         },
                         {
                           "description":   "New Titles",
                           "source":        "titles",
                           "fieldtype":     "textlist",
                           "subtype":       "title",
                           "datatype":      "array"
                         }
                       ]
                     },
    "value":         { "fields":
                       [
                         {
                           "description":   "Data Value Name",
                           "source":        "name",
                           "fieldtype":     "iotext",
                           "subtype":       "datavaluename"
                         },
                         {
                           "description":   "Comments",
                           "source":        "comments",
                           "fieldtype":     "comminfo",
                           "subtype":       "comments"
                         },
                         {
                           "description":   "Data value",
                           "source":        "value",
                           "fieldtype":     "iotext",
                           "subtype":       "datavalue"
                         }
                       ]
                     },
    "visit":         { "fields":
                       [
                         {
                           "description":   "Modification Name",
                           "source":        "name",
                           "fieldtype":     "iotext",
                           "subtype":       "modificationname"
                         },
                         {
                           "description":   "Modification Path Value",
                           "source":        "pathvalue",
                           "fieldtype":     "pathvalue",
                           "subtype":       "Path Value"
                         },
                         {
                           "description":   "Comments",
                           "source":        "comments",
                           "fieldtype":     "comminfo",
                           "subtype":       "comments"
                         },
                         {
                           "description":   "Extra Information",
                           "source":        "extra",
                           "fieldtype":     "extrainfo",
                           "subtype":       "extra"
                         },
                         {
													 "description":   "Probabiltiy",
													 "source":        "probability",
													 "fieldtype":     "float",
													 "subtype":       "probability"
												 },
                         {
													 "description":   "Use Mode",
													 "source":        "usemode",
													 "fieldtype":     "usemode",
													 "subtype":       "usemode"
												 },
                         {
                           "description":   "Created",
                           "source":        "created",
                           "fieldtype":     "dateio",
                           "subtype":       "outputdate"
                         },
                         {
                           "description":   "Last Modified",
                           "source":        "lastModified",
                           "fieldtype":     "dateio",
                           "subtype":       "outputdate"
                         },
                         {
                           "description":   "CSS Selector",
                           "source":        "cssselector",
                           "fieldtype":     "cssinfo",
                           "subtype":       "cssselector"
                         },
                         {
                           "description":   "XPath Information",
                           "source":        "xpath",
                           "fieldtype":     "xpathinfo",
                           "subtype":       "xpath"
                         },
                         {
                           "description":   "Find Information",
                           "source":        "find",
                           "fieldtype":     "findinfo",
                           "subtype":       "find"
                         },
                         {
                           "description":   "Node Identifier",
                           "source":        "nodeiden",
                           "fieldtype":     "nodeiden",
                           "subtype":       "nodeiden"
                         },
                         {
                           "description":   "Modification Enabled",
                           "source":        "enabled",
                           "fieldtype":     "checkbox",
                           "subtype":       "checkbox"
                         },
                         {
                           "description":   "Parameter Number",
                           "source":        "parameter",
                           "fieldtype":     "ionumber",
                           "subtype":       "parameter"
                         },
                         {
                           "description":   "Modification Type",
                           "source":        "type",
                           "fieldtype":     "typelist",
                           "subtype":       "editableruletypelist"
                         },
                         {
                           "description":   "New Visit Values",
                           "source":        "visitvalues",
                           "fieldtype":     "textlist",
                           "subtype":       "visit",
                           "datatype":      "array"
                         }
                       ]
                     },
    "width":         { "fields":
                       [
                         {
                           "description":   "Modification Name",
                           "source":        "name",
                           "fieldtype":     "iotext",
                           "subtype":       "modificationname"
                         },
                         {
                           "description":   "Modification Path Value",
                           "source":        "pathvalue",
                           "fieldtype":     "pathvalue",
                           "subtype":       "Path Value"
                         },
                         {
                           "description":   "Comments",
                           "source":        "comments",
                           "fieldtype":     "comminfo",
                           "subtype":       "comments"
                         },
                         {
                           "description":   "Extra Information",
                           "source":        "extra",
                           "fieldtype":     "extrainfo",
                           "subtype":       "extra"
                         },
                         {
													 "description":   "Probabiltiy",
													 "source":        "probability",
													 "fieldtype":     "float",
													 "subtype":       "probability"
												 },
                         {
													 "description":   "Use Mode",
													 "source":        "usemode",
													 "fieldtype":     "usemode",
													 "subtype":       "usemode"
												 },
                         {
                           "description":   "Created",
                           "source":        "created",
                           "fieldtype":     "dateio",
                           "subtype":       "outputdate"
                         },
                         {
                           "description":   "Last Modified",
                           "source":        "lastModified",
                           "fieldtype":     "dateio",
                           "subtype":       "outputdate"
                         },
                         {
                           "description":   "CSS Selector",
                           "source":        "cssselector",
                           "fieldtype":     "cssinfo",
                           "subtype":       "cssselector"
                         },
                         {
                           "description":   "XPath Information",
                           "source":        "xpath",
                           "fieldtype":     "xpathinfo",
                           "subtype":       "xpath"
                         },
                         {
                           "description":   "Find Information",
                           "source":        "find",
                           "fieldtype":     "findinfo",
                           "subtype":       "find"
                         },
                         {
                           "description":   "Node Identifier",
                           "source":        "nodeiden",
                           "fieldtype":     "nodeiden",
                           "subtype":       "nodeiden"
                         },
                         {
                           "description":   "Modification Enabled",
                           "source":        "enabled",
                           "fieldtype":     "checkbox",
                           "subtype":       "checkbox"
                         },
                         {
                           "description":   "Parameter Number",
                           "source":        "parameter",
                           "fieldtype":     "ionumber",
                           "subtype":       "parameter"
                         },
                         {
                           "description":   "Modification Type",
                           "source":        "type",
                           "fieldtype":     "typelist",
                           "subtype":       "editableruletypelist"
                         },
                         {
                           "description":   "New Widths",
                           "source":        "widths",
                           "fieldtype":     "textlist",
                           "subtype":       "width",
                           "datatype":      "array"
                         }
                       ]
                     }
  }
# The next JSON object contains some name information about
# each type of tree node. Note that we have ten entries for
# company nodes. However, only one of these entry has a key of 
# 'company'. Instead, more specific keys are used. The actual 
# keys are 'compmod' for company nodes used for modifications 
# and 'compproxy' for company nodes used proxy definitions.
# Of course, 'compstore' is used for company node use for 
# store information. Of course, 'compignore' is used for 
# company node use for ignore (ignore-lists) information. 
HDLmModTreeInfo = {
  "auth": {
    "longname":    "authorization",
    "ucfirstname": "Authorization",
    "tooltip":     "Authorization node"
  },
  "companies": {
    "longname":    "companies",
    "ucfirstname": "Companies",
    "tooltip":     "Companies node"
  },
  "company": {
    "longname":    "company",
    "ucfirstname": "Company",
    "tooltip":     "Company node"
  },
  "compdata": {
    "longname":    "company",
    "ucfirstname": "Company",
    "tooltip":     "Company node"
  },
  "compgem": {
    "longname":    "company",
    "ucfirstname": "Company",
    "tooltip":     "Company node"
  },
  "compgxe": {
    "longname":    "company",
    "ucfirstname": "Company",
    "tooltip":     "Company node"
  },
  "compignore": {
    "longname":    "company",
    "ucfirstname": "Company",
    "tooltip":     "Company node"
  },
  "compmod": {
    "longname":    "company",
    "ucfirstname": "Company",
    "tooltip":     "Company node"
  },
  "comppass": {
    "longname":    "company",
    "ucfirstname": "Company",
    "tooltip":     "Company node"
  },
  "comppopup": {
    "longname":    "company",
    "ucfirstname": "Company",
    "tooltip":     "Company node"
  },
  "compproxy": {
    "longname":    "company",
    "ucfirstname": "Company",
    "tooltip":     "Company node"
  },
  "compsimple": {
    "longname":    "company",
    "ucfirstname": "Company",
    "tooltip":     "Company node"
  },
  "compstore": {
    "longname":    "company",
    "ucfirstname": "Company",
    "tooltip":     "Company node"
  },
  "compvalue": {
    "longname":    "company",
    "ucfirstname": "Company",
    "tooltip":     "Company node"
  },
  "config": {
    "longname":    "configuration",
    "ucfirstname": "Configuration",
    "tooltip":     "Configuration node"
  },
  "data": {
    "longname":    "data",
    "ucfirstname": "Data",
    "tooltip":     "Data node"
  },
  "division": {
    "longname":    "division",
    "ucfirstname": "Division",
    "tooltip":     "Division node"
  },
  "ignore": {
    "longname":    "ignore",
    "ucfirstname": "Ignore",
    "tooltip":     "Ignore-list entry node"
  },
  "line": {
    "longname":    "line",
    "ucfirstname": "Line",
    "tooltip":     "Report-line node"
  },
  "lines": {
    "longname":    "lines",
    "ucfirstname": "Lines",
    "tooltip":     "Report-lines node"
  },
  "list": {
    "longname":    "list",
    "ucfirstname": "List",
    "tooltip":     "Ignore-list node"
  },
  "lists": {
    "longname":    "lists",
    "ucfirstname": "Lists",
    "tooltip":     "Ignore-lists node"
  },
  "mod": {
    "longname":    "modification",
    "ucfirstname": "Modification",
    "tooltip":     "Modification node"
  },
  "report": {
    "longname":    "report",
    "ucfirstname": "Report",
    "tooltip":     "Report node"
  },
  "reports": {
    "longname":    "reports",
    "ucfirstname": "Reports",
    "tooltip":     "Reports node"
  },
  "rules": {
    "longname":    "rules",
    "ucfirstname": "Rules",
    "tooltip":     "Rules node"
  },
  "site": {
    "longname":    "site",
    "ucfirstname": "Site",
    "tooltip":     "Site node"
  },
  "store": {
    "longname":    "store",
    "ucfirstname": "Store",
    "tooltip":     "Stored value node"
  },
  "top": {
    "longname":    "top",
    "ucfirstname": "Top",
    "tooltip":     "Top node of the node tree"
  },
  "value": {
    "longname":    "value",
    "ucfirstname": "Value",
    "tooltip":     "Value node"
  },
}
# The next JSON object contains some name information about
# each type of modification. The extra used field shows if
# a modification type uses extra information. It does not
# show if extra information is required by this modification
# type in all cases. 
HDLmModTypeInfo = {
    "attribute":    { "type": "none",  "extraused": True,  "extrarequired": True,  "parmnumberused": False, "longname": "attribute" },
    "changeattrs":  { "type": "none",  "extraused": False, "extrarequired": False, "parmnumberused": True,  "longname": "change attributes" },
    "changenodes":  { "type": "none",  "extraused": False, "extrarequired": False, "parmnumberused": True,  "longname": "change nodes" },
    "extract":      { "type": "none",  "extraused": True,  "extrarequired": False, "parmnumberused": False, "longname": "extract" },
    "fontcolor":    { "type": "none",  "extraused": False, "extrarequired": False, "parmnumberused": True,  "longname": "font color" },
    "fontfamily":   { "type": "none",  "extraused": False, "extrarequired": False, "parmnumberused": True,  "longname": "font family" },
    "fontkerning":  { "type": "none",  "extraused": False, "extrarequired": False, "parmnumberused": True,  "longname": "font kerning" },
    "fontsize":     { "type": "none",  "extraused": False, "extrarequired": False, "parmnumberused": True,  "longname": "font size" },
    "fontstyle":    { "type": "none",  "extraused": False, "extrarequired": False, "parmnumberused": True,  "longname": "font style" },
    "fontweight":   { "type": "none",  "extraused": False, "extrarequired": False, "parmnumberused": True,  "longname": "font weight" },
    "height":       { "type": "none",  "extraused": False, "extrarequired": False, "parmnumberused": True,  "longname": "height" },
    "image":        { "type": "none",  "extraused": False, "extrarequired": False, "parmnumberused": True,  "longname": "image" },
    "modify":       { "type": "none",  "extraused": True,  "extrarequired": True,  "parmnumberused": False, "longname": "modify" },
    "notify":       { "type": "none",  "extraused": True,  "extrarequired": False, "parmnumberused": False, "longname": "notify" },
    "order":        { "type": "none",  "extraused": False, "extrarequired": False, "parmnumberused": True,  "longname": "order" },
    "remove":       { "type": "none",  "extraused": False, "extrarequired": False, "parmnumberused": True,  "longname": "remove" },
    "replace":      { "type": "none",  "extraused": False, "extrarequired": False, "parmnumberused": True,  "longname": "replace" },
    "script":       { "type": "none",  "extraused": False, "extrarequired": False, "parmnumberused": True,  "longname": "script" },
    "style":        { "type": "none",  "extraused": True,  "extrarequired": True,  "parmnumberused": True,  "longname": "style" },
    "text":         { "type": "none",  "extraused": False, "extrarequired": False, "parmnumberused": True,  "longname": "text" },
    "textchecked":  { "type": "none",  "extraused": True,  "extrarequired": True,  "parmnumberused": True,  "longname": "checked text" },
    "title":        { "type": "none",  "extraused": False, "extrarequired": False, "parmnumberused": True,  "longname": "title" },
    "visit":        { "type": "none",  "extraused": True,  "extrarequired": False, "parmnumberused": True,  "longname": "visit" },
    "width":        { "type": "none",  "extraused": False, "extrarequired": False, "parmnumberused": True,  "longname": "width" }
}

class HDLmMod(object):
  # print('In class HDLmMod')
  # print(type(HDLmMod))
  # The __init__ method creates an instance of the class
  def __init__(self, nameStr, extraStr, enabledValue, modType):
    # Each tree node nas a set of fields
    self.find = None
    # The following field is not really used in the Python
    # environment
    # self.values = None
    self.enabled = enabledValue
	  # The next field is used to save the number of errors that
	  # were found building the current modification. If this value
	  # is greater than zero, then the modification can not be used.
	  # Note that the enabled field is not generally changed even
	  # when the error count is greater than zero. The exception
	  # is that a copy of the enabled field is changed when a copy
	  # of the current modification is built. This idea does not 
    # really apply to Python.  
    # 
    # self.errorCount = 0
    # We assume that the path value is not a regex. However, if the path value 
	  # actually is a regex, the regex flag below is set to True. Note that most 
	  # of the work of actually matching path values is done with the match object. 
	  # The field below is used more for communication with JavaScript. 
    self.pathre = False
    self.type = modType  
    # The following field is not really used in the Python
    # environment
    # self.valuesCount = 0
    # Parameter number is handled as a reference so that it can be set to a None
	  # value. If the value is actually set, it must be a positive or zero integer
	  # (zero is allowed).
    self.parameter = None	 
    self.cssselector = None
    self.comments = None
    self.extra = extraStr
    self.name = nameStr
    self.nodeiden = None 
	  # We assume that the path value is not a regex. However, if the path value 
	  # actually is a regex, the regex flag above is set to True. Note that most
	  # of the work of actually matching path values is done with the match object.
	  # The field below is used more for communication with JavaScript. 
    self.pathvalue = None
    # The following field is not really used in the Python
    # environment
    # self.value = None
    # The following field is not really used in the Python
    # environment
    # self.valueSuffix = None 
    self.xpath = None
	  # A reference to the path value match object is stored below. The path 
	  # value match object has methods that handle all types of matching. The
	  # match object may specify a simple string comparison, a regex match, 
	  # a glob match, or a like (SQL LIKE) match. 
    self.pathmatch = None	
  # Build an HTML modification object from the values passed by the
  # caller 
  @staticmethod
  def buildModificationObject(nameStr, pathString, extraStr, enabledValue,
                              cssStr, xpathStr, finds, nodeIdenObj, 
                              modType, parameterNumber):
    # Construct the new modification 
    # print(extraStr) 
    newModification = HDLmMod(nameStr, extraStr, enabledValue, modType)
    # print(newModification) 
    # Add a few additional fields 
    newModification.pathvalue = pathString
    newModification.comments = ''
    newModification.cssselector = cssStr
    newModification.xpath = xpathStr
    newModification.find = finds
    newModification.nodeiden = nodeIdenObj
    newModification.parameter = parameterNumber
    return newModification 
  # Convert a dictionary to an instance of the HDLmMod class. 
  # The new instance is returned to the caller. Specific fields
  # are copied from the dictionary to the new HDLmMod instance. 
  @staticmethod
  def convertDictToMod(infoJsonDict):
    # Change the name of one field 
    if 'path' in infoJsonDict: 
      infoJsonDict['pathValue'] = infoJsonDict['path']
      del infoJsonDict['path'] 
    # Finish building the details   
    curModInstance = HDLmMod(None, None, False, None) 
    # Copy all of the fields from the dictionary to the HDLmMod instance 
    # keyCounter = 0
    for key in infoJsonDict:
      # if hasattr(curModInstance, key) == False:
      #   keyCounter += 1
      #   print(keyCounter )
      #   print(key)
      # if key == 'nodeiden':
      #   print(keyCounter)
      setattr(curModInstance, key, infoJsonDict[key]) 
    return curModInstance
  # Get some information about a type of HTML modification. 
  # The caller passes HTML modification type. This routine
  # returns a set of information about the type. If the type
  # is unknown, than a NULL value is returned to the caller. 
  @staticmethod
  def getModificationTypeInfo(typeStr):
    # Check if information for type specified by the caller exists 
    if typeStr in HDLmModTypeInfo:
      return HDLmModTypeInfo[typeStr]
    return None
  # This method returns a boolean showing if a modification type
  # uses (requires) a parameter number or not. Most types of rules
  # require parameter numbers. However, some do not. This method
  # takes a modification type string and returns a boolean showing
  # if a parameter number is needed or not. If the type is unknown,
  # than a None value is returned to the caller. 
  @staticmethod 
  def getModificationTypeParmNumberUsed(typeStr):
    # Check if information for type specified by the caller exists 
    if typeStr in HDLmModTypeInfo: 
      return HDLmModTypeInfo[typeStr]['parmnumberused']
    return None
  # This routine is used to access the modification type information 
  # from other source modules 
  @staticmethod 
  def getModTypeInfo():
    return HDLmModInfoData
  # This routine is invoked when an update happens and the update
  # should be sent to the rules server. Of course, other actions
  # may be needed as well. Note that this routine is highly
  # unconditional. This routine does not check for errors in
  # anything. 
  def handleUpdateReloadPageUnconditional(callFromCallback):
    # print('HDLmMod.handleUpdateReloadPageUnconditional')   
    # print('HDLmMod.handleUpdateReloadPageUnconditional', HDLmGlobals.checkForInlineEditor()) 
    # print('HDLmMod.handleUpdateReloadPageUnconditional', HDLmGlobals.checkActiveExtensionWindow()) 
    # print('HDLmMod.handleUpdateReloadPageUnconditional', HDLmGlobals.activeEditorType) 
    # print('HDLmGlobals.checkActiveExtensionWindow()') 
    # We really only want to reload the current window if one 
    # of the inline editors is active and we are running in a
    # browser extension window. Note that the current window is 
    # the current content window, not the browser extension. 
    if HDLmGlobals.activeEditorType != HDLmEditorTypes.gem and \
       HDLmGlobals.activeEditorType != HDLmEditorTypes.gxe:
      if HDLmGlobals.checkForInlineEditor() == False or \
         HDLmGlobals.checkActiveExtensionWindow() == False:
        return 
    # print('HDLmMod.handleUpdateReloadPageUnconditional') 
    # We can now try to reload the current content window. 
    # Of course, this will not happen in many environments. 
    if HDLmGlobals.activeEditorType != HDLmEditorTypes.gem and \
       HDLmGlobals.activeEditorType != HDLmEditorTypes.gxe: 
      # The following code should never be executed in the Python 
      # environment. Report an error, if this code is ever reached.
      errorText = 'This code should neve be executed. HDLmPopup has not been ported.'
      HDLmAssert(False, errorText)
      # HDLmPopup.reloadCurrentWindow() 
  # The class method below build an empty instance of this class
  @classmethod 
  def makeEmptyMod(cls):
    emptyMod = cls.__new__(cls) 
    return emptyMod
  # This routine removes all of modification information. This
  # routine removes the DOM elements used to display the data.
  # Note that a lower level routine is used to remove the actual
  # DOM elements. 
  def removeEntries():
    # console.trace() 
    # Remove the new tree node information from the web page 
    divDescriptions = HDLmDefines.getString('HDLMENTRYDESCRIPTIONS')
    divValues = HDLmDefines.getString('HDLMENTRYVALUES')
    HDLmMod.removeMod(divDescriptions)
    HDLmMod.removeMod(divValues) 
  # This routine removes a set of modfication information. This
  # routine removes the DOM elements used to display the data. 
  def removeMod(parentId):
    # We don't have any entries to remove in the Python environment
    #
    # $(parentId).empty() 
    pass