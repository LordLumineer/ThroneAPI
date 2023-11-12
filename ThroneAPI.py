from fastapi import FastAPI, Request, Response, Query, Path, HTTPException, status
from fastapi.responses import JSONResponse, PlainTextResponse, RedirectResponse
from datetime import datetime
import json
import requests

API_VERSION = "0.1.0"

app = FastAPI(
    title="ThroneAPI",
    description="API to get information about the Throne wishlist",
    version=API_VERSION,
    docs_url="/",
)
@app.get("/rawData/Gifted", tags=["Raw"])
async def getRawGifted(
    username: str = Query(..., title="Throne Username", description="Username of the Throne user"),
    ):
    r = requests.get(f"https://throne.com/{username.lower()}/gifters")
    if r.status_code != 200:
        raise HTTPException(status_code=r.status_code, detail=r.content)

    try:
        parsedData = r.content.decode("utf-8").split('<script id="__NEXT_DATA__" type="application/json">')[1].split("</script>")[0]
        parsedData = json.loads(parsedData)
        return JSONResponse(parsedData, status_code=200)
    except :
        return PlainTextResponse(str("Throne has removed the JSON file from their page, Not to late."), status_code=500)

@app.get("/rawData/Wishlist", tags=["Raw"])
async def getRawWishlist(
    username: str = Query(..., title="Throne Username", description="Username of the Throne user"),
    ):
    r = requests.get(f"https://throne.com/{username.lower()}")
    if r.status_code != 200:
        raise HTTPException(status_code=r.status_code, detail=r.content)

    try:
        parsedData = r.content.decode("utf-8").split('<script id="__NEXT_DATA__" type="application/json">')[1].split("</script>")[0]
        parsedData = json.loads(parsedData)
        return JSONResponse(parsedData, status_code=200)
    except :
        return PlainTextResponse(str("Throne has removed the JSON file from their page, Not to late."), status_code=500)

@app.get("/getCleaned", tags=["Raw"])
async def getCleaned(
    username: str = Query(..., title="Throne Username", description="Username of the Throne user")
    ):
    Gifted = await getRawGifted(username)
    Gifted = json.loads(Gifted.body.decode("utf-8"))
    Wishlist = await getRawWishlist(username)
    Wishlist = json.loads(Wishlist.body.decode("utf-8"))
    try:
        _userInfo = Gifted["props"]["pageProps"]["fallback"][f"public/useCreatorByUsername/{username.lower()}"]
        _previousGifts = Gifted["props"]["pageProps"]["fallback"][f"public/wishlist/usePreviousGifts/{_userInfo['_id']}"]
        _leaderboard = Gifted["props"]["pageProps"]["fallback"][f"api-leaderboard/v1/leaderboard/{_userInfo['_id']}"]
        _initialCounts = Gifted["props"]["pageProps"]["initialCounts"]
        _wishlistItems = Wishlist["props"]["pageProps"]["fallback"][f"public/wishlist/useWishlistItems/{_userInfo['_id']}"]
        _wishlistCollections = Wishlist["props"]["pageProps"]["fallback"][f"public/wishlist/useWishlistCollections/{_userInfo['_id']}"]
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
        return HTTPException(status_code=500, detail=str("Throne has changed their JSON file, please contact the developer to fix this issue"))

@app.get("/user/Info", tags=["User"])
async def getUserInfo(
        username: str = Query(..., title="Throne Username", description="Username of the Throne user"),
):
    data = await getCleaned(username)
    data = json.loads(data.body.decode("utf-8"))
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

@app.get("/user/Socials", tags=["User"])
async def getUserSocials(
    username: str = Query(..., title="Throne Username", description="Username of the Throne user")
):
    data = await getCleaned(username)
    userInfo = json.loads(data.body.decode("utf-8"))["userInfo"]
    output = {
        "mainContentPlatform": userInfo["mainContentPlatform"]
    }
    for social in userInfo["socialLinks"]:
        output[social["type"]] = {
            "name": social["name"],
            "url": social["url"]
        }
    return JSONResponse(output, status_code=200)

