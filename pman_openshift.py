"""
OpenShift cluster manager module that provides functionality to schedule services as well as
manage their state in the cluster.
"""

from argparse import ArgumentParser
import configparser
import json
import yaml
from kubernetes import client
from openshift import client as o_client
from openshift import config


class OpenShiftManager(object):

    def __init__(self):
        parser = ArgumentParser(description='Manage a OpenShift cluster')

        group = parser.add_mutually_exclusive_group()
        group.add_argument("-s", "--schedule", help="schedule a new service",
                           metavar='name')
        group.add_argument("-r", "--remove", help="remove a previously scheduled service",
                           metavar='name')
        group.add_argument("--state", help="print state of scheduled service",
                           metavar='name')
        parser.add_argument("--conffile", help="OpenShift cluster configuration file")
        parser.add_argument("-i", "--image",
                            help="docker image for the scheduled service container")
        parser.add_argument("-c", "--command",
                            help="command to be run inside scheduled service container")
        parser.add_argument("-m", "--mount", help="mount directory in the cluster",
                            metavar='dir')
        self.parser = parser
        self.openshift_client = None
        self.kube_client = None
        self.kube_v1_batch_client = None

    def get_openshift_client(self, conf_filepath=None):
        """
        Method to get a OpenShift client connected to remote or local OpenShift.
        """
        config.load_kube_config()
        self.openshift_client = o_client.OapiApi()
        self.kube_client = client.CoreV1Api()
        self.kube_v1_batch_client = client.BatchV1Api()

        
    def schedule(self, image, command, name, mountdir=None):
        """
        Schedule a new job and returns the job object.
        """

        job = """
apiVersion: batch/v1
kind: Job
metadata:
    name: pman-openshift-job
spec:
    parallelism: 1
    completions: 1
    template:
        metadata:
            name: pman-openshift-job
        spec:
            containers:
            - name: pman-openshift-job
              image: fedora
              command: ["ls"]
            restartPolicy: Never
"""
        job_yaml = yaml.load(job)
        resp = self.kube_v1_batch_client.create_namespaced_job(namespace='myproject', body=job_yaml)


    def get_job(self, name):
        """
        Get docker container for a previously scheduled service object.
        """
        return self.kube_v1_batch_client.read_namespaced_job(name, 'myproject')

    def remove(self, name):
        """
        Remove a previously scheduled service.
        """
        self.kube_v1_batch_client.delete_namespaced_job(name, 'myproject', {})
    def parse(self, args=None):
        """
        Parse the arguments passed to the manager and perform the appropriate action.
        """
        # parse argument options
        options = self.parser.parse_args(args)

        # get the docker client
        if options.conffile:
            self.get_openshift_client(options.conffile)
        else:
            self.get_openshift_client()

        if options.schedule:
            if not (options.image and options.command):
                self.parser.error("-s/--schedule requires -i/--image and -c/--command")
            self.schedule(options.image, options.command, options.schedule,
                          options.mount)

        if options.remove:
            self.remove(options.remove)

        if options.state:
            job = self.get_job(options.state)
            print(yaml.dump(job))


# ENTRYPOINT
if __name__ == "__main__":
    manager = OpenShiftManager()
    manager.parse()


