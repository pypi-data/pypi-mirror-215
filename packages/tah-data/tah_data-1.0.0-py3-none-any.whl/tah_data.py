import dvc.api
from dvc.api import DVCFileSystem
import boto3
import os



def get_file(file_system,file_name,local_file_name):
    file_system.get_file(file_name,local_file_name)

def get_dir(file_system,dir_path,local_dir_name):
    file_system.get(dir_path,local_dir_name,recursive=True)


def init_data(Repo_url,branch,PAT_KEY):

    new_url=Repo_url[:8]+PAT_KEY+"@"+Repo_url[8:]

    file_system = DVCFileSystem(new_url, rev=branch)

    return file_system
    