@app.get("/user/Categories", tags=["User"])
async def getUserCategories(
        username: str = Query(..., title="Throne Username", description="Username of the Throne user"),
):
    data = await getCleaned(username)
    output = json.loads(data.body.decode("utf-8"))["userInfo"]["surpriseCategories"]
    return JSONResponse(output, status_code=200)

@app.get("/user/Interests", tags=["User"])
async def getUserInfo(
        username: str = Query(..., title="Throne Username", description="Username of the Throne user"),
):
    data = await getCleaned(username)
    output = json.loads(data.body.decode("utf-8"))["userInfo"]["interests"]
    return JSONResponse(output, status_code=200)


@app.get("/collections", tags=["Collections"])
async def getCollections(
        username: str = Query(..., title="Throne Username", description="Username of the Throne user"),
):
    data = await getCleaned(username)
    data = json.loads(data.body.decode("utf-8"))["wishlistCollections"]
    output = []
    for collection in data:
        output.append({"title": collection["title"], "id": collection["id"]})
    return JSONResponse(output, status_code=200)

@app.get("/collections/Detailed", tags=["Collections"])
async def getCollectionsDetailed(
        username: str = Query(..., title="Throne Username", description="Username of the Throne user"),
        displayCurrency: str = Query(None, title="Display Currency", description="Additional currency to display the value in"),
):
    data = await getCleaned(username)
    data = json.loads(data.body.decode("utf-8"))
    collections = data["wishlistCollections"]
    items = data["wishlistItems"]
    output = []
    for collection in collections:
        collectionOutput = {
            "name": collection["title"],
            "description": collection["description"],
            "id": collection["id"],
            "updatedAt": datetime.fromtimestamp(collection["updatedAt"]/1000).strftime("%Y-%m-%d %H:%M:%S"),
        }
        id = collection["id"]
        count = 0
        individualCount = 0
        price = {}
        for item in items:
            if id in item["collectionIds"]:
                individualCount += 1
                count += 1*item["quantity"]
                if item["quantity"] not in list(price.keys()):
                    price[item["currency"]] = 0
                price[item["currency"]] += (item["price"]/100)*item["quantity"]
        usdValue = 0
        collectionOutput["items"] = count
        collectionOutput["individualItems"] = individualCount
        for currency in list(price.keys()):
            usdValue += await currency_converter(price[currency], currency.upper(), "USD")
            collectionOutput[f"{currency.lower()}_price"] = price[currency]

        collectionOutput["usd_price"] = usdValue



        if displayCurrency :
            collectionOutput[f"{displayCurrency.lower()}_price"] = await currency_converter(usdValue, "USD", displayCurrency.upper())
        output.append(collectionOutput)

    return JSONResponse(output, status_code=200)

@app.get("/collections/Collection", tags=["Collections"])
async def getCollection(
    username: str = Query(..., title="Throne Username", description="Username of the Throne user"),
    id: str = Query(..., title="Collection ID", description="Get details about a specific collection (get its ID from GET /collections)"),
    displayCurrency: str = Query(None, title="Display Currency", description="Additional currency to display the value in"),
):
    data = await getCleaned(username)
    data = json.loads(data.body.decode("utf-8"))
    collections = data["wishlistCollections"]
    items = data["wishlistItems"]
    singleCollection = {}
    output = {}
    for collection in collections:
        if collection["id"] == id:
            singleCollection = collection
            break
    output["name"] = singleCollection["title"]
    output["description"] = singleCollection["description"]
    output["id"] = singleCollection["id"]
    output["cratedAt"] = datetime.fromtimestamp(singleCollection["createdAt"]/1000).strftime("%Y-%m-%d %H:%M:%S")
    output["updatedAt"] = datetime.fromtimestamp(singleCollection["updatedAt"]/1000).strftime("%Y-%m-%d %H:%M:%S")
    output["image"] = singleCollection["imageSrc"]

    count = 0
    individualCount = 0
    price = {}
    for item in items:
        if id in item["collectionIds"]:
            individualCount += 1
            count += 1*item["quantity"]
            if item["quantity"] not in list(price.keys()):
                price[item["currency"]] = 0
            price[item["currency"]] += (item["price"]/100)*item["quantity"]

    output["items"] = count
    output["individualItems"] = individualCount

    usd_price = 0
    for currency in list(price.keys()):
        usd_price += await currency_converter(price[currency], currency.upper(), "USD")
        output[f"{currency.lower()}_price"] = price[currency]

    output["usd_price"] = usd_price

    if displayCurrency :
        output[f"{displayCurrency.lower()}_price"] = await currency_converter(usd_price, "USD", displayCurrency.upper())

    return JSONResponse(output, status_code=200)


