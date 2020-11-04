from telegram.ext import (
    CommandHandler,
    CallbackQueryHandler)

from ..utils.consts import TEXT
from ..tamplates.buttons import login_keyboard
from ..filters.decorators import execute_if_user_dont_exist
from ..database.query import get_password
from ..database.manipulation import (
    hash_user_password,
    append_password,
    create_account, 
    delete_account)


__all__ = [
    "register_step_1",
    "register_step_2",
    "register_step_3",
    "register_step_3_numeric",
    "register_step_4"]


@execute_if_user_dont_exist
def register_callback(update, context):
    pattern_identifier = "register_step_1_"
    markup = login_keyboard(pattern_identifier)["step_1"]
    update.message.reply_text(
        TEXT["ask_if_want_create_a_password"], 
        reply_markup=markup)


def register_callback_query_step_2(update, context):
    query = update.callback_query
    if query.data == "register_step_1_cancel_loging_process":
        query.edit_message_text(TEXT["canceled_operation"])
    elif query.data == "register_step_1_next_step_1_login_process": 
        create_account(query.from_user)
        pattern_identifier = "register_step_2_"
        markup = login_keyboard(pattern_identifier)["step_2"]
        query.edit_message_text(
            TEXT["type_password"], 
            reply_markup=markup)
    else: 
        return


def register_callback_query_step_3(update, context):
    query = update.callback_query
    user_id = query.from_user.id
    if query.data == "register_step_2_cancel_numeric_keyboard":
        delete_account(user_id)
        query.edit_message_text(TEXT["canceled_operation"])
    elif query.data == "register_step_2_end_numeric_keyboard": 
        pattern_identifier = "register_step_3_"
        markup = login_keyboard(pattern_identifier)["step_3"]
        password = get_password(user_id)
        query.edit_message_text(
            "\"" + password + "\", " + 
            TEXT["this_are_the_typed_password"] + 
            TEXT["ask_if_its_all_ok"], 
            reply_markup=markup)
    else: 
        return


def register_callback_query_number_in_numeric_keyboard(update, context):
    query = update.callback_query
    user_id = query.from_user.id
    digit = query.data.replace("register_step_2_digit_", "")
    append_password(user_id, digit)
    pattern_identifier = "register_step_2_"
    markup = login_keyboard(pattern_identifier)["step_2"]
    query.edit_message_text(
        TEXT["typing"] + get_password(user_id),
        reply_markup=markup)



def register_callback_query_step_4(update, context):
    query = update.callback_query
    if query.data == "register_step_3_cancel_loging_process":
        user_id = query.from_user.id
        delete_account(user_id)
        query.edit_message_text(TEXT["canceled_operation"])
    elif query.data == "register_step_3_end_login_process":
        query.edit_message_text(TEXT["user_password_has_stored"])
        user_id = query.from_user.id
        hash_user_password(user_id)
    else:
        return


register_step_1 = CommandHandler("register", register_callback)


register_step_2 = CallbackQueryHandler(
    register_callback_query_step_2,
    pattern="register_step_1_")


register_step_3 = CallbackQueryHandler(
    register_callback_query_step_3,
    pattern="register_step_2_")


register_step_3_numeric = CallbackQueryHandler(
    register_callback_query_number_in_numeric_keyboard,
    pattern="register_step_2_digit_")


register_step_4 = CallbackQueryHandler(
    register_callback_query_step_4,
    pattern="register_step_3_")

