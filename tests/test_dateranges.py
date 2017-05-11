from twitter_analytics import ReportDownloader


def test_split_date_ranges():
    from_date = '01/01/2015'
    to_date = '02/28/2015'
    date_ranges = ReportDownloader.split_date_range_into_91(from_date, to_date)
    print(date_ranges)
    assert len(date_ranges) == 0
