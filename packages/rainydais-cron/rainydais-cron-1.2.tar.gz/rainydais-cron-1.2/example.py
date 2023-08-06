# Import the cron library by RainyDais
import cron

# Initialize cron job library, true to debug, false for silent execution
cron.initialize(True)

# Define a function that says "Hello World!"
def example_function():
  print("Hello World!")
  
# Define a function that says it runs after every x seconds
def time_alert_function(seconds):
  print("I run every {0} seconds!".format(seconds))
  
# Add first example function to run every 5 seconds
cron.addJob(example_function, 5)

# Add second example function to run every 1 second
cron.addJob(time_alert_function, 1, 1)
# The addJob parameters are; function, timeout/cron delay, args (only 1 supported currently)

# When you're ready to run your cron jobs call this function
# Optionally pass 'True' into the function call to make it non-thread blocking,
# Like this: cron.start(True), Default is False or thread blocking.
cron.start()
# It will start the timer to execute your cron jobs

# This will prevent the program from ending if on non-thread blocking mode,
# it will also act as a test to prove cron.start() isn't blocking the thread
input("\n   Hello, this is the end of the file!\n\n")
# It contains newline characters so it doesn't get put on the same line as
# other print messages that will come in from the threaded cron jobs.
