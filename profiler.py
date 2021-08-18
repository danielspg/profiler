
import psutil

print("############################################################")
print("#                     PROFILER STARTED                     #")
print("############################################################")

# mod counter for escape
mod_counter = 0

# coefficient and coeff-counter dict
coefficient = 50
coeff_counter = {}

mod_factor = coefficient / 2

# stores the frist processes stats
# pid:uss pair
first_processes_stats = {}
root_count = 0

# stores consecutive processes stats
# pid:uss pair
latest_processes_stats = {}
# pid:pname pair
processes_pid = {}

# entry/exit control lock
choice = 'go'

# function definition to show memory status
def showMemory ():
  print ("\n")
  print ("############################################################")
  
  for pid in latest_processes_stats:
    print ("P_ID: ", '%5s' % pid, "P_name: ", '%6s' % processes_pid [pid], "Mem.: ", '%10s' % latest_processes_stats [pid], "Bytes")

  print ("############################################################")
  print ("\n")
  
# game loop
while choice != 'letmego':
  if choice == '1':
    showMemory ()

  processes_pid.clear ()
  
  # stores pid and pname in the processes-pid dict
  for proc in psutil.process_iter (['pid', 'name']):
    processes_pid [proc.info ["pid"]] = proc.info ["name"]
  ####DONE####

  # initialising the first processes stats dict once
  # first processes stats store pid and uss first time only
  count = 0
  for pid in processes_pid:
    latest_processes_stats [pid] = psutil.Process (pid).memory_full_info () [7]
    if root_count == 0:
      first_processes_stats [pid] = psutil.Process (pid).memory_full_info () [7]
      coeff_counter [pid] = str (0)
    count = count + 1
  root_count = 1

  # checking if memory is increasing for 'coefficient' times
  count = 0
  for pid in latest_processes_stats:
    if (int (coeff_counter [pid])) > coefficient:
      showMemory ()
      print ("Memory leak detected!")
      print ("P_ID: ", pid, " ", "P_name: ", processes_pid [pid])
      print ("\n")
      exit (0)
      
    if latest_processes_stats [pid] > first_processes_stats [pid]:
      coeff_counter [pid] = str (int (coeff_counter [pid]) + 1)
    
    count = count + 1

  mod_counter = mod_counter + 1

  # exit sequence
  if mod_counter % mod_factor == 0:
    mod_counter = mod_counter % coefficient
    print ("############################################################")
    print ("#               1. Submit 'letmego' to exit.               #")
    print ("#----------------------------------------------------------#")
    print ("#               2. Submit '1' to view memory.              #")
    print ("############################################################")
    choice = input (">>> ")