@app.get("/Collections/Items", tags=["Collections", "Items"])
async def getCollectionItems(
    username: str = Query(..., title="Throne Username", description="Username of the Throne user"),
    id: str = Query(..., title="Collection ID", description="Get details about a specific collection (get its ID from GET /collections)"),
):
    data = await getCleaned(username)
    data = json.loads(data.body.decode("utf-8"))
    items = data["wishlistItems"]
    output = []
    for item in items:
        if id in item["collectionIds"]:
            item={
                "name": item["name"],
                "quantity": item["quantity"],
                "price": item["price"]/100,"currency": item["currency"],
                "id": item["id"],
            }
            output.append(item)


    return JSONResponse(output, status_code=200)


@app.get("/items", tags=["Items"])
async def getItems(
    username: str = Query(..., title="Throne Username", description="Username of the Throne user"),
):
    data = await getCleaned(username)
    wishlistItems = json.loads(data.body.decode("utf-8"))["wishlistItems"]
    output = []
    for item in wishlistItems:
        output.append({"name": item["name"],"id": item["id"],})
    return JSONResponse(output, status_code=200)

@app.get("/items/Detailed", tags=["Items"])
async def getItemsDetailed(
        username: str = Query(..., title="Throne Username", description="Username of the Throne user"),
):
    data = await getCleaned(username)
    wishlistItems = json.loads(data.body.decode("utf-8"))["wishlistItems"]
    output = []
    for item in wishlistItems:
        output.append({
            "name": item["name"],
            "addedAt": datetime.fromtimestamp(item["createdAt"]/1000).strftime("%Y-%m-%d %H:%M:%S"),
            "isDigital": item["isDigitalGood"],
            "isAvailable": None if not "isAvailable" in list(item.keys()) else item["isAvailable"],
            "notInStock": None if not "notInStock" in list(item.keys()) else item["notInStock"], #IDK what this exists
            "quantity": item["quantity"],
            f"{item['currency'].lower()}_total": {
                "currency": item["currency"],
                "price": item["price"]/100,
                "totalPrice": item["price"]/100*item["quantity"],
                "shipping": 0 if ("shipping" not in list(item.keys())) else item["shipping"]/100,
                "totalPriceWithShipping": item["price"]*item["quantity"]/100+(0 if ("shipping" not in list(item.keys())) else item["shipping"]/100),
            }
        })



    return JSONResponse(output, status_code=200)

