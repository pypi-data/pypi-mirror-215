import typing
import grpc
import json
import ftplib
import pathlib

from . import conductor_pb2
from . import conductor_pb2_grpc

TransferFile: typing.TypeAlias = tuple[str, str, str] # filename, local dir, remote dir

class Client:
    def __init__(self, host: str, port: str, email: str, password: str, token_api: str, file_server_addr: str, file_server_port: int):
        self.channel = grpc.insecure_channel(f'{host}:{port}')
        self.stub = conductor_pb2_grpc.ChiralOrchestraConductorStub(self.channel)
        self.metadata = (
            ('user_email', email),
            ('token_api', token_api)
        )
        self.user = email
        self.password = password
        self.ftp_addr = file_server_addr
        self.ftp_port = file_server_port
        self.ftp_root = None

    def connect_file_server(self):
        # self.ftp = ftplib.FTP(user=self.user, passwd=self.password, source_address=(self.ftp_addr, self.ftp_port))
        # self.ftp = ftplib.FTP(source_address=(self.ftp_addr, self.ftp_port))
        self.ftp = ftplib.FTP()
        self.ftp.connect(self.ftp_addr, self.ftp_port)
        self.ftp.login(self.user, self.password)
        self.ftp.cwd(self.user)
        self.ftp_root = self.ftp.pwd()

    def disconnect_file_server(self):
        self.ftp.quit()

    def reconnect_if_disconnected(self):
        try:
            self.ftp.cwd(self.ftp_root)
        except Exception:
            self.connect_file_server()

    def upload_files(self, files: typing.List[TransferFile]):
        self.reconnect_if_disconnected()
        for (fn, local_dir, remote_dir) in files:
            self.ftp.cwd(self.ftp_root)
            self.ftp.cwd(remote_dir)
            with open(pathlib.Path(local_dir).joinpath(fn), 'rb') as file:
                self.ftp.storbinary(f'STOR {fn}', file)

    def download_files(self, files: typing.List[TransferFile]):
        self.reconnect_if_disconnected()
        for (fn, local_dir, remote_dir) in files:
            self.ftp.cwd(self.ftp_root)
            self.ftp.cwd(remote_dir)
            with open(pathlib.Path(local_dir).joinpath(fn), 'wb') as file:
                self.ftp.retrbinary(f'RETR {fn}', file.write)

    def remove_files(self, files: typing.List[TransferFile]):
        self.reconnect_if_disconnected()
        for (fn, _, remote_dir) in files:
            self.ftp.cwd(self.ftp_root)
            self.ftp.cwd(remote_dir)
            self.ftp.delete(fn)

    def is_remote_file(self, file: TransferFile) -> bool:
        filename, _, remote_dir = file
        self.ftp.cwd(self.ftp_root)
        self.ftp.cwd(remote_dir)
        try:
            file_size = self.ftp.size(filename)
            return bool(file_size)
        except Exception:
            return False
        
    def is_remote_dir(self, parent_dir: str, dir: str) -> bool:
        self.ftp.cwd(self.ftp_root)
        self.ftp.cwd(parent_dir)
        return dir in self.ftp.nlst()
    
    def create_remote_dir(self, dir_name: str):
        self.ftp.cwd(self.ftp_root)
        self.ftp.mkd(dir_name)

    def remove_remote_dir(self, parent_dir: str, dir: str):
        # will remove all the files inside
        self.ftp.cwd(self.ftp_root)
        self.ftp.cwd(parent_dir)
        self.ftp.cwd(dir)
        for filename in self.ftp.nlst():
            self.ftp.delete(filename)
        self.ftp.cwd('..')
        self.ftp.rmd(dir)

    def __del__(self):
        self.channel.close()

    def submit_job(self, job_req: str) -> str:
        return self.stub.AcceptJob(conductor_pb2.RequestAcceptJob(job_req=job_req), metadata=self.metadata).job_id
    
    def check_job_status(self, job_ids: typing.List[str]) -> typing.Dict[str, typing.Any]:
        return self.stub.JobStatus(conductor_pb2.RequestJobStatus(job_ids=job_ids), metadata=self.metadata).statuses
    
    def get_job_outputs(self, job_id: str) -> typing.List[str]:
        def get_output(s) -> str:
            if s['error']:
                print(s)
                raise Exception(f'Job error {s["error"]}')
            return s['output']
        result_str = self.stub.JobResult(conductor_pb2.RequestJobResult(job_id=job_id), metadata=self.metadata).result
        result = json.loads(result_str)
        return list(map(get_output, result['results']))



