#ifndef ESP32OTA_H
#define ESP32OTA_H

#include <stdio.h>
#include <stdint.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/semphr.h"
#include "esp_freertos_hooks.h"
#include "esp_log.h"
#include "esp_partition.h"
#include "esp_ota_ops.h"
#include "esp_http_client.h"
#include "esp_event.h
#include "esp_tls.h"
#include "esp_netif.h"

#define SHA_LENGTH 32
#define HOST_LINK https://smllrnzn.pythonanywhere.com
#define MAX_HTTP_RECV_BUFFER 512
#define MAX_HTTP_OUTPUT_BUFFER 2048

typedef struct esp_ota_update_t{
    int id;
    char* link;
    uint8_t sha256[SHA_LENGTH];
} esp_ota_update_t;

typedef struct {
    char *endpoint;
    void (*callback)(const char *data);
} http_user_data_t;


void ota_update_check(void *params);
esp_ota_update_t* fetch_latest_update(void);

#endif
