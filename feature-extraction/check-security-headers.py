import requests

def check_security_headers(url):
    try:
        # HTTP isteği gönder
        response = requests.get(url)
        
        # Güvenlik başlıklarını kontrol et
        headers = {
            'Expect-CT': response.headers.get('Expect-CT', 'Eksik'),
            'X-Content-Type-Options': response.headers.get('X-Content-Type-Options', 'Eksik'),
            'X-Frame-Options': response.headers.get('X-Frame-Options', 'Eksik'),
            'Content-Security-Policy': response.headers.get('Content-Security-Policy', 'Eksik'),
            'Strict-Transport-Security': response.headers.get('Strict-Transport-Security', 'Eksik')
        }
        
        # Sonuçları yazdır
        for header, value in headers.items():
            print(f"{header}: {value}")
    
    except Exception as e:
        print(f"Bir hata oluştu: {e}")

if __name__ == "__main__":
    url = input("Web uygulamasının URL'ini girin (https://example.com): ")
    check_security_headers(url)
