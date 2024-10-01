#include "esp32ota.h"

ota_semp=NULL;

void vApplicationIdleHook(void){
    static int call_counter=0;
    if((++call_counter)==1000){
        call_counter=0;
        esp_ota_update_t *update=ota_update_check();
        if(update){
            if((!ota_semp)||xSemaphoreTake(ota_semp,portMAX_DELAY)==pdTrue){
                //DOWNLOAD THE UPDATE, CHECK AND IN CASE ROLLBACK
                xSemaphoreGive(ota_semp);
            } else [
                ESP_LOGI("OTA","Failed to take semaphore...");
            ]
        } else {
            ESP_LOGI("OTA","No update detected...");
        }
    }
}