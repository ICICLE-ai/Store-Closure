#Constants related to agent algorithm

#Search for stores within SEARCHRADIUS
SEARCHRADIUS = 10 #radius (miles) to search for stores

#Probabilities to choose SPM over CSPM
ERHCFARTHERPROB = 74 #percentage if SPM is farther than CSPM, ERHC
ERLCFARTHERPROB = 72 #percentage if SPM if SPM is farther than CSPM, ERLC
LRHCFARTHERPROB = 64 #percentage if SPM if SPM is farther than CSPM, LRHC
LRLCFARTHERPROB = 60 #percentage if SPM is farther than CSPM, LRLC
CLOSERPROB = 80 #percentage if SPM closer than CSPM, all households

#Max MFAI values used to divide to get MFAI score
ERHCMAX = 700 #max MFAI for ERHC
ERLCMAX = 640 #max MFAI for ERLC
LRHCMAX = 600 #max MFAI for LRHC
LRLCMAX = 480 #max MFAI for LRLC
