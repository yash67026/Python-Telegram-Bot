# Telegram Cyberbullying Moderation Bot

A Python-based Telegram group moderation bot designed to help mitigate **cyberbullying, inappropriate communication, and harmful content** through automated message monitoring and moderation.

The bot, named **LISA**, continuously monitors messages in Telegram groups and takes appropriate moderation actions when potentially harmful or prohibited content is detected.

## Project Overview

Cyberbullying and inappropriate online communication can negatively affect users, particularly in public and community-based messaging groups. Manual moderation can be time-consuming and may not always provide an immediate response.

This project addresses the problem by implementing an **automated content monitoring and moderation system** for Telegram groups.

The bot analyzes incoming text messages and checks them against administrator-defined rules. Depending on the detected content, the bot can:

* Identify messages containing blacklisted words.
* Delete inappropriate messages.
* Temporarily restrict users who violate group rules.
* Detect messages containing links.
* Temporarily ban users who share links.
* Allow administrators to define and manage blacklisted words.
* Provide commands for checking the current blacklist.
* Provide automated responses to users.

## Objectives

The primary objectives of this project are:

1. To reduce cyberbullying in Telegram groups.
2. To automatically identify potentially inappropriate messages.
3. To reduce the workload of human group administrators.
4. To provide immediate moderation responses.
5. To maintain a safer and more controlled online communication environment.
6. To allow administrators to customize the list of prohibited words.
7. To demonstrate the use of Python for automated communication and moderation.

## Key Features

### 1. Automated Message Monitoring

The bot monitors incoming text messages in a Telegram group.

Each message is analyzed to determine whether it contains content that violates the configured moderation rules.

### 2. Blacklisted Word Detection

Administrators can configure a list of words that should not be permitted in the group.

The bot checks incoming messages against the configured blacklist.

If a blacklisted word is detected, the bot can:

* Delete the message.
* Temporarily restrict the user.
* Inform the group that moderation action has been taken.

### 3. Temporary User Restriction

When a user sends a message containing a blacklisted word, the bot temporarily restricts the user from sending messages.

The current implementation applies a temporary restriction for approximately **5 minutes**.

### 4. Link Detection

The bot also monitors messages for HTTP and HTTPS links.

Messages containing detected links trigger an automated moderation action.

The current implementation temporarily bans the user who shares a detected link for approximately **2 hours**.

### 5. Administrator Controls

Only Telegram group administrators can configure the blacklist.

The bot provides commands that allow administrators to manage and view prohibited words.

### 6. Dynamic Blacklist

The blacklist can be updated without modifying the Python source code.

Administrators can provide multiple words separated by commas, allowing the moderation rules to be updated directly through Telegram.

### 7. Persistent Storage

The configured blacklist is stored locally using a Python `pickle` file.

The file used for this purpose is:

```text
blocked.pkl
```

This allows the bot to retain configured blacklist information between executions, subject to the deployment environment.

## Available Commands

### `/start`

Starts the bot and displays a welcome message.

Example:

```text
/start
```

Response:

```text
Hello!
I am LISA, your group manager bot.
```

### `/help`

Provides basic information about reporting or complaints.

```text
/help
```

### `/setblockedwords`

Allows a Telegram group administrator to add blacklisted words.

```text
/setblockedwords
```

The bot asks the administrator to provide the words separated by commas.

Example:

```text
badword1,badword2,badword3
```

### `/showblockedwords`

Displays the currently configured blacklisted words for the group.

```text
/showblockedwords
```

## Moderation Workflow

The general workflow of the bot is:

```text
Telegram Group
       |
       v
Incoming Message
       |
       v
Automated Content Monitoring
       |
       v
Check Against Moderation Rules
       |
       +----------------------+
       |                      |
       v                      v
Blacklisted Word?          Link Detected?
       |                      |
      Yes                    Yes
       |                      |
       v                      v
Delete Message            Moderation Action
       |                      |
       v                      v
Restrict User              Ban User
       |
       v
Send Warning/Notification
```

## Technology Stack

The project uses the following technologies:

* **Python**
* **Telegram Bot API**
* **python-telegram-bot**
* **Pickle**
* **Docker**
* **Render**

The project uses:

```text
python-telegram-bot==13.7
```

## Project Structure

```text
Telegram Bot/
│
├── telegramBot.py
├── blocked.pkl
├── Dockerfile
├── render.yaml
├── requirements.txt
└── README.md
```

### `telegramBot.py`

Contains the main Python implementation of the Telegram moderation bot.

It includes:

* Telegram bot initialization.
* Command handlers.
* Message monitoring.
* Blacklisted-word management.
* User restriction.
* Link detection.
* Message deletion.
* Bot deployment configuration.

