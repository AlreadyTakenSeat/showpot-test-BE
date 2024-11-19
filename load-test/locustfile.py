import requests, random
from locust import HttpUser, task, between

class UserBehavior(HttpUser):
    wait_time = between(1, 2)
    MAX_PAGING_ROW = 300
    SEARCH_WORD = ["저스틴 비버", "콜드 플레이", "애미넴", "KE$HA", "찰리푸스", "두아 리파"]
    SORT = ["RECENT", "POPULAR"]
    ONLY_OPEN_SCHEDULE = [True, False]
    SHOW_TYPE = ["TERMINATED", "CONTINUED"]
    ALERT_TIMES = ["BEFORE_A_DAY", "BEFORE_SIX_HOURS", "BEFORE_A_HOUR"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.genreCursor = None
        self.artistCursor = None
        self.alarmCursor = None
        self.showCursor = None
        self.token = None

    def on_start(self):
        """회원가입 API 호출 및 JWT 토큰 수신"""
        response: requests.Response = self.client.post("/api/v1/users/login", json={
            "socialType": "GOOGLE",
            "identifier": "test",
            "fcmToken": "test"
            }, headers={'Content-Type': 'application/json'})
        
        self.token = response.json().get('data').get('accessToken')

        for _ in range(1, 11):
            headers = {'Authorization': f'Bearer {self.token}'}
            genreParams = {"size" : 2}
            if self.genreCursor:
                genreParams = {"size" : 2, "cursorId" : self.genreCursor}

            response = self.client.get("/api/v1/genres", params=genreParams, headers=headers)
            
            if response.status_code < 300:
                response = response.json().get('data')

                if response:
                    data = response.get('data')
                    if data:
                        body = list(set({'genreIds': [o.get('id') for o in data]}))
                        self.client.post("/api/v1/genres/subscribe", json=body, headers=headers)
                        self.genreCursor = data[-1].get('id')

            artistParams = {"size" : 2}
            if self.artistCursor:
                artistParams = {"size" : 2, "cursorId" : self.artistCursor}

            response = self.client.get("/api/v1/artists", params=artistParams, headers=headers)

            if response.status_code < 300:
                response = response.json().get('data')

                if response:
                    data = response.get('data')
                    if data:
                        body = list(set({'artistIds': [o.get('id') for o in data]}))
                        self.client.post("/api/v1/artists/subscribe", json=body, headers=headers)
                        self.artistCursor = data[-1].get('id')

    @task(3)
    def get_task_1(self):
        """백엔드 서버 API GET 1 : 회원 정보"""
        headers = {'Authorization': f'Bearer {self.token}'}
        self.client.get("/api/v1/users/profile", headers=headers)

    @task(3)
    def get_task_2(self):
        """백엔드 서버 API GET 2 : 장르 전체 목록 조회"""
        headers = {'Authorization': f'Bearer {self.token}'}
        params = {"size" : 30}
        if self.genreCursor:
             params["cursorId"] = self.genreCursor
        response = self.client.get("/api/v1/genres", params=params, headers=headers)
        if response.status_code < 300:
                response = response.json().get('data')
                if response:
                    data = response.get('data')
                    if data:
                        self.genreCursor = data[-1].get('id')

    @task(3)
    def get_task_3(self):
        """백엔드 서버 API GET 3 : 구독하지 않은 장르 목록 조회"""
        headers = {'Authorization': f'Bearer {self.token}'}
        params = {"size" : 30}
        if self.genreCursor:
             params["cursorId"] = self.genreCursor
        response = self.client.get("/api/v1/genres/unsubscriptions", params=params, headers=headers)
        if response.status_code < 300:
                response = response.json().get('data')
                if response:
                    data = response.get('data')
                    if data:
                        self.genreCursor = data[-1].get('id')

    @task(3)
    def get_task_4(self):
        """백엔드 서버 API GET 4 : 구독한 장르 목록 조회"""
        headers = {'Authorization': f'Bearer {self.token}'}
        params = {"size" : 30}
        if self.genreCursor:
             params["cursorId"] = self.genreCursor
        response = self.client.get("/api/v1/genres/subscriptions", params=params, headers=headers)
        if response.status_code < 300:
                response = response.json().get('data')
                if response:
                    data = response.get('data')
                    if data:
                        self.genreCursor = data[-1].get('id')

    @task(3)
    def get_task_5(self):
        """백엔드 서버 API GET 5 : 구독한 장르 수"""
        headers = {'Authorization': f'Bearer {self.token}'}
        self.client.get("/api/v1/genres/subscriptions/count", headers=headers)

    @task(3)
    def get_task_6(self):
        """백엔드 서버 API GET 6 : 구독하지 않은 아티스트 목록 조회"""
        headers = {'Authorization': f'Bearer {self.token}'}
        params = {"size" : 30}
        if self.artistCursor:
             params["cursorId" : self.artistCursor]
        response = self.client.get("/api/v1/artists/unsubscriptions", params=params, headers=headers)
        if response.status_code < 300:
                response = response.json().get('data')
                if response:
                    data = response.get('data')
                    if data:
                        self.artistCursor = data[-1].get('id')

    @task(3)
    def get_task_7(self):
        """백엔드 서버 API GET 7 : 구독한 아티스트 목록 조회"""
        headers = {'Authorization': f'Bearer {self.token}'}
        params = {"size" : 30}
        if self.artistCursor:
            params["cursorId"] = self.artistCursor
        response = self.client.get("/api/v1/artists/subscriptions", params=params, headers=headers)
        if response.status_code < 300:
                response = response.json().get('data')
                if response:
                    data = response.get('data')
                    if data:
                        self.artistCursor = data[-1].get('id')

    @task(3)
    def get_task_8(self):
        """백엔드 서버 API GET 8 : 구독한 아티스트 수"""
        headers = {'Authorization': f'Bearer {self.token}'}
        self.client.get("/api/v1/artists/subscriptions/count", headers=headers)

    @task(3)
    def get_task_9(self):
        """백엔드 서버 API GET 9 : 알림 목록"""
        headers = {'Authorization': f'Bearer {self.token}'}
        params = {"size" : 30}
        if self.alarmCursor:
            params['cursorId'] = self.alarmCursor
        response = self.client.get("/api/v1/users/notifications", params=params, headers=headers)
        if response.status_code < 300:
                response = response.json().get('data')
                if response:
                    data = response.get('data')
                    if data:
                        self.alarmCursor = data[-1].get('id')

    @task(3)
    def get_task_10(self):
        """백엔드 서버 API GET 10 : 알림 미열람 존재 여부"""
        headers = {'Authorization': f'Bearer {self.token}'}
        self.client.get("/api/v1/users/notifications/exist", headers=headers)

    @task(3)
    def get_task_11(self):
        """백엔드 서버 API GET 11 : 공연 목록 조회"""
        headers = {'Authorization': f'Bearer {self.token}'}
        params = {"size" : 30, "sort" : self.SORT[random.randint(0, len(self.SORT) - 1)], "onlyOpenSchedule" : self.ONLY_OPEN_SCHEDULE[random.randint(0, len(self.ONLY_OPEN_SCHEDULE) - 1)]}
        if self.showCursor:
            params["cursorId"] = self.showCursor
        response = self.client.get("/api/v1/shows", params=params, headers=headers)
        if response.status_code < 300:
                response = response.json().get('data')
                if response:
                    data = response.get('data')
                    if data:
                        self.showCursor = data[-1].get('id')
    
    @task(3)
    def get_task_12(self):
        """백엔드 서버 API GET 12 : 공연 상세 조회"""
        headers = {'Authorization': f'Bearer {self.token}'}
        if self.showCursor:
            params = {"Device-Token" : "test"}
            self.client.get(f"/api/v1/shows/{self.showCursor}", params=params, headers=headers)
        else:
             print('cannot call /api/v1/shows/(showId)')
    
    @task(3)
    def get_task_13(self):
        """백엔드 서버 API GET 13 : 티켓팅한 공연의 알림 예약 현황"""
        headers = {'Authorization': f'Bearer {self.token}'}
        if self.showCursor:
            params = {"ticketingApiType" : "NORMAL"}
            self.client.get(f"/api/v1/shows/{self.showCursor}/alert/reservations", params=params, headers=headers)
        else:
             print('cannot call /api/v1/shows/(showId)/alert/reservations')

    @task(3)
    def get_task_14(self):
        """백엔드 서버 API GET 14 : 티켓팅 알림 설정 후 공연이 종료된 개수"""
        headers = {'Authorization': f'Bearer {self.token}'}
        self.client.get("/api/v1/shows/terminated/ticketing/count", headers=headers)

    @task(3)
    def get_task_15(self):
        """백엔드 서버 API GET 15 : 공연 검색하기"""
        headers = {'Authorization': f'Bearer {self.token}'}
        params = {"search" : self.SEARCH_WORD[random.randint(0, len(self.SEARCH_WORD) - 1)], "size" : 30}
        if self.showCursor:
             params["cursorId"] = self.showCursor
        response = self.client.get("/api/v1/shows/search", params=params, headers=headers)
        if response.status_code < 300:
                response = response.json().get('data')
                if response:
                    data = response.get('data')
                    if data:
                        self.showCursor = data[-1].get('id')

    @task(3)
    def get_task_16(self):
        """백엔드 서버 API GET 16 : 관심 등록한 공연 목록 조회"""
        headers = {'Authorization': f'Bearer {self.token}'}
        params = {"size" : 30}
        self.client.get("/api/v1/shows/interests", params=params, headers=headers)

    @task(3)
    def get_task_17(self):
        """백엔드 서버 API GET 17 : 관심 공연 개수"""
        headers = {'Authorization': f'Bearer {self.token}'}
        self.client.get("/api/v1/shows/interests/count", headers=headers)

    @task(3)
    def get_task_18(self):
        """백엔드 서버 API GET 18 : 알림 설정한 공연 목록"""
        headers = {'Authorization': f'Bearer {self.token}'}
        params = {"type" : self.SHOW_TYPE[random.randint(0, len(self.SHOW_TYPE) - 1)], "size" : 30}
        self.client.get("/api/v1/shows/alerts", params=params, headers=headers)

    @task(3)
    def get_task_18(self):
        """백엔드 서버 API GET 18 : 알림 설정한 공연 목록"""
        headers = {'Authorization': f'Bearer {self.token}'}
        self.client.get("/api/v1/shows/alerts/count", headers=headers)


    #@task(3)
    def get_task_spotify_api(self):
        """백엔드 서버 API GET spotify api : 아티스트 검색하기"""
        headers = {'Authorization': f'Bearer {self.token}'}
        params = {"cursorId": self.artistCursor, "size" : 30, "search" : self.SEARCH_WORD[random.randint(0, len(self.SEARCH_WORD) - 1)]}
        response = self.client.get("/api/v1/artists/search", params=params, headers=headers)
        if response.status_code < 300:
                response = response.json().get('data')
                if response:
                    data = response.get('data')
                    if data:
                        self.artistCursor = data[-1].get('id')

    @task(2)
    def post_task_2(self):
        """백엔드 서버 API POST 2 : 장르 구독 취소하기"""
        headers = {'Authorization': f'Bearer {self.token}'}
        body = {'genreIds' : [self.genreCursor]}
        self.client.post("/api/v1/genres/unsubscribe", json=body, headers=headers)

    @task(2)
    def post_task_3(self):
        """백엔드 서버 API POST 3 : 장르 구독하기"""
        headers = {'Authorization': f'Bearer {self.token}'}
        body = {'genreIds' : [self.genreCursor]}
        self.client.post("/api/v1/genres/subscribe", json=body, headers=headers)

    @task(2)
    def post_task_4(self):
        """백엔드 서버 API POST 4 : 아티스트 구독 취소하기"""
        headers = {'Authorization': f'Bearer {self.token}'}
        body = {'artistIds' : [self.artistCursor]}
        self.client.post("/api/v1/artists/unsubscribe", json=body, headers=headers)

    @task(2)
    def post_task_5(self):
        """백엔드 서버 API POST 5 : 아티스트 구독하기"""
        headers = {'Authorization': f'Bearer {self.token}'}
        body = {'artistIds' : [self.artistCursor]}
        self.client.post("/api/v1/artists/subscribe", json=body, headers=headers)

    @task(2)
    def post_task_5(self):
        """백엔드 서버 API POST 5 : 아티스트 구독하기"""
        headers = {'Authorization': f'Bearer {self.token}'}
        self.client.post(f"/api/v1/shows/{self.showCursor}/uninterested", headers=headers)

    @task(2)
    def post_task_5(self):
        """백엔드 서버 API POST 5 : 아티스트 구독하기"""
        headers = {'Authorization': f'Bearer {self.token}'}
        self.client.post(f"/api/v1/shows/{self.showCursor}/interests", headers=headers)

    @task(2)
    def post_task_5(self):
        """백엔드 서버 API POST 5 : 아티스트 구독하기"""
        if self.showCursor:
            headers = {'Authorization': f'Bearer {self.token}'}
            params = {"ticketingApiType" : "NORMAL"}
            body = {"alertTimes" : self.ALERT_TIMES[random.randint(0, len(self.ALERT_TIMES) - 1)]}
            self.client.post(f"/api/v1/shows/{self.showCursor}/alert", params=params, json=body, headers=headers)
        else:
             print("cannot call /api/v1/shows/(showId)/alert")