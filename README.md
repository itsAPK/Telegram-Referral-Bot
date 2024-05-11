# Python Telegram Referral Bot

Bt allows users to generate referral links, track total referrals, and view a leaderboard of top referrers.

## Installation

1. Clone this repository:
```bash
   git clone https://github.com/your_username/python-telegram-referral-bot.git
   ```
2. Install the required dependencies:
  ```bash
      pip install -r requirements.txt
  ```
3. Install and Create Postgresql Database
4. Modify `config.py`
  ```python
   class Config(object):
    LOGGER = True
    DATABASE_URI ='postgresql://postgres:postgres@localhost:5432/db'
    LOG_CHANNEL =     #Channel Id to get bot error logs
    SUDO_USERS=[] #User Ids who can access bot admin panel
    BOT_TOKEN='1393190801:AAFSRCGOQAajiyY7SE5kxTDTcaPDecOQAjs'
    WORKERS = 8
    SUPPORT_CHANNEL='' #Channel where referal users need to join 
   ```
5. Run the bot
  ```bash
   cd src && python3 -m bot
  ```
   
## Usage

- **Automated Referral Generation**: Simplifies the process of generating unique referral links for users.
- **Track Referral Metrics**: Enables users to monitor their total referrals and view their position on the leaderboard effortlessly.
- **Simplified Sharing**: Provides pre-populated sharing messages, facilitating quick and easy dissemination of referral links.
- **Promotional Tool**: Offers businesses a promotional avenue to incentivize user referrals, thereby enhancing user acquisition and   engagement.How It WorksThis bot streamlines the referral process on Telegram, making it convenient for users to participate in referral programs and for businesses to leverage word-of-mouth marketing effectively.

## How It Works

This bot streamlines the referral process on Telegram, making it convenient for users to participate in referral programs and for businesses o leverage word-of-mouth marketing effectively.

# User Dashboard 
- **Dashboard**: User Dashboard Where user can see there primary details like name, refferal link, total invites
- **Leaderboard** : Can see top referrals of the contest
- **Shill** : Generates Promotional Template to share

