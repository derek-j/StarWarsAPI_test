import requests
import json
import unittest
import warnings

"""
    Program to write 5 test cases to test a few StarWarsAPI People REST API endpoints
    https://swapi.co/documentation#people
    These are the only endpoints and they are all read only, so not too much to test.
        /people/        - get all the people resources
        /people/:id/    - get a specific people resource
        /people/schema/ - view the JSON schema for this resource
        
    Written in Python 3.8.1 using standard unittest library.

    Derek Johnson
    408-836-9698
    3/23/2020

    TestPlan:
     #1 Get all People
     #2 Get people, verify certain people are returned and their data is correct.
     #3 Get non-existing people.  Should return not found
     #4 Get people Schema, verify the schema returned contains fields for people
     Negative tests
     #5 Find People by Name:  This is a negative test, passes, when it fails. 
"""

class Test_StarWarsAPI_People(unittest.TestCase):

    def setUp(self):
        self.star_wars_api_base_url = "https://swapi.co/api/people"
        self.headers = {'accept': 'application/json', 'content-type': 'application/json'}

    def ignoreWarnings(self):
        # For this quick test, ignore the warnings.  Normally create a separate test framework class for the
        # service calls and handle resource management to keep them separate from the testcases, to simplify I have them all here.
        warnings.filterwarnings(action="ignore", message="unclosed", category=ResourceWarning)

    def get_people(self):
        self.ignoreWarnings()
        url = self.star_wars_api_base_url
        print("calling GET to: {}".format(url))
        r = requests.get(url, headers=self.headers)
        if r.status_code != 200:
            print("Failed to get people. \nResponse Code: {} \nResponse Body {}".format(r.status_code, r.text))
        return r.status_code, json.loads(r.text)

    def get_people_by_id(self, id):
        self.ignoreWarnings()
        url = self.star_wars_api_base_url + "/" + str(id)
        print("calling GET to: {}".format(url))
        r = requests.get(url, headers=self.headers)
        if r.status_code != 200:
            print("Failed to get people. \nResponse Code: {} \nResponse Body {}".format(r.status_code, r.text))
        return r.status_code, json.loads(r.text)

    def get_people_schema(self):
        self.ignoreWarnings()
        url = self.star_wars_api_base_url + "/schema"
        print("calling GET to: {}".format(url))
        r = requests.get(url, headers=self.headers)
        if r.status_code != 200:
            print("Failed to get people. \nResponse Code: {} \nResponse Body {}".format(r.status_code, r.text))
        return r.status_code, json.loads(r.text)

    def get_people_by_name(self, name):
        self.ignoreWarnings()
        url = self.star_wars_api_base_url + "/" + name
        print("calling GET to: {}".format(url))
        r = requests.get(url, headers=self.headers)
        if r.status_code != 200:
            print("Failed to get people. \nResponse Code: {} \nResponse Body {}".format(r.status_code, r.text))
        return r.status_code, json.loads(r.text)

    def does_pet_with_id_exist(self, id):
        c, r = self.get_people_by_id(id)
        if c == 200:
            return True
        else:
            return False

    # -----------------------------------------------------------------------------------------------------------------
    #   Test Cases
    # -----------------------------------------------------------------------------------------------------------------

    def test_01_get_all_people(self):
        """
            Steps:
            1- call get_people
            2- validate some of the returned values

        """
        c, r = self.get_people()
        assert (c == 200), "Failed to GET people by id \nResponse Code: {} \nResponse Body {}".format(r.status_code, r.text)
        assert (r["count"] == 87)
        assert (r["results"][0]["name"] == "Luke Skywalker")
        assert (r["results"][1]["name"] == "C-3PO")
        assert (r["results"][2]["name"] == "R2-D2")
        assert (r["results"][3]["name"] == "Darth Vader")

    def test_02_get_people_by_id(self):
        """
            Steps:
            1- call get_people_by_id
            2- verify the person is returned
        """
        c, r = self.get_people_by_id(1)
        assert (c == 200), "Failed to GET people by id \nResponse Code: {} \nResponse Body {}".format(r.status_code, r.text)
        assert (r["name"] == "Luke Skywalker")
        assert (r["birth_year"] == "19BBY")

    def test_03_get_people_non_existing(self):
        """
            TEST getting a non existing person, should return 404
            Steps:
            - get_people_by_id(111111)
            - verify person is not found
        """
        c, r = self.get_people_by_id(111111)
        assert (c == 404), "PASS: Failed to GET people by id \nResponse Code: {} \nResponse Body {}".format(r.status_code, r.text)
        assert (r["detail"] == "Not found")

    def test_04_get_people_schema(self):
        """
            TEST Getting the people schema, validate its fields are returned.
            Steps:
            - get_people_schema
            - verify the schema keys are correct.
        """
        c, r = self.get_people_schema()
        assert (c == 200), "Failed to GET people by id \nResponse Code: {} \nResponse Body {}".format(r.status_code, r.text)
        schema_keys = ["required", "description", "title", "properties", "$schema", "type"]
        for key in schema_keys:
            assert (key in r), "Key {} not found in the schema".format(key)


    def test_05_find_people_by_name(self):
        """
            TEST getting a person by name:  (API says can search on this name) should return 404
            Steps:
            - get_people_by_id("Luke Skywalker")
            - verify person is not found
        """
        c, r = self.get_people_by_name("Luke Skywalker")
        assert (c == 404), "PASS: Failed to GET people by id \nResponse Code: {} \nResponse Body {}".format(r.status_code, r.text)
        assert (r["detail"] == "Not found")

if __name__ == '__main__':
    unittest.main()

