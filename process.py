#!/usr/bin/python
import json
import re
import codecs
import ast

class FILE_HANDELER(object):
    def __init__(self):
        self.files = ["status"]
        self.status = {
            'x': 0,
            'y': 1,
            'z': 2
        }

    def _read_file(self, filename, start, end):
        try:
            file = open("datasource/"+filename,"r")
            contents = file.read()
            self.status = ast.literal_eval(contents)
            file.close()
            return True
        except Exception, ex:
            return str(ex)

    def _valid_file(self, name):
        file_name = re.split(r'\s',name)
        valid = False
        for file in self.files:
            if(re.search(file,file_name[0])):
                valid = True
        return valid
