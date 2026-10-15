import numpy as np
from rtlsdr import RtlSdr
import time
import serial

print("=========================================================")
print("=== FHSS TABANLI SPEKTRUM İZLEME VE KOORDİNASYON SİSTEMİ ===")
print("=========================================================")

# --- AJAN ESP HABERLEŞME KURULUMU ---
try:
    telsiz = serial.Serial('/dev/serial0', 9600, timeout=1)
    print("[OK] Ajan ESP komuta hattı kuruldu.")
except Exception as e:
    print(f"[HATA] Telsiz hattı başlatılamadı: {e}")
    exit()

# --- SDR DONANIM KURULUMU ---
try:
    sdr = RtlSdr()
    sdr.sample_rate = 2.048e6
    sdr.gain = 20.0
    print("[OK] RTL-SDR Donanımı bağlandı.\n")
except Exception as e:
    print(f"[HATA] SDR başlatılamadı: {e}")
    exit()

DB_THRESHOLD = 45.0

# Girişim kaynağının zıpladığı 3 FHSS frekansına odaklanıyoruz
frekans_haritasi = [860, 890, 920]
fft_size = 8 * 1024
son_kacis_emri_zamani = 0

try:
    while True:
        for f in frekans_haritasi:
            sdr.center_freq = f * 1e6

            # DONANIMSAL GÜVENCE: PLL çipinin rahat kilitlenmesi için tam 50ms es
            time.sleep(0.05)

            # Tampon temizliği ve taze veri okuma
            _ = sdr.read_samples(1024)
            samples = sdr.read_samples(fft_size)

            # FFT Güç analizi
            power = 10 * np.log10(np.abs(np.fft.fftshift(np.fft.fft(samples)))**2 + 1e-9)
            c_idx = len(power) // 2
            power[c_idx - 5 : c_idx + 5] = -50.0

            peak_idx = np.argmax(power)
            guc = power[peak_idx]

            # Girişim tespit şartı
            if guc > DB_THRESHOLD:
                freqs = np.fft.fftshift(np.fft.fftfreq(fft_size, 1/sdr.sample_rate))
                tam_frekans = f + (freqs[peak_idx] / 1e6)

                zaman = time.strftime("%H:%M:%S")
                print(f"[{zaman}] FHSS GİRİŞİM TESPİT! Frekans: {tam_frekans:.2f} MHz | Güç: {guc:.1f} dB")

                # --- OTONOM FREKANS KAYDIRMA KARARI ---
                su_an = time.time()
                if su_an - son_kacis_emri_zamani > 3.0:
                    if tam_frekans < 890.0:
                        hedef_kanal = 70  # Girişim alttaysa (860), Ajan'ı 920 MHz'e (Kanal 70) taşı
                        yon = "ÜST BANT (920 MHz)"
                    else:
                        hedef_kanal = 10  # Girişim üstteyse, Ajan'ı 860 MHz'e (Kanal 10) taşı
                        yon = "ALT BANT (860 MHz)"

                    emir = f"SHIFT_{hedef_kanal}\n"
                    telsiz.write(emir.encode())
                    telsiz.flush()
                    print(f">>> [KOORDİNASYON] Ajan {yon} frekans kaydırma emri iletildi. <<<\n")
                    son_kacis_emri_zamani = su_an

except KeyboardInterrupt:
    print("\n[SISTEM] Radar kapatılıyor...")
    sdr.close()
    telsiz.close()
