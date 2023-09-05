import asyncio
import datetime

from aiogram import Router, F, types, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, InputMediaPhoto, InputMedia
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config_reader import config
from middlewares.for_album import AlbumMiddleware
from texts import texts

now = datetime.datetime.now()
year = '{:02d}'.format(now.year)
month = '{:02d}'.format(now.month)
day = '{:02d}'.format(now.day)
hour = '{:02d}'.format(now.hour)
minute = '{:02d}'.format(now.minute)
second = '{:02d}'.format(now.second)
tag_day_month_year = "#" + '{}{}{}{}{}{}'.format(year, month, day, hour, minute, second)

router = Router()  # [1]


class PlacingAD(StatesGroup):
    choosing_city = State()
    choosing_model = State()
    choosing_snizz = State()
    choosing_cost = State()
    choosing_text = State()
    choosing_phone_number = State()
    choosing_photo = State()
    choosing_exit = State()
    next_photo = State()


@router.callback_query(F.data == "place_ad_city")
async def cb_place_ad(callback: types.CallbackQuery, state: FSMContext):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text=texts.CB_MAIN_MENU,
        callback_data="main_menu")
    )
    await callback.message.answer(text=texts.MESSAGE_PLACE_AD_CITY, reply_markup=builder.as_markup())
    # Устанавливаем пользователю состояние "выбирает город"
    await state.set_state(PlacingAD.choosing_city)


@router.message(PlacingAD.choosing_city)
async def constructor_city(message: Message, state: FSMContext):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text=texts.CB_MAIN_MENU,
        callback_data="main_menu")
    )
    await state.update_data(chosen_city=message.text.lower())
    await message.answer(
        text=texts.MESSAGE_PLACE_AD_MODEL,
        reply_markup=builder.as_markup()
    )
    # Устанавливаем пользователю состояние "выбирает марку и модель"
    await state.set_state(PlacingAD.choosing_model)


@router.message(PlacingAD.choosing_model)
async def constructor_model(message: Message, state: FSMContext):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text=texts.CB_MAIN_MENU,
        callback_data="main_menu")
    )
    await state.update_data(chosen_model=message.text.lower())
    await message.answer(
        text=texts.MESSAGE_PLACE_AD_SNIZZ,
        reply_markup=builder.as_markup()
    )
    # Устанавливаем пользователю состояние "выбирает косяки"
    await state.set_state(PlacingAD.choosing_snizz)


@router.message(PlacingAD.choosing_snizz)
async def constructor_snizz(message: Message, state: FSMContext):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text=texts.CB_MAIN_MENU,
        callback_data="main_menu")
    )
    await state.update_data(chosen_snizz=message.text.lower())
    await message.answer(
        text=texts.MESSAGE_PLACE_AD_COST,
        reply_markup=builder.as_markup()
    )
    # Устанавливаем пользователю состояние "выбирает цену"
    await state.set_state(PlacingAD.choosing_cost)


@router.message(PlacingAD.choosing_cost)
async def constructor_cost(message: Message, state: FSMContext):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text=texts.CB_MAIN_MENU,
        callback_data="main_menu")
    )
    await state.update_data(chosen_cost=message.text.lower())
    await message.answer(
        text=texts.MESSAGE_PLACE_AD_TEXT,
        reply_markup=builder.as_markup()
    )
    # Устанавливаем пользователю состояние "выбирает описание"
    await state.set_state(PlacingAD.choosing_text)


@router.message(PlacingAD.choosing_text)
async def constructor_text(message: Message, state: FSMContext):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text=texts.CB_MAIN_MENU,
        callback_data="main_menu")
    )
    await state.update_data(chosen_text=message.text.lower())
    await message.answer(
        text=texts.MESSAGE_PLACE_AD_PHONE_NUMBER,
        reply_markup=builder.as_markup()
    )
    # Устанавливаем пользователю состояние "выбирает телефон"
    await state.set_state(PlacingAD.choosing_phone_number)


@router.message(PlacingAD.choosing_phone_number)
async def constructor_phone_number(message: Message, state: FSMContext):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text=texts.CB_MAIN_MENU,
        callback_data="main_menu")
    )
    await state.update_data(chosen_phone=message.text.lower())
    await message.answer(
        text=texts.MESSAGE_PLACE_AD_PHOTO,
        reply_markup=builder.as_markup()
    )
    # Устанавливаем пользователю состояние "выбирает фото"
    await state.set_state(PlacingAD.choosing_photo)


router.message.middleware(AlbumMiddleware())


