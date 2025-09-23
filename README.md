# Movie Recommendation System

A movie recommendation system using **NLP** and **cosine similarity**.
It processes the [MovieLens dataset](https://grouplens.org/datasets/movielens/) to generate recommendations, enriched with metadata from [TMDB API](https://developer.themoviedb.org/).

The purpose of this repository is to serve the **trained recommendation model** through an API exposed by FastAPI.

Related repositories:
- [Model training repository](https://github.com/marchewadm/movie-recommendation-model)
- [Backend repository (Laravel)](https://github.com/marchewadm/movie-recommendation-backend)

## Table Of Contents

- [Demo](#demo)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
    - [Cloning the Repository](#cloning-the-repository)
    - [Before Running](#before-running)
      - [Running the Project via Docker](#running-the-project-via-docker)
      - [Running the Project via uv](#running-the-project-via-uv)
- [Usage](#usage)
    - [Example API Request](#example-api-request) 

## Demo

https://github.com/user-attachments/assets/9d4c3a07-3b6a-484a-a69a-661858d00b4d

## Prerequisites

- **uv** if you don't want to use Docker. You can download it [here](https://docs.astral.sh/uv/).
- **Docker** if you want to run the application inside a container.

## Installation

### Cloning the Repository

```bash
git clone https://github.com/marchewadm/movie-recommendation-fastapi-service.git
cd movie-recommendation-fastapi-service
```

### Before Running

Before starting the application, make sure you place the trained model in the `./app/models/` folder under the name `recommendation_model.pkl`.

Don't know where to get the trained model? Check out the [model training repository](https://github.com/marchewadm/movie-recommendation-model).

#### Running the Project via Docker

You can build the Docker image with:

```bash
docker build -t fastapi-service .
```

and run it locally:

```bash
docker run -p 8000:80 fastapi-service
```

or use Docker Compose:

```bash
docker compose up --build
```

#### Running the Project via uv

In the project root directory, run:

```bash
uv run fastapi dev
```

## Usage

Once the service is running, you can access the OpenAPI documentation and test the API at `http://127.0.0.1:8000/docs`.

### Example API Request

To get movie recommendations, send a **GET** request to:

```bash
curl http://localhost:8000/api/v1/movies/recommend?tmdb_id=680&limit=3&min_rating_count=50
```

**Response:**

```json
{
  "recommendations": [
    {
      "tmdbId": 115,
      "similarityScore": 0.35814
    },
    {
      "tmdbId": 101,
      "similarityScore": 0.27574
    },
    {
      "tmdbId": 550,
      "similarityScore": 0.26478
    }
  ]
}
```

**Query parameters:**

- `tmdb_id` - TMDB movie ID to find recommendations for.
- `limit` - Maximum number of recommended movies (**default is 10**).
- `min_rating_count` - Minimum number of ratings a movie must have to be considered (**default is 50**).
