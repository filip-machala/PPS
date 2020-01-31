import pytest
from pps import enqueuer


@pytest.mark.parametrize(
    [420, 595, "A5"],
    # [595, 842, "A4"],
    # [842, 1191, "A3"],
    # [200, 200, "XXX"]
)
def test_get_format_from_size(a ,b , format):
    out = enqueuer.get_format_from_size(a,b)
    assert out == format