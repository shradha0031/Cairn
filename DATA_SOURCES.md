# Cairn data sources

Cairn uses one site only: a small working area in Jezero Crater. A source listed below is not considered bundled or production-ready until the team verifies the selected product, download method, attribution requirements, and terms of use.

## Current demo fixture

The initial app uses a synthetic Jezero Crater fixture so the application runs end to end while the real products are checked. It is not scientific data and must not be presented as an official NASA measurement.

Planned local placeholder: `backend/data/sample_elevation.tif` after terrain-processing work begins. If created, it must be labelled synthetic in the data README and application UI until replaced by a verified product.

## Assigned resources

| Resource | URL | Role in Cairn | Status and terms |
| --- | --- | --- | --- |
| JPL Mars Trek | https://trek.nasa.gov/mars/ | **Currently integrated:** Mars Viking MDIM21 color mosaic imagery is used as the Leaflet base layer. Planned next: verified Jezero elevation for slope computation. Verify which layers and downloads exist before relying on them, especially temperature. | Imagery tile template observed on the Mars Trek page and used with `Mars Trek / NASA` attribution. Verify current access, attribution, and terms before deployment or redistribution. |
| USGS-NASA Planetary Geologic Mapping | https://astrogeology-usgs.hub.arcgis.com/pages/interactive-maps-mars | Geologic units used to distinguish firm and loose ground for hazard penalties, and to locate science stops such as river channels, delta deposits, and rock units. | Research target. Verify the selected map product, service access, attribution, and redistribution terms. |
| Mars Perseverance Raw Images | https://mars.nasa.gov/mars2020/multimedia/raw-images/ | **Currently integrated:** one NASA Perseverance Mastcam-Z preview is shown for the Delta deposit stop. It is a visual context preview only and is not georegistered to the synthetic stop. | NASA image asset: `ZL0_2024_0846622583_145EBY_N0930000ZCAM10058_1100LMJ02_320.jpg`. Keep the source-page link and image identifier with the demo attribution. |
| Curiosity's proposed path up Mount Sharp | https://science.nasa.gov/resource/curiositys-proposed-path-up-mount-sharp/ | Design reference for presenting routes, stops, and labelled science regions. | Reference only. Not a Jezero dataset and never used for route computation. |
| NASA Worldview | https://worldview.earthdata.nasa.gov/ | Inspiration only for layer menus and time-based layer controls. | Not a Cairn data source. Do not use it as an input dataset. |

## Additional mineral source under evaluation

| Resource | URL | Role in Cairn | Status and terms |
| --- | --- | --- | --- |
| MRO CRISM Map-projected Targeted Reduced Data Record v1.0 | https://pds.nasa.gov/ds-view/pds/viewDataset.jsp?dsid=MRO-M-CRISM-5-RDR-MPTARGETED-V1.0 | Candidate mineral evidence for science stops. The archive contains map-projected CRISM multiband image cubes and value-added mineral-signature products from targeted Mars Reconnaissance Orbiter observations. | NASA PDS dataset, DOI [10.17189/1519470](https://doi.org/10.17189/1519470). Product `frt000047a3_07_if166j_mtr3` was inspected locally: its header footprint is approximately 14.75-15.00 N, 77.38-77.64 E, outside Jezero, so it is **not used** by Cairn. Select a product whose footprint overlaps Jezero before integration. |

Official access paths listed by the dataset page include [PDS Geosciences Web Services](http://pds-geosciences.wustl.edu/missions/mro/crism.htm), [Mars Orbital Data Explorer](http://ode.rsl.wustl.edu/mars), and the [Geosciences Online Archive](http://pds-geosciences.wustl.edu/mro/mro-m-crism-5-rdr-mptargeted-v1/mrocr_4001/).

## Data types

- **Topographic:** Mars Trek elevation; Cairn computes slope from elevation.
- **Geologic:** USGS-NASA terrain and geologic units; Cairn applies ground penalties and identifies science regions.
- **Optical:** Mars Trek imagery and Perseverance raw-image previews.
- **Mineralogical:** CRISM map-projected targeted products, once a Jezero observation and mineral-signature product are verified.

Temperature is not included until a real Jezero product is verified. The UI must not imply temperature coverage from an unverified source.
