import unittest
import random
import string
import kubernetes
from pman_openshift import OpenShiftManager


class OpenShiftManagerTests(unittest.TestCase):
    """
    Test the OpenShiftManager's methods
    """

    def setUp(self):
        self.manager = OpenShiftManager()
        self.manager.get_openshift_client()
        self.job_name = 'job' + ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(10))
        self.image = 'fedora'
        self.command = 'echo test'
        self.project = 'myproject'

    def test_schedule(self):
        self.manager.schedule(self.image, self.command, self.job_name, self.project)
        job = self.manager.get_job(self.job_name, self.project)
        self.assertIsInstance(job, kubernetes.client.models.v1_job.V1Job)
        self.manager.remove(self.job_name, self.project)
"""
    def test_get_job(self):
        service = self.openshift_client.services.create(self.image, self.command, name=self.job_name)
        service1 = self.manager.get_service(self.job_name)
        self.assertEqual(service, service1)
        service.remove()

    def test_remove(self):
        self.openshift_client.services.create(self.image, self.command, name=self.job_name)
        self.assertEqual(len(self.openshift_client.services.list()), 1)
        self.manager.remove(self.job_name)
        self.assertEqual(len(self.openshift_client.services.list()), 0)
"""

if __name__ == '__main__':
    unittest.main()
