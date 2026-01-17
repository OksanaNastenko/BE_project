from api.base_api import BaseAPI

class UsersAPI(BaseAPI):
    def get_users(self, page=1):
        return self.request("GET", "/users", params={"page": page}).json()

    def get_user(self, user_id):
        return self.request("GET", f"/users/{user_id}").json()
    
    def post_user(self, body):
        return self.request("POST", "/users", json=body).json()
