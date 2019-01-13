from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from base import mods


class PostProcTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        mods.mock_query(self.client)

    def tearDown(self):
        self.client = None

    def test_identity(self):
        data = {
            "type": "IDENTITY",
            "options": [
                { "option": "Option 1", "number": 1, "votes": 5 },
                { "option": "Option 2", "number": 2, "votes": 0 },
                { "option": "Option 3", "number": 3, "votes": 3 },
                { "option": "Option 4", "number": 4, "votes": 2 },
                { "option": "Option 5", "number": 5, "votes": 5 },
                { "option": "Option 6", "number": 6, "votes": 1 }
            ]
        }

        expected_result = [
            { "option": "Option 1", "number": 1, "votes": 5, "postproc": 5 },
            { "option": "Option 5", "number": 5, "votes": 5, "postproc": 5 },
            { "option": "Option 3", "number": 3, "votes": 3, "postproc": 3 },
            { "option": "Option 4", "number": 4, "votes": 2, "postproc": 2 },
            { "option": "Option 6", "number": 6, "votes": 1, "postproc": 1 },
            { "option": "Option 2", "number": 2, "votes": 0, "postproc": 0 }
        ]

        response = self.client.post('/postproc/', data, format='json')
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)


    def test_sainte_lague(self):
        data = {
            "type": "SAINTELAGUE",
            "seats": "20",
            "options": [
                { "option": "Option 1", "number": 1, "votes": 5 },
                { "option": "Option 2", "number": 2, "votes": 0 },
                { "option": "Option 3", "number": 3, "votes": 3 },
                { "option": "Option 4", "number": 4, "votes": 2 },
                { "option": "Option 5", "number": 5, "votes": 5 },
                { "option": "Option 6", "number": 6, "votes": 1 }
            ]
        }

        expected_result = [
            { "option": "Option 1", "number": 1, "votes": 5, "seats": 6 },
            { "option": "Option 5", "number": 5, "votes": 5, "seats": 6 },
            { "option": "Option 3", "number": 3, "votes": 3, "seats": 4 },
            { "option": "Option 4", "number": 4, "votes": 2, "seats": 3 },
            { "option": "Option 6", "number": 6, "votes": 1, "seats": 1 },
            { "option": "Option 2", "number": 2, "votes": 0, "seats": 0 }
        ]

        response = self.client.post("/postproc/", data, format="json")
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)


    def test_dhondt(self):
        data = {
            "type": "DHONDT",
            "seats": "8",
            "options": [
                { "option": "Option 1", "number": 1, "votes": 5 },
                { "option": "Option 2", "number": 2, "votes": 0 },
                { "option": "Option 3", "number": 3, "votes": 3 },
                { "option": "Option 4", "number": 4, "votes": 2 },
                { "option": "Option 5", "number": 5, "votes": 5 },
                { "option": "Option 6", "number": 6, "votes": 1 }
            ]
        }

        expected_result = [
            { "option": "Option 1", "number": 1, "votes": 5, "seats": 3 },
            { "option": "Option 5", "number": 5, "votes": 5, "seats": 3 },
            { "option": "Option 3", "number": 3, "votes": 3, "seats": 1 },
            { "option": "Option 4", "number": 4, "votes": 2, "seats": 1 },
            { "option": "Option 2", "number": 2, "votes": 0, "seats": 0 },
            { "option": "Option 6", "number": 6, "votes": 1, "seats": 0 }
        ]

        response = self.client.post("/postproc/", data, format="json")
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)
		
    def test_equalityVoting(self):
        data = {
            "type": "SAINTELAGUE",
			"groups": True,	
            "seats": "20",
            "options": [
                { "option": "Option 1", "number": 1, "votes": 5, "group":"g1" },
                { "option": "Option 2", "number": 2, "votes": 0, "group":"g2" },
                { "option": "Option 3", "number": 3, "votes": 3, "group":"g2" },
                { "option": "Option 4", "number": 4, "votes": 2 },
                { "option": "Option 5", "number": 5, "votes": 5 },
                { "option": "Option 6", "number": 6, "votes": 1, "group":"g1" }
            ]
        }

        expected_result = [
            {'option': 'Option 3', 'number': 3, 'votes': 3, 'group': 'g2', 'seats': 6}, 
            {'option': 'Option 1', 'number': 1, 'votes': 5, 'group': 'g1', 'seats': 5},
            {'option': 'Option 5', 'number': 5, 'votes': 5, 'seats': 4}, 
            {'option': 'Option 4', 'number': 4, 'votes': 2, 'seats': 2}, 
            {'option': 'Option 6', 'number': 6, 'votes': 1, 'group': 'g1', 'seats': 1},
            {'option': 'Option 2', 'number': 2, 'votes': 0, 'group': 'g2', 'seats': 0}
        ]        

        response = self.client.post("/postproc/", data, format="json")
        self.assertEqual(response.status_code, 200)

        values = response.json()
        self.assertEqual(values, expected_result)