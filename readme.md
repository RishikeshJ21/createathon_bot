# Bot Project

## Overview

This project is a bot designed to perform various tasks efficiently and interact seamlessly with users. It leverages advanced features and integrations to provide an optimized experience.
for whole code [https://drive.google.com/file/d/1YBDWOv_308ezp9I2QFaTZEepbsvPZYHK/view?usp=sharing](https://github.com/RishikeshJ21/createathon_bot/releases/tag/beta)
## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## Features

- Seamless interaction with Telegram users.
- Allows crowdfunding campaigns via a blink link.
- Advanced validation of wallet seed phrases.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/RishikeshJ21/createathon_bot
   ```

2. Navigate to the project directory:
   ```bash
   cd repository
   ```

3. Install dependencies for the frontend:
   ```bash
   npm install
   ```

4. Start the development server for the frontend:
   ```bash
   npm run dev
   ```

5. Set up the environment variables:
   Create a `.env` file in the project root and add the following:
   ```env
   BOT_TOKEN=
   DB_NAME=createathon
   DB_USER=postgres
   DB_PASSWORD=
   DB_HOST=localhost
   FB_ACCESS_
   ```

6. Database setup:
   - Paste the `Database/SQL` file into PostgreSQL to create the database.
   - Ensure the database is running and accessible with the details provided in the `.env` file.

7. Backend setup:
   - Download the backend from the provided link.
   - Configure the database and SMTP details in the backend.
   - Specify the hosting path if you are hosting the app.

## Usage

1. Start the bot:
   ```bash
   npm start
   ```

2. Interact with the bot via Telegram by searching for it using its username.


3. Crowdfunding Example:
   - List your application using the DSCVR API.
   - Receive a blink link for your campaign.


## Contributing

Contributions are welcome! Follow these steps:

1. Fork the repository.
2. Create a feature branch:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add your message here"
   ```
4. Push to your fork:
   ```bash
   git push origin feature-name
   ```
5. Create a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements


---

### Contact

For any inquiries, please contact Rishikesh Jadhav at rishikesh21.job@gmail.com.

