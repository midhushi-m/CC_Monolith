from locust import task, run_single_user
from locust import FastHttpUser
from insert_product import login

class AddToCart(FastHttpUser):
    host = "http://localhost:5000"
    username = "test123"
    password = "test123"
    
    # Define headers as a class-level variable
    default_headers = {
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "DNT": "1",
        "Sec-GPC": "1",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0",
    }

    def on_start(self):
        """Runs once when the user starts."""
        cookies = login(self.username, self.password)
        self.token = cookies.get("token")
        if not self.token:
            raise ValueError("Failed to retrieve the authentication token.")

    @task
    def browse_cart(self):
        """Task to view the cart."""
        self._request_cart()

    def _request_cart(self):
        """Helper method to request the cart."""
        with self.client.get(
            "/cart",
            headers={
                **self.default_headers,  # Merging default headers
                "Cookies": f"token={self.token}",
                "Referer": "http://localhost:5000/product/1",
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "same-origin",
                "Sec-Fetch-User": "?1",
                "Upgrade-Insecure-Requests": "1",
            },
            catch_response=True,
        ) as resp:
            if resp.status_code == 200:
                resp.success()
            else:
                resp.failure(f"Failed to load cart, status code {resp.status_code}")


if __name__ == "__main__":
    run_single_user(AddToCart)