@app.get("/items/Item", tags=["Items"])
async def getItem(
    username: str = Query(..., title="Throne Username", description="Username of the Throne user"),
    id: str = Query(..., title="Item ID", description="Get details about a specific item (get its ID from GET /items)"),
    displayCurrency: str = Query(None, title="Display Currency", description="Additional currency to display the value in"),
):
    data = await getCleaned(username)
    wishlistItems = json.loads(data.body.decode("utf-8"))["wishlistItems"]
    singleItem = {}
    output = {}
    for item in wishlistItems:
        if item["id"] == id:
            singleItem = item
            break
    output["name"] = singleItem["name"]
    output["link"] = None if not "link" in list(singleItem.keys()) else singleItem["link"]
    output["addedAt"] = datetime.fromtimestamp(singleItem["createdAt"]/1000).strftime("%Y-%m-%d %H:%M:%S")
    output["isDigital"] = singleItem["isDigitalGood"]
    output["isAvailable"] = None if not "isAvailable" in list(singleItem.keys()) else singleItem["isAvailable"]
    output["notInStock"] = None if not "notInStock" in list(singleItem.keys()) else singleItem["notInStock"], #IDK what this exist

    output["quantity"] = singleItem["quantity"]

    price = singleItem["price"]/100
    total_price = price*singleItem["quantity"]
    shipping = 0 if ("shipping" not in list(singleItem.keys())) else singleItem["shipping"]/100
    total_price_with_shipping = total_price + shipping
    output[f"{singleItem['currency'].lower()}_total"] = {
        "currency": singleItem["currency"],
        "price": price,
        "totalPrice": total_price,
        "shipping": shipping,
        "totalPriceWithShipping": total_price_with_shipping,
    }

    price = await currency_converter(singleItem["price"]/100, singleItem["currency"].upper(), "USD"),
    price = price[0]
    total_price = price*singleItem["quantity"]
    shipping = 0 if ("shipping" not in list(singleItem.keys())) else await currency_converter(singleItem["shipping"]/100, singleItem["currency"].upper(), "USD"),
    shipping = shipping[0]
    total_price_with_shipping = total_price + shipping
    output["usd_total"] = {
        "currency": "USD",
        "price": price,
        "totalPrice": total_price,
        "shipping": shipping,
        "totalPriceWithShipping": total_price_with_shipping,
    }
    if displayCurrency :
        price = await currency_converter(singleItem["price"]/100, singleItem["currency"].upper(), displayCurrency.upper()),
        price = price[0]
        total_price = price*singleItem["quantity"]
        shipping = 0 if ("shipping" not in list(singleItem.keys())) else await currency_converter(singleItem["shipping"]/100, singleItem["currency"].upper(), displayCurrency.upper()),
        shipping = shipping[0]
        total_price_with_shipping = total_price + shipping
        output[f"{displayCurrency.lower()}_total"] = {
            "currency": displayCurrency.upper(),
            "price": price,
            "totalPrice": total_price,
            "shipping": shipping,
            "totalPriceWithShipping": total_price_with_shipping,
        }
    output["image"] = singleItem["imgLink"]
    output["id"] = singleItem["id"]

    return JSONResponse(output, status_code=200)


@app.get("/previousGifts", tags=["Previous Gifts"])
async def getPreviousGifts(
    username: str = Query(..., title="Throne Username", description="Username of the Throne user"),
):
    data = await getCleaned(username)
    previousGifts = json.loads(data.body.decode("utf-8"))["previousGifts"]
    output = []
    for gift in previousGifts:
        gifters = []
        for gifter in gift["customizations"]["customers"]:
            gifters.append({"username": gifter["customerUsername"]})
        output.append({"name": gift["name"], "gifters": gifters,"id": gift["id"],})
    return JSONResponse(output, status_code=200)

@app.get("/previousGifts/Detailed", tags=["Previous Gifts"])
async def getPreviousGiftsDetailed(
    username: str = Query(..., title="Throne Username", description="Username of the Throne user"),
):
    data = await getCleaned(username)
    previousGifts = json.loads(data.body.decode("utf-8"))["previousGifts"]
    output = []
    for gift in previousGifts:
        gifters = []
        for gifter in gift["customizations"]["customers"]:
            gifters.append({"username": gifter["customerUsername"]})
        output.append({
            "name": gift["name"],
            "gifters": gifters,
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
        })
    return JSONResponse(output, status_code=200)

