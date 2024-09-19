import json
import os
from pathlib import Path
from dotenv import load_dotenv
from vk_api import vk_api
from vk_api.utils import get_random_id

load_dotenv()
vk_session = vk_api.VkApi(token=os.getenv('VKTOKEN'))
vk = vk_session.get_api()


def get_data():
    return json.loads(Path("vars.json").read_text(encoding='utf-8'))


def post_data(data):
    Path("vars.json").write_text(json.dumps(data, sort_keys=False, indent=4, ensure_ascii=False), encoding='utf-8')


def get_conversation_members(chat_id):
    response = vk_session.method('messages.getConversationMembers', {
        'peer_id': 2000000000 + chat_id
    })
    members_ids = [member['member_id'] for member in response['items'] if not (member.get('is_admin') and member['is_admin'])]
    return members_ids


def menu():
    data = get_data()
    inp = int(input('1) Рассылка в беседы\n2) Рассылка ученикам\n3) Настройка\n4) Выход\n\n'))
    if inp == 1:
        group_number = input(f'Введите номер группы из доступных: {", ".join(data.keys())}; или введите номер тарифа: 1 = Стандарт, 2 = Про, 3 = Ультима')
        groups_ids = []
        groups_numbers = []
        if group_number.isdigit() and int(group_number) in range(1, 4):
            group_number = int(group_number)
            group_number = 'Стандарт' if group_number == 1 else ('Про' if group_number == 2 else 'Ультима')
            for number, i in data.items():
                if i[0] == group_number:
                    groups_ids.append(i[2])
                    groups_numbers.append(number)
        else:
            while group_number not in data.keys():
                group_number = input(f'Введите номер группы из доступных: {", ".join(data.keys())}')
                if not group_number:
                    return
            groups_ids = [data[group_number][2]]
            groups_numbers = [group_number]
        if not len(groups_ids):
            print('Групп нет')
            return
        inp2 = input(f'Введите сообщение, которое будет прислано в выбранные беседы. Чтобы прервать, нажмите Enter. Беседы: ' + ', '.join(groups_numbers))
        if inp2 != "":
            inp3 = input('Доп. подтверждение, введите \"Да\"')
            if inp3 == 'Да':
                print('Отправка начинается')
                for i in groups_ids:
                    vk.messages.send(
                        peer_id=2000000000 + i,
                        random_id=get_random_id(),
                        message=inp2
                    )
                print('Отправка окончена')
            else:
                print('Отменено')
        else:
            print('Отменено')
    elif inp == 2:
        group_number = input(f'Введите номер группы из доступных: {", ".join(data.keys())}; или введите номер тарифа: 1 = Стандарт, 2 = Про, 3 = Ультима')
        students = []
        if group_number.isdigit() and int(group_number) in range(1, 4):
            group_number = int(group_number)
            group_number = 'Стандарт' if group_number == 1 else ('Про' if group_number == 2 else 'Ультима')
            for i in data.values():
                if i[0] == group_number:
                    students.extend(i[1])
        else:
            while group_number not in data.keys():
                group_number = input(f'Введите номер группы из доступных: {", ".join(data.keys())}')
                if not group_number:
                    return
            students = data[group_number]
        if not len(students):
            print('Учеников нет')
            return
        inp2 = input(f'Введите сообщение, которое будет прислано всем ученикам из группы в ЛС. Чтобы прервать, нажмите Enter. Страницы учеников: ' + '; '.join([f'https://vk.com/id{student_id}' for student_id in students]))
        if inp2 != "":
            inp3 = input('Доп. подтверждение, введите \"Да\"')
            if inp3 == 'Да':
                print('Отправка начинается')
                for i in students:
                    vk.messages.send(
                        user_id=i,
                        random_id=get_random_id(),
                        message=inp2
                    )
                print('Отправка окончена')
            else:
                print('Отменено')
        else:
            print('Отменено')
    elif inp == 3:
        inp2 = int(input('1) Добавить новую беседу\n2) Убрать беседу\n3) Добавить человека в беседу\n4) Убрать человека из беседы'))
        if inp2 == 1:
            group_number = input('Введите номер группы (1А, 2Д и т.д.)')
            if data.get(group_number):
                print('Уже есть такая группа')
                return
            level = int(input('Введите номер тарифа: 1 = Стандарт, 2 = Про, 3 = Ультима'))
            level = 'Стандарт' if level == 1 else ('Про' if level == 2 else 'Ультима')
            group_id = vk.messages.searchConversations(q=f'{group_number} | {level} | ЕГЭ 2025 по информатике', count=1)['items'][-1]['peer']['local_id']
            data[group_number] = [level, get_conversation_members(group_id), group_id]
            print('Готово')
        elif inp2 == 2:
            group_number = input('Введите номер группы (1А, 2Д и т.д.)')
            if data.get(group_number):
                data.remove(group_number)
                print('Удалено')
            else:
                print('Нет такой группы')
        elif inp2 == 3:
            group_number = input('Введите номер группы (1А, 2Д и т.д.)')
            if data.get(group_number):
                data[group_number][1].append(int(input('Введите айди ученика')))
            else:
                print('Нет такой группы')
        elif inp2 == 4:
            student_id = int(input('Введите айди ученика'))
            for i in data.values():
                if student_id in i[1]:
                    i[1].remove(student_id)
                    print(f'Удалён из группы {i[0]}')
                    break
            else:
                print('Нет такого ученика')
    elif inp == 4:
        raise SystemExit
    else:
        menu()
    post_data(data)


def main():
    while True:
        menu()


if __name__ == '__main__':
    main()
