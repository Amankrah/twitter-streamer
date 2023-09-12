# Twitter Streamer

## Overview

Twitter Streamer is a Python application that utilizes Tweepy to stream tweets based on specified tracking terms. The streamed tweets are stored in a database and can be exported to a CSV file at regular intervals. Sentiment analysis on the tweets is performed using TextBlob.

## Features

- Streams live tweets using Tweepy based on specified tracking terms.
- Stores tweet data and user data in a database.
- Performs sentiment analysis on tweets using TextBlob.
- Exports stored tweets to a CSV file at regular intervals.
- Uses APScheduler for scheduling CSV export tasks.

## Prerequisites

- Python 3.x
- pip
- A Twitter Developer Account and API keys

## Installation

1. Clone the repository:

   ```
   git clone https://github.com/yourusername/twitter-streamer.git
   ```

2. Change into the project directory:

   ```
   cd twitter-streamer
   ```

3. Install the required packages:

   ```
   pip install -r requirements.txt
   ```

## Setup

1. Create a `.env` file in the project root directory and populate it with your Twitter API keys and database connection string:

   ```env
   TWITTER_APP_KEY=your_twitter_app_key
   TWITTER_APP_SECRET=your_twitter_app_secret
   TWITTER_KEY=your_twitter_key
   TWITTER_SECRET=your_twitter_secret
   CONNECTION_STRING=your_db_connection_string
   TABLE_NAME=your_table_name
   TRACK_TERMS=term1,term2,term3
   CSV_NAME=your_exported_csv_name.csv
   ```

2. Make sure your database is up and running and accessible through the connection string.

## Usage

1. Run the main script:

   ```
   python scraper.py
   ```

   This will start streaming tweets based on the tracking terms specified in the `.env` file.

2. The application will store the tweets in the database and will export the data to a CSV file every 30 minutes.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

---
