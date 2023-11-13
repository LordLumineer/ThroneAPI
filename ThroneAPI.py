from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse, PlainTextResponse
from datetime import datetime
import json
import requests

API_VERSION = "1.0.0"
DOCS_URL = "/"

app = FastAPI(
    title="ThroneAPI",
    description="TEST",
    version=API_VERSION,
    docs_url=DOCS_URL,
)


@app.get("/rawData/Gifted", tags=["Raw"],
         responses={
    200: {
        "description": "Successful response with JSON information about the user's gifted items",
        "content": {"application/json": {"example": {
            "props": "Json information about the user's & gifted items",
            "another_key": "another_value"
        }}}
    },
    500: {
        "description": "Error response when there is an issue with the request",
        "content": {"text/plain": {"example": "Are you sure this is a Throne user with a whitelist? Or Throne removed the JSON file from their page."}}
    }
}
)
async def get_raw_gifted(
    username: str = Query(..., title="Throne Username",
                          description="Username of the Throne user"),
):
    """
    Retrieve information about a Throne user's gifted items.

    Parameters:
    - `username` (str): The username of the Throne user.

    Returns:
    - JSONResponse: A JSON response containing information about the user's gifted items.
    - HTTPException: An exception with a 500 status code and an error message if there is an issue with the request.
    - PlainTextResponse: A plain text response with an error message if there is an issue decoding the JSON data.

    Example:
    ```
    GET /rawData/Gifted?username=example_user

    Response:
    {
        "props": "Json information about the user's & gifted items",
        "another_key": "another_value"
    }
    ```
    """
    throne_url = f"https://throne.com/{username.lower()}/gifters"
    try:
        r = requests.get(throne_url)
        r.raise_for_status()

        start_marker = '<script id="__NEXT_DATA__" type="application/json">'
        end_marker = '</script>'
        start_index = r.text.find(start_marker) + len(start_marker)
        end_index = r.text.find(end_marker, start_index)
        json_data = r.text[start_index:end_index]

        parsed_data = json.loads(json_data)
        return JSONResponse(parsed_data, status_code=200)

    except requests.exceptions.RequestException as e:
        return HTTPException(status_code=500, detail=str(e))

    except json.JSONDecodeError:
        return PlainTextResponse(
            "Are you sure this is a Throne user with a whitelist? Or Throne removed the JSON file from their page.",
            status_code=500,
        )


@app.get("/rawData/Wishlist", tags=["Raw"],
         responses={
    200: {
        "content": {
            "application/json": {
                "example": {
                    "props": "Json information about the user's & wishlist",
                    "another_key": "another_value"
                }
            }
        }
    },
    500: {
        "description": "Error response when there is an issue with the request",
        "content": {
            "text/plain": {
                "example": "Throne API Error: Are you sure this is a Throne user with a wishlist? Or Throne removed the JSON file from their page."
            }
        }
    }
}
)
async def get_raw_wishlist(
    username: str = Query(..., title="Throne Username",
                          description="Username of the Throne user"),
):
    """
    Retrieve information about a Throne user's wishlist.

    Parameters:
    - `username` (str): The username of the Throne user.

    Returns:
    - JSONResponse: A JSON response containing information about the user's wishlist.
    - HTTPException: An exception with a 500 status code and an error message if there is an issue with the request.
    - PlainTextResponse: A plain text response with an error message if there is an issue decoding the JSON data.

    Example:
    ```
    GET /rawData/Wishlist?username=example_user

    Response:
    {
        "props": "Json information about the user's & wishlist",
        "another_key": "another_value"
    }
    ```
    """
    throne_url = f"https://throne.com/{username.lower()}"
    try:
        r = requests.get(throne_url)
        r.raise_for_status()

        start_marker = '<script id="__NEXT_DATA__" type="application/json">'
        end_marker = '</script>'
        start_index = r.text.find(start_marker) + len(start_marker)
        end_index = r.text.find(end_marker, start_index)
        json_data = r.text[start_index:end_index]

        parsed_data = json.loads(json_data)
        return JSONResponse(parsed_data, status_code=200)

    except requests.exceptions.RequestException as e:
        error_message = f"Throne API Request Error: {str(e)}"
        return HTTPException(status_code=500, detail=error_message)

    except json.JSONDecodeError:
        error_message = "Throne API Error: Are you sure this is a Throne user with a wishlist? Or Throne removed the JSON file from their page."
        return PlainTextResponse(error_message, status_code=500)


@app.get("/get_cleaned", tags=["Raw"], 
    responses={
        200: {
            "description": "Successful response with cleaned and organized information about the user",
            "content": {
                "application/json": {
                    "example": {
                        "initialCounts": {"...": "..."},
                        "userInfo": {"...": "..."},
                        "previousGifts": [],
                        "leaderboard": {
                            "lastTwentyGifters": ["..."],
                            "leaderboardAllTime": ["..."],
                            "leaderboardLastWeek": ["..."],
                            "leaderboardLastMonth": ["..."]
                        },
                        "wishlistItems": ["..."],
                        "wishlistCollections": ["..."]
                    }
                }
            }
        },
        500: {
            "description": "Error response when there is an issue with the request",
            "content": {
                "text/plain": {
                    "example": "Throne API Error: Throne has changed their JSON file, please contact the developer to fix this issue."
                }
            }
        }
    }
)
async def get_cleaned(
    username: str = Query(..., title="Throne Username",
                          description="Username of the Throne user")
):
    """
    Retrieve cleaned and organized information about a Throne user.

    Parameters:
    - `username` (str): The username of the Throne user.

    Returns:
    - JSONResponse: A JSON response containing cleaned and organized information about the user.
    - HTTPException: An exception with a 500 status code and an error message if there is an issue with the request.

    Example:
    ```
    GET /get_cleaned?username=example_user

    Successful Response:
    {
        "initialCounts": {"...": "..."},
        "userInfo": {"...": "..."},
        "previousGifts": [],
        "leaderboard": {
            "lastTwentyGifters": ["..."],
            "leaderboardAllTime": ["..."],
            "leaderboardLastWeek": ["..."],
            "leaderboardLastMonth": ["..."]
        },
        "wishlistItems": ["..."],
        "wishlistCollections": ["..."]
    }

    Error Response:
    Throne API Error: Throne has changed their JSON file, please contact the developer to fix this issue.
    ```
    """
    try:
        # Retrieve raw gifted data
        Gifted = json.loads((await get_raw_gifted(username)).body.decode("utf-8"))

        # Retrieve raw wishlist data
        Wishlist = json.loads((await get_raw_wishlist(username)).body.decode("utf-8"))

        # Extract relevant information
        _userInfo = Gifted["props"]["pageProps"]["fallback"][f"public/useCreatorByUsername/{username.lower()}"]
        _previousGifts = Gifted["props"]["pageProps"]["fallback"][f"public/wishlist/usePreviousGifts/{_userInfo['_id']}"]
        _leaderboard = Gifted["props"]["pageProps"]["fallback"][f"api-leaderboard/v1/leaderboard/{_userInfo['_id']}"]
        _initialCounts = Gifted["props"]["pageProps"]["initialCounts"]
        _wishlistItems = Wishlist["props"]["pageProps"]["fallback"][f"public/wishlist/useWishlistItems/{_userInfo['_id']}"]
        _wishlistCollections = Wishlist["props"]["pageProps"]["fallback"][f"public/wishlist/useWishlistCollections/{_userInfo['_id']}"]

        # Organize the information
        output = {
            "initialCounts": _initialCounts,
            "userInfo": _userInfo,
            "previousGifts": _previousGifts,
            "leaderboard": _leaderboard,
            "wishlistItems": _wishlistItems,
            "wishlistCollections": _wishlistCollections
        }

        return JSONResponse(output, status_code=200)

    except Exception as e:
        error_message = "Throne API Error: Throne has changed their JSON file, please contact the developer to fix this issue."
        return HTTPException(status_code=500, detail=str(error_message))


