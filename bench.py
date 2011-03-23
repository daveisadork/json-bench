#!/usr/bin/env python

import time
import anyjson
import demjson

if __name__ == "__main__":
    print "Reading JSON data file into memory:",
    start_time = time.time()
    with open("data.json", "r") as data_file:
        data = data_file.read()
    finish_time = time.time()
    print "Read %0.2fMiB in %0.2f seconds." % (len(data) / 1024.0 / 1024.0, finish_time - start_time)
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
    print "Beginning main benchmarks at 10 iterations per operation:\n"
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
            print "%s[            ]" % method.ljust(19),
            try:
                for i in range(10):
                    print "\b" * 15 + "[ " + "-" * i + " " * (10 - i) + " ]",
                    start_time = time.time()
                    func(data)
                    finish_time = time.time()
                    runs.append(finish_time - start_time)
            except:
                del runs
                print "\b" * 15 + "[    FAIL    ]"
                continue
            average = float(sum(runs) / len(runs))
            average_string = "[ %0.4f sec ] " % average
            del runs
            final = "\b" * 15 + average_string + "=" * int(average * 100.0 / 4.0)
            if len(final) > 75:
                final = final[:74] + "+"
            print final
