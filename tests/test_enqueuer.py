import pytest
from pps import logic
from pps import config
import flexmock
import os


@pytest.mark.parametrize(
    ['a', 'b', 'f'],
    [(420, 595, "A5"),
     (595, 420, "A5"),
     (595, 842, "A4"),
     (842, 595, "A4"),
     (842, 1191, "A3"),
     (200, 200, config.PPS_CONFIG.UNKNOWN_PAPER_FORMAT)]
)
def test_get_format_from_size(a, b, f):
    out = logic.get_format_from_size(a, b)
    assert out == f

@pytest.mark.parametrize(
    ['file', 'output_to_test'],
     [("not_existing_", config.PPS_CONFIG.UNKNOWN_PRINT_JOB_NAME),
      ("A4.test", 'Document')])
def test_get_job_name(file, output_to_test):
    fake = flexmock(critical=lambda message: None)
    path = os.path.dirname(os.path.abspath(__file__)) + "/fixtures/"
    full_path_file = path + file
    out = logic.get_print_job_name(full_path_file, fake)
    assert out == output_to_test


def test_get_print_job_name():
    fake = flexmock(critical=lambda message: None)
    file = 'jj.log'
    out = logic.get_print_job_name(file, fake)
    assert out == config.PPS_CONFIG.UNKNOWN_PRINT_JOB_NAME


def test_get_file_format():
    fake = flexmock(critical=lambda message: None)
    out = logic.get_file_format("aa", "aa", fake)
    assert out == config.PPS_CONFIG.UNKNOWN_PAPER_FORMAT


@pytest.mark.parametrize(
    ['file', 'format_to_test'],
    [("A4.test", "A4")]
)
def test_get_file_format(file, format_to_test):
    path = os.path.dirname(os.path.abspath(__file__)) + "/fixtures/"
    fake = flexmock(critical=lambda message: None)
    out = logic.get_file_format(path, file, fake)
    assert out == format_to_test


@pytest.mark.parametrize(
    ['file', 'page_count_to_test'],
    [("A4_4.test", "4"),
     ("A4.test", "1"),
     ("Not_existing_file", config.PPS_CONFIG.UNKNOWN_PAGE_COUNT)]
)
def test_get_number_of_pages(file, page_count_to_test):
    path = os.path.dirname(os.path.abspath(__file__)) + "/fixtures/"
    full_path = path + file
    fake = flexmock(critical=lambda message: None)
    out = logic.get_number_of_pages(full_path, fake)
    assert out == page_count_to_test


@pytest.mark.parametrize(
    ['file', 'print_job_to_test'],
    [("Not_existing_file", config.PPS_CONFIG.UNKNOWN_PRINT_JOB_ID)]
)
def test_get_print_job_id(file, print_job_to_test):
    path = os.path.dirname(os.path.abspath(__file__)) + "/fixtures/"
    full_path = path + file
    fake = flexmock(critical=lambda message: None)
    out = logic.get_print_job_id(full_path, fake)
    assert out == print_job_to_test



