import unittest
from mock import patch
from webservice import app
import json

class Webservice_Tester(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        
        
    @patch("webservice.model")
    def test_successfull_response(self, mocking):
        mocking.predict.return_value = "best"
        
        request = {
            "text": "The best Italian dish is Lasagne!!",
            "sentiment": "positive"
        }
        
        response = self.app.post(
            "/sentiment",
            json=request
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertIn("prediction", data)
        self.assertIn("response time in seconds", data)
        self.assertEqual("best", data["prediction"])
        
        
    def test_missing_text(self):
        request = {
            "sentiment": "positive"
        }
        
        response = self.app.post(
            "/sentiment",
            json=request
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertIn("error", data)
        self.assertEqual("check text specifier format", data["error"])
        
        
    def test_missing_sentiment(self):
        request = {
            "text": "The best Italian dish is Lasagne!!"
        }
        
        response = self.app.post(
            "/sentiment",
            json=request
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertIn("error", data)
        self.assertEqual("check sentiment specifier format", data["error"])
        

if __name__ == "__main__":
    unittest.main()