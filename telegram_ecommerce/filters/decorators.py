from ..utils.consts import TEXT
from ..database.query import (
    user_exist,
    is_admin)


def warning_the_user_that_already_have_an_account(update, context):
    text = TEXT["user_have_account"]
    update.message.reply_text(text)


def warning_the_user_that_he_dont_have_an_account(update, context):
    text = TEXT["user_dont_have_account"]
    update.message.reply_text(text)


def execute_if_user_exist(callback):
    def execute_warning_if_user_dont_exist(update, context):
        user_id = update.effective_user.id
        if user_exist(user_id):
            callback(update, context)
        else:
            warning_the_user_that_he_dont_have_an_account(update, context)
    return execute_warning_if_user_dont_exist


def execute_if_user_dont_exist(callback):
    def execute_warning_if_user_exist(update, context):
        user_id = update.effective_user.id
        if user_exist(user_id):
            warning_the_user_that_already_have_an_account(update, context)
        else:
            callback(update, context)
    return execute_warning_if_user_exist

