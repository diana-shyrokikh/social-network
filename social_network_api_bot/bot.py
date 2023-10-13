import json
import random
import time

import requests

from faker import Faker
from tqdm import tqdm

BASE_URL = "http://app:8000/api/v1/social_network/"

with open(
    "social_network_api_bot/bot_config.json", "r"
) as config_file:
    config = json.load(config_file)

number_of_users = config.get("number_of_users")
max_posts_per_user = config.get("max_posts_per_user")
max_likes_per_user = config.get("max_likes_per_user")


class SocialNetworkAPIBot:
    def __init__(
        self,
        base_url,
        number_of_users,
        max_posts_per_user,
        max_likes_per_user,
    ) -> None:
        self.fake = Faker()
        self.base_url = base_url

        self.number_of_users = number_of_users
        self.max_posts_per_user = max_posts_per_user
        self.max_likes_per_user = max_likes_per_user

        self.users = []

    def wait_for_running_server(self):
        while True:
            try:
                requests.get(self.base_url)
            except (
                    ConnectionError,
                    requests.exceptions.RequestException
            ):
                print("Connection failed. Retrying in 30 seconds...")
                time.sleep(30)
            else:
                print("Connected to the server.")
                break

    def users_make_posts(self) -> None:
        for _ in tqdm(
            range(self.number_of_users),
            desc="Signup users"
        ):
            self.user_actions()

    def users_like_posts(self) -> None:
        posts = self.get_all_posts()

        for user_auth_header in tqdm(
            self.users,
            desc=f"Authorise users"
        ):
            liked_posts = random.sample(
                posts,
                random.randint(
                    1, self.max_likes_per_user
                )
            )
            for post in tqdm(
                liked_posts,
                desc="Like posts"
            ):
                self.like_post(
                    post.get("id"), user_auth_header
                )

    def user_actions(self) -> None:
        user_credentials = self.signup_user()
        user_auth_header = self.get_auth_headers(user_credentials)

        for _ in tqdm(
            range(random.randint(
                1, self.max_posts_per_user
            )),
            desc=f"Creating posts"
        ):
            self.create_post(user_auth_header)

        self.users.append(user_auth_header)

    def signup_user(self) -> dict:
        data = {
            "username": self.fake.user_name(),
            "password": self.fake.password(),
        }

        requests.post(
            f"{self.base_url}signup/",
            data=data
        )

        return data

    def get_auth_headers(self, user: dict) -> dict:
        access_token = requests.post(
            f"{self.base_url}token/",
            data={
                "username": user.get("username"),
                "password": user.get("password"),
            }
        ).json().get("access")
        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        return headers

    def create_post(self, headers: dict) -> None:
        requests.post(
            f"{self.base_url}posts/",
            data={
                "text": self.fake.text(),
            },
            headers=headers
        )

    def like_post(self, post_id, headers: dict) -> None:
        requests.get(
            f"{self.base_url}posts/{post_id}/like",
            headers=headers
        )

    def get_all_posts(self) -> list:
        all_posts = []
        i = 1

        while True:
            posts = requests.get(
                f"{self.base_url}posts/?page={i}"
            ).json()
            all_posts.extend(posts.get("results"))

            if not posts.get("next"):
                break

            i += 1

        return all_posts


if __name__ == "__main__":
    bot = SocialNetworkAPIBot(
        BASE_URL,
        number_of_users,
        max_posts_per_user,
        max_likes_per_user,
    )

    bot.wait_for_running_server()
    bot.users_make_posts()
    bot.users_like_posts()
