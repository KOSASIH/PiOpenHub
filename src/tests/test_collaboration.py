# tests/test_collaboration.py

import unittest
from collaborationService import CollaborationService

class TestCollaborationService(unittest.TestCase):
    def setUp(self):
        self.service = CollaborationService()

    def test_add_partner(self):
        partner_info = {'name': 'IBM', 'api_endpoint': 'https://api.ibm.com/data'}
        self.service.add_partner(partner_info)
        self.assertIn(partner_info, self.service.partners)

    def test_remove_partner(self):
        partner_info = {'name': 'IBM', 'api_endpoint': 'https://api.ibm.com/data'}
        self.service.add_partner(partner_info)
        self.service.remove_partner('IBM')
        self.assertNotIn(partner_info, self.service.partners)

    def test_list_partners(self):
        partner_info1 = {'name': 'IBM', 'api_endpoint': 'https://api.ibm.com/data'}
        partner_info2 = {'name': 'Microsoft', 'api_endpoint': 'https://api.microsoft.com/data'}
        self.service.add_partner(partner_info1)
        self.service.add_partner(partner_info2)
        partners = self.service.list_partners()
        self.assertEqual(len(partners), 2)

    def test_share_data_with_partner(self):
        partner_info = {'name': 'IBM', 'api_endpoint': 'https://api.ibm.com/data'}
        self.service.add_partner(partner_info)
        response = self.service.share_data_with_partner('IBM', {'key': 'value'})
        self.assertIsNotNone(response)

    def test_fetch_data_from_partner(self):
        partner_info = {'name': 'IBM', 'api_endpoint': 'https://api.ibm.com/data'}
        self.service.add_partner(partner_info)
        data = self.service.fetch_data_from_partner('IBM')
        self.assertIsNotNone(data)

if __name__ == '__main__':
    unittest.main()