@router.message(PlacingAD.choosing_photo)
async def constructor_photo(message: Message, state: FSMContext, album: list[Message]):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text=texts.CB_MAIN_MENU,
        callback_data="main_menu")
    )
    data = await state.get_data()
    text = f'''
    Город: {data['chosen_city']}\nМарка и модель: {data['chosen_model']}\nКосяки: {data['chosen_snizz']}
Цена: {data['chosen_cost']}\nОписание: {data['chosen_text']}\nТелефон: {data['chosen_phone']}\n\n\n{tag_day_month_year}\n\n@{message.chat.username}
    '''

    media_group = []
    itit = 1
    for msg in album:
        if msg.photo:
            file_id = msg.photo[-1].file_id
            if itit > 0:
                media_group.append(InputMediaPhoto(media=file_id, caption=text))
                itit -= 1
            elif itit < 1:
                media_group.append(InputMediaPhoto(media=file_id))
        else:
            obj_dict = msg.dict()
            file_id = obj_dict[msg.content_type]['file_id']
            media_group.append(InputMedia(media=file_id))
    await message.answer_media_group(media=media_group)
    await message.answer(
        text=texts.MESSAGE_PLACE_AD_EXIT,
        reply_markup=builder.as_markup()
    )
    await Bot(token=config.bot_token.get_secret_value()).send_media_group(
        chat_id=config.chat_id_kolesnikov.get_secret_value(), media=media_group)
    await asyncio.sleep(35)
    await Bot(token=config.bot_token.get_secret_value()).send_media_group(
        chat_id=config.chat_id_auto_39.get_secret_value(), media=media_group)

    await state.clear()


@router.message(PlacingAD.choosing_exit)
async def constructor_exit(message: Message, state: FSMContext):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text=texts.CB_MAIN_MENU,
        callback_data="main_menu")
    )

    await message.answer(
        text=texts.MESSAGE_PLACE_AD_EXIT,
        reply_markup=builder.as_markup()
    )

    await state.clear()


@router.callback_query(F.data == "main_menu")
async def cb_main_menu(callback: types.CallbackQuery, state: FSMContext):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text=texts.CB_SELL_AUTO,
        callback_data="sell_auto")
    )
    builder.add(types.InlineKeyboardButton(
        text=texts.CB_BUY_AUTO,
        callback_data="buy_auto")
    )
    await state.clear()
    await callback.message.answer(text=texts.MESSAGE_MAIN_MENU, reply_markup=builder.as_markup())
    await callback.message.delete()


@router.callback_query(F.data == "sell_auto")
async def cb_sell_auto(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text=texts.CB_VERY_FAST,
        callback_data="very_fast")
    )
    builder.add(types.InlineKeyboardButton(
        text=texts.CB_PLACE_AD,
        callback_data="place_ad_city")
    )
    builder.row(types.InlineKeyboardButton(
        text=texts.CB_MAIN_MENU,
        callback_data="main_menu")
    )

    await callback.message.answer(text=texts.MESSAGE_SELL_AUTO, reply_markup=builder.as_markup())
    await callback.message.delete()


@router.callback_query(F.data == "place_ad")
async def cb_place_ad(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text=texts.CB_MAIN_MENU,
        callback_data="main_menu")
    )

    await callback.message.answer(text=texts.MESSAGE_MAIN_MENU, reply_markup=builder.as_markup())
    await callback.message.answer(text=texts.PLACE_AD, reply_markup=builder.as_markup())
    await callback.message.delete()


@router.callback_query(F.data == "very_fast")
async def cb_very_fast(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text=texts.CB_MAIN_MENU,
        callback_data="main_menu")
    )

    await callback.message.answer(text=texts.VERY_FAST + texts.PLACE_AD, parse_mode="HTML",
                                  reply_markup=builder.as_markup())
    await callback.message.delete()


@router.callback_query(F.data == "buy_auto")
async def cb_buy_auto(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text=texts.CB_GENERAL_BASE,
        callback_data="general_base")
    )
    builder.add(types.InlineKeyboardButton(
        text=texts.CB_HOT_STUFF,
        callback_data="hot_stuff")
    )
    builder.row(types.InlineKeyboardButton(
        text=texts.CB_MAIN_MENU,
        callback_data="main_menu")
    )

    await callback.message.answer(text=texts.MESSAGE_BUY_AUTO, reply_markup=builder.as_markup())
    await callback.message.delete()


@router.callback_query(F.data == "general_base")
async def cb_general_base(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text=texts.CB_MAIN_MENU,
        callback_data="main_menu")
    )

    await callback.message.answer(text=texts.MESSAGE_GENERAL_BASE, reply_markup=builder.as_markup())
    await callback.message.delete()


@router.callback_query(F.data == "hot_stuff")
async def cb_hot_stuff(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text=texts.CB_MAIN_MENU,
        callback_data="main_menu")
    )

    await callback.message.answer(text=texts.MESSAGE_HOT_STUFF, reply_markup=builder.as_markup())
    await callback.message.delete()
