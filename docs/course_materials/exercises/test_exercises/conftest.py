"""
Helper functions for automatically checking student's exercises

The tests will check:
 1. The content of the exercise file, needs expected answers and file to test.
 2. The output of the exercise file to the cmd.
 3. If the student answer file exists.
"""
import os
import re
import pytest
from subprocess import PIPE, STDOUT, Popen, TimeoutExpired
import logging
from rose_check import HOME

LOGGER = logging.getLogger()


@pytest.fixture
def home_folder():
    return HOME


class Test_helpers:
    def __init__(self):
        self.student_file = ''
        self.expected_pycode = []
        self.expected_stdout = []
        self.input = []
        self.exact_answer = False

    def test_assignment(self):
        '''
        Runs all checks on a assignment
        1. If student answer file exists
        2. If the writen code corresponds to the requirments
        3. If the output corresponds to the requirments
        '''
        self.test_file_exist()

        # testing the code
        if len(self.expected_pycode) > 0:
            student_code = self.get_student_code()
            # LOGGER.info(student_code)
            self.test_answers(self.expected_pycode, student_code)

        # Testing the output
        if len(self.expected_stdout) > 0:
            if self.input:
                for data, expected_stdout in zip(self.input,
                                                 self.expected_stdout):
                    student_stdout = self.run_cmd(data)
                    self.test_answers([expected_stdout], [student_stdout],
                                      word_pattern=self.exact_answer)
            else:
                student_stdout = self.run_cmd()
                self.test_answers(self.expected_stdout, student_stdout.strip(),
                                  word_pattern=self.exact_answer)

    def test_file_exist(self):
        '''
        Checks if the student file exists
        '''
        assert os.path.exists(self.student_file), LOGGER.warning(
                                                  'Student homework file ' +
                                                  'not found: ' +
                                                  self.student_file)

    def get_student_code(self):
        '''
        Returns the student code/text as an array by lines
        '''
        with open(self.student_file, 'r') as f:
            student_code = f.read()
        return student_code

    def run_cmd(self, data=[], **kwargs):
        '''
        Simulates a cmd action to check output
        '''
        input_data = ('\n'.join(data).encode('utf-8') if data
                      else None)

        p = Popen(['python', self.student_file], stdout=PIPE, stdin=PIPE,
                  stderr=STDOUT)
        try:
            stdout, stderr = p.communicate(input=input_data, timeout=20,
                                           **kwargs)
        except TimeoutExpired:
            p.kill()
            stdout, stderr = p.communicate()
        assert p.returncode == 0, LOGGER.error(stderr)

        return stdout.decode('utf-8')

    @staticmethod
    def test_answers(expected_list, answer_list, word_pattern=False):
        '''
        Compares students answers with expected ones.
        '''
        message = ''
        LOGGER.debug(f'expected: {expected_list}')
        for answer in expected_list:
            pattern = f'\\b{answer[0]}\\b' if word_pattern else answer[0]
            LOGGER.debug(f'pattern: {pattern}')
            matched = False
            answers = answer_list if word_pattern else answer_list.splitlines()
            for line in answers:
                LOGGER.debug(f'line: |{line}|')
                if re.search(pattern, line, re.MULTILINE):
                    LOGGER.debug("MATCHED")
                    matched = True
                    break
            if not matched:
                message += '\n' + answer[1]
        assert len(message) == 0, LOGGER.warning(message)

    def set_student_file(self, file):
        self.student_file = os.path.join(str(HOME), file)


@pytest.fixture
def helpers():
    return Test_helpers()
