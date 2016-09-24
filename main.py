#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
main.py
Created by Émilio G! on 160912
Updated last by Émilio G! 160915

Contains functions to transform a list of string to UTF-8 cards.
Use get_cards to get the result.

"""

import math

MIN_CARD_HEIGHT = 8
CARD_TOP = "┌─────────────┐"
CARD_MID = "│{:<13}│"
CARD_FOOT= "│{:>13}|"
CARD_BOT = "└─────────────┘"
NUMBER_OF_CARDS_PER_ROW = 5

def get_cards(string_list):
	"""
	:param string_list: the list of cards text to display.
	:return: The UTF-8 cards to display.
	"""

	cards = []
	if not isinstance(string_list, list):
		raise TypeError("Invalid Type in get_cards")
	else:
		for string in string_list:
			cards.append(get_card(string, 0, 0))
		card_height = get_cards_height(cards, len(CARD_BOT))
		if card_height < MIN_CARD_HEIGHT:
			card_height = MIN_CARD_HEIGHT
		cards = []
		i = 0
		for string in string_list:
			cards.append(get_card(string, i, card_height))
			i += 1
	return format_cards(cards, len(CARD_BOT), NUMBER_OF_CARDS_PER_ROW)


def get_card(value, card_id, card_height):
	"""
	:param value: the value (text) of the card.
	:param card_id: the id (string) of the card.
	:param card_height: The height of a card (in rows).
	:return: A single, UTF-8 formatted card.
	"""
	return_value = ""
	words_presplit = None
	words_split = []
	if not isinstance(value, str):
		raise TypeError("Invalid type in get_card for value")
	else:
		words_presplit = value.split(" ")

		#Separate words with a "-" also
		for word in words_presplit:
			count_before = len(words_split)
			words_split.extend(word.split("-"))
			if len(words_split) > count_before + 1:
				words_split[count_before] += "-"

		return_value += CARD_TOP

		return_value += add_content(words_split)

		#Complete the card with blank shiez
		continue_fill = True
		while continue_fill:
			if (len(return_value) - len(CARD_TOP)) / len(CARD_TOP) <= card_height:
				return_value += CARD_MID.format("")
			else:
				continue_fill = False

		#add the ID
		return_value += CARD_FOOT.format(card_id)
		#add the bottom
		return_value += CARD_BOT

	return return_value


def add_content(words_split):
	"""
	Returns the core of the card.
	:param words_split: the list of words.
	:return: A string containing the core (middle) of a card.
	"""

	return_value = ""
	# Add text to the card
	buffer = ""
	i = 0
	words_to_count = len(words_split)
	while i < words_to_count:

		# Add words as long as the width of a line allows it
		line = ""
		line += buffer
		buffer = ""
		add_word = True
		while add_word:
			line += words_split[i]
			if line[-1] != "-" or len(line) == len(CARD_TOP) - 2:
				line += " "
			i += 1
			if len(words_split) > i:
				if len(line) + len(words_split[i]) > len(CARD_TOP) - 2:
					add_word = False
					if line[-1] != "-":
						line = line[:-1]
			else:
				add_word = False

		chars_number = len(line)
		string_to_format = line[:len(CARD_BOT) - 3]
		if len(CARD_BOT) - 1 <= chars_number:
			string_to_format += "-"
			buffer += line[len(CARD_BOT) - 3: len(line)] + " "
		else:
			string_to_format += line[len(CARD_BOT) - 3: len(CARD_BOT) - 2]

		return_value += CARD_MID.format(string_to_format)

	if buffer != "":
		return_value += add_content([buffer])

	return return_value


def format_cards(cards, cards_length, cards_per_row):
	"""
		Takes a list of cards from get_card and makes it as one beautiful string.
	:param cards: the list of individual card from get_card
	:param cards_length: the length in columns for a single card
	:param cards_per_row: number of cards per row to display
	:return: A single string with formatted cards
	"""
	return_value = ""
	if len(cards[0]) % cards_length != 0:
		raise ValueError("Bad format for cards")
	else:
		number_of_rows_per_card = round(len(cards[0]) / cards_length)
		row_number = 0
		max_row_number = math.ceil(len(cards) / cards_per_row)

		while row_number < max_row_number:
			if row_number + 1 < max_row_number:
				cards_in_row = cards[row_number * cards_per_row:(row_number + 1) * cards_per_row]
			else:
				cards_in_row = cards[row_number * cards_per_row:len(cards)]
			for i in range(number_of_rows_per_card):
				for card in cards_in_row:
					return_value += card[i * cards_length: (i + 1) * cards_length]
				return_value += "\n"
			row_number += 1

	return return_value


def get_cards_height(cards, card_width):
	"""
	:param cards: The cards .
	:param card_width: The width (in columns) of a card.
	:return: The height (in rows) of the biggest card.
	"""
	max_height = -1
	for card in cards:
		card_height = len(card) / card_width
		if card_height > max_height:
			max_height = card_height
	return max_height - 3

print(get_cards(["Aujourd'hui, dans le cours de documentation, nous allons voir <blank>."]))