#!/usr/bin/env python3
"""
Demo penggunaan Fizzo automation endpoint
Menunjukkan cara menggunakan API untuk auto-update novel ke fizzo.org
"""

import json
import requests
from datetime import datetime

def demo_fizzo_usage():
    """Demo cara menggunakan Fizzo automation"""
    
    print("🚀 DEMO: Fizzo.org Auto-Update API")
    print("=" * 50)
    
    # URL endpoint (ganti dengan URL HF Spaces yang benar)
    BACKEND_URL = "https://your-backend.hf.space"  # Ganti dengan URL yang benar
    endpoint = f"{BACKEND_URL}/api/fizzo-auto-update"
    
    print(f"🌐 Backend URL: {BACKEND_URL}")
    print(f"📡 Endpoint: {endpoint}")
    print()
    
    # Data untuk upload chapter
    chapter_data = {
        "email": "your_email@gmail.com",           # Email login fizzo.org
        "password": "your_password",               # Password login fizzo.org
        "chapter_title": f"Bab 28: Pertarungan Terakhir - {datetime.now().strftime('%d/%m/%Y')}",
        "chapter_content": """
Angin malam bertiup kencang di atas atap gedung pencakar langit. Akira berdiri di tepi, matanya menatap tajam ke arah musuh yang sudah menunggunya sejak tadi.

"Akhirnya kau datang juga," ucap Kazuki dengan seringai dingin. Pedang di tangannya berkilau menantang di bawah sinar bulan.

Akira tidak menjawab. Dia tahu ini adalah pertarungan terakhir. Setelah ini, semuanya akan berakhir. Entah dia yang menang, atau Kazuki yang akan mengambil alih kekuasaan organisasi.

"Kau masih punya kesempatan untuk menyerah," Kazuki melanjutkan. "Bergabunglah denganku, dan aku akan membiarkanmu hidup."

"Tidak akan pernah," Akira akhirnya bersuara. Tangannya perlahan menggenggam gagang katana di pinggangnya. "Aku tidak akan membiarkanmu menghancurkan semua yang telah kita bangun."

Kazuki tertawa keras. "Naif! Organisasi ini sudah busuk dari dalam. Aku hanya akan membersihkannya."

Tanpa peringatan, Kazuki melompat maju dengan kecepatan kilat. Pedangnya melesat ke arah leher Akira. Tapi Akira sudah siap. Katananya terhunus dalam sekejap, menangkis serangan mematikan itu.

CLANG!

Suara benturan logam bergema di malam sunyi. Kedua pejuang itu saling berhadapan, mata mereka saling menatap dengan kebencian yang mendalam.

"Kau sudah berlatih," Kazuki mengakui dengan nada mengejek. "Tapi masih belum cukup untuk mengalahkanku."

Mereka berpisah sejenak, lalu kembali bertarung dengan intensitas yang lebih tinggi. Setiap gerakan mereka presisi dan mematikan. Tidak ada ruang untuk kesalahan.

Akira meluncurkan serangan bertubi-tubi, tapi Kazuki berhasil menghindar dengan gesit. Sebaliknya, serangan balik Kazuki hampir mengenai vital Akira beberapa kali.

Pertarungan berlangsung sengit. Keduanya sama-sama kuat, sama-sama terlatih. Tapi Akira tahu dia harus mengakhiri ini segera. Stamina mereka mulai terkuras.

"Teknik terlarang... Kirisame no Jutsu!" Akira berteriak sambil melompat tinggi ke udara.

Katananya berkilau dengan cahaya biru misterius. Ini adalah teknik yang diajarkan kakeknya, teknik yang tidak boleh digunakan kecuali dalam situasi hidup mati.

Kazuki terkejut melihat teknik legendaris itu. Matanya membelalak. "Tidak mungkin! Teknik itu sudah hilang!"

Tapi sudah terlambat. Akira menukik dari atas dengan kecepatan yang tidak bisa dilihat mata telanjang. Cahaya biru dari katananya membelah udara malam.

SLASH!

Semuanya terdiam. Kedua pejuang itu berdiri tidak bergerak di tengah atap gedung. Angin malam kembali bertiup pelan.

Perlahan, Kazuki merasakan sesuatu yang hangat mengalir di dadanya. Dia menunduk dan melihat darah segar membasahi bajunya. Katana Akira telah menembus pertahanannya.

"Bagaimana... bisa..." Kazuki tergagap.

"Karena aku bertarung untuk melindungi orang-orang yang aku sayangi," Akira menjawab dengan suara lirih. "Sedangkan kau hanya bertarung untuk kekuasaan."

Kazuki tersenyum pahit. "Mungkin... kau benar..." Dia terjatuh ke lutut, lalu rebah ke lantai atap.

Akira menarik katananya dan membersihkan darah di bilahnya. Pertarungan telah berakhir. Organisasi aman. Tapi kemenangan ini terasa pahit di hatinya.

Dia menatap tubuh Kazuki yang terbujur kaku. Dulu mereka adalah sahabat terbaik. Tapi ambisi telah membutakan Kazuki dan mengubahnya menjadi monster.

"Selamat jalan, sahabat lama," Akira berbisik sebelum melangkah pergi meninggalkan atap gedung itu.

Malam itu, legenda baru lahir. Akira, sang penjaga terakhir, telah membuktikan bahwa kebaikan akan selalu mengalahkan kejahatan, tidak peduli seberapa kuat musuhnya.

Tapi di balik kemenangannya, Akira tahu bahwa ini bukan akhir dari segalanya. Masih banyak ancaman lain yang mengintai di kegelapan. Dan dia harus siap menghadapi semuanya.

Karena itulah takdirnya. Sebagai penjaga terakhir organisasi, dia akan terus berjuang melindungi perdamaian, sampai nafas terakhirnya.

[Bersambung...]
        """.strip()
    }
    
    print("📝 Data Chapter:")
    print(f"   📧 Email: {chapter_data['email']}")
    print(f"   📖 Title: {chapter_data['chapter_title']}")
    print(f"   📄 Content Length: {len(chapter_data['chapter_content'])} characters")
    print()
    
    # Contoh request dengan Python requests
    print("🐍 Python Code Example:")
    print("=" * 30)
    print("""
import requests
import json

# Data chapter
chapter_data = {
    "email": "your_email@gmail.com",
    "password": "your_password", 
    "chapter_title": "Bab 28: Pertarungan Terakhir",
    "chapter_content": "Isi chapter minimal 1000 karakter..."
}

# Send request
response = requests.post(
    "https://your-backend.hf.space/api/fizzo-auto-update",
    json=chapter_data,
    headers={"Content-Type": "application/json"}
)

# Check result
if response.status_code == 200:
    result = response.json()
    if result["success"]:
        print("✅ Chapter berhasil diupload ke fizzo.org!")
        print(f"📊 Data: {result['data']}")
    else:
        print(f"❌ Upload gagal: {result['error']}")
else:
    print(f"❌ HTTP Error: {response.status_code}")
    """)
    
    # Contoh request dengan JavaScript/Frontend
    print("\n🌐 JavaScript/Frontend Example:")
    print("=" * 35)
    print("""
// Data chapter
const chapterData = {
    email: "your_email@gmail.com",
    password: "your_password",
    chapter_title: "Bab 28: Pertarungan Terakhir", 
    chapter_content: "Isi chapter minimal 1000 karakter..."
};

// Send request
fetch("https://your-backend.hf.space/api/fizzo-auto-update", {
    method: "POST",
    headers: {
        "Content-Type": "application/json"
    },
    body: JSON.stringify(chapterData)
})
.then(response => response.json())
.then(result => {
    if (result.success) {
        console.log("✅ Chapter berhasil diupload!");
        console.log("📊 Data:", result.data);
    } else {
        console.error("❌ Upload gagal:", result.error);
    }
})
.catch(error => {
    console.error("❌ Network error:", error);
});
    """)
    
    # Contoh response
    print("\n📊 Expected Response:")
    print("=" * 25)
    
    success_response = {
        "success": True,
        "message": "Chapter berhasil diupload ke fizzo.org",
        "data": {
            "success": True,
            "message": "Chapter created successfully",
            "chapter_title": "Bab 28: Pertarungan Terakhir",
            "content_length": 2847,
            "published": True,
            "confirmed": True
        }
    }
    
    error_response = {
        "success": False,
        "error": "Chapter content must be at least 1,000 characters"
    }
    
    print("✅ Success Response:")
    print(json.dumps(success_response, indent=2, ensure_ascii=False))
    
    print("\n❌ Error Response:")
    print(json.dumps(error_response, indent=2, ensure_ascii=False))
    
    print("\n🎯 Usage Tips:")
    print("=" * 15)
    print("✅ Content harus minimal 1,000 karakter")
    print("✅ Content maksimal 60,000 karakter") 
    print("✅ Gunakan email/password yang valid untuk fizzo.org")
    print("✅ Chapter title sebaiknya unik (contoh: 'Bab 28: Judul')")
    print("✅ Process memakan waktu 15-25 detik")
    print("✅ Endpoint bersifat public (tidak perlu authentication)")
    
    print("\n🚀 Ready to use!")
    print("Ganti URL dan credentials, lalu jalankan request!")

if __name__ == "__main__":
    demo_fizzo_usage()