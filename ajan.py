#include "LoRa_E22.h"

// --- E22 LORA MODÜLÜ PİNLERİ (Serial2) ---
// (Senin kendi kartındaki fiziksel pin dizilimi)
#define E22_RX 23  // ESP'nin RX2'si -> E22'nin TXD'si
#define E22_TX 22  // ESP'nin TX2'si -> E22'nin RXD'si
#define AUX_PIN 18 
#define M0_PIN 19
#define M1_PIN 21

LoRa_E22 e22ttl(&Serial2, AUX_PIN, M0_PIN, M1_PIN); 
Configuration globalConfig;
bool ayarBasarili = false;

void setup() {
  // Bilgisayar Ekranı (Loglar)
  Serial.begin(115200); 
  delay(1500);

  // E22 Modül Hattı
  Serial2.begin(9600, SERIAL_8N1, E22_RX, E22_TX);
  e22ttl.begin();
  delay(1000);
  
  Serial.println("\n=================================================");
  Serial.println("[AJAN ESP] Telsiz Hattindan (LoRa) Emirler Dinleniyor...");
  Serial.println("=================================================");

  ResponseStructContainer c = e22ttl.getConfiguration();
  if (c.status.code == 1) {
    globalConfig = *(Configuration*) c.data;
    ayarBasarili = true;
    
    // Modülü normal haberleşme (Alıcı) moduna al
    e22ttl.setMode(MODE_0_NORMAL);
    Serial.print("[OK] Ajan Kablosuz Dinlemede! Aktif Kanal: ");
    Serial.println(globalConfig.CHAN);
    c.close();
  } else {
    Serial.println("[HATA] E22 Modulucevap vermiyor! Pinleri kontrol et.");
  }
}

void kanalDegistir(int yeniKanal) {
  if (!ayarBasarili) return;
  
  Serial.println("\n🚨 [ALARM] Havadan Kacis Emri Yakalandi!");
  Serial.print(">>> Yeni Guvenli Kanal Ayarlaniyor: ");
  Serial.println(yeniKanal);

  // Yeni Kanala Sıçra
  globalConfig.CHAN = yeniKanal;
  e22ttl.setConfiguration(globalConfig, WRITE_CFG_PWR_DWN_LOSE);
  
  // Tekrar Alıcı Moduna Dön
  e22ttl.setMode(MODE_0_NORMAL);
  delay(50); 
  
  Serial.println(">>> [BAŞARILI] Frekans Kaydirildi. Yeni guvenli kanalda bekliyorum.\n");
}

void loop() {
  // ARTIK KABLO DEĞİL, HAVADAKİ SİNYALİ DİNLİYORUZ
  if (e22ttl.available() > 0) {
    // Havadan gelen mesaj paketini yakala
    ResponseContainer rc = e22ttl.receiveMessage();
    
    if (rc.status.code == 1) {
      String komut = rc.data;
      komut.trim(); 
      
      Serial.print("[TELSİZDEN GELEN RAW]: ");
      Serial.println(komut);
      
      // Komut "SHIFT_" ile başlıyorsa frekansı kaydır
      if (komut.startsWith("SHIFT_")) {
        int hedefKanal = komut.substring(6).toInt();
        kanalDegistir(hedefKanal);
      }
    }
  }
}
