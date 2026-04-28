import requests
import sqlite3
import json
import os
import time

def flatten_json(y):
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(y)
    return out

def scrape_nemo():
    base_url = "https://www.nemoapp.kr/api/store/search-list"
    params = {
        "Subway": "222",
        "Radius": "1000",
        "CompletedOnly": "false",
        "NELat": "37.524082652435375",
        "NELng": "127.04633639319073",
        "SWLat": "37.471760955370655",
        "SWLng": "127.00886288970709",
        "Zoom": "15",
        "SortBy": "29",
        "PageIndex": 0
    }
    
    headers = {
        "referer": "https://www.nemoapp.kr/store",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
        "sec-ch-ua": '"Google Chrome";v="147", "Not.A/Brand";v="8", "Chromium";v="147"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin"
    }

    all_items = []
    page = 0
    
    while True:
        params["PageIndex"] = page
        print(f"Requesting Page {page}...")
        
        try:
            response = requests.get(base_url, headers=headers, params=params)
            
            if response.status_code != 200:
                print(f"Error on Page {page}: {response.status_code}")
                break

            data = response.json()
            items = data.get("items", [])
            
            if not items:
                print(f"No more items found at page {page}. Stopping.")
                break

            print(f"Page {page}: Found {len(items)} items.")
            all_items.extend(items)
            
            # 다음 페이지로 이동
            page += 1
            
            # 서버 부하 방지를 위한 짧은 휴식
            time.sleep(1)
            
        except Exception as e:
            print(f"Exception occurred: {e}")
            break

    if not all_items:
        print("No data collected.")
        return

    print(f"Total items collected: {len(all_items)}")

    # 데이터 평탄화 (Flattening)
    flattened_items = [flatten_json(item) for item in all_items]

    # DB 저장 설정
    db_path = os.path.join("data", "nemo_data.db")
    
    # 기존 파일 삭제 후 새로 생성
    if os.path.exists(db_path):
        os.remove(db_path)
        
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 모든 아이템의 키를 합쳐서 전체 컬럼 세트 생성 (페이지마다 컬럼이 다를 수 있음)
    all_keys = set()
    for item in flattened_items:
        all_keys.update(item.keys())
    
    columns = sorted(list(all_keys))
    
    # SQLite 컬럼 정의
    column_defs = ", ".join([f'"{col}" TEXT' for col in columns])
    create_table_query = f"CREATE TABLE IF NOT EXISTS stores ({column_defs})"
    cursor.execute(create_table_query)

    # 데이터 삽입
    placeholders = ", ".join(["?" for _ in columns])
    insert_query = f"INSERT INTO stores ({', '.join([f'\"{col}\"' for col in columns])}) VALUES ({placeholders})"
    
    for item in flattened_items:
        values = [str(item.get(col)) if item.get(col) is not None else None for col in columns]
        cursor.execute(insert_query, values)

    conn.commit()
    conn.close()
    print(f"Successfully saved {len(all_items)} items to {db_path}")

if __name__ == "__main__":
    scrape_nemo()
