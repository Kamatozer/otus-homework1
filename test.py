import log_analyzer


def test_file_gz():
    pass


def test_file_plain():
    pass


def test_add_new_url():
    url = 'test_url'
    time = 100
    report_list = []
    log_analyzer.add_new_url(url, time, report_list)
    assert report_list == [{
        'url': 'test_url',
        'count': 1,
        'count_perc': 0,
        'time_avg': 100,
        'time_max': 100,
        'time_med': [100],
        'time_perc': 0,
        'time_sum': 100
                            }], f'report_list: {report_list}\n' \
                                f'should be [{{\'url\': \'test_url\', \'count\': 1, \'count_perc\': 0, ' \
                                f'\'time_avg\': 100, \'time_max\': 100, \'time_med\': [100], \'time_perc\': 0, ' \
                                f'\'time_sum\': 100}}]'


def test_count_time():
    pass


def test_median():
    pass


def test_config_load():
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
    test_add_new_url()
    print("Everything passed")
