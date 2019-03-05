import sys
import os
import docker

"""
Creates a Dockerfile and a docker image from that Dockerfile
*Must have Docker engine installed and running on your computer in oder to create docker images
"""

def create_dockerfile(program_path, init_file=None, requirements_file=None):
    """
    Creates a Dockerfile for a python program using layer from python:3.6 docker image.
    Copies the program files into the directory /program/

    Parameters:
    1) program_path (str): absolute file path to the program
    2) init_file (str): bash script that contains all of the installation necessary to run the program
    3) requirements_file (str): requirements file with all the pip installation necessary to run the program
    """
    paths = program_path.split("/")
    if(paths[-1] == 'Dockerfile'): #in ['Dockerfile','dockerfile']):
        program_path = "".join(paths[:-1])
    if(program_path and program_path[-1] == '/'):
        program_path = program_path[:-1]
    
    filename = program_path+"/Dockerfile"
    print ("Dockerfile Path:", filename)
    try:
        file = open(filename, 'w' )
        file.writelines(["FROM python:3.6\n", 
                        "RUN apt-get update\n", 
                        "RUN apt-get install sudo\n",
                        "COPY . ./program/\n",
                        "WORKDIR /program\n"])
        
        if init_file:
            if (init_file.split(".")[-1] == '.sh'):
                line = "RUN sh {}\n".format(init_file)
                file.write(line)
        if requirements_file == 'requirements.txt':
            line = "RUN pip install -r requirements.txt\n"
            file.write(line)
        file.close()
    except Exception as e:
        print(e)

def create_docker_image(program_path, image_name, image_version='latest'):
    """
    Creates a docker image.

    Parameters:
    1) program_path (str): absolute file path to the program
    2) image_name (str): name for the docker image
    3) image_version (str): version of the docker image (default version is 'latest')
    """
    tag = image_name+":"+image_version
    cmd = "docker build -t {} {}".format(tag, program_path)
    print("Image build cmd:", cmd)
    os.system(cmd)
    return

