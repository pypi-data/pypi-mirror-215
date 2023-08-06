import typing
import json
import chiral_bindings
from .client import Client

class GromacsJob:
    client: Client
    id: str = None
    status_label: str = None
    input: chiral_bindings.gromacs_gmx_command.Input = None
    output: chiral_bindings.gromacs_gmx_command.Output = None

    def __init__(self, client: Client ):
        self.client = client

    @property
    def requirement(self) -> str:
        return chiral_bindings.job_module.create_requirement(self.input.to_str(), "gromacs_run_gmx_command", "empty") if self.input else ""

    def set_input(self, simulation_id: str, sub_command: str, arguments: str, prompts: typing.List[str], file_folder: str, files_input: typing.List[str], files_output: typing.List[str]):
        self.input = chiral_bindings.gromacs_gmx_command.Input(simulation_id, sub_command, arguments.split(' '), prompts, file_folder, files_input, files_output)

    def submit(self):
        self.id = self.client.submit_job(self.requirement)

    def check_status(self):
        statuses = self.client.check_job_status([self.id])
        status = json.loads(statuses[self.id])
        self.status_label = status["label"]
    
    def get_output(self):
        outputs_str_list = self.client.get_job_outputs(self.id)
        self.output = chiral_bindings.gromacs_gmx_command.Output(outputs_str_list[0])
    
