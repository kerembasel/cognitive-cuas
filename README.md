# cognitive-cuas

Sistemi bogdum, sonra ondan kaçan sistemi de kendim yaptım. Saldırıyı da savunmayı da tek elden kurdum.

Küçük ölçekli bir **C-UAS / Electronic Warfare** döngüsü — gerçek RF donanımıyla, uçtan uca:

**tespit → karar → otonom kaçış**

---

## Ne yapıyor

-  **Jammer** (`jammmr.py` / ESP32 + LoRa E22) — 868 MHz kanalını sinyal doygunluğuna boğar. Kırmızı takım.
-  **Kognitif Radar** (`akbaba.py` / Raspberry Pi 4 + RTL-SDR) — RF ortamını dinler, ham IQ verisini Python'da FFT ile analiz eder, güç spektral yoğunluğunu hesaplar ve jammer'ı milisaniyeler içinde tespit eder.
-  **Otonom Ajan** (`ajan.py` / ESP32 + LoRa) — radardan gelen kaçış emrini alır, sürüyü temiz banda kaydırır. Link kopmaz.

---

## Donanım

- Raspberry Pi 4B
- RTL-SDR Blog V3
- Waveshare SX126x LoRa HAT
- ESP32 (S3 + WROOM-32)
- Ebyte E22-900T22D LoRa modülleri

---

## En büyük kavga

Jammer aktifken kaçış komutunun ta kendisi jammer'ın gürültüsüyle havada çarpışıyordu (packet collision) ve alıcıyı sağırlaştırıyordu. Alıcı tarafında, gürültüye gömülü kirli paketlerin içinden hedef frekansı çekip çıkaran bir pattern-extraction filtresiyle çözdüm.

---

*Eğitim ve araştırma amaçlı, kontrollü test ortamında.*
