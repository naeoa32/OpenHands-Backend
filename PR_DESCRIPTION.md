# 🚀 OpenHands Backend dengan Integrasi Fizzo.org

## Deskripsi

PR ini menambahkan sistem autentikasi pengguna lengkap dan integrasi Fizzo.org ke OpenHands Backend, membuatnya siap untuk deployment di Hugging Face Spaces.

## ✨ Fitur Utama

1. **Sistem Autentikasi Pengguna**:
   - Endpoint `/api/fizzo-login` untuk login dengan email/password
   - Sistem token sesi untuk menjaga status login
   - Mendukung login dengan akun Fizzo.org dan Gmail

2. **Manajemen Novel Berbasis Pengguna**:
   - Endpoint `/api/fizzo-list-novels` menampilkan novel milik pengguna
   - Endpoint `/api/fizzo-novel/{novel_id}` untuk detail novel
   - Endpoint `/api/fizzo-create-novel` untuk membuat novel baru
   - Endpoint `/api/fizzo-add-chapter` untuk menambah chapter
   - Endpoint `/api/fizzo-auto-update` untuk memperbarui novel

3. **Integrasi Fizzo.org**:
   - Endpoint `/api/fizzo-direct-upload` untuk upload langsung ke Fizzo.org
   - Otomatisasi browser dengan Playwright untuk login dan upload
   - Opsi `upload_to_fizzo` pada endpoint auto-update

4. **Perbaikan Teknis**:
   - Penyimpanan berbasis memori untuk menghindari masalah izin file
   - Manajemen browser Playwright yang robust dengan fallback
   - API fallback ketika modul OpenHands tidak dapat diimpor
   - Penanganan error yang lebih baik

## 🧪 Pengujian

1. Login dengan kredensial Fizzo.org:
   ```bash
   curl -X POST -H "Content-Type: application/json" -d '{"email": "minatoz1997@gmail.com", "password": "Luthfi123*"}' https://work-2-wsyybosjhyaetudd.prod-runtime.all-hands.dev/api/fizzo-login
   ```

2. Lihat daftar novel:
   ```bash
   curl -X GET -H "Authorization: Bearer TOKEN" https://work-2-wsyybosjhyaetudd.prod-runtime.all-hands.dev/api/fizzo-list-novels
   ```

3. Buat novel baru:
   ```bash
   curl -X POST -H "Content-Type: application/json" -H "Authorization: Bearer TOKEN" -d '{"title":"Novel Baru","description":"Deskripsi novel","status":"ongoing","genre":"fantasy","tags":["fantasy","adventure"]}' https://work-2-wsyybosjhyaetudd.prod-runtime.all-hands.dev/api/fizzo-create-novel
   ```

4. Upload langsung ke Fizzo.org:
   ```bash
   curl -X POST -H "Content-Type: application/json" -H "Authorization: Bearer TOKEN" -d '{"novel_id":"ID_NOVEL","title":"Judul Novel","description":"Deskripsi novel","chapters":[{"title":"Bab 1","content":"Isi chapter..."}]}' https://work-2-wsyybosjhyaetudd.prod-runtime.all-hands.dev/api/fizzo-direct-upload
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
- Fitur upload ke Fizzo.org menggunakan otomatisasi browser