@app.get("/user/Info", tags=["User"], 
    responses={
        200: {
            "description": "Successful response with JSON information about the Throne user",
            "content": {
                "application/json": {
                    "example": {
                        "displayName": "John Doe",
                        "birthday": {"month": 1, "day": 1},
                        "bio": "A passionate Throne user",
                        "createdAt": "2023-01-01 12:00:00",
                        "wishlistItemsCount": 420,
                        "giftedItemsCount": 69,
                        "collectionsCount": 42,
                        "username": "john_doe",
                        "_id": "1234567890",
                        "picture": "https://thronecdn.com/users/john_doe.jpg",
                        "backgroundPictureUrl": "https://thronecdn.com/user-cover-pictures/john_doe_cover.jpg",
                    }
                }
            }
        },
        500: {
            "description": "Error response when there is an issue with the request",
            "content": {"text/plain": {"example": "Throne API Error: Unable to retrieve user information"}},
        },
    },
)
async def get_user_info(
        username: str = Query(..., title="Throne Username",
                              description="Username of the Throne user"),
):
    """
    Retrieve information about a Throne user.

    Parameters:
    - `username` (str): The username of the Throne user.

    Returns:
    - JSONResponse: A JSON response containing user information.
    - HTTPException: An exception with a 500 status code and an error message if there is an issue with the request.
    """
    
    try: 
        data = json.loads((await get_cleaned(username)).body.decode("utf-8"))
        userInfo = data["userInfo"]
        output = {
            "displayName": userInfo["displayName"],
            "birthday": userInfo["birthday"],
            "bio": userInfo["bio"],
            "createdAt": datetime.fromtimestamp(userInfo["createdAt"]/1000).strftime("%Y-%m-%d %H:%M:%S"),
            "wishlistItemsCount": data["initialCounts"]["wishlist"],
            "giftedItemsCount": data["initialCounts"]["previousGifts"],
            "collectionsCount": data["initialCounts"]["collections"],
            "username": userInfo["username"],
            "_id": userInfo["_id"],
            "picture": userInfo["pictureUrl"],
            "backgroundPictureUrl": userInfo["backgroundPictureUrl"],
        }
        return JSONResponse(output, status_code=200)
    
    except Exception as e:
        error_message = f"Throne API Error: {str(e)}"
        return HTTPException(status_code=500, detail=error_message)


@app.get("/user/Socials", tags=["User"], 
    responses={
        200: {
            "description": "Successful response with JSON information about the Throne user's social links",
            "content": {
                "application/json": {
                    "example": {
                        "mainContentPlatform": "Twitch",
                        "Twitch": {"name": "Twitch", "url": "https://twitch.tv/..."},
                        "YouTube": {"name": "YouTube", "url": "https://www.youtube.com/@..."},
                        # Add more social links as needed
                        "...": "..."
                    }
                }
            }
        },
        500: {
            "description": "Error response when there is an issue with the request",
            "content": {"text/plain": {"example": "Throne API Error: Unable to retrieve user social links"}},
        },
    },
)
async def get_user_socials(
    username: str = Query(..., title="Throne Username",
                          description="Username of the Throne user")
):
    """
    Retrieve information about a Throne user's social links.

    Parameters:
    - `username` (str): The username of the Throne user.

    Returns:
    - JSONResponse: A JSON response containing user social links.
    - HTTPException: An exception with a 500 status code and an error message if there is an issue with the request.
    """
    try:
        userInfo = json.loads((await get_cleaned(username)).body.decode("utf-8"))["userInfo"]
        output = {"mainContentPlatform": userInfo["mainContentPlatform"]}
        for social in userInfo["socialLinks"]:
            output[social["type"]] = {"name": social["name"],"url": social["url"]}
        return JSONResponse(output, status_code=200)

    except Exception as e:
        error_message = f"Throne API Error: Unable to retrieve user social links. {str(e)}"
        return HTTPException(status_code=500, detail=error_message)


@app.get("/user/Categories",tags=["User"],
    responses={
        200: {
            "description": "Successful response with JSON information about the Throne user's surprise categories",
            "content": {
                "application/json": {
                    "example": ["Category1", "Category2", "..."]
                }
            }
        },
        500: {
            "description": "Error response when there is an issue with the request",
            "content": {"text/plain": {"example": "Throne API Error: Unable to retrieve user categories"}},
        },
    },
)
async def get_user_categories(
    username: str = Query(..., title="Throne Username", 
                          description="Username of the Throne user"),
):
    """
    Retrieve information about a Throne user's surprise categories.

    Parameters:
    - `username` (str): The username of the Throne user.

    Returns:
    - JSONResponse: A JSON response containing user surprise categories.
    - HTTPException: An exception with a 500 status code and an error message if there is an issue with the request.
    """
    try:
        user_categories = json.loads((await get_cleaned(username)).body.decode("utf-8"))["userInfo"]["surpriseCategories"]
        return JSONResponse(user_categories, status_code=200)

    except Exception as e:
        error_message = f"Throne API Error: Unable to retrieve user categories. {str(e)}"
        return HTTPException(status_code=500, detail=error_message)


@app.get("/user/Interests", tags=["User"],
    responses={
        200: {
            "description": "Successful response with JSON information about the Throne user's interests",
            "content": {
                "application/json": {
                    "example": ["Interest1", "Interest2", "..."]
                }
            }
        },
        500: {
            "description": "Error response when there is an issue with the request",
            "content": {"text/plain": {"example": "Throne API Error: Unable to retrieve user interests"}},
        },
    },
)
async def get_user_interest(
    username: str = Query(..., title="Throne Username", 
                          description="Username of the Throne user"),
):
    """
    Retrieve information about a Throne user's interests.

    Parameters:
    - `username` (str): The username of the Throne user.

    Returns:
    - JSONResponse: A JSON response containing user interests.
    - HTTPException: An exception with a 500 status code and an error message if there is an issue with the request.
    """
    try:
        user_interests = json.loads((await get_cleaned(username)).body.decode("utf-8"))["userInfo"]["interests"]
        return JSONResponse(user_interests, status_code=200)

    except Exception as e:
        error_message = f"Throne API Error: Unable to retrieve user interests. {str(e)}"
        return HTTPException(status_code=500, detail=error_message)


@app.get("/collections", tags=["Collections"],
    responses={
        200: {
            "description": "Successful response with JSON information about the Throne user's collections",
            "content": {
                "application/json": {
                    "example": [
                        {"title": "Collection1", "id": "collection_id_1"},
                        {"title": "Collection2", "id": "collection_id_2"},
                        "..."
                    ]
                }
            }
        },
        500: {
            "description": "Error response when there is an issue with the request",
            "content": {"text/plain": {"example": "Throne API Error: Unable to retrieve user collections"}},
        }
    }
)
async def get_collections(
    username: str = Query(..., title="Throne Username", 
                          description="Username of the Throne user"
    ),
):
    """
    Retrieve information about a Throne user's collections.

    Parameters:
    - `username` (str): The username of the Throne user.

    Returns:
    - JSONResponse: A JSON response containing user collections.
    - HTTPException: An exception with a 500 status code and an error message if there is an issue with the request.
    """
    try:
        wishlist_collections = json.loads((await get_cleaned(username)).body.decode("utf-8"))["wishlistCollections"]

        output = [{"title": collection["title"], "id": collection["id"]} for collection in wishlist_collections]
        return JSONResponse(output, status_code=200)

    except Exception as e:
        error_message = f"Throne API Error: Unable to retrieve user collections. {str(e)}"
        return HTTPException(status_code=500, detail=error_message)

@app.get("/collections/Detailed", tags=["Collections"],
    responses={
        200: {
            "description": "Successful response with JSON information about the Throne user's detailed collections",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "name": "Collection1",
                            "description": "Description of Collection1",
                            "id": "collection_id_1",
                            "updatedAt": "2023-01-01 12:00:00",
                            "items": 3,
                            "individualItems": 2,
                            "<local_currency>_price": 150,
                            "usd_price": 200,
                            "(Optional) <displayCurrency>_price": 180,
                        },
                        "..."
                    ]
                }
            }
        },
        500: {
            "description": "Error response when there is an issue with the request",
            "content": {"text/plain": {"example": "Throne API Error: Unable to retrieve detailed collections"}},
        }
    }
)
async def get_collections_detailed(
    username: str = Query(..., title="Throne Username", 
                          description="Username of the Throne user"),
    displayCurrency: str = Query(None, title="Display Currency", 
                                 description="Additional currency to display the value in"),
):
    """
    Retrieve detailed information about a Throne user's collections.

    Parameters:
    - `username` (str): The username of the Throne user.
    - `displayCurrency` (str): (Optional) Additional currency to display the value in.

    Returns:
    - JSONResponse: A JSON response containing detailed information about user collections.
    - HTTPException: An exception with a 500 status code and an error message if there is an issue with the request.
    """
    try:
        data = json.loads((await get_cleaned(username)).body.decode("utf-8"))
        collections = data["wishlistCollections"]
        items = data["wishlistItems"]
        output = []

        for collection in collections:
            collection_output = {
                "name": collection["title"],
                "description": collection["description"],
                "id": collection["id"],
                "updatedAt": datetime.fromtimestamp(collection["updatedAt"] / 1000).strftime("%Y-%m-%d %H:%M:%S"),
            }

            collection_id = collection["id"]
            total_count = 0
            individual_count = 0
            price = {}

            for item in items:
                if collection_id in item["collectionIds"]:
                    individual_count += 1
                    total_count += 1 * item["quantity"]
                    if item["currency"] not in price:
                        price[item["currency"]] = 0
                    price[item["currency"]] += (item["price"] / 100) * item["quantity"]

            usd_value = 0
            collection_output["items"] = total_count
            collection_output["individualItems"] = individual_count

            for currency in price:
                usd_value += await currency_converter(price[currency], currency.upper(), "USD")
                collection_output[f"{currency.lower()}_price"] = price[currency]

            collection_output["usd_price"] = usd_value

            if displayCurrency:
                collection_output[f"{displayCurrency.lower()}_price"] = await currency_converter(
                    usd_value, "USD", displayCurrency.upper()
                )

            output.append(collection_output)

        return JSONResponse(output, status_code=200)

    except Exception as e:
        error_message = f"Throne API Error: Unable to retrieve detailed collections. {str(e)}"
        return HTTPException(status_code=500, detail=error_message)


