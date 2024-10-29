import datetime
import time

glbmapping = {'A':0, 'B':1, 'C':2}

# Run a game
def runGame(firstPlayer, secondPlayer, totalGames, winningStreak):
  # Build the list of players
  players = [firstPlayer, secondPlayer]
  # Increment the total number of games
  firstNumber = glbmapping[firstPlayer]
  secondNumber = glbmapping[secondPlayer]
  totalGames[firstNumber] += 1
  totalGames[secondNumber] += 1
  # Check for a game between A and B
  if 'A' in players and 'B' in players:
    didNotPlay = 'C'
    winner = 'B'
  elif 'C' in players:
    # Find out who did not play
    if 'B' in players:
      # Check if C should win this game. Sometimes C loses.
      playerNumber = glbmapping['C']
      if winningStreak[playerNumber] >= 4:
        winner = 'B'
      else:
        winner = 'C'
      didNotPlay = 'A'
    else:
      winner = 'C'
      didNotPlay = 'B'
  else:
    raise RuntimeError('Logic did not work')
  # Raise the number of consecutive wins
  winnerNumber = glbmapping[winner]
  winningCount = winningStreak[winnerNumber] + 1
  for i in range(3):
    winningStreak[i] = 0
  winningStreak[winnerNumber] = winningCount
  return winner, didNotPlay

# Run a set of games
def runGameSet():
  totalGames = [0 for i in range(3)]   
  winningStreak = [0 for i in range(3)]   
  firstPlayer = 'C'
  secondPlayer = 'B'
  for i in range(17):
    winner, didNotPlay = runGame(firstPlayer, secondPlayer, totalGames, winningStreak)
    print(winner, firstPlayer, secondPlayer, didNotPlay)
    firstPlayer = winner
    secondPlayer = didNotPlay
  return

    
# Main program
def main():
  # Collect a few time values for determining how long this takes
  cpuTimeStart = time.process_time()
  wallTimeStart = time.time()
  printTimeStart = datetime.datetime.now()
  # Test code
  if 1 == 1:
    runGameSet()  
  # Collect some ending time values  
  cpuTimeEnd = time.process_time()
  wallTimeEnd = time.time()
  printTimeEnd = datetime.datetime.now()
  # Show how long this took
  print('CPU    ', cpuTimeEnd - cpuTimeStart)
  print('Elapsed', wallTimeEnd - wallTimeStart)

# Actual starting point
if __name__ == "__main__":
  main()
   