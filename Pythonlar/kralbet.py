import requests
from bs4 import BeautifulSoup
import re

def m3u_olustur():
    try:
        print("⚡ M3U oluşturucu başlatıldı...")
        
        # Proxy üzerinden kaynağı al
        kaynak_url = "https://royalvipcanlimac.com/channels.php"
        proxy_url = f"https://vettelchannelowner-kralbet.hf.space/proxy/m3u?url={kaynak_url}"
        
        print(f"🔗 URL: {proxy_url}")
        
        # User-agent ekleyerek istek yap
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(proxy_url, headers=headers, timeout=20)
        response.raise_for_status()
        
        print(f"✅ Sayfa başarıyla çekildi ({len(response.text)} karakter)")
        
        # Debug için raw HTML'i kaydet
        with open('debug_raw.html', 'w', encoding='utf-8') as f:
            f.write(response.text)
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Tüm olası kanal container'larını deneyeceğiz
        kanallar = soup.find_all(['div', 'li'], class_=re.compile(r'channel|item|list', re.I))
        
        if not kanallar:
            kanallar = soup.select('div[id*="channel"], li[id*="channel"]')
        
        print(f"🔍 {len(kanallar)} adet kanal elementi bulundu")
        
        m3u_icerik = "#EXTM3U\n"
        kanal_sayisi = 0
        
        for kanal in kanallar:
            try:
                # Kanal adını bulmak için alternatif yollar (DÜZELTİLDİ)
                isim = kanal.find(class_=re.compile(r'home|title|name', re.I)) or \
                       kanal.find(['h2', 'h3', 'h4', 'div', 'span'])
                
                if not isim:
                    continue
                    
                kanal_adi = isim.get_text(strip=True)
                
                # Linki bulmak için alternatif yollar
                link = kanal.find('a', href=True) or \
                      kanal.find('iframe', src=True) or \
                      kanal.find('link', href=True)
                
                if not link:
                    continue
                    
                href = link.get('href') or link.get('src')
                
                if not href:
                    continue
                
                # URL'yi temizle ve düzenle
                if not href.startswith(('http', '/')):
                    href = '/' + href
                
                if href.startswith('/'):
                    href = f"https://1029kralbettv.com{href}"
                
                # M3U'ya ekle
                m3u_icerik += f'#EXTINF:-1 tvg-name="{kanal_adi}",{kanal_adi}\n'
                m3u_icerik += f"{href}\n"
                kanal_sayisi += 1
                print(f"➕ {kanal_adi} eklendi")
                
            except Exception as e:
                print(f"⚠️ Kanal işlenirken hata: {str(e)}")
                continue
        
        # Dosyaya yaz
        with open('kralbet.m3u', 'w', encoding='utf-8') as dosya:
            dosya.write(m3u_icerik)
        
        print(f"\n🎉 {kanal_sayisi} kanal başarıyla eklendi!")
        return True
        
    except Exception as hata:
        print(f"❌ Kritik hata: {str(hata)}")
        return False

if __name__ == "__main__":
    m3u_olustur()
