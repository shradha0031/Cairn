from app.crism import read_crism_product


def _header(tmp_path, origin_x: float, origin_y: float) -> str:
    path = tmp_path / "sample_mtr3.hdr"
    path.write_text(
        """ENVI
samples = 10
lines = 10
bands = 4
map info = {MRO Mars Equirectangular [15.00N; 0.00E], 1.0000, 1.0000, %s, %s, 18.0, 18.0, D_Mars_2000_IAU_IAG_custom_sphere_lat15, units=Meters}
""" % (origin_x, origin_y),
        encoding="utf-8",
    )
    return str(path)


def test_reads_product_dimensions_and_footprint(tmp_path) -> None:
    product = read_crism_product(_header(tmp_path, 4430000, 1100000))

    assert product.samples == 10
    assert product.lines == 10
    assert product.bands == 4
    assert product.footprint.east > product.footprint.west


def test_rejects_non_jezero_footprint(tmp_path) -> None:
    product = read_crism_product(_header(tmp_path, 4428386.8, 1107292.6))

    assert product.footprint.overlaps_jezero is False
