from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, Bot
from telegram.ext import CommandHandler, MessageHandler, Filters, commandhandler
from telegram.ext import CallbackContext, Dispatcher, ConversationHandler

import constants as const
from player import RealPlayer, Simulator
from game import Game


lst_games: list = list()  # Список раундов
lst_no_players: list = list()  # Список потенциальных игроков
lst_players: list = list()  # Список уже играющих игроков


def cmd_start(update: Update, context: CallbackContext) -> None:
    """
    По команде /start выдать три кнопки вариантов дальнейших действий:
    Играть с ботом, с партнером или отменить действие
    Получаем из message параметры игрока (id, name, chat_id)
    Проверяем наличие игрока в списке уже играющих игроков, если он там уже есть - сообщаем об этом
    """
    player_id = update.message.from_user.id
    for game in lst_games:
        player_a = game.player_a.player_id
        player_b = game.player_b.player_id
        if player_id == player_a or player_id == player_b:
            update.message.reply_text(const.MES_ALREADY_IN_GAME.format(player_id), reply_markup=ReplyKeyboardRemove())
            return
    buttons = const.START_BUTTONS
    keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    name = update.message.from_user.first_name
    update.message.reply_text(const.MES_WHAT_DO.format(player_id, name), reply_markup=keyboard)


def choice_bot(update: Update, context: CallbackContext) -> None:
    """
    Создаем объект игрока. Создаем имитатор игрока. Создаем объект Game. Запускаем процесс игры
    """
    player_id = update.message.from_user.id
    player_name = update.message.from_user.first_name
    bot = update.message.bot
    chat = update.message.chat.id
    player = RealPlayer(player_id, player_name, chat)
    simulator = Simulator()
    game = Game(player, simulator, bot)
    game.run()


def get_allocation(bot: Bot, chat_id: int, player_id: int) -> None:
    # Запрашиваем координаты четерехпалубного корабля
    deck_4 = bot.send_message(chat_id, text=const.MES_ASK_POSITION.format('4=х'))
    print(deck_4)


def cmd_quit(update: Update, context: CallbackContext) -> None:
    """ 
    Выходим из игры. Находим в в списке игр игруЮ  в котрой играет данный игрок,
    удадем из нее игроков, затем удаляем данную игру из списка игр, выходим
    """
    # TODO посмотреть как очищать историю чата при выходе
    player_id = update.message.from_user.id
    for game in lst_games:
        if game.player_a.player_id == player_id or game.player_b.player_id == player_id:
            game.delete_players()
            lst_games.remove(game)
            context.bot.send_message(update.message.chat_id, text=const.MES_QUIT)
            break


def choice_partner(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Пока не реализовано", reply_markup=ReplyKeyboardRemove())
    

def choice_cancel(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(const.MES_QUIT, reply_markup=ReplyKeyboardRemove())


def fixup_value(update: Update, context: CallbackContext) -> None:
    ...


def shot(update: Update, context: CallbackContext) -> None:
    ...


def add_command_handler(dp: Dispatcher) -> None:
    dp.add_handler(CommandHandler('start', cmd_start))
    dp.add_handler(CommandHandler('quit', cmd_quit))

def add_messgae_handler(dp: Dispatcher) -> None:
    choice_bot_handler = MessageHandler(Filters.regex('Играть с ботом'), choice_bot)
    choice_partner_handler = MessageHandler(Filters.regex("Играть с партнером"), choice_partner)
    choice_cancel_handler = MessageHandler(Filters.regex("Отмена"), choice_cancel)
    fixup_value_handler = MessageHandler(Filters.regex('[абвгдежзик][0-9]+-[абвгдежзик][0-9]+'), fixup_value)
    shot_handler = MessageHandler(Filters.regex('[абвгдежзик][0-9]+)'), shot)

    dp.add_handler(choice_bot_handler)
    dp.add_handler(choice_partner_handler)
    dp.add_handler(choice_cancel_handler)
    dp.add_handler(fixup_value_handler)
    dp.add_handler(shot_handler)