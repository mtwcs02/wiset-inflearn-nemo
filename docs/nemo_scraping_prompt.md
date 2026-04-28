## 1) HTTP 요청정보와 헤더

요청 URL
https://www.nemoapp.kr/api/store/search-list?Subway=222&Radius=1000&CompletedOnly=false&NELat=37.524082652435375&NELng=127.04633639319073&SWLat=37.471760955370655&SWLng=127.00886288970709&Zoom=15&SortBy=29&PageIndex=0
요청 메서드
GET
상태 코드
200 OK
원격 주소
3.168.178.10:443
리퍼러 정책
strict-origin-when-cross-origin


referer
https://www.nemoapp.kr/store
sec-ch-ua
"Google Chrome";v="147", "Not.A/Brand";v="8", "Chromium";v="147"
sec-ch-ua-mobile
?0
sec-ch-ua-platform
"Windows"
sec-fetch-dest
empty
sec-fetch-mode
cors
sec-fetch-site
same-origin
user-agent
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36

## 2) Payload 정보

Subway=222&Radius=1000&CompletedOnly=false&NELat=37.524082652435375&NELng=127.04633639319073&SWLat=37.471760955370655&SWLng=127.00886288970709&Zoom=15&SortBy=29&PageIndex=0


## 3) 응답의 일부를 Response 에서 일부를 복사해서 넣어주기 (전체는 토큰 수 제한으로 어렵습니다.)

items 하단의 모든 데이터를 수집할 것

```json
{
    "items": [
        {
```

## 4) 한페이지가 성공적으로 수집되는지 확인하기 sqlitedb에 저장하기

*수집한 데이터는 data 폴더에 저장하고, 소스코드는 src 폴더에 저장할 것
