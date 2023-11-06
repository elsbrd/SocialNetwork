import asyncio
import aiohttp
import json
import random
from faker import Faker
from typing import Any, Dict, List, Optional, Tuple

fake = Faker()

CONFIG_FILE = "config.json"
BASE_URL = (
    "http://localhost:8000/api"  # Adjust with the actual base URL of your project
)


async def read_config() -> Dict[str, Any]:
    """Reads the configuration file for the bot."""

    with open(CONFIG_FILE, "r") as f:
        return json.load(f)


async def signup_and_login_user(
    session: aiohttp.ClientSession, user_data: Dict[str, str]
) -> Optional[Dict[str, str]]:
    """
    Signs up a user and logs them in to obtain authentication tokens.

    Args:
        session: The HTTP client session.
        user_data: A dictionary with user signup data.

    Returns:
        A dictionary containing the user's authentication tokens.
    """

    async with session.post(
        f"{BASE_URL}/authentication/signup/", json=user_data
    ) as signup_response:
        if signup_response.status == 201:
            login_data = {
                "username": user_data["username"],
                "password": user_data["password"],
            }
            async with session.post(
                f"{BASE_URL}/authentication/token/", data=login_data
            ) as login_response:
                return await login_response.json()
        else:
            return None


async def create_users(
    session: aiohttp.ClientSession, config: Dict[str, int]
) -> List[Dict[str, str]]:
    """
    Creates users according to the specified configuration.

    Args:
        session: The HTTP client session.
        config: Configuration parameters, including the number of users.

    Returns:
        A list of dictionaries containing the authentication tokens for the created users.
    """

    users = []
    for _ in range(config["number_of_users"]):
        password = fake.password()
        user_data = {
            "username": fake.user_name(),
            "email": fake.email(),
            "password": password,
            "password_confirm": password,
        }

        user = await signup_and_login_user(session, user_data)
        if user:
            users.append(user)

    return users


async def create_post(
    session: aiohttp.ClientSession, token: str, title: str, content: str
) -> Dict[str, Any]:
    """
    Creates a post for a user with the given authentication token.

    Args:
        session: The HTTP client session.
        token: The user's authentication token.
        title: The title of the post.
        content: The content of the post.

    Returns:
        A dictionary representing the created post.
    """

    headers = {"Authorization": f"Bearer {token}"}
    async with session.post(
        f"{BASE_URL}/posts/", headers=headers, json={"title": title, "content": content}
    ) as response:
        return await response.json()


async def create_posts_for_user(
    session: aiohttp.ClientSession, user: Dict[str, str], max_posts: int
) -> Tuple[Dict[str, Any]]:
    """
    Creates a specified number of posts for a user.

    Args:
        session: The HTTP client session.
        user: A dictionary containing the user's authentication token.
        max_posts: The maximum number of posts to create for the user.

    Returns:
        A list of dictionaries representing the created posts.
    """

    return await asyncio.gather(
        *[
            create_post(session, user["access"], fake.name(), fake.text())
            for _ in range(random.randint(1, max_posts))
        ]
    )


async def like_post(session: aiohttp.ClientSession, token: str, post_id: int) -> int:
    """
    Likes a post on behalf of a user.

    Args:
        session: The HTTP client session.
        token: The user's authentication token.
        post_id: The ID of the post to like.

    Returns:
        The HTTP status code of the like operation.
    """

    async with session.post(
        f"{BASE_URL}/posts/{post_id}/like/", headers={"Authorization": f"Bearer {token}"}
    ) as response:
        return response.status


async def like_random_posts(
    session: aiohttp.ClientSession,
    users: List[Dict[str, str]],
    posts: List[Dict[str, Any]],
    max_likes: int,
) -> None:
    """
    Likes random posts for each user up to the specified maximum number of likes.

    Args:
        session: The HTTP client session.
        users: A list of users with their authentication tokens.
        posts: A list of posts available to like.
        max_likes: The maximum number of likes a user can make.

    """

    like_tasks = []

    for user in users:
        token = user["access"]

        for _ in range(random.randint(1, max_likes)):
            post = random.choice(posts)
            like_tasks.append(like_post(session, token, post["id"]))

    await asyncio.gather(*like_tasks)


async def main() -> None:
    """
    Main execution function that orchestrates the creation of users, posts, and likes.
    """

    config = await read_config()
    async with aiohttp.ClientSession() as session:
        users = await asyncio.gather(
            *[create_users(session, config) for _ in range(config["number_of_users"])]
        )
        users = [user for sublist in users for user in sublist if user]

        posts = []
        for user in users:
            user_posts = await create_posts_for_user(
                session, user, config["max_posts_per_user"]
            )
            posts.extend(user_posts)

        await like_random_posts(session, users, posts, config["max_likes_per_user"])


if __name__ == "__main__":
    asyncio.run(main())