@app.get("/collections/Collection", tags=["Collections"],
    responses={
        200: {
            "description": "Successful response with JSON information about a specific Throne user's collection",
            "content": {
                "application/json": {
                    "example": {
                        "name": "Collection1",
                        "description": "Description of Collection1",
                        "id": "collection_id_1",
                        "createdAt": "2023-01-01 12:00:00",
                        "updatedAt": "2023-01-01 12:30:00",
                        "image": "https://thronecdn.com/wishlistCollections/collection_image.jpg",
                        "items": 3,
                        "individualItems": 2,
                        "<local_currency>_price": 150,
                        "usd_price": 200,
                        "(Optional) <display_currency>_price": 180,
                    }
                }
            }
        },
        500: {
            "description": "Error response when there is an issue with the request",
            "content": {"text/plain": {"example": "Throne API Error: Unable to retrieve collection details"}},
        },
    },
)
async def get_collection(
    username: str = Query(..., title="Throne Username", 
                          description="Username of the Throne user"),
    id: str = Query(..., title="Collection ID", 
                    description="Get details about a specific collection (get its ID from GET /collections)"),
    displayCurrency: str = Query(None, title="Display Currency", 
                                 description="Additional currency to display the value in"),
):
    """
    Retrieve detailed information about a specific collection of a Throne user.

    Parameters:
    - `username` (str): The username of the Throne user.
    - `id` (str): Collection ID obtained from the GET /collections endpoint.
    - `displayCurrency` (str): (Optional) Additional currency to display the value in.

    Returns:
    - JSONResponse: A JSON response containing detailed information about the user's collection.
    - HTTPException: An exception with a 500 status code and an error message if there is an issue with the request.
    """
    try:
        data = json.loads((await get_cleaned(username)).body.decode("utf-8"))
        collections = data["wishlistCollections"]
        items = data["wishlistItems"]
        single_collection = {}

        for collection in collections:
            if collection["id"] == id:
                single_collection = collection
                break

        output = {
            "name": single_collection["title"],
            "description": single_collection["description"],
            "id": single_collection["id"],
            "createdAt": datetime.fromtimestamp(single_collection["createdAt"] / 1000).strftime("%Y-%m-%d %H:%M:%S"),
            "updatedAt": datetime.fromtimestamp(single_collection["updatedAt"] / 1000).strftime("%Y-%m-%d %H:%M:%S"),
            "image": single_collection["imageSrc"],
        }

        total_count = 0
        individual_count = 0
        price = {}

        for item in items:
            if id in item["collectionIds"]:
                individual_count += 1
                total_count += 1 * item["quantity"]
                if item["currency"] not in price:
                    price[item["currency"]] = 0
                price[item["currency"]] += (item["price"] / 100) * item["quantity"]

        output["items"] = total_count
        output["individualItems"] = individual_count

        usd_price = 0

        for currency in price:
            usd_price += await currency_converter(price[currency], currency.upper(), "USD")
            output[f"{currency.lower()}_price"] = price[currency]

        output["usd_price"] = usd_price

        if displayCurrency:
            output[f"{displayCurrency.lower()}_price"] = await currency_converter(
                usd_price, "USD", displayCurrency.upper()
            )

        return JSONResponse(output, status_code=200)

    except Exception as e:
        error_message = f"Throne API Error: Unable to retrieve collection details. {str(e)}"
        return HTTPException(status_code=500, detail=error_message)


@app.get("/Collections/Items", tags=["Collections", "Items"],
    responses={
        200: {
            "description": "Successful response with JSON information about items in a specific collection",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "name": "Item1",
                            "quantity": 1,
                            "price": 4.20,
                            "currency": "USD",
                            "id": "item_id_1",
                        },
                        # Add more items as needed
                        "..."
                    ]
                }
            }
        },
        500: {
            "description": "Error response when there is an issue with the request",
            "content": {"text/plain": {"example": "Throne API Error: Unable to retrieve collection items"}},
        },
    },
)
async def get_collection_items(
    username: str = Query(..., title="Throne Username", 
                          description="Username of the Throne user"),
    id: str = Query(..., title="Collection ID", 
                    description="Get details about a specific collection (get its ID from GET /collections)"),
):
    """
    Retrieve information about items in a specific collection of a Throne user.

    Parameters:
    - `username` (str): The username of the Throne user.
    - `id` (str): Collection ID obtained from the GET /collections endpoint.

    Returns:
    - JSONResponse: A JSON response containing information about items in the specified collection.
    - HTTPException: An exception with a 500 status code and an error message if there is an issue with the request.
    """
    try:
        items = json.loads((await get_cleaned(username)).body.decode("utf-8"))["wishlistItems"]
        output = []

        for item in items:
            if id in item["collectionIds"]:
                item_info = {
                    "name": item["name"],
                    "quantity": item["quantity"],
                    "price": item["price"] / 100,
                    "currency": item["currency"],
                    "id": item["id"],
                }
                output.append(item_info)

        return JSONResponse(output, status_code=200)

    except Exception as e:
        error_message = f"Throne API Error: Unable to retrieve collection items. {str(e)}"
        return HTTPException(status_code=500, detail=error_message)


@app.get("/items", tags=["Items"],
    responses={
        200: {
            "description": "Successful response with JSON information about items in a user's wishlist",
            "content": {
                "application/json": {
                    "example": [
                        {"name": "Item1", "id": "item_id_1"},
                        "..."
                    ]
                }
            }
        },
        500: {
            "description": "Error response when there is an issue with the request",
            "content": {"text/plain": {"example": "Throne API Error: Unable to retrieve wishlist items"}},
        },
    },
)
async def get_items(
    username: str = Query(..., title="Throne Username", 
                          description="Username of the Throne user"),
):
    """
    Retrieve information about items in a user's wishlist.

    Parameters:
    - `username` (str): The username of the Throne user.

    Returns:
    - JSONResponse: A JSON response containing information about items in the user's wishlist.
    - HTTPException: An exception with a 500 status code and an error message if there is an issue with the request.
    """
    try:
        wishlist_items = json.loads((await get_cleaned(username)).body.decode("utf-8"))["wishlistItems"]
        output = [{"name": item["name"], "id": item["id"]} for item in wishlist_items]

        return JSONResponse(output, status_code=200)

    except Exception as e:
        error_message = f"Throne API Error: Unable to retrieve wishlist items. {str(e)}"
        return HTTPException(status_code=500, detail=error_message)


