# OpenTCM -- Open Platform for Traditional Chinese Medicine

## Overview

Welcome to the OpenTCM Chat Application! This project consists of three major components:
1. **web-frontend**: The frontend interface of the chat application.
2. **web-backend**: The backend server that handles API requests.
3. **data/**: The directory containing data and configuration files used by the application.

This application allows users to search, chat, and access a wiki about Traditional Chinese Medicine (TCM), providing interactive and intelligent responses.

## Project Structure

```plaintext
OpenTCM
├── web-frontend
├── web-backend
└── data
    ├── db
    ├── src
    ├── books
    └── ...
```

### web-frontend

The frontend of the application is built using React and Next.js, and styled with Material-UI. It provides a user-friendly interface for searching, chatting, and accessing the TCM wiki.

- **components/**: Reusable React components used throughout the application.
- **layouts/**: Layout components that define the overall structure of the pages.
- **pages/**: Next.js pages that define the routes and main views of the application.
- **public/**: Static assets such as images and icons.
- **styles/**: Global and modular CSS styles.

### web-backend

The backend of the application is built using Node.js and Express. It handles API requests, manages sessions, and interacts with external services such as the FastGPT API.

- **controllers/**: Functions that handle requests and responses.
- **models/**: Data models for interacting with the database.
- **routes/**: API routes and endpoints.
- **services/**: Services that interact with external APIs and perform business logic.
- **app.js**: The main entry point of the backend application.

### data

This directory contains data and configuration files used by the application.

- **db/**: Database files and schemas.
- **config/**: Configuration files for various services and settings.

## Features

### Search

The search feature allows users to find information about various TCM herbs, treatments, and concepts. It provides a comprehensive search interface that queries the backend and displays relevant results.

### Chat

The chat feature allows users to interact with a GPT-like chatbot. Users can ask questions and receive intelligent, conversational responses about TCM and related topics.

### Wiki

The TCM wiki provides a wealth of information about Traditional Chinese Medicine, including detailed descriptions of herbs, treatments, and other related concepts. Users can browse the wiki to learn more about TCM.

## Getting Started

### Prerequisites

- Node.js (v18 or later)
- npm or yarn
- SQLite

### Installation

1. **Clone the repository:**

    ```sh
    git clone https://github.com/luckiday/open-tcm.git 
    cd open-tcm
    ```

2. **Install frontend dependencies:**

    ```sh
    cd web-frontend
    yarn install
    ```

3. **Install backend dependencies:**

    ```sh
    cd ../web-backend
    pip install -r requirements.txt
    ```

### Running the Application

1. **Start the backend server:**

    ```sh
    cd web-backend
    python run.py
    ```

2. **Start the frontend development server:**

    ```sh
    cd ../web-frontend
    yarn dev
    ```

3. **Open your browser and navigate to:**

    ```sh
    http://localhost:3100
    ```

## Usage

- Open the chat interface in your browser.
- Use the search bar to find information about TCM herbs, treatments, and concepts.
- Type your messages in the chat to interact with the GPT-like chatbot.
- Browse the wiki to learn more about Traditional Chinese Medicine.

## Contributing

We welcome contributions from the community. Please fork the repository and submit pull requests for any features, bug fixes, or improvements.

## License

This project is licensed under the MIT License.

## Acknowledgments

- Special thanks to the developers of FastGPT for providing the API used in this application.
- Thanks to the contributors and community for their support and contributions.
