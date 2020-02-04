import pytest
from pps import enqueuer
import flexmock
from pps import config


@pytest.mark.parametrize(
    ['a', 'b', 'f'],
    [(420, 595, "A5"),
     (595, 420, "A5"),
     (595, 842, "A4"),
     (842, 595, "A4"),
     (842, 1191, "A3"),
     (200, 200, config.PPS.UNKNOWN_PAPER_FORMAT)]
)
def test_get_format_from_size(a, b, f):
    out = enqueuer.get_format_from_size(a, b)
    assert out == f


def test_get_job_name():
    fake = flexmock(critical=lambda message: None)
    file = 'jj.log'
    with pytest.raises(FileNotFoundError) as e_info:
        enqueuer.get_job_name(file)


def test_get_print_job_name():
    fake = flexmock(critical=lambda message: None)
    file = 'jj.log'
    out = enqueuer.get_print_job_name(file, fake)
    assert out == "___"


def test_get_file_format():
    fake = flexmock(critical=lambda message: None)
    out = enqueuer.get_file_format("aa", "aa", fake)
    assert out == config.PPS.UNKNOWN_PAPER_FORMAT


def test_get_file_format():
#     TODO test
    pass