@app.get("/items/Detailed", tags=["Items"],
    responses={
        200: {
            "description": "Successful response with detailed JSON information about items in a user's wishlist",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "name": "Item1",
                            "id": "item_id_1",
                            "addedAt": "2023-01-01 12:00:00",
                            "isDigital": False,
                            "isAvailable": True,
                            "notInStock": False,
                            "quantity": 1,
                            "<local_currency>_total": {
                                "currency": "USD",
                                "price": 4.20,
                                "totalPrice": 4.20,
                                "shipping": 0.69,
                                "totalPriceWithShipping": 4.89,
                            },
                        },
                        "..."
                    ]
                }
            }
        },
        500: {
            "description": "Error response when there is an issue with the request",
            "content": {"text/plain": {"example": "Throne API Error: Unable to retrieve detailed wishlist items"}},
        },
    },
)
async def get_items_detailed(
    username: str = Query(..., title="Throne Username", 
                          description="Username of the Throne user"),
):
    """
    Retrieve detailed information about items in a user's wishlist.

    Parameters:
    - `username` (str): The username of the Throne user.

    Returns:
    - JSONResponse: A JSON response containing detailed information about items in the user's wishlist.
    - HTTPException: An exception with a 500 status code and an error message if there is an issue with the request.
    """
    try:
        wishlist_items = json.loads((await get_cleaned(username)).body.decode("utf-8"))["wishlistItems"]
        output = []

        for item in wishlist_items:
            item_info = {
                "name": item["name"],
                "id": item["id"],
                "addedAt": datetime.fromtimestamp(item["createdAt"] / 1000).strftime("%Y-%m-%d %H:%M:%S"),
                "isDigital": item["isDigitalGood"],
                "isAvailable": item.get("isAvailable", None),
                "notInStock": item.get("notInStock", None),
                "quantity": item["quantity"],
                f"{item['currency'].lower()}_total": {
                    "currency": item["currency"],
                    "price": item["price"] / 100,
                    "totalPrice": item["price"] / 100 * item["quantity"],
                    "shipping": item.get("shipping", 0) / 100,
                    "totalPriceWithShipping": item["price"] * item["quantity"] / 100 + item.get("shipping", 0) / 100,
                },
            }
            output.append(item_info)

        return JSONResponse(output, status_code=200)

    except Exception as e:
        error_message = f"Throne API Error: Unable to retrieve detailed wishlist items. {str(e)}"
        return HTTPException(status_code=500, detail=error_message)


@app.get("/items/Item", tags=["Items"],
    responses={
        200: {
            "description": "Successful response with detailed JSON information about a specific item in a user's wishlist",
            "content": {
                "application/json": {
                    "example": {
                        "name": "Item1",
                        "link": "https://example.com/item1",
                        "addedAt": "2023-01-01 12:00:00",
                        "isDigital": False,
                        "isAvailable": True,
                        "notInStock": [False],
                        "quantity": 1,
                        "<local_currency>_total": {
                            "currency": "<local_currency>",
                            "price": 4.20,
                            "totalPrice": 4.20,
                            "shipping": 0.69,
                            "totalPriceWithShipping": 4.89,
                        },
                        "usd_total": {
                            "currency": "USD",
                            "price": 4.20,
                            "totalPrice": 4.20,
                            "shipping": 0.69,
                            "totalPriceWithShipping": 4.89,
                        },
                        "(optional) <display_currency>_total": {
                            "currency": "<display_currency>",
                            "price": 3.50,
                            "totalPrice": 3.50,
                            "shipping": 0.50,
                            "totalPriceWithShipping": 4.00,
                        },
                        "image": "https://thronecdn.com/wishlistItems/item_id_1.jpg",
                        "id": "item_id_1",
                    }
                }
            }
        },
        500: {
            "description": "Error response when there is an issue with the request",
            "content": {"text/plain": {"example": "Throne API Error: Unable to retrieve detailed item"}},
        },
    },
)
async def get_item(
    username: str = Query(..., title="Throne Username", 
                          description="Username of the Throne user"),
    id: str = Query(..., title="Item ID", 
                    description="Get details about a specific item (get its ID from GET /items)"),
    displayCurrency: str = Query(None, title="Display Currency", 
                                 description="Additional currency to display the value in"),
):
    """
    Retrieve detailed information about a specific item in a user's wishlist.

    Parameters:
    - `username` (str): The username of the Throne user.
    - `id` (str): The ID of the item to retrieve details.
    - `displayCurrency` (str, optional): Additional currency to display the value in.

    Returns:
    - JSONResponse: A JSON response containing detailed information about the specified item.
    - HTTPException: An exception with a 500 status code and an error message if there is an issue with the request.
    """
    try:
        wishlist_items = json.loads((await get_cleaned(username)).body.decode("utf-8"))["wishlistItems"]
        single_item = {}

        for item in wishlist_items:
            if item["id"] == id:
                single_item = item
                break

        output = {
            "name": single_item["name"],
            "link": single_item.get("link", None),
            "addedAt": datetime.fromtimestamp(single_item["createdAt"] / 1000).strftime("%Y-%m-%d %H:%M:%S"),
            "isDigital": single_item["isDigitalGood"],
            "isAvailable": single_item.get("isAvailable", None),
            "notInStock": single_item.get("notInStock", None),
            "quantity": single_item["quantity"],
            f"{single_item['currency'].lower()}_total": {
                "currency": single_item["currency"],
                "price": single_item["price"] / 100,
                "totalPrice": single_item["price"] / 100 * single_item["quantity"],
                "shipping": single_item.get("shipping", 0) / 100,
                "totalPriceWithShipping": (single_item["price"] * single_item["quantity"] / 100) + single_item.get("shipping", 0) / 100,
            },
            "usd_total": {
                "currency": "USD",
                "price": await currency_converter(single_item["price"] / 100, single_item["currency"].upper(), "USD"),
                "totalPrice": await currency_converter(single_item["price"] / 100 * single_item["quantity"], single_item["currency"].upper(), "USD"),
                "shipping": await currency_converter(single_item.get("shipping", 0) / 100, single_item["currency"].upper(), "USD"),
                "totalPriceWithShipping": await currency_converter((single_item["price"] * single_item["quantity"] / 100) + single_item.get("shipping", 0) / 100, single_item["currency"].upper(), "USD"),
            },
        }

        if displayCurrency:
            output[f"{displayCurrency.lower()}_total"] = {
                "currency": displayCurrency.upper(),
                "price": await currency_converter(single_item["price"] / 100, single_item["currency"].upper(), displayCurrency.upper()),
                "totalPrice": await currency_converter(single_item["price"] / 100 * single_item["quantity"], single_item["currency"].upper(), displayCurrency.upper()),
                "shipping": await currency_converter(single_item.get("shipping", 0) / 100, single_item["currency"].upper(), displayCurrency.upper()),
                "totalPriceWithShipping": await currency_converter((single_item["price"] * single_item["quantity"] / 100) + single_item.get("shipping", 0) / 100, single_item["currency"].upper(), displayCurrency.upper()),
            }

        output["image"] = single_item["imgLink"]
        output["id"] = single_item["id"]

        return JSONResponse(output, status_code=200)

    except Exception as e:
        error_message = f"Throne API Error: Unable to retrieve detailed item. {str(e)}"
        return HTTPException(status_code=500, detail=error_message)


@app.get("/previousGifts", tags=["Previous Gifts"],
    responses={
        200: {
            "description": "Successful response with JSON information about previous gifts received by the user",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "name": "Gift1",
                            "gifters": [
                                {"username": "Gifter1"},
                                {"username": "Gifter2"},
                            ],
                            "id": "gift_id_1",
                        },
                        "..."
                    ]
                }
            }
        },
        500: {
            "description": "Error response when there is an issue with the request",
            "content": {"text/plain": {"example": "Throne API Error: Unable to retrieve previous gifts"}},
        },
    },
)
async def get_previous_gifts(
    username: str = Query(..., title="Throne Username", 
                          description="Username of the Throne user"),
):
    """
    Retrieve information about previous gifts received by the user.

    Parameters:
    - `username` (str): The username of the Throne user.

    Returns:
    - JSONResponse: A JSON response containing information about previous gifts.
    - HTTPException: An exception with a 500 status code and an error message if there is an issue with the request.
    """
    try:
        previous_gifts = json.loads((await get_cleaned(username)).body.decode("utf-8"))["previousGifts"]
        output = []

        for gift in previous_gifts:
            gifters = [{"username": gifter["customerUsername"]} for gifter in gift["customizations"]["customers"]]
            output.append({"name": gift["name"], "gifters": gifters, "id": gift["id"]})

        return JSONResponse(output, status_code=200)

    except Exception as e:
        error_message = f"Throne API Error: Unable to retrieve previous gifts. {str(e)}"
        return HTTPException(status_code=500, detail=error_message)

