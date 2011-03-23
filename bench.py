#!/usr/bin/env python

import time
import anyjson
import demjson

if __name__ == "__main__":
    libraries = {}
    with open("data.json", "r") as data_file:
        data = data_file.read()
    python_obj = demjson.decode(data)
    json_string = demjson.encode(python_obj)
    del data
    for implementation in anyjson._modules:
        name = implementation[0]
        try:
            anyjson.force_implementation(name)
        except:
            continue
        for func, data, action in [(anyjson.serialize, python_obj, 'encode'),
                                  (anyjson.deserialize, json_string, 'decode')]:
            runs = []
            try:
                for i in range(10):
                    start_time = time.time()
                    func(data)
                    finish_time = time.time()
                    runs.append(finish_time - start_time)
            except:
                del runs
                method = "%s %s:" % (name, action)
                print "%s\tERROR" % method.ljust(20)
                continue
            average = float(sum(runs) / len(runs))
            del runs
            method = "%s %s:" % (name, action)
            print "%s\t%f seconds" % (method.ljust(20), average)
