#!/usr/bin/env python
# -*- coding: utf-8 -*-

# log_format ui_short '$remote_addr  $remote_user $http_x_real_ip [$time_local] "$request" '
#                     '$status $body_bytes_sent "$http_referer" '
#                     '"$http_user_agent" "$http_x_forwarded_for" "$http_X_REQUEST_ID" "$http_X_RB_USER" '
#                     '$request_time';

import os
import re
import gzip
import json
import sys
import logging


default_config = {
    "REPORT_SIZE": 1000,
    "REPORT_DIR": "./reports",
    "LOG_DIR": "./log",
    'ERR_PERC': 0.3
}

logger = logging.getLogger('main')
logger.level = logging.DEBUG
formatter = logging.Formatter('[%(asctime)s] %(levelname).1s %(message)s')
formatter.datefmt = '%Y.%m.%d %H:%M:%S'
ch = logging.StreamHandler(sys.stdout)
ch.setFormatter(formatter)
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)


def open_gz_plain(file_name):
    extension = file_name.split('.')[-1]
    if extension == 'gz':
        return gzip.open(file_name), 'gzip'
    else:
        return open(file_name), 'plain'


def add_new_url(url, time, report_list):
    new_report_item = {
        'url': url,
        'count': 1,
        'count_perc': 0,
        'time_avg': time,
        'time_max': time,
        'time_med': [time],
        'time_perc': 0,
        'time_sum': time
    }
    report_list.append(new_report_item)


def count_time(report_item, time):
    modified_report_item = {
        'url': report_item['url'],
        'count': report_item['count'] + 1,
        'count_perc': 0,
        'time_avg': (report_item['time_avg'] + time)/2,
        'time_max': time if time > report_item['time_max'] else report_item['time_max'],
        'time_med': report_item['time_med'].append(time),
        'time_perc': 0,
        'time_sum': report_item['time_sum'] + time
    }
    return modified_report_item


