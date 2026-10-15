# cognitive-cuas

Önce kontrollü bir RF girişim senaryosu kurdum, sonra o girişim altında bağlantısını koruyabilen sistemi de kendim yaptım. Test sinyalini de savunmayı da tek elden tasarladım.

Küçük ölçekli bir **C-UAS / RF spektrum izleme** döngüsü — gerçek RF donanımıyla, uçtan uca:

**tespit → karar → otonom frekans kaydırma**

---

## Ne yapıyor

-  **Girişim Üreteci** (`girisim_ureteci.py` / ESP32 + LoRa E22) — kontrollü test amacıyla 868 MHz kanalını sinyal doygunluğuna getirir. Test tarafı.
-  **Kognitif Radar** (`akbaba.py` / Raspberry Pi 4 + RTL-SDR) — RF ortamını dinler, ham IQ verisini Python'da FFT ile analiz eder, güç spektral yoğunluğunu hesaplar ve girişimi milisaniyeler içinde tespit eder.
-  **Otonom Ajan** (`ajan.py` / ESP32 + LoRa) — radardan gelen frekans kaydırma emrini alır, sistemi temiz banda taşır. Link kopmaz.

---

## Donanım

- Raspberry Pi 4B
- RTL-SDR Blog V3
- Waveshare SX126x LoRa HAT
- ESP32 (S3 + WROOM-32)
- Ebyte E22-900T22D LoRa modülleri

---

## En büyük mühendislik problemi

Girişim aktifken, frekans kaydırma komutunun kendisi de girişim gürültüsüyle havada çarpışıyordu (packet collision) ve alıcıyı sağırlaştırıyordu. Alıcı tarafında, gürültüye gömülü bozuk paketlerin içinden hedef frekansı çekip çıkaran bir pattern-extraction filtresiyle çözdüm.

---

*Eğitim ve araştırma amaçlı, kontrollü test ortamında.*
