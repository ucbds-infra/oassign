import unittest
import subprocess
from subprocess import PIPE
from oassign.oassign import main
import os

class TestConversion(unittest.TestCase):
    
    def test_convert_example(self):
        run_oassign_args = ["--no-run-tests", "test/example.ipynb", "test/output", "test/data.csv"]
        main(run_oassign_args)

        self.assertTrue(os.path.isdir("test/output"))
        self.assertEqual(os.listdir("test/output"), ["autograder", "student"])

        # check contents of autograder directory
        self.assertEqual(os.listdir("test/output/autograder"), ["tests", "data.csv", "example.ipynb"])
        self.assertEqual(os.listdir("test/output/autograder/tests"), ["q1H.py", "q1.py", "q3.py"])

        for file in ["example.ipynb", "data.csv", "tests/q1.py", "tests/q1H.py", "tests/q3.py"]:
            with open(os.path.join("test/output-correct/autograder", file)) as f:
                correct_contents = f.read()
            with open(os.path.join("test/output/autograder", file)) as f:
                contents = f.read()
            self.assertEqual(correct_contents, contents, "Autograder file {} incorrect".format(file))
        
        # check contents of student directory
        self.assertEqual(os.listdir("test/output/student"), ["tests", "data.csv", "example.ipynb"])
        self.assertEqual(os.listdir("test/output/student/tests"), ["q1.py", "q3.py"])

        for file in ["example.ipynb", "data.csv", "tests/q1.py", "tests/q3.py"]:
            with open(os.path.join("test/output-correct/student", file)) as f:
                correct_contents = f.read()
            with open(os.path.join("test/output/student", file)) as f:
                contents = f.read()
            self.assertEqual(correct_contents, contents, "Student file {} incorrect".format(file))
        