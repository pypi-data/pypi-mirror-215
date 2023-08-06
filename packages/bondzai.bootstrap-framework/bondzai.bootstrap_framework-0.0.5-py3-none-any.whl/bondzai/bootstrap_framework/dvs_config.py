import yaml
from pathlib import Path

from bondzai.davinsy_py.model import VirtualModel
from bondzai.davinsy_py.operations import OperationRegistry
from bondzai.davinsy_py.model import PreprocPhase

from .file_handler import Tar, handle_binary_file_data


class DvsConfig():
    """
    Define the config object
    """
    _instance: "DvsConfig" = None

    @classmethod
    def get_instance(cls, path: Path = Path(__file__).parent.resolve()):
        if not cls._instance:
            cls._instance = DvsConfig(path)
        return cls._instance

    def __init__(self, path: Path):
        """
        Constructs a new instance.
        Args:
            path: The path of the configuration file
        """
            
        self.rootPath = path       

        self.registry = OperationRegistry()

        self.vm = []
        self.nb_vm = 0

        self.max_raw_data = 0
        self.max_input_data = 0
        self.bootstrap_info = {}
        self.max_models = 0
        self.max_labels = 0
        self.max_reg_len = 0
        self.max_nb_raw_data = 3000


    def set_data_path(self,data_path):
        self.rootPath = data_path

    def preload_vms(self,vmFiles = None):

        if vmFiles is None:
            vmFiles = [ self.rootPath / "vm"] # 
        vmFiles_udpated = []
        for vmFile in vmFiles:
            pathvmfiles = Path(vmFile)
            if pathvmfiles.is_dir():
                for file in pathvmfiles.iterdir():
                    if file.is_file() and file.suffix=='.yml':
                        vmFiles_udpated.append(file)
            else:
                if pathvmfiles.is_file() and pathvmfiles.suffix=='.yml':
                    vmFiles_udpated.append(pathvmfiles)
            
            for vmFile in vmFiles_udpated:
                vmPath = self.rootPath / vmFile
                self.vm.append(VirtualModel(path=vmPath, templatePath=self.rootPath / "templates" ))

        # post-analysis
        self.max_models = 0
        self.max_labels = 0
        self.max_reg_len = 0
        self.nb_vm = 0
        all_axis = []
        for vm in self.vm:
            model = vm.get_model()
            self.nb_vm +=1
            # complete VM
            if model["deeplomath"]["nbInstances"] > 0:
                if model["deeplomath"]["mode"] == 0: # classification
                    axis = model["description"]["axis"]
                    isNew = True
                    for existing_axis in all_axis:
                        if existing_axis[0] == axis[0] and existing_axis[1] == axis[1]:
                            isNew = False
                            break
                    if isNew:
                        all_axis.append(model["description"]["axis"])
                        self.max_labels +=1
                else:
                    reg_len = model["deeplomath"]["mode"]["dim_out"]
                    if reg_len > self.max_reg_len:
                        self.max_reg_len = reg_len

                if model["description"]["maxsplit"] == 0:
                    self.max_models +=1    
                else:
                    self.max_models += model["description"]["maxsplit"]

            bootstrap_info = vm.get_bootstrap_info()
            if bootstrap_info is not None :
                self.bootstrap_info[vm.get_name()] =  bootstrap_info
                if "source" in bootstrap_info:
                    if self.max_raw_data < bootstrap_info["source"]["preproc_out_len"] :
                        self.max_raw_data = bootstrap_info["source"]["preproc_out_len"]
                    
                    input_len = bootstrap_info["source"]["frame_len"] * bootstrap_info["source"]["max_frames_number"]
                    if self.max_input_data < input_len :
                        self.max_input_data = input_len
                # max_nb_raw_data
        return self.vm
    
    def load_initial_dataset_definition(self,path : Path = None):
        if path is None:
            path = self.rootPath / "dataset" /"myDataset.yml"

        if not Path.exists(path):
            return None
        
        with open(path, 'r') as file:
            dataset = yaml.safe_load(file)

        return dataset
    
    def load_data_from_dataset(self,filename,path : Path = None):
        if path is None:
            path = self.rootPath / "dataset" / filename

        if not Path.exists(path):
            return None
        
        with open(path, "rb") as f:
            if f is None:
                raise Exception(f" file {path} not found")
            data = f.read()
        
        return handle_binary_file_data(data)


    def preload_targz(self,path : Path = None):
        if path is None:
            path = self.rootPath / "dataset.tar.gz"
        my_tar = Tar(path)
        return my_tar
    
    def close_targz(self,my_tar):
        my_tar.__del__()

    def load_initial_dataset_definition_targz(self,my_tar,path : Path = None):
        # my_tar = Tar(path)
        dataset = my_tar.read_yml("./myDataset.yml")
        return dataset


    def load_data_from_dataset_targz(self,my_tar,path : Path = None):
        
        bindata = my_tar.read_binary(path)

        return bindata

    def set_max_nb_raw_data (self,max_nb_raw_data:int):
        self.max_nb_raw_data = max_nb_raw_data

    def get_vms(self):
        return self.vm

    def get_max_raw_data(self):
        return self.max_raw_data
    
    def get_max_input_data(self):
        return self.max_input_data
    
    def get_max_models(self):
        return self.max_models

    def get_max_labels(self):
        return self.max_labels
    
    def get_max_reg_len(self):
        return self.max_reg_len
    
    def get_max_nb_raw_data(self):
        return self.max_nb_raw_data

    def get_nb_vm(self):
        return self.nb_vm
    
    def get_bootstrap_info_list(self):
        return self.bootstrap_info

    def get_bootstrap_dataconditionning(self,preproc):
        return preproc[PreprocPhase.INFERENCE]

    def register_external_ops(self,opId: str,operation: callable):
        self.registry.add_custom_operation(opId,operation)