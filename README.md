# ThroneAPI

ThroneAPI is a FastAPI-based API for retrieving information about the Throne wishlist. It provides endpoints to fetch various details such as raw wishlist data, user information, collections, items, previous gifts, and more.

---

## Table of Contents

- [1. Features (Endpoints)](#1-features-endpoints)
- [2. How to Use](#2-how-to-use)
  - [2.1. Deploying](#21-deploying)
  - [2.2. Running Locally](#22-running-locally)
    - [2.2.1. With Docker (compose)](#221-with-docker-compose)
    - [2.2.2. With Docker (manual)](#222-with-docker-manual)
    - [2.2.3. With Uvicorn (python)](#223-with-uvicorn-python)
  - [2.3. Development](#23-development)
  - [2.4. Changing the Port](#24-changing-the-port)

## 1. Features (Endpoints)

- **Raw Data Endpoints:**
  - `/rawData/Gifted`: Get raw gifted data for a Throne user.
  - `/rawData/Wishlist`: Get raw wishlist data for a Throne user.

- **Cleaned Data Endpoint:**
  - `/getCleaned`: Get cleaned and organized data for a Throne user, combining gifted and wishlist information.

- **User Information Endpoints:**
  - `/user/Info`: Get general information about a Throne user.
  - `/user/Socials`: Get social media information of a Throne user.
  - `/user/Categories`: Get categories associated with a Throne user.
  - `/user/Interests`: Get interests of a Throne user.

- **Collections Endpoints:**
  - `/collections`: Get collections associated with a Throne user.
  - `/collections/Detailed`: Get detailed information about collections.
  - `/collections/Collection`: Get details about a specific collection.
  - `/Collections/Items`: Get items associated with a specific collection.

- **Items Endpoints:**
  - `/items`: Get items associated with a Throne user.
  - `/items/Detailed`: Get detailed information about items.
  - `/items/Item`: Get details about a specific item.

- **Previous Gifts Endpoints:**
  - `/previousGifts`: Get previous gifts associated with a Throne user.
  - `/previousGifts/Detailed`: Get detailed information about previous gifts.
  - `/previousGifts/Gift`: Get details about a specific previous gift.
  - `/previousGifts/latest`: Get information about the latest previous gift.
  - `/previousGifts/total`: Get the total number of previous gifts.

- **Gifters Endpoints:**
  - `/gifters/latest`: Get information about the latest gifter.
  - `/gifters/last20`: Get the last 20 gifters.
  - `/gifters/all`: Get information about all gifters.
  - `/gifters/leaderboard`: Get the gifter leaderboard for a specific time period.

- **Testing Endpoint:**
  - `/version`: Get the current version of the API.
  - `/test`: Test endpoint for checking the functionality, providing an option for currency conversion.

## 2. How to Use

### 2.1. Deploying

1. With docker compose

- Use the provided Docker Compose configuration to deploy ThroneAPI.

    ```yaml
    version: "3"
    services:
      throneapi:
        image: lordlumineer/throne-api:latest
        ports:
          - 8000:8000
    ```

- Run the following command:

    ```bash
    docker-compose up -d
    ```

2. With docker

- Pull the Docker image and run the container.

    ```bash
    docker pull lordlumineer/throne-api:latest
    docker run -d -p 8000:8000 lordlumineer/throne-api:latest
    ```

### 2.2. Running Locally

1. Clone the repository

```bash
git clone https://github.com/LordLumineer/ThroneAPI.git
cd ThroneAPI
```

#### 2.2.1. With Docker (compose)

1. Build the image

```bash
docker-compose build
```

2. Run the container

```bash
docker-compose up -d
```

#### 2.2.2. With Docker (manual)

1. Build the image

```bash
docker build -t throne-api .
```

2. Run the container

```bash
docker run -d -p 8000:8000 throne-api
```

#### 2.2.3. With Uvicorn (python)

1. Install dependencies

```bash
pip install -r requirements.txt
```

2. Run the server

```bash
uvicorn main:app
```

### 2.3. Development

1. Clone the repository

```bash
git clone https://github.com/LordLumineer/ThroneAPI.git
cd ThroneAPI
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the server

```bash
uvicorn main:app --reload
``` 

### 2.4. Changing the Port

#### 2.3.1. With Docker (compose)

1. Change the port in the `docker-compose.yml` file

```yaml
version: "3"
services:
  throneapi:
    image: lordlumineer/throne-api:latest
    ports:
      - <PORT>:8000 # Change this to the desired port
```

2. Run the container

```bash
docker-compose up -d
```

#### 2.3.2. With Docker (manual)

1. Build the image

```bash
docker build -t throne-api .
```

2. Run the container with the `--port` flag

```bash
docker run -d -p <PORT>:8000 throne-api
```

#### 2.3.2. With Uvicorn

1. Run the server with the `--port` flag

```bash
uvicorn main:app --port <PORT>
```

### 2.5. Testing

1. Run the server (see [2.2.3. With Uvicorn (python)](#223-with-uvicorn-python))

2. Open the Swagger UI at `http://localhost:8000`

## 3. License

```
MIT License

Copyright (c) 2023 LordLumineer

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