### `blocked.pkl`

Stores the configured blacklisted words for Telegram groups.

### `requirements.txt`

Contains the Python dependency required by the project:

```text
python-telegram-bot==13.7
```

### `Dockerfile`

Provides container configuration for deploying the application.

### `render.yaml`

Contains deployment configuration for hosting the Telegram bot on Render.

### `README.md`

Provides project documentation, installation instructions, features, and usage information.

## Installation

### Prerequisites

Before running the project, install:

* Python 3.x
* Git
* A Telegram account
* A Telegram Bot created through BotFather

### Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
```

Navigate to the project directory:

```bash
cd Telegram-Bot
```

### Install Dependencies

Install the required Python package:

```bash
pip install -r requirements.txt
```

## Configuration

The Telegram Bot API token should be stored securely as an environment variable rather than directly inside the source code.

Example:

```text
TELEGRAM_TOKEN=your_bot_token
```

The application can then retrieve the token through Python:

```python
import os

bot_token = os.environ.get("TELEGRAM_TOKEN")
```

**Never publish your actual Telegram Bot API token on GitHub.**

## Running the Bot

After configuring the Telegram bot token and installing the dependencies, run:

```bash
python telegramBot.py
```

The bot can then be added to a Telegram group and provided with the required administrator permissions.

## Telegram Permissions

For effective moderation, the bot should have appropriate administrator permissions in the Telegram group.

Depending on the required functionality, permissions may include:

* Delete messages.
* Restrict users.
* Ban users.
* Manage group messages.

## Deployment

The project includes configuration for deployment using Render.

The deployment configuration uses Python and starts the application using:

```text
python telegramBot.py
```

The bot is configured to use a webhook for receiving Telegram updates.

## Cyberbullying Mitigation

The primary purpose of this project is to provide an automated first layer of moderation against potentially harmful online communication.

The system can help identify:

* Abusive language.
* Prohibited words.
* Potentially inappropriate messages.
* Unwanted links.
* Repeated violations of group rules.

Automated moderation can provide a rapid response while reducing the amount of manual monitoring required from group administrators.

## Advantages

* Automated message monitoring.
* Immediate moderation response.
* Customizable blacklist.
* Administrator-controlled configuration.
* Reduced manual moderation effort.
* Simple Python-based implementation.
* Telegram Bot API integration.
* Suitable for deployment on cloud platforms.

## Limitations

The current implementation primarily relies on **rule-based content detection**, particularly blacklisted words and link detection.

Therefore, it may not understand:

* Context of a conversation.
* Sarcasm.
* Indirect cyberbullying.
* Misspelled or intentionally modified offensive words.
* Images or videos containing harmful content.
* Complex forms of harassment.

Future versions could incorporate more advanced Natural Language Processing (NLP) or machine-learning techniques to improve contextual content analysis.

## Future Enhancements

Potential improvements include:

* AI-based cyberbullying detection.
* Natural Language Processing (NLP).
* Sentiment analysis.
* Context-aware moderation.
* Detection of repeated harassment.
* User violation history.
* Automated warning escalation.
* Administrator moderation dashboard.
* Database-based storage.
* Detection of harmful images and media.
* Improved multilingual content detection.
* Detailed moderation logs.
* Analytics and reporting.
* Integration with machine-learning classification models.

## Security Considerations

The Telegram Bot API token should always be stored securely.

Environment variables should be used for sensitive credentials.

Sensitive files and credentials should not be committed to public GitHub repositories.

A `.gitignore` file should be used to prevent accidental upload of secrets, temporary files, and unnecessary generated files.

## Learning Outcomes

This project demonstrates practical experience with:

* Python programming.
* Telegram Bot API.
* API integration.
* Event-driven programming.
* Automated content moderation.
* File-based data persistence.
* User permission management.
* Git and GitHub.
* Docker.
* Cloud deployment.
* Basic cybersecurity and online safety concepts.

## Conclusion

The **Telegram Cyberbullying Moderation Bot** demonstrates how Python and the Telegram Bot API can be used to automate basic online community moderation.

By monitoring messages, identifying configured prohibited content, deleting inappropriate messages, restricting users, and detecting unwanted links, the system provides an automated moderation layer for Telegram groups.

The project can serve as a foundation for developing more advanced AI-powered content moderation systems capable of understanding context and detecting increasingly complex forms of online harassment.

## Author

**Yashwanth H**

Electronics and Telecommunication Engineering

GitHub:
`https://github.com/YOUR_USERNAME`

---

## License

This project is intended for educational and demonstration purposes.
