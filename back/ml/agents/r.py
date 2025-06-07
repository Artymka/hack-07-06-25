import requests
from bs4 import BeautifulSoup
import urllib3
from PyPDF2 import PdfReader
from io import BytesIO

# Отключаем предупреждения о SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def safe_request(url, params=None, max_retries=3):
    """
    Делает GET-запрос по URL с опциональными параметрами params,
    пробует несколько раз при ошибках, возвращает объект response.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'text/html,application/xhtml+xml'
    }
    
    for attempt in range(max_retries):
        try:
            # Передаём params в запрос
            response = requests.get(url, headers=headers, params=params, verify=False, timeout=15)
            response.raise_for_status()
            return response
        except requests.exceptions.SSLError:
            # Пробуем с альтернативными параметрами SSL
            try:
                response = requests.get(url, headers=headers, params=params, verify='/path/to/cert.pem', timeout=15)
                return response
            except:
                continue
        except Exception as e:
            print(f"Попытка {attempt + 1} не удалась: {str(e)}")
            continue
    
    raise Exception(f"Не удалось загрузить страницу после {max_retries} попыток")


def parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    
    # Удаляем скрипты, стили, навигацию и футер
    for element in soup(['script', 'style', 'nav', 'footer']):
        element.decompose()
    
    # Специфичные для Росстата: основной контент обычно в div.main-content или в теге <main>
    main_content = soup.find('div', class_='main-content') or soup.find('main') or soup
    
    # Извлекаем таблицы (если нужно)
    tables = []
    for table in main_content.find_all('table'):
        tables.append(str(table))
    
    return {
        'title': soup.title.text.strip() if soup.title else 'Без названия',
        'text': main_content.get_text('\n', strip=True),
        'tables': tables
    }


def parse_pdf(pdf_content):
    try:
        pdf_file = BytesIO(pdf_content)
        reader = PdfReader(pdf_file)
        text = "\n".join([page.extract_text() or "" for page in reader.pages])
        return {'type': 'pdf', 'content': text}
    except Exception as e:
        return {'error': str(e)}


def rosstat_search(query):
    """
    Делает поиск на сайте rosstat.gov.ru через их встроенный search-интерфейс,
    возвращает список словарей {title, url, date}.
    """
    base_url = "https://rosstat.gov.ru/search"
    params = {
        'q': query,
        'sort': 'date',
        'items_per_page': 10
    }
    
    try:
        # Передаём params в safe_request
        response = safe_request(base_url, params=params)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        results = []
        # Здесь предполагаем, что результаты лежат в контейнере с классом .search-results
        # и каждая запись — в элементе с классом .search-item
        for item in soup.select('.search-results .search-item'):
            title_tag = item.select_one('.search-title a')
            if title_tag:
                url = title_tag['href']
                title = title_tag.text.strip()
                date_tag = item.select_one('.search-date')
                date = date_tag.text.strip() if date_tag else ''
                
                # Если внутренняя ссылка без домена, дополняем
                if url.startswith('/'):
                    url = 'https://wikipedia.org' + url
                
                results.append({
                    'title': title,
                    'url': url,
                    'date': date
                })
        
        return results
    except Exception as e:
        return {'error': str(e)}


rosstat_search('население ростова')