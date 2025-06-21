import requests
import json
import sys

# Kredensial untuk testing
EMAIL = "minatoz1997@gmail.com"
PASSWORD = "luthfi123"

# URL endpoint (sesuaikan dengan URL deployment)
BASE_URL = "http://localhost:7860"  # Default untuk local testing

def test_list_novel():
    """Test endpoint fizzo-list-novel"""
    print("\n🔍 Testing endpoint /api/fizzo-list-novel...")
    url = f"{BASE_URL}/api/fizzo-list-novel"
    payload = {
        "email": EMAIL,
        "password": PASSWORD
    }
    
    try:
        response = requests.post(url, json=payload, timeout=120)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            novels = response.json()
            print(f"Response: {json.dumps(novels, indent=2)}")
            
            if isinstance(novels, list):
                print(f"✅ Berhasil mendapatkan daftar novel: {len(novels)} novel ditemukan")
                
                # Print novel details
                for i, novel in enumerate(novels):
                    if isinstance(novel, dict):
                        print(f"  {i+1}. ID: {novel.get('id')}, Judul: {novel.get('title')}")
                    else:
                        print(f"  {i+1}. {novel}")
                
                return novels
            else:
                print(f"⚠️ Response bukan list: {novels}")
                return None
        else:
            print(f"❌ Gagal mendapatkan daftar novel: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error saat testing endpoint list novel: {e}")
        return None

def test_auto_update(novel_id=None):
    """Test endpoint fizzo-auto-update dengan novel_id"""
    print(f"\n🔍 Testing endpoint /api/fizzo-auto-update dengan novel_id: {novel_id if novel_id else 'None (default)'}")
    url = f"{BASE_URL}/api/fizzo-auto-update"
    payload = {
        "email": EMAIL,
        "password": PASSWORD,
        "chapter_title": "Chapter Test dari OpenHands",
        "chapter_content": "Ini adalah chapter test yang dibuat oleh OpenHands untuk testing fitur novel_id.\n\n" + ("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. " * 10)
    }
    
    if novel_id:
        payload["novel_id"] = novel_id
    
    try:
        response = requests.post(url, json=payload, timeout=180)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Berhasil mengupload chapter: {json.dumps(result, indent=2)}")
            return result
        else:
            print(f"❌ Gagal mengupload chapter: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error saat testing endpoint auto update: {e}")
        return None

if __name__ == "__main__":
    # Check if URL is provided as argument
    if len(sys.argv) > 1:
        BASE_URL = sys.argv[1]
    
    print(f"🚀 Menjalankan test dengan URL: {BASE_URL}")
    
    # Test list novel endpoint
    novels = test_list_novel()
    
    if novels and isinstance(novels, list) and len(novels) > 0:
        # Cek apakah novels berisi dictionary atau string
        if isinstance(novels[0], dict) and 'id' in novels[0]:
            # Test auto update dengan novel_id dari hasil list novel
            novel_id = novels[0].get("id")
            print(f"\n📝 Menggunakan novel_id pertama untuk testing: {novel_id}")
            test_auto_update(novel_id)
            
            # Jika ada lebih dari satu novel, test dengan novel kedua juga
            if len(novels) > 1:
                novel_id = novels[1].get("id")
                print(f"\n📝 Menggunakan novel_id kedua untuk testing: {novel_id}")
                test_auto_update(novel_id)
        else:
            # Jika novels berisi string, gunakan string pertama sebagai novel_id
            novel_id = novels[0]
            print(f"\n📝 Menggunakan novel_id string untuk testing: {novel_id}")
            test_auto_update(novel_id)
    else:
        # Test auto update tanpa novel_id (default)
        print("\n📝 Tidak ada novel ditemukan, testing dengan novel default")
        test_auto_update()
    
    print("\n✨ Testing selesai!")