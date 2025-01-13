from   HDLmConfig     import *
from   HDLmConfigInfo import *
from   typing         import Dict
import openai 
import time

glbApiKey = ''

# Generate some text choices
def generate(apiKey, context, goal, temperature=0.9):
  openai.api_key = apiKey
  try:
    response: Dict = openai.ChatCompletion.create(
      model = "gpt-4o",
      max_tokens = 2048,
      temperature = 0.9,
      messages = [
        {"role": "system", "content": context},
        {"role": "user", "content": goal}
                 ]
    )
    print(14)
    # for fn in response:
    #   print()
    #   print(fn)
    #   print(response[fn])
    # print(response)
    if "choices" in response and len(response["choices"]) == 1:
      answer = response["choices"][0]["message"]["content"]
    else:
      answer = "I don't know"
  except Exception as e:
    answer = f"*** An exception occured: {e}"
  print(answer) 
  return  

# Main program
def main():  
  # Collect a few time values for determining how long this takes
  cpuTimeStart = time.process_time()
  wallTimeStart = time.time()  
  # Get the Open AI key
  global glbApiKey
  glbApiKey = HDLmConfigInfo.getOpenAIApiKey()  
  # Generate some choices
  context = "You are a web designer. You have a website where tickets are sold for concerts." + \
            " You want to create text that is modern and doesn't sound like marketing speak, " + \
            "yet encourages action. Your answers are always in JSON form, " + \
            "such as [\"Text 1\", \"Text 2\", \"Text 3\", \"Text 4\", " +\
            "\"Text 5\", \"Text 6\", \"Text 7\", \"Text 8\", \"Text 9\", \"Text 10\"]"
  goal = "Generate variations for a 'Buy now' button"  
  generate(glbApiKey, context, goal, temperature=0.9)
  # Collect some ending time values 
  cpuTimeEnd = time.process_time()
  wallTimeEnd = time.time()
  # Show how long this took
  print('CPU    ', cpuTimeEnd - cpuTimeStart)
  print('Elapsed', wallTimeEnd - wallTimeStart)

# Actual starting point
if __name__ == '__main__':
  main()