@app.get("/previousGifts/Gift", tags=["Previous Gifts"])
async def getPreviousGift(
    username: str = Query(..., title="Throne Username", description="Username of the Throne user"),
    id: str = Query(..., title="Gift ID", description="Get details about a specific gift (get its ID from GET /previousGifts)"),
    displayCurrency: str = Query(None, title="Display Currency", description="Additional currency to display the value in"),
):
    data = await getCleaned(username)
    previousGifts = json.loads(data.body.decode("utf-8"))["previousGifts"]
    singleGift = {}
    for gift in previousGifts:
        if gift["id"] == id:
            singleGift = gift
            break

    gifters = []
    for gifter in gift["customizations"]["customers"]:
        gifters.append({
            "username": gifter["customerUsername"],
            "image": gifter["customerImage"]
        })

    output = {
        "name": singleGift["name"],
        "gifters": gifters,
        "purchasedAt": datetime.fromtimestamp(singleGift["purchasedAt"]/1000).strftime("%Y-%m-%d %H:%M:%S"),
        "status": singleGift["status"],
        "id": singleGift["id"],
        "link": None if not "link" in list(gift.keys()) else gift["link"],
        "image": singleGift["imageSrc"],
        "status": singleGift["status"],
        "isComplete": gift["isComplete"],
        "isDigital": singleGift["isDigitalGood"],
        "isCrowdfunded": singleGift["isCrowdfunded"],
        f"{singleGift['total']['currency'].lower()}_total": {
                "currency": singleGift["total"]["currency"],
                "price": singleGift["total"]["price"]/100,
                "fees": 0 if not singleGift["total"]["fees"] else singleGift["total"]["fees"]/100,
                "subTotal": 0 if not singleGift["total"]["subTotal"] else singleGift["total"]["subTotal"]/100,
                "shipping": singleGift["total"]["shipping"]/100,
                "total": 0 if not singleGift["total"]["total"] else singleGift["total"]["total"]/100,
            },
        f"{singleGift['totalUsd']['currency'].lower()}_total": {
                "currency": singleGift["totalUsd"]["currency"],
                "price": singleGift["totalUsd"]["price"]/100,
                "fees": 0 if not singleGift["totalUsd"]["fees"] else singleGift["totalUsd"]["fees"]/100,
                "subtoTal": 0 if not singleGift["totalUsd"]["subTotal"] else singleGift["totalUsd"]["subTotal"]/100,
                "shipping": singleGift["totalUsd"]["shipping"]/100,
                "total": 0 if not singleGift["totalUsd"]["total"] else singleGift["totalUsd"]["total"]/100,
            },
    }
    if displayCurrency:
        output[f"{displayCurrency.lower()}_total"] = {
            "currency": displayCurrency.upper(),
            "price": await currency_converter(singleGift["totalUsd"]["price"]/100, "USD", displayCurrency.upper()),
            "fees": 0 if not singleGift["totalUsd"]["fees"] else await currency_converter(singleGift["totalUsd"]["fees"]/100, "USD", displayCurrency.upper()),
            "subTotal": 0 if not singleGift["totalUsd"]["subTotal"] else await currency_converter(singleGift["totalUsd"]["subTotal"]/100, "USD", displayCurrency.upper()),
            "shipping": await currency_converter(singleGift["totalUsd"]["shipping"]/100, "USD", displayCurrency.upper()),
            "total": 0 if not singleGift["totalUsd"]["total"] else await currency_converter(singleGift["totalUsd"]["total"]/100, "USD", displayCurrency.upper()),
        }
    return JSONResponse(output, status_code=200)

