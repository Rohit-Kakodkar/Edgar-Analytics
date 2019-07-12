import argparse
from datetime import datetime, timedelta
import sys
from queue import Queue


def parse_args():
    '''
        Parse command line arguments
    '''
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--log_file', type=str, default='log_file.csv',\
                                help='name of the log file')
    parser.add_argument('--inactivity_file', type=str, default= 'inactivity_file.txt', \
                                    help='name of the inactivity file')
    parser.add_argument('--sessionization_file', type=str, default='sessionization.csv', \
                                help='name of the sessionization file')
    args = parser.parse_args()

    return args

def parse_inactivity_file(inactivity_file):
    '''
        parse inactivity time from inactivity file

            input : inactivity file
            output : inactivity time in seconds
    '''
    try:
        f = open(inactivity_file, 'r')
        try:
            inactivity_time = int(f.readline())
        except ValueError:
            sys.exit('Unable to parse ' + inactivity_file)
    except FileNotFoundError:
        sys.exit(inactivity_file + ' not found')
    except IOError : # file doesnt have write permissions
        sys.exit(inactivity_file + ' not accessible')
    except:
        sys.exit('Unable to open ' + inactivity_file)

    return inactivity_time

def calculate_session_end_time(start_time, inactivity_time):
    '''
        calculate session end time

        input: session last request time
        endtime: session end time
    '''

    return (start_time + timedelta(seconds = inactivity_time))


def parse_log_line(line):
    '''
        parse one line of log file
    '''
    record = line.rstrip('\n').split(',')

    if len(record)!=15:
        return None

    ip_addess = record[0]
    try:
        log_datetime = datetime.strptime((record[1] + ' ' + record[2]), '%Y-%m-%d %H:%M:%S')
    except ValueError:
        return None

    return ip_addess, log_datetime


def parse_log_file(log_file, inactivity_time, sessionization_file):
    '''
        Parse log file and calculate matrics to write to sessionization_file
    '''

    file = open(log_file)

    file.readline() # bypass header line

    number_of_corrupted = 0
    session_dict = {}
    q = Queue()

    first_time = True
    start_getting = False
    for line in file:
        try:
            ip_addess, log_datetime = parse_log_line(line)
        except TypeError:
            number_of_corrupted += 1
            continue

        if first_time:
            start_time = log_datetime

        if (start_time + timedelta(seconds = inactivity_time)) <= log_datetime:
            start_getting = True

        q.put((ip_addess, log_datetime))

        if start_getting:
            expired_ip, expired_log_time = q.get()
            if ((expired_log_time + timedelta(seconds = 2)) == session_dict[expired_ip][2]):
                with open(sessionization_file, 'a') as f:
                    f.write('%s,%s,%s,%i,%i\n' % (expired_ip, session_dict[expired_ip][1], (session_dict[expired_ip][2] - timedelta(seconds = inactivity_time)),\
                                        (session_dict[expired_ip][2] - timedelta(seconds = inactivity_time -1) - session_dict[expired_ip][1]).total_seconds(), session_dict[expired_ip][0]))
                session_dict.pop(expired_ip)

        try :
            session_dict[ip_addess][0] += 1
            session_dict[ip_addess][2] = calculate_session_end_time(log_datetime, inactivity_time)
        except KeyError:
            session_dict[ip_addess] = [1.0, log_datetime, calculate_session_end_time(log_datetime, inactivity_time)]



        first_time = False

    with open(sessionization_file, 'a') as f:
        for ip_addess in session_dict:
            f.write('%s,%s,%s,%i,%i\n' % (ip_addess, session_dict[ip_addess][1], (session_dict[ip_addess][2] - timedelta(seconds = inactivity_time)),\
                                (session_dict[ip_addess][2] - timedelta(seconds = inactivity_time -1) - session_dict[ip_addess][1]).total_seconds(), session_dict[ip_addess][0]))

if __name__ == '__main__':
    '''
        Driver
    '''

    args = parse_args()

    log_file = args.log_file
    inactivity_file = args.inactivity_file
    sessionization_file = args.sessionization_file

    inactivity_time = parse_inactivity_file(inactivity_file)
    parse_log_file(log_file, inactivity_time, sessionization_file)
