#Changes made from orginial git repo:
    #Python version must be exactly 3.7.1
    #Deleted first two lines of "run.py"
    #Changed all relative imports to direct imports: eg "from .main" to "from main"
from server import server
from main import ABM
import profile
abm_steps = ABM()
for i in range(1):
    abm_steps.step()
#profile.run(server.launch())
