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
   python3 -m bot
   ```
   
