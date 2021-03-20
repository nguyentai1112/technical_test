'''This is test module for pushing product
    and caculate the mean of product in streaming'''
import os
import tempfile
import unittest
import db
import route


class ProductTestCase(unittest.TestCase):
    '''
    The class contains all tests:
        - Test input
            not valid
            out of range
        - Test accuracy of result

    Attributes:
        app (str): FlaskClient to test
        db_temp (file object): file object to open database file from temp, deleted when finishing
    '''
    def setUp(self):
        #print(self._testMethodName)
        self.db_temp, db.DATABASE = tempfile.mkstemp()
        self.app = route.APP.test_client()
        self.app.get('/api/init_db')

    def tearDown(self):
        os.close(self.db_temp)

    def test_product_not_int(self):
        '''test pushing a product with score is a float (not integer) (score = 2.3)'''
        json_response = self.app.post('/api/push', json={
            'UUID': 'a1-b1', 'score': 2.3
        }).get_json()

        self.assertEqual(json_response, route.ERROR_VALIDATE)

    def test_product_score_out_of_range(self):
        '''test pushing a product with out of range score <0 or >5 (score =6)'''
        json_response = self.app.post('/api/push', json={
            'UUID': 'a1-b1', 'score': 6
        }).get_json()

        self.assertEqual(json_response, route.ERROR_VALIDATE)

    def test_push_product_three_times(self):
        '''test pushing a product with 3 different score'''
        json_response = self.app.post('/api/push', json={
            'UUID': 'a1-b1', 'score': 5
        }).get_json()
        self.assertEqual(json_response, {'UUID': 'a1-b1', 'mean': 5})

        json_response = self.app.post('/api/push', json={
            'UUID': 'a1-b1', 'score': 3
        }).get_json()
        self.assertEqual(json_response, {'UUID': 'a1-b1', 'mean': 4})

        json_response = self.app.post('/api/push', json={
            'UUID': 'a1-b1', 'score': 4
        }).get_json()

        self.assertEqual(json_response, {'UUID': 'a1-b1', 'mean': 4})

    if __name__ == '__main__':
        unittest.main()
