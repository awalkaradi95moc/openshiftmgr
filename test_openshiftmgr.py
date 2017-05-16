import unittest
from unittest.mock import patch, MagicMock
import random
import string
import kubernetes
from openshiftmgr import OpenShiftManager


class OpenShiftManagerTests(unittest.TestCase):
    """
    Test the OpenShiftManager's methods
    """

    @patch('openshiftmgr.config.load_kube_config')
    def setUp(self, mock_config):
        self.manager = OpenShiftManager()
        self.manager.get_openshift_client()
        self.job_name = 'job' + ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(10))
        self.image = 'fedora'
        self.command = 'echo test'
        self.project = 'myproject'

    @patch('kubernetes.client.apis.batch_v1_api.BatchV1Api.create_namespaced_job')
    def test_schedule(self, mock_create):
        mock_create.return_value = kubernetes.client.models.v1_job.V1Job()
        job = self.manager.schedule(self.image, self.command, self.job_name, self.project)
        self.assertIsInstance(job, kubernetes.client.models.v1_job.V1Job)
        #mock_create.assert_called_once() Available in 3.6
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
