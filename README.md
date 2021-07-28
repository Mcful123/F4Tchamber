# F4Tchamber

The V1 code will write the following steps into profile 4. <br />
<br />
The chamber will go from -20C to 100C with 20C increments then come back down to -20C in the same manner. At each temperature, it will soak for 30 minutes. <br />
At the end of the profile, the chamber will turn off. 

The V2 code is essentially the same code but it can be easily edited to make a custom profile. 
# convert(t) 

This function is only used internally. It changes decimal celsius value to the format required for the chamber to read

# reconnect()

This function is used to reconnect to the chamber if the host computer gets disconnected for whatever reason 

# set_profile(t_hr, t_min, profile)

This function is what will actually make and send profiles to the chamber. 'profile' takes an integer from 1 to 39: profile 40 is reserved for turning off the chamber using Python. The profile will be saved to this profile slot. <br />
t_hr and t_min takes integer from 0-999 and 0-59 respectively. This specifies the time spent soaking at each temperature. <br />
The global variable temps should be filled with every temperature the chamber should soak at. This can be done manually or aided with the 'set_temps()' function.

# set_temps()

This function will directly change the temps list. 

# start_profile(profile)

This function starts the specified profile number (integer from 1 to 39).

# terminate()

This function takes advantage of the fact the chamber can be turned off at the end of profiles. terminate() will write a simple one step profile to profile #40. Then it will terminate any running profile, and start profile 40. Profile 40 will run its 1 second long profile and turn off the chamber after it is completed. 

# pause()
pauses the currently running profile. It will do nothing if no profile is running.
# resume()
resumes the paused profile. It will do nothing if no profile is paused.
