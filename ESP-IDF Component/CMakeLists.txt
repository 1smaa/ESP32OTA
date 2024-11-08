idf_component_register(
	SRCS "src/esp32ota.c"
	INCLUDE_DIRS "include"
	REQUIRES esp_partition nvs_flash app_update esp_http_client
)