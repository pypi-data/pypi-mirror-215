from zenodoclient.catalog import Deposits


def test_Deposits(tmp_path, TestEntity):
    p = tmp_path / 'catalog.json'
    with Deposits(p) as d:
        d.add(TestEntity(test='y'))

    with Deposits(p) as d2:
        assert 'x' in d2.objects
