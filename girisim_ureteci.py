#include "LoRa_E22.h"

#define RX_PIN 16  
#define TX_PIN 17  
#define AUX_PIN 18 
#define M0_PIN 19
#define M1_PIN 21

LoRa_E22 e22ttl(&Serial2, AUX_PIN, M0_PIN, M1_PIN); 

// FHSS Atlama Noktaları: Kanal 10 (860MHz), Kanal 40 (890MHz), Kanal 70 (920MHz)
int fhss_kanallari[] = {10, 40, 70};
int kanal_index = 0;

Configuration globalConfig; 
bool ayarBasarili = false;

void setup() {
  Serial.begin(115200);
  delay(1500); 

  Serial2.begin(9600, SERIAL_8N1, RX_PIN, TX_PIN);
  e22ttl.begin();
  
  Serial.println("\n[SETUP] FHSS Girisim Ureteci basliyor...");

  ResponseStructContainer c = e22ttl.getConfiguration();
  if (c.status.code == 1) {
    globalConfig = (Configuration) c.data;
    ayarBasarili = true;
    c.close();
    Serial.println("[OK] FHSS Dinamik Atlama Aktif!");
  } else {
    Serial.println("[HATA] Modül okunamadı.");
  }
}

void loop() {
  if (!ayarBasarili) return;

  // 1. FHSS Dizisindeki Aktif Kanalı Seç ve Ayarla
  int aktif_kanal = fhss_kanallari[kanal_index];
  globalConfig.CHAN = aktif_kanal;
  e22ttl.setConfiguration(globalConfig, WRITE_CFG_PWR_DWN_LOSE);
  
  // 2. Modülü Yayına Uyandır
  e22ttl.setMode(MODE_0_NORMAL);
  delay(50); 

  Serial.print("[FHSS GIRISIM] Test sinyali gonderiliyor - Aktif Kanal: ");
  Serial.println(aktif_kanal);

  // 3. 1.5 Saniye Boyunca Kanala Test Gürültüsü Bas
  unsigned long baslangic = millis();
  while (millis() - baslangic < 1500) {
    Serial2.print("TEST_");
    delay(20);
  }

  // 4. Sıradaki FHSS Frekansına Atla
  kanal_index = (kanal_index + 1) % 3; 
}
