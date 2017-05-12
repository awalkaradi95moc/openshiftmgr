import unittest
from pman-openshift import OpenShiftManager


class OpenShiftManagerTests(unittest.TestCase):
    """
    Test the OpenShiftManager's methods
    """

    @classmethod
    def setUpClass(cls):
        # initialize a single-node openshift

    @classmethod
    def tearDownClass(cls):

    def setUp(self):
        self.manager = OpenShiftManager()
        self.manager.get_openshift_client()
        self.service_name = 'simple_service'
        self.image = 'fedora'
        self.command = 'echo test'

    def test_schedule(self):
        self.manager.schedule(self.image, self.command, self.service_name)
        service = self.openshift_client.services.get(self.service_name)
        #self.assertIsInstance(service, docker.models.services.Service)
        service.remove()

    def test_get_service(self):
        service = self.openshift_client.services.create(self.image, self.command, name=self.service_name)
        service1 = self.manager.get_service(self.service_name)
        self.assertEqual(service, service1)
        service.remove()

    def test_get_service_container(self):
        service = self.openshift_client.services.create(self.image, self.command, name=self.service_name)
        container = self.manager.get_service_container(self.service_name)
        #self.assertEqual(container['ServiceID'], service.id)
        service.remove()

    def test_remove(self):
        self.openshift_client.services.create(self.image, self.command, name=self.service_name)
        self.assertEqual(len(self.openshift_client.services.list()), 1)
        self.manager.remove(self.service_name)
        self.assertEqual(len(self.openshift_client.services.list()), 0)

if __name__ == '__main__':
    unittest.main()
