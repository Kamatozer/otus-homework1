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
    test_count_time()
    test_median()
    print("Everything passed")
