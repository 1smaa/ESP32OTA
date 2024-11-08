#include "esp32ota.h"
#include "esp_http_client.h"
#include "freertos/projdefs.h"
#include "portmacro.h"

#define CALL_COUNTER_TH 1000

static const char* TAG="HTTP_CLIENT";
static SemaphoreHandle_t ota_sem_comp=NULL;
static uint8_t digest[32];

esp_err_t _http_event_handler(esp_http_client_event_t *evt){
	http_user_data_t *data=evt->user_data;
	switch (evt->event_id) {
        case HTTP_EVENT_ERROR:
        	xSemaphoreGive(ota_sem_comp);
            return ESP_ERR_HTTP_BASE;
        case HTTP_EVENT_ON_CONNECTED:
            break;
        case HTTP_EVENT_ON_DATA:
            if (!esp_http_client_is_chunked_response(evt->client)) {
                ESP_LOGI(TAG, "HTTP_EVENT_ON_DATA, len=%d", evt->data_len);
                 void (*data_callback)(char *, int) = (void (*)(char *, int)) data;
                 data_callback((char*) evt->data,evt->data_len);
            }
            break;
        default:
            ESP_LOGW(TAG, "Unhandled event: %d", evt->event_id);
            break;
    }
    return ESP_OK;
}

void handle_link(char* link,int length){
	//Check for link existence 
	if(length==0){
		xSemaphoreGive(ota_sem_comp);
		return;
	}
}

void fetch_link(char* timestamp,int length){
	//If there is not matching timestamp, signal task completion and return
	if(length==0){
		xSemaphoreGive(ota_sem_comp);
		return;
	}
	//Create request string buffer
	static char req_url[64]="HOST_LINK/link";
	// Create request for link
	char json_data[64];
	// Check for entity id macro declaration
	#ifndef ENTITY_ID
		#define ENTITY_ID 1
	#endif
	// Create json data string and memorize its length inside the variable ll
	int ll=sprintf(json_data,"{\"id\":%d,\"timestamp\":%s}",ENTITY_ID,timestamp);
	// Client configuration specification
	esp_http_client_config_t config={
		.url=req_url,
		.method=HTTP_METHOD_POST,
		.user_data=(void*)handle_link,
		.event_handler=_http_event_handler
	};
	// Initialization of the client
	esp_http_client_handle_t client=esp_http_client_init(&config);
	// Set POST data
	esp_http_client_set_post_field(client,json_data,ll);
	// Perform request and leave the rest to the event handler
	esp_http_client_perform(client);
}

void elab_digest(char* dg,int length){
	//If the 2 sha256 digests match, there is no new update available, give up the semaphore to signal task completion
	if(strcmp((char*)digest,dg)==0){
		xSemaphoreGive(ota_sem_comp);
		return;
	}
	//Otherwise proceed with update procedure by requesting the latest update timestamp
	static char req_url[64];
	sprintf(req_url,"HOST_LINK/timestamps?id=ENTITY_ID&last=1");
	esp_http_client_config_t config={
		.url=req_url,
		.method=HTTP_METHOD_GET,
		.user_data=(void*)fetch_link,
		.event_handler=_http_event_handler
	};
	esp_http_client_handle_t client=esp_http_client_init(&config);
	esp_http_client_perform(client);
}



void check_digest(int id){
	//Create buffer to store link
	static char req_url[64];
	sprintf(req_url,"HOST_LINK/fetchlatest?id=%d",id);
	//Create request configuration by passing the correct callback function
	esp_http_client_config_t config={
		.url=req_url,
		.method=HTTP_METHOD_GET,
		.user_data=(void*)elab_digest,
		.event_handler=_http_event_handler
	};
	//Perform the request with a blocking function call
	esp_http_client_handle_t client=esp_http_client_init(&config);
	esp_http_client_perform(client);
}

//Function to check for updates
void ota_update_check(void *params){
	if (ota_sem_comp == NULL) {
        ota_sem_comp = xSemaphoreCreateMutex(); // Create a mutex if it hasn't been created yet
        if (ota_sem_comp == NULL) {
            ESP_LOGE(TAG, "Failed to create mutex");
            vTaskDelete(NULL); // Delete the task if semaphore creation failed
            return;
        }
    }
	//Get current partition digest
	const esp_partition_t *running_partition=esp_ota_get_running_partition();
	ESP_ERROR_CHECK(esp_partition_get_sha256(running_partition,digest));
	//Check for ENTITY_ID macro declaration, otherwise default to 1
	int id;
	#ifndef ENTITY_ID
		#define ENTITY_ID 1
	#endif 
	//Take semaphore to prevent task from being deleted prematurely
	xSemaphoreTake(ota_sem_comp,portMAX_DELAY);
	//Start the request "chain"
	check_digest(ENTITY_ID);
	//Wait for semaphore to be available
	while(xSemaphoreTake(ota_sem_comp,portMAX_DELAY)==pdFALSE) vTaskDelay(100/portTICK_PERIOD_MS);
    vTaskDelete(NULL); //Delete current task when finished
}


void vApplicationIdleHook(void){
	//Declares static variable to track number of hook calls
    static int call_counter=0;
    //If the threshold has been reached, enter
    if((++call_counter)==CALL_COUNTER_TH){
		printf("Check...");
        call_counter=0; //Reset the counter
        xTaskCreate( // Create the task to asynchronously check for updates ( the hook should not be stack-heavy )
			ota_update_check,
			"UpdateTask",
			2048,
			NULL,
			1,
			NULL
		);
    } 
}