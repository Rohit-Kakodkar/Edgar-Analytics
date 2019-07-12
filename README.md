# Insight data engineering coding challend
This project is part of insight data engineering coding challenge

# Repository Structure

    ├── README.md
    ├── run.sh
    ├── unittesting.py
    ├── src
    │   └── sessionization.py
    |   test
        ├── input
        │   └── inactivity_period.txt
        │   └── log.csv
        ├── output
        |   └── sessionization.txt
    ├── insight_testsuite
        └── run_tests.sh
        └── tests
            └── test_1
            |   ├── input
            |   │   └── inactivity_period.txt
            |   │   └── log.csv
            |   |__ output
            |   │   └── sessionization.txt

# Installation and run

clone this repository using `git@github.com:Rohit-Kakodkar/Edgar-Analytics.git`
Run the code using `python src/sessionization.py --log_file <log_file> --inactivity_file <inactivity_file> --sessionization_file <sessionization_file>` example run script is provided in `run.sh`

# Implementation

Read the log file line by line to create a hash map with ip-adress as the key. Store the read data in queue which will be used to track expiry time. dequeue the queue after certain expiry time to check if the hash map has the same expiry time, in which case write the log to the sessionization file.

# Future considerations
In case of very high frequency log files the data can be streamed through kafka into spark which calculates the expiry time the metrics.
