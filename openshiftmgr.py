"""
OpenShift cluster manager module that provides functionality to schedule jobs as well as
manage their state in the cluster.
"""

from argparse import ArgumentParser
import yaml
from kubernetes import client
from openshift import client as o_client
from openshift import config


class OpenShiftManager(object):

    def __init__(self):
        parser = ArgumentParser(description='Manage a OpenShift cluster')

        group = parser.add_mutually_exclusive_group()
        group.add_argument("-s", "--schedule", help="schedule a new job",
                           metavar='name')
        group.add_argument("-r", "--remove", help="remove a previously scheduled job",
                           metavar='name')
        group.add_argument("--state", help="print state of scheduled job",
                           metavar='name')
        parser.add_argument("--conffile", help="OpenShift cluster configuration file")
        parser.add_argument("-p", "--project", help="The OpenShift project to create jobs in")
        parser.add_argument("-i", "--image",
                            help="docker image for the scheduled job container")
        parser.add_argument("-c", "--command",
                            help="command to be run inside scheduled job container")
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
        if conf_filepath is None:
            config.load_kube_config()
        else:
            config.load_kube_config(config_file=conf_filepath)
        self.openshift_client = o_client.OapiApi()
        self.kube_client = client.CoreV1Api()
        self.kube_v1_batch_client = client.BatchV1Api()

    def schedule(self, image, command, name, project, mountdir=None):
        """
        Schedule a new job and returns the job object.
        """
        job_str = """
apiVersion: batch/v1
kind: Job
metadata:
    name: {name}
spec:
    parallelism: 1
    completions: 1
    template:
        metadata:
            name: {name}
        spec:
            containers:
            - name: {name}
              image: {image}
              command: {command}
            restartPolicy: Never
""".format(name=name, command=str(command.split(" ")), image=image)
        job_yaml = yaml.load(job_str)
        job = self.kube_v1_batch_client.create_namespaced_job(namespace=project, body=job_yaml)
        print(yaml.dump(job))
        return job

    def get_job(self, name, project):
        """
        Get the previously scheduled job object.
        """
        return self.kube_v1_batch_client.read_namespaced_job(name, project)

    def remove(self, name, project):
        """
        Remove a previously scheduled job.
        """
        self.kube_v1_batch_client.delete_namespaced_job(name, project, {})

    def parse(self, args=None):
        """
        Parse the arguments passed to the manager and perform the appropriate action.
        """
        # parse argument options
        options = self.parser.parse_args(args)

        if not options.project:
            self.parser.error("-p/--project is required")

        # get the docker client
        if options.conffile:
            self.get_openshift_client(options.conffile)
        else:
            self.get_openshift_client()

        if options.schedule:
            if not (options.image and options.command):
                self.parser.error("-s/--schedule requires -i/--image and -c/--command")
            self.schedule(options.image, options.command, options.schedule,
                          options.project, options.mount)

        if options.remove:
            self.remove(options.remove, options.project)

        if options.state:
            job = self.get_job(options.state, options.project)
            print(yaml.dump(job))


# ENTRYPOINT
if __name__ == "__main__":
    manager = OpenShiftManager()
    manager.parse()


