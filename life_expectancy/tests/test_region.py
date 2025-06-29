from life_expectancy.region import Region


def test_region_countries_excludes_aggregates():
    regions = Region.countries()

    # Check que só há valores do tipo Region
    assert all(isinstance(r, Region) for r in regions)

    # Check que valores agregados não estão incluídos
    excluded = {
        Region.DE_TOT,
        Region.EU27_2020,
        Region.EU27_2007,
        Region.EU28,
        Region.EEA30_2007,
        Region.EEA31,
        Region.EFTA,
        Region.EA18,
        Region.EA19,
    }
    for region in excluded:
        assert region not in regions

    # E.g. Portugal deve estar incluído
    assert Region.PT in regions
