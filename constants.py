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

#Trips to the store per month by each agent type
ERHCTRIPSPERMONTH = 7 #trips for ERHC
ERLCTRIPSPERMONTH = 8 #trips for ERLC
LRHCTRIPSPERMONTH = 6 #trips for LRHC
LRLCTRIPSPERMONTH = 6 #trips for LRLC

#Percentage that each agent type is able to carry home per trip to the store
ERHCCARRYPERCENT = 1.0 #percent for ERHC
ERLCCARRYPERCENT = 0.8 #percent for ERLC
LRHCCARRYPERCENT = 1.0 #percent for LRHC
LRLCCARRYPERCENT = 0.8 #percent for LRLC