@app.get("/previousGifts/latest", tags=["Previous Gifts"])
async def getLatestGift(
    username: str = Query(..., title="Throne Username", description="Username of the Throne user"),
    displayCurrency: str = Query(None, title="Display Currency", description="Additional currency to display the value in"),
):
    data = await getCleaned(username)
    previousGifts = json.loads(data.body.decode("utf-8"))["previousGifts"]
    latestGift = previousGifts[0]
    for gift in previousGifts:
        if datetime.fromtimestamp(gift["purchasedAt"]/1000) > datetime.fromtimestamp(latestGift["purchasedAt"]/1000):
            latestGift = gift

    gifters = []
    for gifter in latestGift["customizations"]["customers"]:
        gifters.append({
            "username": gifter["customerUsername"],
            "image": gifter["customerImage"]
        })
    output = {
        "name": latestGift["name"],
        "gifters": gifters,
        "purchasedAt": datetime.fromtimestamp(latestGift["purchasedAt"]/1000).strftime("%Y-%m-%d %H:%M:%S"),
        "status": latestGift["status"],
        "id": latestGift["id"],
        "link": None if not "link" in list(gift.keys()) else gift["link"],
        "image": latestGift["imageSrc"],
        "status": latestGift["status"],
        "isComplete": gift["isComplete"],
        "isDigital": latestGift["isDigitalGood"],
        "isCrowdfunded": latestGift["isCrowdfunded"],
        f"{latestGift['total']['currency'].lower()}_total": {
                "currency": latestGift["total"]["currency"],
                "price": latestGift["total"]["price"]/100,
                "fees": 0 if not latestGift["total"]["fees"] else latestGift["total"]["fees"]/100,
                "subTotal": 0 if not latestGift["total"]["subTotal"] else latestGift["total"]["subTotal"]/100,
                "shipping": latestGift["total"]["shipping"]/100,
                "total": 0 if not latestGift["total"]["total"] else latestGift["total"]["total"]/100,
            },
        f"{latestGift['totalUsd']['currency'].lower()}_total": {
                "currency": latestGift["totalUsd"]["currency"],
                "price": latestGift["totalUsd"]["price"]/100,
                "fees": 0 if not latestGift["totalUsd"]["fees"] else latestGift["totalUsd"]["fees"]/100,
                "subtoTal": 0 if not latestGift["totalUsd"]["subTotal"] else latestGift["totalUsd"]["subTotal"]/100,
                "shipping": latestGift["totalUsd"]["shipping"]/100,
                "total": 0 if not latestGift["totalUsd"]["total"] else latestGift["totalUsd"]["total"]/100,
            },
    }
    if displayCurrency:
        output[f"{displayCurrency.lower()}_total"] = {
            "currency": displayCurrency.upper(),
            "price": await currency_converter(latestGift["totalUsd"]["price"]/100, "USD", displayCurrency.upper()),
            "fees": 0 if not latestGift["totalUsd"]["fees"] else await currency_converter(latestGift["totalUsd"]["fees"]/100, "USD", displayCurrency.upper()),
            "subTotal": 0 if not latestGift["totalUsd"]["subTotal"] else await currency_converter(latestGift["totalUsd"]["subTotal"]/100, "USD", displayCurrency.upper()),
            "shipping": await currency_converter(latestGift["totalUsd"]["shipping"]/100, "USD", displayCurrency.upper()),
            "total": 0 if not latestGift["totalUsd"]["total"] else await currency_converter(latestGift["totalUsd"]["total"]/100, "USD", displayCurrency.upper()),
        }
    return JSONResponse(output, status_code=200)

@app.get("/previousGifts/total", tags=["Previous Gifts"])
async def getTotal(
    username: str = Query(..., title="Throne Username", description="Username of the Throne user"),
    displayCurrency: str = Query(None, title="Display Currency", description="Additional currency to display the value in"),
):
    data = await getCleaned(username)
    previousGifts = json.loads(data.body.decode("utf-8"))["previousGifts"]
    nbGifts = 0
    gifters = []
    price = 0
    fees = 0
    subtotal = 0
    shipping = 0
    total = 0

    for gift in previousGifts:
        nbGifts += 1
        for gifter in gift["customizations"]["customers"]:
            if gifter["customerUsername"] not in gifters:
                gifters.append(gifter["customerUsername"])
        price += gift["totalUsd"]["price"]/100
        fees += 0 if not gift["totalUsd"]["fees"] else gift["totalUsd"]["fees"]/100
        subtotal += 0 if not gift["totalUsd"]["subTotal"] else gift["totalUsd"]["subTotal"]/100
        shipping += gift["totalUsd"]["shipping"]/100
        total += 0 if not gift["totalUsd"]["total"] else gift["totalUsd"]["total"]/100
    output = {
        "nbGifts": nbGifts,
        "nbGifters": len(gifters),
        "usd_price": price,
        "usd_fees": fees,
        "usd_subtotal": subtotal,
        "usd_shipping": shipping,
        "usd_total": total,
    }
    if displayCurrency:
        output[f"{displayCurrency.lower()}_price"] = await currency_converter(price, "USD", displayCurrency.upper())
        output[f"{displayCurrency.lower()}_fees"] = await currency_converter(fees, "USD", displayCurrency.upper())
        output[f"{displayCurrency.lower()}_subtotal"] = await currency_converter(subtotal, "USD", displayCurrency.upper())
        output[f"{displayCurrency.lower()}_shipping"] = await currency_converter(shipping, "USD", displayCurrency.upper())
        output[f"{displayCurrency.lower()}_total"] = await currency_converter(total, "USD", displayCurrency.upper())

    return JSONResponse(output, status_code=200)

