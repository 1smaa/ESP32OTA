#ifndef ESP32OTA_H
#define ESP32OTA_H

#include <stdio.h>
#include <stdint.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/semphr.h"
#include <esp_ota_ops.h>
#include <esp_http_client.h>
#include "esp_https_ota.h"

extern SemaphoreHandle_t ota_semp;

typedef struct esp_ota_update_t{
    int id;
    char* link;
    uint8_t sha256[32];
} esp_ota_update_t;

esp_ota_update_t* ota_update_check();

void vApplicationIdleHook(void);

#endif