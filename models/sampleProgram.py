import time
import sys

sleepTime = 5
print("Sleeping for", sleepTime, "seconds.")
time.sleep(sleepTime)
print("Slept for", sleepTime, "seconds.")
try:
    input_arg = [sys.argv[1]]
    print ("Argument:", input_arg)
except Exception as e:
    print ("Exception:", e, end=" -- ")
    print ("No arguments provided")