@app.get("/gifters/latest", tags=["Gifters"])
async def getLatestGifter(
    username: str = Query(..., title="Throne Username", description="Username of the Throne user"),
    displayCurrency: str = Query(None, title="Display Currency", description="Additional currency to display the value in"),
):
    data = await getCleaned(username)
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
                "price": await currency_converter(gifter["latestGift"]["usd_total"]["price"]/100, "USD", displayCurrency.upper()),
                "fees": await currency_converter(gifter["latestGift"]["usd_total"]["fees"]/100, "USD", displayCurrency.upper()),
                "subtotal": await currency_converter(gifter["latestGift"]["usd_total"]["subTotal"]/100, "USD", displayCurrency.upper()),
                "shipping": await currency_converter(gifter["latestGift"]["usd_total"]["shipping"]/100, "USD", displayCurrency.upper()),
                "total": await currency_converter(gifter["latestGift"]["usd_total"]["total"]/100, "USD", displayCurrency.upper())
            }

            gifter["summary"][f"{displayCurrency.lower()}_price"] = await currency_converter(price, "USD", displayCurrency.upper())
            gifter["summary"][f"{displayCurrency.lower()}_fees"] = await currency_converter(fees, "USD", displayCurrency.upper())
            gifter["summary"][f"{displayCurrency.lower()}_subtotal"] = await currency_converter(subtotal, "USD", displayCurrency.upper())
            gifter["summary"][f"{displayCurrency.lower()}_shipping"] = await currency_converter(shipping, "USD", displayCurrency.upper())
            gifter["summary"][f"{displayCurrency.lower()}_total"] = await currency_converter(total, "USD", displayCurrency.upper())
        output.append(gifter)
    return JSONResponse(output, status_code=200)

@app.get("/gifters/last20", tags=["Gifters"])
async def getLast20Gifters(
    username: str = Query(..., title="Throne Username", description="Username of the Throne user"),
):
    data = await getCleaned(username)
    last20 = json.loads(data.body.decode("utf-8"))["leaderboard"]["lastTwentyGifters"]
    output = []
    for gifter in last20:
        output.append({
            "username": gifter["gifterUsername"],
            "purchasedAt": datetime.fromtimestamp(gifter["purchasedAt"]/1000).strftime("%Y-%m-%d %H:%M:%S"),
            "image": gifter["gifterImage"],
        })
    return JSONResponse(output, status_code=200)

@app.get("/gifters/all", tags=["Gifters"])
async def getAllGifters(
    username: str = Query(..., title="Throne Username", description="Username of the Throne user"),
):
    data = await getCleaned(username)
    previousGifts = json.loads(data.body.decode("utf-8"))["previousGifts"]
    output = {}
    for gift in previousGifts:
        for gifter in gift["customizations"]["customers"]:
            if gifter["customerUsername"] not in list(output.keys()):
                output[gifter["customerUsername"]]={
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
                output[gifter["customerUsername"]]["summary"]["usd_price"] += gift["totalUsd"]["price"]/100
                output[gifter["customerUsername"]]["summary"]["usd_fees"] += 0 if not gift["totalUsd"]["fees"] else gift["totalUsd"]["fees"]/100
                output[gifter["customerUsername"]]["summary"]["usd_subtotal"] += 0 if not gift["totalUsd"]["subTotal"] else gift["totalUsd"]["subTotal"]/100
                output[gifter["customerUsername"]]["summary"]["usd_shipping"] += gift["totalUsd"]["shipping"]/100
                output[gifter["customerUsername"]]["summary"]["usd_total"] += 0 if not gift["totalUsd"]["total"] else gift["totalUsd"]["total"]/100
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

@app.get("/gifters/leaderboard", tags=["Gifters"])
async def getLeaderboard(
    username: str = Query(..., title="Throne Username", description="Username of the Throne user"),
    time: str = Query(..., description="Select a period to display", enum=["all", "month", "week"]),
):
    data = await getCleaned(username)
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

@app.get("/version", tags=["TEST"])
async def getVersion():
    return API_VERSION

@app.get("/test", tags=["TEST"])
async def test(
    username: str = Query(..., title="Throne Username", description="Username of the Throne user"),
    displayCurrency: str = Query(None, title="Display Currency", description="Additional currency to display the value in")
    ):
    try:
        data = await getCleaned(username)
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

def get_api_version():
    return API_VERSION