# Start a set of tests class. Note that no instances of this class
# are ever created (actually I don't know how Python unit testing
# works).

from   deepdiff     import DeepDiff
from   HDLmNodeIden import *
import unittest
import jsons
import time

# Handle startup 
def startup():   
  pass

class Test_HDLmTest8():
  # Run a set of innerText tests 
  @staticmethod
  def test_runInnerTextTests():
    # The array below contains all of the innerText tests. For each test, we have an
    # input string (some HTML),  an output string (the return value converted to JSON), 
    # and an error message string 
    innerTextTests = [        
                       # test 1
                       [ """
                         <p id="demo"> This element has extra       spacing and contains 
                         <span>a span element</span>.</p>
                         """,
                         'demo',
                         'This element has extra spacing and contains a span element.',
                       ],
                       # test 2
                       [ '<div id="mydiv">foo <span>bar</span> baz</div>',
                         'mydiv',
                         'foo bar baz',
                       ], 
                       # test 3
                       [ """
                         <p id="p1">
                         This is an <small>example</small> of<strong> innerText </strong>
                         </p>
                         """,
                         'p1',
                         'This is an example of innerText',
                       ],  
                       # test 4
                       [ """
                         <button id="geeks">
                             Submit
                         </button>
                         """,
                         'geeks',
                         'Submit',
                       ],  
                       # test 5
                       [ """
                         <div id='textcontent'>Welcome to <strong> Educative Answers ! </strong></div>
                         """,
                         'textcontent',
                         'Welcome to Educative Answers !',
                       ],   
                       # test 6
                       [ """
                         <div id="mylinks">
                           This is my <b>link collection</b>:
                           <ul>
                             <li><a href="www.borland.com">Bye bye <b>Borland</b> </a></li>
                             <li><a href="www.microfocus.com">Welcome to <b>Micro Focus</b></a></li>
                           </ul>
                         </div>
                         """,
                         'mylinks',
                         'This is my link collection:\nBye bye Borland\nWelcome to Micro Focus',
                       ],      
                       # test 7  
                       [ """
                         <p id="demo"> This element has extra       spacing and contains 
                         <span>a span element</span>.</p>
                         """,
                         'demo',
                         'This element has extra spacing and contains a span element.',
                       ],
                       # test 8
                       [ """
                         <p id="demo">
                             some paragraph text
                             <style>
                               p {
                                 color: red;
                               }
                             </style>
                         </p>
                         """,
                         'demo',
                         'some paragraph text',
                       ],
                       # test 9
                       [ '<button id="myBtn">Try it</button>',
                         'myBtn',
                         'Try it',
                       ],    
                       # test 10
                       [ '<button id="myBtn"> Try it </button>',
                         'myBtn',
                         'Try it',
                       ],      
                       # test 11      
                       [ '<html><body><div id="mydiv">Hello, <b>world!</b></div></body></html>',
                         'mydiv',
                         'Hello, world!',
                       ],  
                       # test 12
                       [ '<div id="mydiv">foo <span>bar</span> baz</div>',
                         'mydiv',
                         'foo bar baz',
                       ],    
                       # test 13
                       [ """
                         <p id="source">
                           <style>
                             #source {
                               color: red;
                             }
                             #text {
                               text-transform: uppercase;
                             }
                           </style>
                           <span id="text">
                             Take a look at<br />
                             how this text<br />
                             is interpreted below.
                           </span>
                           <span style="display:none">HIDDEN TEXT</span>
                         </p>
                         """,
                         'source',
                         'Take a look at\nhow this text\nis interpreted below.',
                       ],
                       # test 14
                       [ """
                         <p id="source">xyz
                           <style>
                             #source {
                               color: red;
                             }
                             #text {
                               text-transform: uppercase;
                             }
                           </style>
                           <span id="text">
                             Take a look at<br />
                             how this text<br />
                             is interpreted below.
                           </span>
                           <span style="display:none">HIDDEN TEXT</span>
                         </p>
                         """,
                         'source',
                         'xyz Take a look at\nhow this text\nis interpreted below.',
                       ],
                       # test 15        
                       [ '<div id="demo">Hello <b>World</b> <i>Some Text</i></div>',
                         'demo',
                         'Hello World Some Text',
                       ],   
                       # test 16        
                       [ '<div id="result">innerHTML =</div>',
                         'result',
                         'innerHTML =',
                       ],   
                       # test 17        
                       [ '<div id="result">innerText =</div>',
                         'result',
                         'innerText =',
                       ],   
                       # test 18        
                       [ '<button id="Btn">Click here</button>',
                         'Btn',
                         'Click here',
                       ],  
                       # test 19        
                       [ "<p id='example'>This is an <span> example </span>.</p>",
                         'example',
                         'This is an example .',
                       ],
                       # test 20 
                       [ """
                         <div id="t"><div>lions,
                         tigers</div><div style="visibility:hidden">and bears</div></div>
                         """,
                         't',
                         'lions, tigers',
                       ],
                       # test 21 
                       [ """
                         <div id='form1' runat="server">
                           <div>
                             <b><span id="Message" runat="server"> xyz </span></b>
                           </div>
                         </div>
                         """,
                         'form1',
                         'xyz',
                       ],
                       # test 22 
                       [ """
                         <a class="button" id='btn'href="#">ONLINE APPLY
                           <span id="Message" style="display: none">HERE</span> 
                         </a>
                         """,
                         'btn',
                         'ONLINE APPLY',
                       ],
                       # test 23 
                       [ """
                         <div id="myDiv">
                           This is a division element that contains some <span style="color: red">red text</span>.
                         </div>
                         """,
                         'myDiv',
                         'This is a division element that contains some red text.',
                       ],
                       # test 24        
                       [ "<label id='my_label'>The text string</label>",
                         'my_label',
                         'The text string',
                       ],
                       # test 25        
                       [ "<label id='my_label'>The text string <label>The text of descendant</label></label>",
                         'my_label',
                         'The text string The text of descendant',
                       ],
                       # test 26        
                       [ "<p id='sandwich'>I love a good tuna sandwich!</p>",
                         'sandwich',
                         'I love a good tuna sandwich!',
                       ],
                       # test 27        
                       [ "<p id='sandwich''>I love a good <strong>tuna</strong> sandwich!</p>",
                         'sandwich',
                         'I love a good tuna sandwich!',
                       ],
                       # test 28
                       [ """
                         <div id="greeting">
	                         <style type="text/css">
		                         p {
			                         color: rebeccapurple;
		                         }
	                         </style>
	                         <p hidden>This is not rendered.</p>
	                         <p>Hello world!</p>
                         </div>
                         """,
                         'greeting',
                         'Hello world!',
                       ],
                       # test 29
                       #
                       # This test has a bug. The text really should be in 
                       # uppercase. The style sheet makes the text uppercase.
                       # This means that the innerText should also be uppercase.
                       # In other words, we should get 'MODUS CREATE' (without
                       # the quotes), not 'Modus Create' (without the quotes).
                       [ """
	                       <style type="text/css">
		                       body {
			                       text-align: center;
		                         }
		                       span {
			                       line-height: 100vh;
			                       text-transform: uppercase;
		                       }
	                       </style>
                         <span id='greeting'>Modus Create</span>
                         """,
                         'greeting',
                         'Modus Create',
                       ],
                       # test 30                       
                       [ """
                         <div id='greeting'>   
                           This element is <strong>strong</strong> and     has some super fun <code>code</code>!
                         </div>
                         """,
                         'greeting',
                         'This element is strong and has some super fun code!',
                       ],
                     ]
    # Get the count of the number of tests and run each test 
    tests = innerTextTests    
    testCount = len(tests)
    for i in range(testCount): 
      # Get the current test
      curTest = tests[i]
      curTestLen = len(curTest)
      curInputHtml = curTest[0]
      curNodeId = curTest[1]
      curExpectedOutputStr = curTest[2]      
      # Try running the actual test. The test may throw an exception. If the
      # test does not throw an exception, it will produce output. We need to
      # check the output.
      try:
        # print(f'Test {i} {curInput} started') 
        soup = BeautifulSoup(curInputHtml, 'html.parser')
        curNodeElement = soup.find_all(id=curNodeId)[0] 
        # inner_text = nodeElement.string
        actualOutputStr = HDLmNodeIden.getInnerText(curNodeElement)
        diff = DeepDiff(actualOutputStr, curExpectedOutputStr, ignore_order=True)
        diffLen = len(diff)
        # Check if the actual dictionary matches the expected dictionary
        if diffLen > 0:
          testNumber = i + 1
          testMessage = f'Test {testNumber} failed - Invalid output' 
          print(testMessage)
      # The test threw an exception. The exception may have been expected. 
      except Exception as e:
        actualErrorMessage = str(e) 
        testNumber = i + 1
        testMessage = f'Test {testNumber} failed - {actualErrorMessage}' 
        print(testMessage)

# Main program
def main(): 
  # Collect a few time values for determining how long this takes
  cpuTimeStart = time.process_time()
  wallTimeStart = time.time()  
  # Start the current program  
  startup()  
  # Run the actual tests
  Test_HDLmTest8.test_runInnerTextTests()
  # Collect some ending time values 
  cpuTimeEnd = time.process_time()
  wallTimeEnd = time.time()
  # Show how long this took  
  print('CPU    ', cpuTimeEnd - cpuTimeStart)
  print('Elapsed', wallTimeEnd - wallTimeStart)  

# Actual starting point
if __name__ == '__main__':
  main()