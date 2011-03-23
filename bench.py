#!/usr/bin/env python

import time
import anyjson
import demjson

if __name__ == "__main__":
    libraries = {}
    with open("data.json", "r") as data_file:
        data = data_file.read()
    print "Creating Python object from JSON data using demjson:",
    start_time = time.time()
    python_obj = demjson.decode(data)
    finish_time = time.time()
    print "Finished in %0.2f seconds." % (finish_time - start_time)
    print "Creating JSON data from Python object using demjson:",
    start_time = time.time()
    json_string = demjson.encode(python_obj)
    finish_time = time.time()
    print "Finished in %0.2f seconds." % (finish_time - start_time)
    del data
    print "Beginning main benchmarks at 14 iterations per operation:\n"
    for implementation in anyjson._modules:
        name = implementation[0]
        if name == 'cjson':
            continue
        try:
            anyjson.force_implementation(name)
        except:
            continue
        for func, data, action in [(anyjson.serialize, python_obj, 'encode'),
                                  (anyjson.deserialize, json_string, 'decode')]:
            runs = []
            method = "%s %s:" % (name, action)
            print "%s\t" % method.ljust(20),
            print "",
            try:
                for i in range(14):
                    print "\b.",
                    start_time = time.time()
                    func(data)
                    finish_time = time.time()
                    runs.append(finish_time - start_time)
            except:
                del runs
                print "ERROR"
                continue
            average = float(sum(runs) / len(runs))
            del runs
            print "\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b%0.4f seconds" % average
