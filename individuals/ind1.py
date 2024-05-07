# !/usr/bin/env python3
# -*- coding: utf-8 -*-

#Выполнить индивидуальное задание 1 лабораторной работы 2.19, добавив возможность работы с
#исключениями и логгирование.

import argparse
import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import List

from jsonschema import validate
from jsonschema.exceptions import ValidationError


@dataclass
class People:
    people: List[dict] = field(default_factory=list)

    def add(self, surname, name, zodiac, birthday):
        try:
            dict = {
                "surname": surname,
                "name": name,
                "zodica": zodiac,
                "birthday": birthday.split("."),
            }
            self.people.append(dict)
        except Exception as e:
            raise e

    def __str__(self):
        table = []
        line = "+-{}-+-{}-+-{}-+-{}-+-{}-+".format(
            "-" * 4, "-" * 30, "-" * 30, "-" * 20, "-" * 20
        )
        table.append(line)
        table.append(
            "| {:^4} | {:^30} | {:^30} | {:^20} | {:^20} |".format(
                "№", "Фамилия", "Имя", "Знак зодиака", "Дата рождения"
            )
        )
        table.append(line)

        for idx, person in enumerate(self.people, 1):
            print(
                "| {:>4} | {:<30} | {:<30} | {:<20} | {:>20} |".format(
                    idx,
                    person.get("surname", ""),
                    person.get("name", ""),
                    person.get("zodiac", ""),
                    ".".join(person.get("birthday", "")),
                )
            )
        table.append(line)
        return "\n".join(table)

    def select(self, surname):
        result = People()
        for i in self.people:
            if i.surname == surname:
                result.add(i)
        return result

    def load(self, file_name):
        with open(file_name, "r") as f:
            people = json.load(f)

        if validation(people):
            self.people = people

    def save(self, file_name):
        with open(file_name, "w", encoding="utf-8") as f:
            json.dump(self.people, f, ensure_ascii=False, indent=4)


def validation(instance):
    schema = {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "surname": {"type": "string"},
                "name": {"type": "string"},
                "zodiac": {"type": "string"},
                "birthday": {
                    "type": "array",
                    "items": {"type": "string"},
                    "minitems": 3,
                },
            },
            "required": ["surname", "name", "birthday"],
        },
    }
    try:
        validate(instance, schema=schema)
        return True
    except ValidationError as err:
        print(err.message)
        return False


def main(command_line=None):
    """
    Главная функция программы.
    """
    logger = logging.getLogger(__name__)
    # Выполнить настройку логгера
    logging.basicConfig(
        filename="people.log", level=logging.DEBUG, encoding="utf-8"
    )

    # Создать родительский парсер для определения имени файла.
    file_parser = argparse.ArgumentParser(add_help=False)
    file_parser.add_argument(
        "filename", action="store", help="The data file name"
    )

    # Создать основной парсер командной строки.
    parser = argparse.ArgumentParser("people")
    parser.add_argument("--version", action="version", version="%(prog)s 0.1.0")

    subparsers = parser.add_subparsers(dest="command")

    # Создать субпарсер для добавления человека.
    add = subparsers.add_parser(
        "add", parents=[file_parser], help="Add a new person"
    )
    add.add_argument(
        "-s",
        "--surname",
        action="store",
        required=True,
        help="The person's surname",
    )
    add.add_argument(
        "-n", "--name", action="store", required=True, help="The person's name"
    )
    add.add_argument(
        "-z", "--zodiac", action="store", help="The person's zodiac"
    )
    add.add_argument(
        "-b",
        "--birthday",
        action="store",
        required=True,
        help="The person's birthday",
    )

    # Создать субпарсер для отображения всех людей.
    _ = subparsers.add_parser(
        "display", parents=[file_parser], help="Display people"
    )

    # Создать субпарсер для выбора людей по фамилии.
    select = subparsers.add_parser(
        "select", parents=[file_parser], help="Select people by surname"
    )
    select.add_argument(
        "-s",
        "--surname",
        action="store",
        type=str,
        required=True,
        help="The required surname",
    )

    # Выполнить разбор аргументов командной строки.
    args = parser.parse_args(command_line)

    people = People()

    # Домашний каталог
    home_path = Path.home() / args.filename

    is_dirty = False
    if home_path.exists():
        try:
            people.load(home_path)
            logger.info(f"Загружены данные в файл {args.filename}")
        except ValidationError:
            logger.error("Ошибка валидации при загрузке данных из файла.")

    match args.command:
        case "add":
            try:
                people.add(args.surname, args.name, args.zodiac, args.birthday)
                is_dirty = True
                logger.info(
                    f"Добавлен человек: {args.surname}, {args.name}"
                    f"Зодиак: {args.zodiac}"
                    f"День рождения: {args.birthday}"
                )
            except Exception as e:
                logger.error(f"Ошибка: {e}")

        case "select":
            selected = people.select(args.surname, people)
            if selected.people:
                print(selected)
                logger(
                    f"Найдено {len(selected.people)} людей с"
                    f"фамилией {args.surname}"
                )
            else:
                print("Люди с заданной фамилией не найдены")
                logger.warning(f"Люди с фамилией {args.surname} не найдены")

        case "display":
            print(people)
            logger.info("Отображен список сотрудников")

        case _:
            logger.error(f"Введена неверная команда: {args.command}")

    if is_dirty:
        people.save(home_path)
        logger.info(f"Сохранены данные в файл {home_path}.")


if __name__ == "__main__":
    main()
