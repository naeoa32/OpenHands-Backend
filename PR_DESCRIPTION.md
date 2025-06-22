
## Deskripsi


## ✨ Fitur Utama

1. **Sistem Autentikasi Pengguna**:
   - Sistem token sesi untuk menjaga status login

2. **Manajemen Novel Berbasis Pengguna**:

   - Otomatisasi browser dengan Playwright untuk login dan upload

4. **Perbaikan Teknis**:
   - Penyimpanan berbasis memori untuk menghindari masalah izin file
   - Manajemen browser Playwright yang robust dengan fallback
   - API fallback ketika modul OpenHands tidak dapat diimpor
   - Penanganan error yang lebih baik

## 🧪 Pengujian

   ```bash
   ```

2. Lihat daftar novel:
   ```bash
   ```

3. Buat novel baru:
   ```bash
   ```

   ```bash
   ```

## 🚀 Deployment

Siap untuk deployment di Hugging Face Spaces dengan variabel lingkungan berikut:

```
PORT=12001
HOST=0.0.0.0
PLAYWRIGHT_BROWSERS_PATH=/tmp/playwright_browsers
```

## 📝 Catatan Tambahan

- Semua data disimpan dalam memori untuk menghindari masalah izin file
- Browser Playwright diinstal di `/tmp/playwright_browsers`
- Semua endpoint novel memerlukan autentikasi dengan token
