# GRASS
Repository structure:
* green_web_foundation/
* caida/
* geolocate/
* as2co2_mapping/
* Calculate_N/
Step 1 - Green Web Foundation Data Download the CO2 intensity dataset from The Green Web Foundation and add it to the corresponding folder: wget https://github.com/thegreenwebfoundation/co2.js/blob/main/data/output/average-intensities.json
Step 2 - AS Geolocation
2.1 Download CAIDA and PeeringDB Data wget https://publicdata.caida.org/datasets/peeringdb-v2/2025/05/peeringdb_2_dump_2025_05_01.json wget https://publicdata.caida.org/datasets/as-relationships/serial-2/20250501.as-rel2.txt.bz2 bunzip2 20250501.as-rel2.txt.bz2
2.2 Run geolocation scripts python3 geolocate_ases_via_peeringdb.py Output: geolocate/output/presence_per_AS_peeringdb_may_2025.json
python3 geolocate_ases_via_prefix.py Output: geolocate/output/presence_per_AS_maxmind_may_2025.json
2.3 Map PoPs to ASNs python3 map_pops_to_ases.py Input: ../caida/peeringdb_2_dump_2025_05_01.json Output: output/asn_per_pop_map_may_2025.json and output/pop_per_asn_map_may_2025.json
2.4 Map ASNs to CO2 Intensities python3 map_co2_to_asn.py Output: as2co2_mapping/output/as2co2_intensity_may_2025.json
Step 3 - Link Extraction
3.1 Download Team Cymru Bogon Lists wget https://www.team-cymru.org/Services/Bogons/fullbogons-ipv4.txt wget https://www.team-cymru.org/Services/Bogons/fullbogons-ipv6.txt
3.2 Collect BGP Path Data python3 bgp_path_collector.py Output: ribs/_ribs.csv (for example 2025-05-01_ribs.csv)
3.3 Extract Prefix Paths python3 extract_prefix_paths.py Input: ../ribs/2025-05-01_ribs.csv Output: 2025-05-01_prefixes_aspaths.csv
Step 4 - RouteViews Data and Prefix Processing
4.1 Download RouteViews datasets wget https://publicdata.caida.org/datasets/routing/routeviews-prefix2as/2025/05/routeviews-rv2-20250501-1200.pfx2as.gz wget https://publicdata.caida.org/datasets/routing/routeviews6-prefix2as/2025/05/routeviews-rv6-20250501-1200.pfx2as.gz gunzip routeviews-rv2-20250501-1200.pfx2as.gz gunzip routeviews-rv6-20250501-1200.pfx2as.gz
4.2 Filter Prefix Paths python3 getprefixes.py Inputs: ../routeviews-rv2-20250501-1200.pfx2as ../routeviews-rv6-20250501-1200.pfx2as 2025-05-01_prefixes_aspaths.csv Output: 2025-05-01_filtered_prefixes_aspaths.csv
4.3 Count AS Links python3 count_links.py Input: 2025-05-01_filtered_prefixes_aspaths.csv Output: 2025-05-01_as_links_count.csv
Step 5 - Link-Level CO2 Emissions python3 c02emissions_links_extended_countversion.py Inputs: geolocate/output/presence_per_AS_peeringdb_may_2025.json geolocate/output/presence_per_AS_maxmind_may_2025.json green_web_foundation/gwf_average-intensities_last_updated_may_2025.json caida/20250501.as-rel2.txt Calculate_N/2025-05-01_as_links_count.csv Output: as_link_emissions_may_2025.csv
Final outputs:
* geolocate/output/presence_per_AS_peeringdb_may_2025.json: AS geolocation via PeeringDB
* geolocate/output/presence_per_AS_maxmind_may_2025.json: AS geolocation via prefix mapping
* as2co2_mapping/output/as2co2_intensity_may_2025.json: CO2 intensity per AS
* Calculate_N/2025-05-01_as_links_count.csv: AS link frequency counts
* as_link_emissions_may_2025.csv: Final CO2 emissions per AS link
Notes: All datasets are publicly available and regularly updated. Ensure all paths are correct relative to your local folder structure. Scripts are written for Python 3.8 or later. Outputs can be visualized or aggregated for sustainability metrics at the network or country level.