@app.get("/previousGifts/Detailed", tags=["Previous Gifts"],
    responses={
        200: {
            "description": "Successful response with detailed JSON information about previous gifts received by the user",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "name": "Gift1",
                            "gifters": [
                                {"username": "Gifter1"},
                                {"username": "Gifter2"},
                            ],
                            "purchasedAt": "2023-01-01 12:00:00",
                            "status": "delivered",
                            "isComplete": False,
                            "isDigital": False,
                            "isCrowdfunded": False,
                            "<local_currency>_total": {
                                "currency": "<local_currency>",
                                "price": 1,
                                "fees": 0,
                                "subTotal": 2,
                                "shipping": 1,
                                "total": 3,
                            },
                            "usd_total": {
                                "currency": "USD",
                                "price": 1,
                                "fees": 0,
                                "subTotal": 2,
                                "shipping": 1,
                                "total": 3,
                            },
                            "id": "gift_id_1",
                        },
                        "..."
                    ]
                }
            }
        },
        500: {
            "description": "Error response when there is an issue with the request",
            "content": {"text/plain": {"example": "Throne API Error: Unable to retrieve detailed previous gifts"}},
        },
    },
)
async def get_previous_gifts_detailed(
    username: str = Query(..., title="Throne Username", 
                          description="Username of the Throne user"),
):
    """
    Retrieve detailed information about previous gifts received by the user.

    Parameters:
    - `username` (str): The username of the Throne user.

    Returns:
    - JSONResponse: A JSON response containing detailed information about previous gifts.
    - HTTPException: An exception with a 500 status code and an error message if there is an issue with the request.
    """
    try:
        previous_gifts = json.loads((await get_cleaned(username)).body.decode("utf-8"))["previousGifts"]
        output = []

        for gift in previous_gifts:
            gifters = [{"username": gifter["customerUsername"]} for gifter in gift["customizations"]["customers"]]
            output.append({
                "name": gift["name"],
                "gifters": gifters,
                "purchasedAt": datetime.fromtimestamp(gift["purchasedAt"]/1000).strftime("%Y-%m-%d %H:%M:%S"),
                "status": gift["status"],
                "isComplete": gift["isComplete"],
                "isDigital": gift["isDigitalGood"],
                "isCrowdfunded": gift["isCrowdfunded"],
                "local_currency_total": {
                    "currency": gift["total"]["currency"],
                    "price": gift["total"]["price"]/100,
                    "fees": 0 if not gift["total"]["fees"] else gift["total"]["fees"]/100,
                    "subTotal": 0 if not gift["total"]["subTotal"] else gift["total"]["subTotal"]/100,
                    "shipping": gift["total"]["shipping"]/100,
                    "total": 0 if not gift["total"]["total"] else gift["total"]["total"]/100,
                },
                "usd_total": {
                    "currency": "USD",
                    "price": gift["totalUsd"]["price"]/100,
                    "fees": 0 if not gift["totalUsd"]["fees"] else gift["totalUsd"]["fees"]/100,
                    "subTotal": 0 if not gift["totalUsd"]["subTotal"] else gift["totalUsd"]["subTotal"]/100,
                    "shipping": gift["totalUsd"]["shipping"]/100,
                    "total": 0 if not gift["totalUsd"]["total"] else gift["totalUsd"]["total"]/100,
                },
                "id": gift["id"],
            })

        return JSONResponse(output, status_code=200)

    except Exception as e:
        error_message = f"Throne API Error: Unable to retrieve detailed previous gifts. {str(e)}"
        return HTTPException(status_code=500, detail=error_message)


@app.get("/previousGifts/Gift", tags=["Previous Gifts"],
    responses={
        200: {
            "description": "Successful response with detailed JSON information about a specific previous gift received by the user",
            "content": {
                "application/json": {
                    "example": {
                        "name": "Gift1",
                        "gifters": [
                            {"username": "Gifter1", "image": "https://thronecdn.com/users/gifter1.jpg"},
                            {"username": "Gifter2", "image": "https://thronecdn.com/users/gifter2.jpg"},
                        ],
                        "purchasedAt": "2023-09-08 23:56:43",
                        "status": "delivered",
                        "id": "gift_id_1",
                        "link": "https://throne.com/gift1",
                        "image": "https://thronecdn.com/wishlistItems/gift1.jpg",
                        "isComplete": False,
                        "isDigital": False,
                        "isCrowdfunded": False,
                        "<local_currency>_total": {
                            "currency": "<local_currency>",
                            "price": 1,
                            "fees": 0,
                            "subTotal": 2,
                            "shipping": 1,
                            "total": 3,
                        },
                        "usd_total": {
                            "currency": "USD",
                            "price": 1,
                            "fees": 0,
                            "subTotal": 2,
                            "shipping": 1,
                            "total": 3,
                        },
                        "<display_currency>_total": {
                            "currency": "<display_currency>",
                            "price": 1,
                            "fees": 0,
                            "subTotal": 2,
                            "shipping": 1,
                            "total": 3,
                        },
                    }
                }
            }
        },
        500: {
            "description": "Error response when there is an issue with the request",
            "content": {"text/plain": {"example": "Throne API Error: Unable to retrieve detailed previous gift"}},
        },
    },
)
async def get_previous_gift(
    username: str = Query(..., title="Throne Username", 
                          description="Username of the Throne user"),
    id: str = Query(..., title="Gift ID", 
                    description="Get details about a specific gift (get its ID from GET /previousGifts)"),
    displayCurrency: str = Query(None, title="Display Currency", 
                                 description="Additional currency to display the value in"),
):
    """
    Retrieve detailed information about a specific previous gift received by the user.

    Parameters:
    - `username` (str): The username of the Throne user.
    - `id` (str): The ID of the specific gift to retrieve details.
    - `displayCurrency` (str, optional): Additional currency to display the value in.

    Returns:
    - JSONResponse: A JSON response containing detailed information about the specified previous gift.
    - HTTPException: An exception with a 500 status code and an error message if there is an issue with the request.
    """
    try:
        previous_gifts = json.loads((await get_cleaned(username)).body.decode("utf-8"))["previousGifts"]
        single_gift = next((gift for gift in previous_gifts if gift["id"] == id), None)

        if single_gift:
            gifters = [{"username": gifter["customerUsername"], "image": gifter["customerImage"]} for gifter in single_gift["customizations"]["customers"]]
            output = {
                "name": single_gift["name"],
                "gifters": gifters,
                "purchasedAt": datetime.fromtimestamp(single_gift["purchasedAt"]/1000).strftime("%Y-%m-%d %H:%M:%S"),
                "status": single_gift["status"],
                "id": single_gift["id"],
                "link": single_gift.get("link", None),
                "image": single_gift["imageSrc"],
                "isComplete": single_gift["isComplete"],
                "isDigital": single_gift["isDigitalGood"],
                "isCrowdfunded": single_gift["isCrowdfunded"],
                "local_currency_total": {
                    "currency": single_gift["total"]["currency"],
                    "price": single_gift["total"]["price"]/100,
                    "fees": 0 if not single_gift["total"]["fees"] else single_gift["total"]["fees"]/100,
                    "subTotal": 0 if not single_gift["total"]["subTotal"] else single_gift["total"]["subTotal"]/100,
                    "shipping": single_gift["total"]["shipping"]/100,
                    "total": 0 if not single_gift["total"]["total"] else single_gift["total"]["total"]/100,
                },
                "usd_total": {
                    "currency": "USD",
                    "price": single_gift["totalUsd"]["price"]/100,
                    "fees": 0 if not single_gift["totalUsd"]["fees"] else single_gift["totalUsd"]["fees"]/100,
                    "subTotal": 0 if not single_gift["totalUsd"]["subTotal"] else single_gift["totalUsd"]["subTotal"]/100,
                    "shipping": single_gift["totalUsd"]["shipping"]/100,
                    "total": 0 if not single_gift["totalUsd"]["total"] else single_gift["totalUsd"]["total"]/100,
                },
            }

            if displayCurrency:
                output[f"{displayCurrency.lower()}_total"] = {
                    "currency": displayCurrency.upper(),
                    "price": await currency_converter(single_gift["totalUsd"]["price"]/100, "USD", displayCurrency.upper()),
                    "fees": 0 if not single_gift["totalUsd"]["fees"] else await currency_converter(single_gift["totalUsd"]["fees"]/100, "USD", displayCurrency.upper()),
                    "subTotal": 0 if not single_gift["totalUsd"]["subTotal"] else await currency_converter(single_gift["totalUsd"]["subTotal"]/100, "USD", displayCurrency.upper()),
                    "shipping": await currency_converter(single_gift["totalUsd"]["shipping"]/100, "USD", displayCurrency.upper()),
                    "total": 0 if not single_gift["totalUsd"]["total"] else await currency_converter(single_gift["totalUsd"]["total"]/100, "USD", displayCurrency.upper()),
                }

            return JSONResponse(output, status_code=200)

        return JSONResponse({"detail": "Gift not found"}, status_code=404)

    except Exception as e:
        error_message = f"Throne API Error: Unable to retrieve detailed previous gift. {str(e)}"
        return HTTPException(status_code=500, detail=error_message)


