"""Constants related to agent algorithm."""
#derived from Hyder(2019)
#- Examining disparities in food accessibility among households in Columbus, Ohio- an agent-based model

#Search for stores within SEARCHRADIUS
SEARCHRADIUS = 5000 #radius (units unclear??) to search for stores

#Probabilities to choose SPM over CSPM
ERHCFARTHERPROB = .74 #probability if SPM is farther than CSPM, ERHC
ERLCFARTHERPROB = .72 #probability if SPM if SPM is farther than CSPM, ERLC
LRHCFARTHERPROB = .64 #probability if SPM if SPM is farther than CSPM, LRHC
LRLCFARTHERPROB = .60 #probability if SPM is farther than CSPM, LRLC
CLOSERPROB = .80 #probability if SPM closer than CSPM, all households

#Max MFAI values used to divide to get MFAI score
ERHCMAX = 700 #max MFAI for ERHC
ERLCMAX = 640 #max MFAI for ERLC
LRHCMAX = 600 #max MFAI for LRHC
LRLCMAX = 480 #max MFAI for LRLC

#Store constants
SPMRANGE = (80,95,80) #SPM FSA score range from 80 to 95 with mean of 80
CSPMRANGE = (20,55,30) #CSPM FSA score range from 20 to 55 with mean of 30
