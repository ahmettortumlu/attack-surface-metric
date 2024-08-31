import ssl
import socket
import sys

def get_ssl_version(url):
    try:
        # URL'deki 'https://' kısmını kaldır
        hostname = url.replace("https://", "").replace("http://", "").split("/")[0]
        
        # Port ve bağlantı ayarları
        context = ssl.create_default_context()
        conn = context.wrap_socket(
            socket.socket(socket.AF_INET), server_hostname=hostname,
        )
        
        # Zaman aşımını ayarla
        conn.settimeout(3.0)
        
        # Bağlantıyı kur
        conn.connect((hostname, 443))
        
        # Sertifikayı al
        cert = conn.getpeercert()
        
        # SSL/TLS versiyonunu al
        ssl_version = conn.version()
        conn.close()
        
        return ssl_version
    
    except Exception as e:
        print(f"Bir hata oluştu: {e}")
        return None

if __name__ == "__main__":
    url = input("Enter web application URL address (https://example.com): ")
    version = get_ssl_version(url)
    
    if version:
        print(f"URL: {url}\nSSL/TLS Versiyonu: {version}")
    else:
        print("Sertifika versiyonu alınamadı.")