@app.get("/previousGifts/latest", tags=["Previous Gifts"],
    responses={
        200: {
            "description": "Successful response with detailed JSON information about the latest previous gift received by the user",
            "content": {
                "application/json": {
                    "example": {
                        "name": "Latest Gift",
                        "gifters": [
                            {"username": "Gifter1", "image": "https://thronecdn.com/users/gifter1.jpg"},
                            {"username": "Gifter2", "image": "https://thronecdn.com/users/gifter2.jpg"},
                        ],
                        "purchasedAt": "2023-09-08 23:56:43",
                        "status": "delivered",
                        "id": "latest_gift_id",
                        "link": "https://throne.com/latest-gift",
                        "image": "https://thronecdn.com/wishlistItems/latest-gift.jpg",
                        "isComplete": False,
                        "isDigital": False,
                        "isCrowdfunded": False,
                        "<local_currency>_total": {
                            "currency": "<local_currency>",
                            "price": 1,
                            "fees": 0,
                            "subTotal": 2,
                            "shipping": 1,
                            "total": 3,
                        },
                        "usd_total": {
                            "currency": "USD",
                            "price": 1,
                            "fees": 0,
                            "subTotal": 2,
                            "shipping": 1,
                            "total": 3,
                        },
                        "<display_currency>_total": {
                            "currency": "<display_currency>",
                            "price": 1,
                            "fees": 0,
                            "subTotal": 2,
                            "shipping": 1,
                            "total": 3,
                        },
                    }
                }
            }
        },
        500: {
            "description": "Error response when there is an issue with the request",
            "content": {"text/plain": {"example": "Throne API Error: Unable to retrieve detailed latest gift"}},
        },
    },
)
async def get_latest_gift(
    username: str = Query(..., title="Throne Username", 
                          escription="Username of the Throne user"),
    displayCurrency: str = Query(None, title="Display Currency", 
                                 description="Additional currency to display the value in"),
):
    """
    Retrieve detailed information about the latest previous gift received by the user.

    Parameters:
    - `username` (str): The username of the Throne user.
    - `displayCurrency` (str, optional): Additional currency to display the value in.

    Returns:
    - JSONResponse: A JSON response containing detailed information about the latest previous gift.
    - HTTPException: An exception with a 500 status code and an error message if there is an issue with the request.
    """
    try:
        previous_gifts = json.loads((await get_cleaned(username)).body.decode("utf-8"))["previousGifts"]
        latest_gift = max(previous_gifts, key=lambda x: x["purchasedAt"])

        gifters = [{"username": gifter["customerUsername"], "image": gifter["customerImage"]} for gifter in latest_gift["customizations"]["customers"]]
        output = {
            "name": latest_gift["name"],
            "gifters": gifters,
            "purchasedAt": datetime.fromtimestamp(latest_gift["purchasedAt"]/1000).strftime("%Y-%m-%d %H:%M:%S"),
            "status": latest_gift["status"],
            "id": latest_gift["id"],
            "link": latest_gift.get("link", None),
            "image": latest_gift["imageSrc"],
            "isComplete": latest_gift["isComplete"],
            "isDigital": latest_gift["isDigitalGood"],
            "isCrowdfunded": latest_gift["isCrowdfunded"],
            "local_currency_total": {
                "currency": latest_gift["total"]["currency"],
                "price": latest_gift["total"]["price"]/100,
                "fees": 0 if not latest_gift["total"]["fees"] else latest_gift["total"]["fees"]/100,
                "subTotal": 0 if not latest_gift["total"]["subTotal"] else latest_gift["total"]["subTotal"]/100,
                "shipping": latest_gift["total"]["shipping"]/100,
                "total": 0 if not latest_gift["total"]["total"] else latest_gift["total"]["total"]/100,
            },
            "usd_total": {
                "currency": "USD",
                "price": latest_gift["totalUsd"]["price"]/100,
                "fees": 0 if not latest_gift["totalUsd"]["fees"] else latest_gift["totalUsd"]["fees"]/100,
                "subTotal": 0 if not latest_gift["totalUsd"]["subTotal"] else latest_gift["totalUsd"]["subTotal"]/100,
                "shipping": latest_gift["totalUsd"]["shipping"]/100,
                "total": 0 if not latest_gift["totalUsd"]["total"] else latest_gift["totalUsd"]["total"]/100,
            },
        }

        if displayCurrency:
            output[f"{displayCurrency.lower()}_total"] = {
                "currency": displayCurrency.upper(),
                "price": await currency_converter(latest_gift["totalUsd"]["price"]/100, "USD", displayCurrency.upper()),
                "fees": 0 if not latest_gift["totalUsd"]["fees"] else await currency_converter(latest_gift["totalUsd"]["fees"]/100, "USD", displayCurrency.upper()),
                "subTotal": 0 if not latest_gift["totalUsd"]["subTotal"] else await currency_converter(latest_gift["totalUsd"]["subTotal"]/100, "USD", displayCurrency.upper()),
                "shipping": await currency_converter(latest_gift["totalUsd"]["shipping"]/100, "USD", displayCurrency.upper()),
                "total": 0 if not latest_gift["totalUsd"]["total"] else await currency_converter(latest_gift["totalUsd"]["total"]/100, "USD", displayCurrency.upper()),
            }

        return JSONResponse(output, status_code=200)

    except Exception as e:
        error_message = f"Throne API Error: Unable to retrieve detailed latest gift. {str(e)}"
        return HTTPException(status_code=500, detail=error_message)


@app.get("/previousGifts/total", tags=["Previous Gifts"],
    responses={
        200: {
            "description": "Successful response with total summary of the user's previous gifts",
            "content": {
                "application/json": {
                    "example": {
                        "nbGifts": 420,
                        "nbGifters": 69,
                        "usd_price": 1,
                        "usd_fees": 1,
                        "usd_subtotal": 2,
                        "usd_shipping": 1,
                        "usd_total": 3,
                        "<display_currency>_price": 1,
                        "<display_currency>_fees": 1,
                        "<display_currency>_subtotal": 2,
                        "<display_currency>_shipping": 1,
                        "<display_currency>_total": 3,
                    }
                }
            }
        },
        500: {
            "description": "Error response when there is an issue with the request",
            "content": {"text/plain": {"example": "Throne API Error: Unable to retrieve total summary of previous gifts"}},
        },
    },
)
async def get_total(
    username: str = Query(..., title="Throne Username", 
                          description="Username of the Throne user"),
    displayCurrency: str = Query(None, title="Display Currency", 
                                 description="Additional currency to display the value in"),
):
    """
    Retrieve the total summary of the user's previous gifts.

    Parameters:
    - `username` (str): The username of the Throne user.
    - `displayCurrency` (str, optional): Additional currency to display the value in.

    Returns:
    - JSONResponse: A JSON response with the total summary of the user's previous gifts.
    - HTTPException: An exception with a 500 status code and an error message if there is an issue with the request.
    """
    try:
        previous_gifts = json.loads((await get_cleaned(username)).body.decode("utf-8"))["previousGifts"]

        nb_gifts = len(previous_gifts)
        gifters = set()
        usd_price = 0
        usd_fees = 0
        usd_subtotal = 0
        usd_shipping = 0
        usd_total = 0

        for gift in previous_gifts:
            for gifter in gift["customizations"]["customers"]:
                gifters.add(gifter["customerUsername"])

            usd_price += gift["totalUsd"]["price"]/100
            usd_fees += 0 if not gift["totalUsd"]["fees"] else gift["totalUsd"]["fees"]/100
            usd_subtotal += 0 if not gift["totalUsd"]["subTotal"] else gift["totalUsd"]["subTotal"]/100
            usd_shipping += gift["totalUsd"]["shipping"]/100
            usd_total += 0 if not gift["totalUsd"]["total"] else gift["totalUsd"]["total"]/100

        output = {
            "nbGifts": nb_gifts,
            "nbGifters": len(gifters),
            "usd_price": usd_price,
            "usd_fees": usd_fees,
            "usd_subtotal": usd_subtotal,
            "usd_shipping": usd_shipping,
            "usd_total": usd_total,
        }

        if displayCurrency:
            output[f"{displayCurrency.lower()}_price"] = await currency_converter(usd_price, "USD", displayCurrency.upper())
            output[f"{displayCurrency.lower()}_fees"] = await currency_converter(usd_fees, "USD", displayCurrency.upper())
            output[f"{displayCurrency.lower()}_subtotal"] = await currency_converter(usd_subtotal, "USD", displayCurrency.upper())
            output[f"{displayCurrency.lower()}_shipping"] = await currency_converter(usd_shipping, "USD", displayCurrency.upper())
            output[f"{displayCurrency.lower()}_total"] = await currency_converter(usd_total, "USD", displayCurrency.upper())

        return JSONResponse(output, status_code=200)

    except Exception as e:
        error_message = f"Throne API Error: Unable to retrieve total summary of previous gifts. {str(e)}"
        return HTTPException(status_code=500, detail=error_message)


