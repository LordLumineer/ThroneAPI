# ThroneAPI <img src="./images/SVG/rgbb.svg" height="40" alt="fullLogoSideTxtRBGB">

ThroneAPI is a FastAPI-based API for retrieving information about the Throne wishlist. It provides endpoints to fetch various details such as raw wishlist data, user information, collections, items, previous gifts, and more.

## Getting Started

You can find ThroneAPI on [Docker Hub](https://hub.docker.com/r/lordlumineer/throne-api) for easy deployment. Follow the instructions below to get started.

## Deploy with Docker

   ```bash
   docker run -p 8000:8000 lordlumineer/throne-api
   ```

   Access the API at [localhost:8000/docs](http://localhost:8000/docs) for interactive documentation.

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
- [3. Logos](#3-logos)
- [4. Issues](#4-issues)
- [5. Disclaimer](#5-disclaimer)
- [6. License](#6-license)

## 1. Features (Endpoints)

- **Raw Data Endpoints:**
  - `/rawData/Gifted`: Get raw gifted data for a Throne user.
  - `/rawData/Wishlist`: Get raw wishlist data for a Throne user.

- **Cleaned Data Endpoint:**
  - `/getCleaned`: Get cleaned and organized data for a Throne user,    combining gifted and wishlist information.

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
  - `/gifters/leaderboard`: Get the gifter leaderboard for a specific time    period.

- **Testing Endpoint:**
  - `/version`: Get the current version of the API.
  - `/test`: Test endpoint for checking the functionality, providing an    option for currency conversion.
  - `/ping/throne`: Get information about the ping to the Throne servers.

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

  1. Run the server (see [2.2.3. With Uvicorn](#223-with-uvicorn-python))

     - **Note:** You might want to add the `--reload` flag to the command to enable hot reloading.

  2. Open the Swagger UI at [localhost:8000/docs](http://localhost:8000/docs).

## 3. Logos

<img src="./images/SVG/bwb.svg" width="100" alt="fullLogoBW">
<img src="./images/SVG/bww.svg" width="100" alt="fullLogoWB">
<img src="./images/SVG/rgbb.svg" width="100" alt="fullLogoRBGB">
<img src="./images/SVG/rgbw.svg" width="100" alt="fullLogoRBGW">

<img src="./images/SVG/bwbB.svg" width="100" alt="fullLogoTxtBW">
<img src="./images/SVG/bwwB.svg" width="100" alt="fullLogoTxtWB">
<img src="./images/SVG/rgbbB.svg" width="100" alt="fullLogoTxtRBGB">
<img src="./images/SVG/rgbwB.svg" width="100" alt="fullLogoTxtRBGW">

<img src="./images/SVG/bwbS.svg" width="200" alt="fullLogoSideTxtBW">
<img src="./images/SVG/bwwS.svg" width="200" alt="fullLogoSideTxtWB">
<img src="./images/SVG/rgbbS.svg" width="200" alt="fullLogoSideTxtRBGB">
<img src="./images/SVG/rgbwS.svg" width="200" alt="fullLogoSideTxtRBGW">

## 4. Issues

If you encounter any issues, discrepancies, or have suggestions for improvement, please feel free to open an issue on the [GitHub repository](https://github.com/lordlumineer/ThroneApi/issues). Before opening a new issue, please check if a similar issue already exists.

When reporting issues, consider providing the following details:

- A clear and descriptive title for the issue.
- Steps to reproduce the problem.
- Details about your environment (e.g., operating system, Python version).
- Screenshots, if applicable.
- Any error messages or stack traces.
- Your feedback is valuable in enhancing the functionality and reliability of the API. Thank you for your contribution!

## 5. Disclaimer

This project is not affiliated with Throne in any way. It is an unofficial API for Throne.

**Note:** This API is developed by a single enthusiast, and while efforts have been made to ensure its functionality and reliability, it is important to note that I am not a professional. There may be better or more efficient ways to implement certain features. Users are encouraged to provide feedback, suggestions, and open issues if they encounter any issues or have recommendations for improvements.

Please use this API responsibly, and be aware that it will not cover all edge cases or scenarios. Your understanding and collaboration are appreciated.

## 6. License

This project is licensed under the MIT License - see the [LICENSE.md](./LICENSE) file for details.

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
