echo "Forcing ckan.uploads_enabled = true"
ckan config-tool $CKAN_INI "ckan.uploads_enabled = true"

echo "Forcing ckan.storage_path = /var/lib/ckan"
ckan config-tool $CKAN_INI "ckan.storage_path = /var/lib/ckan"

echo "Forcing ckan.requests.timeout = 300"
ckan config-tool $CKAN_INI "ckan.requests.timeout = 300"

echo "Forcing ckan.requests.timeout = 300"
ckan config-tool $CKAN_INI "ckan.locale_default = pt_BR"

echo "Forcing ckan.views.default_views = image_view text_view datatables_view geo_view geojson_view shp_view"
ckan config-tool $CKAN_INI "ckan.views.default_views = image_view text_view datatables_view geo_view geojson_view shp_view"

echo "Forcing ckanext.spatial.common_map.type = OpenStreetMap.Mapnik"
ckan config-tool $CKAN_INI "ckanext.spatial.common_map.type = OpenStreetMap.Mapnik"