@app.get("/gifters/latest", tags=["Gifters"], responses={
    200: {
        "content": {
            "application/json": {
                "example": [
                    {
                        "username": "...",
                        "image": "https://thronecdn.com/users/...",
                        "latestGift": {
                            "name": "...",
                            "purchasedAt": "YYYY-MM-DD hh:mm:ss",
                            "status": "shipped",
                            "isComplete": False,
                            "isDigital": False,
                            "isCrowdfunded": False,
                            "<local currency>_total": {
                                "currency": "...",
                                "price": 2,
                                "fees": 0,
                                "subTotal": 0,
                                "shipping": 1,
                                "total": 0
                            },
                            "usd_total": {
                                "currency": "USD",
                                "price": 2,
                                "fees": 0,
                                "subTotal": 0,
                                "shipping": 1,
                                "total": 0
                            },
                            "id": "25aef500-c235-4eac-87bb-0f1ba90b08ed",
                            "eur_total": {
                                "price": 2,
                                "fees": 0,
                                "subtotal": 0,
                                "shipping": 1,
                                "total": 0
                            }
                        },
                        "summary": {
                            "nbGifts": 7,
                            "usd_price": 91.36645258000001,
                            "usd_fees": 8.92413275,
                            "usd_subtotal": 100.29058533,
                            "usd_shipping": 36.12115824,
                            "usd_total": 136.41174357,
                            "eur_price": 85.51899961488002,
                            "eur_fees": 8.352988254000001,
                            "eur_subtotal": 93.87198786888,
                            "eur_shipping": 33.80940411264,
                            "eur_total": 127.68139198152001
                        }
                    }
                ]
            }
        }
    }
})
async def getLatestGifter(
    username: str = Query(..., title="Throne Username",
                          description="Username of the Throne user"),
    displayCurrency: str = Query(None, title="Display Currency",
                                 description="Additional currency to display the value in"),
):
    data = await get_cleaned(username)
    previousGifts = json.loads(data.body.decode("utf-8"))["previousGifts"]
    latestGift = previousGifts[0]
    for gift in previousGifts:
        if datetime.fromtimestamp(gift["purchasedAt"]/1000) > datetime.fromtimestamp(latestGift["purchasedAt"]/1000):
            latestGift = gift
    output = []
    for gifter in latestGift["customizations"]["customers"]:
        gifter = {
            "username": gifter["customerUsername"],
            "image": gifter["customerImage"],
            "latestGift": {
                "name": latestGift["name"],
                "purchasedAt": datetime.fromtimestamp(gift["purchasedAt"]/1000).strftime("%Y-%m-%d %H:%M:%S"),
                "status": gift["status"],
                "isComplete": gift["isComplete"],
                "isDigital": gift["isDigitalGood"],
                "isCrowdfunded": gift["isCrowdfunded"],
                f"{gift['total']['currency'].lower()}_total": {
                    "currency": gift["total"]["currency"],
                    "price": gift["total"]["price"]/100,
                    "fees": 0 if not gift["total"]["fees"] else gift["total"]["fees"]/100,
                    "subTotal": 0 if not gift["total"]["subTotal"] else gift["total"]["subTotal"]/100,
                    "shipping": gift["total"]["shipping"]/100,
                    "total": 0 if not gift["total"]["total"] else gift["total"]["total"]/100,
                },
                f"{gift['totalUsd']['currency'].lower()}_total": {
                    "currency": gift["totalUsd"]["currency"],
                    "price": gift["totalUsd"]["price"]/100,
                    "fees": 0 if not gift["totalUsd"]["fees"] else gift["totalUsd"]["fees"]/100,
                    "subTotal": 0 if not gift["totalUsd"]["subTotal"] else gift["totalUsd"]["subTotal"]/100,
                    "shipping": gift["totalUsd"]["shipping"]/100,
                    "total": 0 if not gift["totalUsd"]["total"] else gift["totalUsd"]["total"]/100,
                },
                "id": gift["id"],
            }
        }
        nbGifts = 0
        price = 0
        fees = 0
        subtotal = 0
        shipping = 0
        total = 0
        for gift in previousGifts:
            isGifter = False
            for _gifter in gift["customizations"]["customers"]:
                if _gifter["customerUsername"] == gifter["username"]:
                    isGifter = True
                    break
            if isGifter:
                nbGifts += 1
                price += gift["totalUsd"]["price"]/100
                fees += 0 if not gift["totalUsd"]["fees"] else gift["totalUsd"]["fees"]/100
                subtotal += 0 if not gift["totalUsd"]["subTotal"] else gift["totalUsd"]["subTotal"]/100
                shipping += gift["totalUsd"]["shipping"]/100
                total += 0 if not gift["totalUsd"]["total"] else gift["totalUsd"]["total"]/100
        gifter["summary"] = {
            "nbGifts": nbGifts,
            "usd_price": price,
            "usd_fees": fees,
            "usd_subtotal": subtotal,
            "usd_shipping": shipping,
            "usd_total": total,
        }
        if displayCurrency:
            gifter["latestGift"][f"{displayCurrency.lower()}_total"] = {
                "price": await currency_converter(gifter["latestGift"]["usd_total"]["price"], "USD", displayCurrency.upper()),
                "fees": await currency_converter(gifter["latestGift"]["usd_total"]["fees"], "USD", displayCurrency.upper()),
                "subtotal": await currency_converter(gifter["latestGift"]["usd_total"]["subTotal"], "USD", displayCurrency.upper()),
                "shipping": await currency_converter(gifter["latestGift"]["usd_total"]["shipping"], "USD", displayCurrency.upper()),
                "total": await currency_converter(gifter["latestGift"]["usd_total"]["total"], "USD", displayCurrency.upper())
            }

            gifter["summary"][f"{displayCurrency.lower()}_price"] = await currency_converter(price, "USD", displayCurrency.upper())
            gifter["summary"][f"{displayCurrency.lower()}_fees"] = await currency_converter(fees, "USD", displayCurrency.upper())
            gifter["summary"][f"{displayCurrency.lower()}_subtotal"] = await currency_converter(subtotal, "USD", displayCurrency.upper())
            gifter["summary"][f"{displayCurrency.lower()}_shipping"] = await currency_converter(shipping, "USD", displayCurrency.upper())
            gifter["summary"][f"{displayCurrency.lower()}_total"] = await currency_converter(total, "USD", displayCurrency.upper())
        output.append(gifter)
    return JSONResponse(output, status_code=200)


@app.get("/gifters/last20", tags=["Gifters"], responses={
    200: {
        "content": {
            "application/json": {
                "example": [
                    {
                        "username": "...",
                        "purchasedAt": "YYYY-MM-DD hh:mm:ss",
                        "image": "https://thronecdn.com/users/..."
                    },
                    "..."
                ]
            }
        }
    }
})
async def getLast20Gifters(
    username: str = Query(..., title="Throne Username",
                          description="Username of the Throne user"),
):
    data = await get_cleaned(username)
    last20 = json.loads(data.body.decode(
        "utf-8"))["leaderboard"]["lastTwentyGifters"]
    output = []
    for gifter in last20:
        output.append({
            "username": gifter["gifterUsername"],
            "purchasedAt": datetime.fromtimestamp(gifter["purchasedAt"]/1000).strftime("%Y-%m-%d %H:%M:%S"),
            "image": gifter["gifterImage"],
        })
    return JSONResponse(output, status_code=200)