def median(list_: list):
    length = len(list_)
    list_ = sorted(list_)
    if length == 1:
        return list_[0]
    if length % 2 != 0:
        return list_[length // 2]
    else:
        med = (list_[length // 2 - 1] + list_[length // 2]) / 2
        return med


def setup_config():
    config_ = {}
    # check if it is config file in attributes
    if (len(sys.argv)) > 1:
        if sys.argv[1] == '--config':
            try:
                with open(sys.argv[2]) as f:
                    try:
                        config_ = json.load(f)
                    except json.decoder.JSONDecodeError:
                        print('Wrong config format or file empty\nUsing default config')
            except IOError:
                print(f'Could not read file: {sys.argv[2]}\nUsing default config')
    # check is config from file have needed values, if not - use defaults
    if 'REPORT_SIZE' not in config_:
        config_['REPORT_SIZE'] = default_config['REPORT_SIZE']
    if 'REPORT_DIR' not in config_:
        config_['REPORT_DIR'] = default_config['REPORT_DIR']
    if 'LOG_DIR' not in config_:
        config_['LOG_DIR'] = default_config['LOG_DIR']
    if 'ERR_PERC' not in config_:
        config_['ERR_PERC'] = default_config['ERR_PERC']
    if 'SCRIPT_LOG' not in config_:
        config_['SCRIPT_LOG'] = None
    # Set log to file if need
    if config_['SCRIPT_LOG'] is not None:
        fh = logging.FileHandler(config_['SCRIPT_LOG'] + '/' + 'log_analyzer.log')
        fh.setFormatter(formatter)
        fh.setLevel(logging.INFO)
        logger.addHandler(fh)
    return config_


def find_nginx_log_file(config_):
    # search for logs
    file_list = [f for f in os.listdir(config_["LOG_DIR"]) if re.match(r'^nginx-access-ui.log-[0-9]{8}\.[gz|plain]', f)]
    if len(file_list) < 1:
        logger.error(f'No logs in directory {config_["LOG_DIR"]}')
        sys.exit()
    # get last file

    log_file_name = file_list[-1]
    log_file = open_gz_plain(str(config_["LOG_DIR"] + '/' + log_file_name))[0]
    logger.info(f'Reading file: {log_file_name}')
    return log_file, log_file_name


def get_report_file_name(log_file_name_, config_):
    # form report file name
    log_date = re.findall(r'[0-9]', log_file_name_)
    report_file_name_ = 'report-' + log_date[0] + log_date[1] + log_date[2] + log_date[3] + '.' \
                        + log_date[4] + log_date[5] + '.' + log_date[6] + log_date[7] + '.html'
    # check report file from previous launches
    if report_file_name_ in os.listdir(config_['REPORT_DIR']):
        logger.info(f'Report already exist: {report_file_name_}')
        sys.exit()
    return report_file_name_


def get_report_list(log_list):
    # write report list
    report_list_ = []
    count = 0
    total_count = len(log_list)
    total_time = 0
    for log_line in log_list:
        count += 1
        url = log_line[0]
        time = log_line[1]
        total_time += time
        found = False
        sys.stdout.write(f'Calculating values progress:({round((count/total_count)*100, 2)}%)[{count}/{total_count}]\r')
        for report_item in report_list_:
            if report_item['url'] == url:
                # calculate values what we can now
                modified_report_item = count_time(report_item, time)
                report_item['count'] = modified_report_item['count']
                report_item['time_avg'] = modified_report_item['time_avg']
                report_item['time_max'] = modified_report_item['time_max']
                report_item['time_sum'] = modified_report_item['time_sum']
                found = True
                break
        if not found:
            add_new_url(url, time, report_list_)
    # calculate remaining values
    for report_item in report_list_:
        report_item['time_med'] = median(report_item['time_med'])
        report_item['count_perc'] = (report_item['count'] / total_count) * 100
        report_item['time_perc'] = (report_item['time_sum'] / total_time) * 100
    return report_list_


def make_report_file(report_list_, config_, report_file_name_):
    # make report file based on template
    with open('./report.html', 'r') as template_report_file:
        report_html = template_report_file.read()
        report_html = report_html.replace('$table_json', json.dumps(sorted(report_list_[:config_['REPORT_SIZE']],
                                                                           key=lambda i: i['time_sum'], reverse=True)))
    try:
        with open(config_['REPORT_DIR'] + '/report.tmp', 'w+') as report_file:
            report_file.write(report_html)
        os.rename(config_['REPORT_DIR'] + '/report.tmp', config_['REPORT_DIR'] + '/' + report_file_name_)
        logger.info(f'Report {report_file_name_} formed successful')
    except IOError:
        logger.error(f'Smth going wrong:\n {IOError}')


def main(config_):
    log_file, log_file_name = find_nginx_log_file(config_)
    report_file_name = get_report_file_name(log_file_name, config_)
    # parse log from file to list
    log_list = []
    errors_count = 0
    # if read 'log_file' for count lines, this generator exhausted before parse
    log_file_for_count, file_type = open_gz_plain(str(config_["LOG_DIR"] + '/' + log_file_name))
    end_of_string = b'\n' if file_type == 'gzip' else '\n'
    log_length = log_file_for_count.read().count(end_of_string)
    for line in log_file:
        if (errors_count / log_length) > config_['ERR_PERC']:
            logger.error(f'Too much format errors in logfile: {errors_count}')
            sys.exit()
        if type(line) == bytes:
            line = line.decode('utf-8')
        line = line.rstrip()
        if len(line.split('"')) > 12:
            request = line.split('"')[1]
            if len(request.split()) > 1:
                url = request.split()[1]
                time = float(line.split('"')[12])
                log_list.append([url, time])
            else:
                errors_count += 1
        else:
            errors_count += 1
    report_list = get_report_list(log_list)
    make_report_file(report_list, config_, report_file_name)


if __name__ == "__main__":
    try:
        config = setup_config()
        main(config)
    except KeyboardInterrupt:
        logger.error('Aborted')
        sys.exit(2)
