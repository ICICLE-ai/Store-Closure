#Radius that households look for stores on first search iteration. Units unclear ^^
SEARCHRADIUS = 500

#crs geometry for map (this is web mercator)
CRS = "3857"

#Census codes
FIPSCODE = "39049" #fips code for franklin county ohio - use this to fill in state code and county code below
COUNTYCODE = "049" #code for franklin county
STATECODE = "39" #code for Ohio

#File paths
HOUSEHOLDSFILEPATH = "data/households.csv"
STORESFILEPATH = "data/stores.csv"
COUNTYDATAFILEPATH = "data/county_data.csv"
GEODATAFILEPATH = "data/tract_boundaries.zip"