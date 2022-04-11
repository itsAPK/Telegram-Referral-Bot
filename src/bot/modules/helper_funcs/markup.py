from telegram import ReplyKeyboardMarkup,KeyboardButton,ReplyKeyboardRemove,InlineKeyboardButton,InlineKeyboardMarkup


def start_markup():
    return ReplyKeyboardMarkup([
        [
            KeyboardButton("📋 Dashboard"),   
        ],
        [
            KeyboardButton("🔝 Leaderboard")
        ],
        [
            KeyboardButton('SHILL - 1'),
            KeyboardButton('SHILL - 2'),
            KeyboardButton('SHILL - 3 ')
        ]       
        ],resize_keyboard=True)
    
def dashboard_markup():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(text='🧰 Update Wallet',callback_data='set_wallet')
        ]
    ])

def join_markup():
    return ReplyKeyboardMarkup([
        [KeyboardButton('✅ Joined')]
        
        ],resize_keyboard=True)

def admin_markup():
    return ReplyKeyboardMarkup([
    [
        KeyboardButton('📢 Broadcast'),
        KeyboardButton('📝 Edit Shill Post'),
        KeyboardButton('➕ Add Admin')
        
        
    ],
    [
        
        KeyboardButton('📊 Statistics'),
        KeyboardButton('👤 Get User Info'),
        KeyboardButton("ℹ️ Export Data")
    ],
    [
        KeyboardButton('🔄 Reset Contest'),
        KeyboardButton('✉️ Set Message'),
        KeyboardButton('🖼 Set Image')
    ],
    [
        KeyboardButton('🔓 Open Contest'),
        KeyboardButton('🔒 Close Contest')
    ],
    [
        KeyboardButton('🔙 Back')
    ]
    ],resize_keyboard=True)
    
    
def cancel_markup():
    return ReplyKeyboardMarkup([
        [KeyboardButton('🚫 Cancel')]
    ],resize_keyboard=True)
    
def edit_shill_post_markup():
    return ReplyKeyboardMarkup([
        [
            KeyboardButton('SHILL - 1'),
            KeyboardButton('SHILL - 2'),
            KeyboardButton('SHILL - 3')
        ],
    [
        KeyboardButton('🔙 Back')
    ]
    ],resize_keyboard=True)
