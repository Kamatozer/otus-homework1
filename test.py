import log_analyzer
import argparse


def test_open_gz_plain():
    success_string = b'1.196.116.32 -  - [29/Jun/2017:03:50:22 +0300] "GET /api/v2/banner/25019354 HTTP/1.1" 200 927 "-" "Lynx/2.8.8dev.9 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/2.10.5" "-" "1498697422-2190034393-4708-9752759" "dc7161be3" 0.390\r\n'
    gz_file_path = './tests/test_nginx_logs/nginx-access-ui.log-20170801.gz'
    plain_file_path = './tests/test_nginx_logs/nginx-access-ui.log-20170801.plain'
    gz_file, gz_type = log_analyzer.open_gz_plain(gz_file_path)
    line = gz_file.read() # TODO read 1st line
    assert line == success_string, f'string:\n{line}\nshould be:\n{success_string}'
    assert gz_type == 'gzip', 'should be gzip'


def test_add_new_url():
    url = 'test_url'
    time = 100
    report_list = []
    log_analyzer.add_new_url(url, time, report_list)
    success_report_list = [{
        'url': 'test_url',
        'count': 1,
        'count_perc': 0,
        'time_avg': 0,
        'time_max': 100,
        'time_med': [100],
        'time_perc': 0,
        'time_sum': 100
    }]
    assert report_list == success_report_list, f'report_list: {report_list}\nshould be: {success_report_list}'


def test_count_time():
    test_report_item = {
        'url': 'test_url',
        'count': 12,
        'count_perc': 0,
        'time_avg': 0,
        'time_max': 0.7,
        'time_med': [0.3, 0.7, 0.5],
        'time_perc': 0,
        'time_sum': 1.5
    }
    modified_test_report_item = log_analyzer.count_time(test_report_item, 1.5)
    success_item = {
        'url': 'test_url',
        'count': 13,
        'count_perc': 0,
        'time_avg': 0,
        'time_max': 1.5,
        'time_med': [0.3, 0.7, 0.5, 1.5],
        'time_perc': 0,
        'time_sum': 3.0
    }
    assert modified_test_report_item == success_item, f'report item:\n{modified_test_report_item}\n' \
                                                      f'should be:\n{success_item}'


def test_median():
    test_list = [0.3, 0.7, 0.5, 1.5]
    median = log_analyzer.median(test_list)
    assert median == 0.6, f'median: {median}, should be 0.6'


def test_custom_config_load():
    args1 = argparse.Namespace(config=None)
    args2 = argparse.Namespace(config='./tests/test_config.json')
    args3 = argparse.Namespace(config='./tests/no_file')
    args4 = argparse.Namespace(config='./tests/empty.json')
    args5 = argparse.Namespace(config='./tests/not_full.json')
    test_config1 = log_analyzer.setup_config(args1)
    test_config2 = log_analyzer.setup_config(args2)
    test_config3 = log_analyzer.setup_config(args3)
    test_config4 = log_analyzer.setup_config(args4)
    test_config5 = log_analyzer.setup_config(args5)
    success_config1 = {
        'REPORT_SIZE': 1000,
        'REPORT_DIR': './reports',
        'LOG_DIR': './log',
        'ERR_PERC': 0.3,
        'SCRIPT_LOG': None
    }
    success_config2 = {
        'REPORT_SIZE': 10,
        'REPORT_DIR': './reports',
        'LOG_DIR': './log',
        'ERR_PERC': 0.1,
        'SCRIPT_LOG': './'
    }
    success_config3 = {
        'REPORT_SIZE': 1,
        'REPORT_DIR': './reports',
        'LOG_DIR': './log',
        'ERR_PERC': 0.3,
        'SCRIPT_LOG': None
    }
    assert test_config1 == success_config1, f'config:\n{test_config1}\nshould be:\n{success_config1}'
    assert test_config2 == success_config2, f'config:\n{test_config2}\nshould be:\n{success_config2}'
    assert test_config3 == success_config1, f'config:\n{test_config3}\nshould be:\n{success_config1}'
    assert test_config4 == success_config1, f'config:\n{test_config4}\nshould be:\n{success_config1}'
    assert test_config5 == success_config3, f'config:\n{test_config5}\nshould be:\n{success_config3}'
    pass


def test_find_log():
    pass


def test_get_report_file_name():
    pass


def test_get_report_list():
    pass


def test_report_file():
    pass


if __name__ == "__main__":
    test_open_gz_plain()
    test_add_new_url()
    test_count_time()
    test_median()
    test_custom_config_load()
    print("Everything passed")
