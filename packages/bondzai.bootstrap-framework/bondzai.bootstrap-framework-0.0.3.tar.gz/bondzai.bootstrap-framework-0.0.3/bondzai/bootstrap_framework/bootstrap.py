##############################################
#    _              __   
#   | \ _     o __ (_  \/
#   |_/(_|\_/ | | |__) / 
#
###############################################
# This is DavinSy boot script
# The script is executed at the very beginning of the boot sequence
# At this time DavinSy is not ready to handle any command, still you can
# do some pure python initialization
# 
# Then, if this is the first time the system boot
# the boot function is called with 0 as a parameter
# At this time you should populate the database.
# 
# Later on the boot function is called again with 1 as a parameter
# just before the application starts.
# 
# And one time again with 2 as a parameter just after the application started
# At this time you should start running you simulation script/
# ########################################################

from .dvs_agent import DvsAgent
from .logger import logger
from .dvs_com import DvsCom

class Bootstrap:
    _instance: "Bootstrap" = None

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = cls()
        return cls._instance
    
    def __init__(self):
        self.agent = DvsAgent(link=self.configure_communication())
        self.callbacks = {}
        self.custom_ops = {}

    # super seed for FOREIGN
    def configure_communication(self):
        return DvsCom()

    def set_data_path(self,data_path):
        return self.agent.set_data_path(data_path)

    def set_max_nb_raw_data (self,max_nb_raw_data:int):
        self.agent.set_max_nb_raw_data(max_nb_raw_data)
        
    def register_external_op(self,opId,operation):
        self.custom_ops[opId] = operation

    def register_callbacks(self,step,callbackfunction:callable):

        if step in self.callbacks:
            logger.warn(f" bootstrap callback already defined for {step}, replaced")
        self.callbacks[step] = callbackfunction

    def boot_init(self):

        self.agent.init_and_load()
        
        self.agent.register_custom_ops_in_agent(self.custom_ops)

        if self.agent.lifecycle == 1 :
            # ---- LOAD INITIAL self.dataset ----
            self.agent.load_initial_data()
            logger.info("==> ending the init sequence")
            #self.agent.link.end_init()

    def boot_start(self):
        self.agent.update_tables()

    def boot_ready(self):
        return

    def boot(self, step):
        if step == 0:
            self.boot_init()
        elif step == 1:
            self.boot_start()
        elif step == 2:
            self.boot_ready()

        if step in self.callbacks:
            self.callbacks[step]()

def boot(step):
    Bootstrap.get_instance().boot(step)