@app.get("/gifters/all", tags=["Gifters"], responses={
    200: {
        "content": {
            "application/json": {
                "example": [
                    {
                        "username": "...",
                        "image": "https://thronecdn.com/users/...",
                        "latestGift": {
                            "name": "...",
                            "purchasedAt": "YYYY-MM-DD hh:mm:ss",
                            "status": "delivered",
                            "isComplete": False,
                            "isDigital": False,
                            "isCrowdfunded": False,
                            "<local currency>_total": {
                                "currency": "...",
                                "price": 2,
                                "fees": 1,
                                "subTotal": 3,
                                "shipping": 1,
                                "total": 4
                            },
                            "usd_total": {
                                "currency": "USD",
                                "price": 2,
                                "fees": 1,
                                "subTotal": 3,
                                "shipping": 1,
                                "total": 4
                            },
                            "id": "..."
                        },
                        "summary": {
                            "nbGifts": 2,
                            "usd_price": 4,
                            "usd_fees": 2,
                            "usd_subtotal": 6,
                            "usd_shipping": 2,
                            "usd_total": 8
                        }
                    },
                    "..."
                ]
            }
        }
    }
})
async def getAllGifters(
    username: str = Query(..., title="Throne Username",
                          description="Username of the Throne user"),
):
    data = await get_cleaned(username)
    previousGifts = json.loads(data.body.decode("utf-8"))["previousGifts"]
    output = {}
    for gift in previousGifts:
        for gifter in gift["customizations"]["customers"]:
            if gifter["customerUsername"] not in list(output.keys()):
                output[gifter["customerUsername"]] = {
                    "username": gifter["customerUsername"],
                    "image": gifter["customerImage"],
                    "latestGift": {
                        "name": gift["name"],
                        "purchasedAt": datetime.fromtimestamp(gift["purchasedAt"]/1000).strftime("%Y-%m-%d %H:%M:%S"),
                        "status": gift["status"],
                        "isComplete": gift["isComplete"],
                        "isDigital": gift["isDigitalGood"],
                        "isCrowdfunded": gift["isCrowdfunded"],
                        f"{gift['total']['currency'].lower()}_total": {
                            "currency": gift["total"]["currency"],
                            "price": gift["total"]["price"]/100,
                            "fees": 0 if not gift["total"]["fees"] else gift["total"]["fees"]/100,
                            "subTotal": 0 if not gift["total"]["subTotal"] else gift["total"]["subTotal"]/100,
                            "shipping": gift["total"]["shipping"]/100,
                            "total": 0 if not gift["total"]["total"] else gift["total"]["total"]/100,
                        },
                        f"{gift['totalUsd']['currency'].lower()}_total": {
                            "currency": gift["totalUsd"]["currency"],
                            "price": gift["totalUsd"]["price"]/100,
                            "fees": 0 if not gift["totalUsd"]["fees"] else gift["totalUsd"]["fees"]/100,
                            "subTotal": 0 if not gift["totalUsd"]["subTotal"] else gift["totalUsd"]["subTotal"]/100,
                            "shipping": gift["totalUsd"]["shipping"]/100,
                            "total": 0 if not gift["totalUsd"]["total"] else gift["totalUsd"]["total"]/100,
                        },
                        "id": gift["id"],
                    },
                    "summary": {
                        "nbGifts": 1,
                        "usd_price": gift["totalUsd"]["price"]/100,
                        "usd_fees": 0 if not gift["totalUsd"]["fees"] else gift["totalUsd"]["fees"]/100,
                        "usd_subtotal": 0 if not gift["totalUsd"]["subTotal"] else gift["totalUsd"]["subTotal"]/100,
                        "usd_shipping": gift["totalUsd"]["shipping"]/100,
                        "usd_total": 0 if not gift["totalUsd"]["total"] else gift["totalUsd"]["total"]/100,
                    },
                }
            else:
                output[gifter["customerUsername"]]["summary"]["nbGifts"] += 1
                output[gifter["customerUsername"]
                       ]["summary"]["usd_price"] += gift["totalUsd"]["price"]/100
                output[gifter["customerUsername"]
                       ]["summary"]["usd_fees"] += 0 if not gift["totalUsd"]["fees"] else gift["totalUsd"]["fees"]/100
                output[gifter["customerUsername"]
                       ]["summary"]["usd_subtotal"] += 0 if not gift["totalUsd"]["subTotal"] else gift["totalUsd"]["subTotal"]/100
                output[gifter["customerUsername"]
                       ]["summary"]["usd_shipping"] += gift["totalUsd"]["shipping"]/100
                output[gifter["customerUsername"]
                       ]["summary"]["usd_total"] += 0 if not gift["totalUsd"]["total"] else gift["totalUsd"]["total"]/100
                if datetime.strptime(output[gifter["customerUsername"]]["latestGift"]["purchasedAt"], "%Y-%m-%d %H:%M:%S") < datetime.fromtimestamp(gift["purchasedAt"]/1000):
                    output[gifter["customerUsername"]]["latestGift"] = {
                        "name": gift["name"],
                        "purchasedAt": datetime.fromtimestamp(gift["purchasedAt"]/1000).strftime("%Y-%m-%d %H:%M:%S"),
                        "status": gift["status"],
                        "isComplete": gift["isComplete"],
                        "isDigital": gift["isDigitalGood"],
                        "isCrowdfunded": gift["isCrowdfunded"],
                        f"{gift['total']['currency'].lower()}_total": {
                            "currency": gift["total"]["currency"],
                            "price": gift["total"]["price"]/100,
                            "fees": 0 if not gift["total"]["fees"] else gift["total"]["fees"]/100,
                            "subTotal": 0 if not gift["total"]["subTotal"] else gift["total"]["subTotal"]/100,
                            "shipping": gift["total"]["shipping"]/100,
                            "total": 0 if not gift["total"]["total"] else gift["total"]["total"]/100,
                        },
                        f"{gift['totalUsd']['currency'].lower()}_total": {
                            "currency": gift["totalUsd"]["currency"],
                            "price": gift["totalUsd"]["price"]/100,
                            "fees": 0 if not gift["totalUsd"]["fees"] else gift["totalUsd"]["fees"]/100,
                            "subTotal": 0 if not gift["totalUsd"]["subTotal"] else gift["totalUsd"]["subTotal"]/100,
                            "shipping": gift["totalUsd"]["shipping"]/100,
                            "total": 0 if not gift["totalUsd"]["total"] else gift["totalUsd"]["total"]/100,
                        },
                        "id": gift["id"],
                    }
    return JSONResponse(list(output.values()), status_code=200)


@app.get("/gifters/leaderboard", tags=["Gifters"], responses={
    200: {
        "content": {
            "application/json": {
                "example": [
                    {
                        "username": "Anonymous",
                        "nbGifts": 4,
                        "usd_total": 16,
                        "image": None
                    },
                    "..."
                ]
            }
        }
    }
})
async def getLeaderboard(
    username: str = Query(..., title="Throne Username",
                          description="Username of the Throne user"),
    time: str = Query(..., description="Select a period to display", enum=[
                      "all", "month", "week"]),
):
    data = await get_cleaned(username)
    leaderboard = json.loads(data.body.decode("utf-8"))["leaderboard"]
    output = []
    if time == "all":
        for gifter in leaderboard["leaderboardAllTime"]:
            output.append({
                "username": gifter["gifterUsername"],
                "nbGifts": gifter["totalPaymentNumber"],
                "usd_total": gifter["totalAmountSpentUSD"]/100,
                "image": gifter["gifterImage"],
            })
    elif time == "month":
        for gifter in leaderboard["leaderboardLastMonth"]:
            output.append({
                "username": gifter["gifterUsername"],
                "nbGifts": gifter["totalPaymentNumber"],
                "usd_total": gifter["totalAmountSpentUSD"]/100,
                "image": gifter["gifterImage"],
            })
    elif time == "week":
        for gifter in leaderboard["leaderboardLastWeek"]:
            output.append({
                "username": gifter["gifterUsername"],
                "nbGifts": gifter["totalPaymentNumber"],
                "usd_total": gifter["totalAmountSpentUSD"]/100,
                "image": gifter["gifterImage"],
            })
    else:
        return PlainTextResponse("Invalid time period", status_code=400)
    return JSONResponse(output, status_code=200)


@app.get("/version", tags=["TEST"], responses={
    200: {
        "content": {
            "application/json": {
                "example": API_VERSION
            }
        }
    }
})
async def getVersion():
    return API_VERSION


@app.get("/test", tags=["TEST"], responses={
    200: {
        "content": {
            "application/json": {
                "example": True
            }
        }
    }
})
async def test(
    username: str = Query(..., title="Throne Username",
                          description="Username of the Throne user"),
    displayCurrency: str = Query(None, title="Display Currency",
                                 description="Additional currency to display the value in")
):
    try:
        data = await get_cleaned(username)
        data = json.loads(data.body.decode("utf-8"))
        if displayCurrency:
            test = await currency_converter(1, "USD", displayCurrency.upper())
        return True
    except:
        return False


async def currency_converter(amount, from_currency, to_currency):
    # API endpoint to get exchange rates
    endpoint = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"

    # Send a GET request to the API
    response = requests.get(endpoint)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        # Get the exchange rate for the target currency
        exchange_rate = data['rates'][to_currency]

        # Calculate the converted amount
        converted_amount = amount * exchange_rate
        return converted_amount
    else:
        return "Error: Unable to fetch data from the API"
