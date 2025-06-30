from life_expectancy.region import Region


def test_region_countries_excludes_aggregates():
    """Test that the countries method of Region excludes aggregate regions."""
    regions = Region.countries()

    # Checks if all regions are instances of Region
    assert all(isinstance(r, Region) for r in regions)

    # Checks if the excluded regions are not in the list
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

    # Checks if PT is in the list of regions
    assert Region.PT in regions
