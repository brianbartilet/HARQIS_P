from Applications import *
from Business.habits import *

from datetime import datetime, timedelta
import re
import yaml
from celery.schedules import crontab
import random

INDEX_ROOT_NAME_HABITS = 'TRELLO_DAILY_TASKS_TRACKER'


def create_card(
        trello_id,
        target_board,
        id_list,
        card_title,
        position='top',
        description=None,
        labels_list: [] = None,
        attachment_url=None):

    trello_cards_service = ApiServiceCards(trello_id)
    trello_boards_service = ApiServiceBoards(trello_id)

    #  region Add Reminders as Cards

    labels_id_list = None
    if labels_list is not None:
        labels_id_list = [l.id for l in QList(trello_boards_service.get_board_labels(target_board))
            .where(lambda x: x.name in labels_list)]

    card_dto = DtoCard(
        name=card_title,
        idList=id_list.id,
        idLabels=labels_id_list,
        pos=position,
        desc=description,

    )

    card_create = trello_cards_service.add_card(card_dto)

    if attachment_url is not None:
        attachment_dto = DtoAttachment(
            url=attachment_url,
            setCover=True
        )

        trello_cards_service.add_attachment_to_card(card_create.id, attachment_dto)

    return card_create


@app.task()
def create_trello_reminder(
        trello_id,
        board_name,
        list_name,
        card_title,
        position='top',
        description=None,
        labels_list: [] = None,
        attachment_url=None):
    current_cards, id_list, target_board = get_board_data(trello_id, board_name, list_name)

    return create_card(
                trello_id,
                target_board,
                id_list,
                card_title,
                position,
                description,
                labels_list,
                attachment_url)

    #  endregion


def get_card_reminders_configuration(card_item):

    #  region Get Reminders as Cards From Backticks Markdown From Description

    reminders_config = re.findall(r"(?<=\`\`\`\+\+\+\n).*?(?=\n\`\`\`)", card_item.desc, re.DOTALL)

    #  endregion

    #  region Store in List of YAML

    configs = []
    for result in range(len(reminders_config)):
        try:
            configs.append(yaml.load(reminders_config[result]))
        except Exception:
            log.warning("Failed to create reminder on card: {0}".format(card_item.name))

    #  endregion

    return configs


@app.task()
@elastic_logging()
def create_daily_tasks_metrics(
        elastic_id,
        trello_id,
        board_name,
        list_name):

    current_cards, id_list, target_board = get_board_data(trello_id, board_name, list_name)

    index_name = '{0}'.format(INDEX_ROOT_NAME_HABITS).lower()

    for card_ in current_cards:

        label_names = [x.name for x in card_.labels]
        points = QList(card_.labels).first(lambda x: x.color == 'black').name
        completed = True if 'DONE' in label_names else False
        roles = [x.name for x in QList(card_.labels).where(lambda x: '|' in x.name)]
        name = str(card_.name).split('[')[0] if '[' in card_.name else card_.name
        priority = get_habits_quadrant_priority(label_names)
        url = card_.short_link
        name_final = " ".join(re.findall(r"[a-zA-Z0-9]+", name))
        dto_task = DtoTaskReminder(
            name=name_final,
            description=card_.desc,
            completed=completed,
            points=int(points),
            tags=label_names,
            roles=roles,
            priority=priority,
            url=url
        )
        try:
            send_json_data_to_elastic_server(app_config_name=elastic_id,
                                             json_dump=dto_task.get_dict(),
                                             index_name=index_name,
                                             use_interval_map=True,
                                             location_key='{0}'.format(dto_task.name.replace(' ', '_').lower()),
                                             )
        except AssertionError:
            log.warning("Unable to add data: {0}{1}".format(index_name, dto_task.name))


def create_cards_to_reminder(
        trello_id: str,
        target_board,
        id_list,
        reminders_config: []):

    output = []
    for reminder in reminders_config:

        schedule_strings = reminder['REMINDER']['schedule']

        schedule = eval("{1}({0})".format(schedule_strings, crontab.__name__))
        schedule.app.conf.enable_utc = False
        app.conf.timezone = 'Asia/Manila'

        if reminder['REMINDER']['last_run'] != 'None':
            try:
                datetime_object = datetime.strptime(reminder['REMINDER']['last_run'], '%B %d %Y - %H:%M:%S')
            except Exception:
                #datetime_object = datetime.utcnow() - timedelta(days=1)
                datetime_object = datetime.now()
        else:
            #datetime_object = datetime.utcnow() - timedelta(days=1)
            datetime_object = datetime.now()
        due = schedule.is_due(datetime_object)[0]
        if not due:
            continue

        try:
            labels = reminder['REMINDER']['tags'] + ['RECURRING', '{0}'.format(reminder['REMINDER']['points'])]
        except Exception:
            continue

        created_card = create_card(
            trello_id=trello_id,
            target_board=target_board,
            id_list=id_list,
            card_title=reminder['REMINDER']['card_title'],
            position=reminder['REMINDER']['position'],
            description=reminder['REMINDER']['description'],
            labels_list=labels,
            attachment_url=reminder['REMINDER']['attachment'],

        )
        last_run = datetime.utcnow().strftime('%B %d %Y - %H:%M:%S')
        output.append({'last_run': last_run, 'created_card': created_card})

    return output


def update_habit_card_from_output(trello_id, habit_card_item, reminder_cards_created: []):

    if len(reminder_cards_created) > 0:
        trello_cards_service = ApiServiceCards(trello_id)

        reminders_config = re.findall(r"(?<=\`\`\`\+\+\+\n).*?(?=\n\`\`\`)", habit_card_item.desc, re.DOTALL)
        start = 'last_run: '
        end = '\n'

        new_description = ''
        stop_index = 0
        for index in range(len(reminder_cards_created)):
            match = re.match(r'(.+%s\s*).+?(\s*%s.+)' % (start, end), reminders_config[index], re.DOTALL)
            new_config = match.group(1) + "'{0}'".format(reminder_cards_created[index]['last_run']) + match.group(2) + '\n'
            new_description += "```+++\n" + new_config + "```\n"
            stop_index = index

        for index_remaining in range(stop_index + 1, len(reminders_config)):
            new_description += "```+++\n" + reminders_config[index_remaining] + "\n```\n"

        dto = DtoCard(id=habit_card_item.id, desc=new_description)
        trello_cards_service.update_card(dto)


@app.task()
def create_trello_reminders_from_habit_cards(trello_id,
                                             board_name,
                                             habit_list_name,
                                             reminders_list_name):
    #  region Get All Cards in Target List

    habits_current_cards, habits_id_list, habits_target_board = get_board_data(trello_id, board_name, habit_list_name)
    reminders_current_cards, reminders_id_list, reminders_target_board = get_board_data(trello_id, board_name, reminders_list_name)

    for habit_card_item in habits_current_cards:
        if habit_card_item.is_template:
            continue
        reminders_config = get_card_reminders_configuration(habit_card_item)
        reminder_cards_created = create_cards_to_reminder(
            trello_id, reminders_target_board, reminders_id_list, reminders_config)
        update_habit_card_from_output(trello_id, habit_card_item, reminder_cards_created)

    #  endregion


@app.task()
def archive_trello_reminders_from_habit_cards(trello_id,
                                              board_name,
                                              reminders_list_name,
                                              completed_list_name,
                                              filter_tag_recur,
                                              filter_tag_done):

    #  region Archive with Tag in Target List

    trello_cards_service = ApiServiceCards(trello_id)
    trello_boards_service = ApiServiceBoards(trello_id)
    reminders_current_cards, reminders_id_list, reminders_target_board = \
        get_board_data(trello_id, board_name, reminders_list_name)
    completed_current_cards, completed_list, completed_target_board = \
        get_board_data(trello_id, board_name, completed_list_name)

    filter_id_done = QList(trello_boards_service.get_board_labels(reminders_target_board)) \
        .first(lambda x: x.name == filter_tag_done)

    filter_id = QList(trello_boards_service.get_board_labels(reminders_target_board)) \
        .first(lambda x: x.name == filter_tag_recur)

    for do_work_card_item in reminders_current_cards:
        if do_work_card_item.is_template:
            continue
        if filter_id.id in do_work_card_item.id_labels:
            trello_cards_service.archive_card(do_work_card_item)
        else:
            if filter_id_done.id in do_work_card_item.id_labels:
                card_dto = DtoCard(
                    id=do_work_card_item.id,
                    idList=completed_list.id,
                    pos='top'
                )

                trello_cards_service.update_card(card_dto)

    #  endregion


@app.task()
def move_cards_to_target_list(*args):
    move_cards_with_title_to_target_list(*args)


@app.task()
def create_homework_for_life(trello_id, board_name, list_name):
    message = "*HFL {0}* [text here]".format(datetime.now().strftime("%m/%d/%Y"))

    create_trello_reminder(trello_id, board_name, list_name,
                           card_title=message,
                           description='Log HFL at 10pm for 15 minutes',
                           labels_list=['Organization | Everyman Skills', '1']
                           )


@app.task()
def clean_blank_homework_for_life(trello_id, board_name, list_name, contains_string='[text here]'):

    #  region Archive with Tag in Target List
    trello_cards_service = ApiServiceCards(trello_id)
    reminders_current_cards, reminders_id_list, reminders_target_board = get_board_data(trello_id, board_name, list_name)

    for card_item in reminders_current_cards:
        if contains_string in card_item.name:
            trello_cards_service.archive_card(card_item)

    #  endregion


@app.task()
def create_meal_planning(trello_id, board_name, list_name_recipes, allow_repeat=False):

    tags_days_sequence = ['MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY', 'SUNDAY']

    trello_cards_service = ApiServiceCards(trello_id)
    service_trello_boards = ApiServiceBoards(trello_id)

    recipe_cards, source_list, bs = get_board_data(trello_id=trello_id,
                                         board_name=board_name,
                                         list_name=list_name_recipes)

    template = QList(recipe_cards).where(lambda x: x.is_template).first()
    recipes = QList(recipe_cards).where(lambda x: not x.is_template)

    config = parse_configuration_from_desc(template.desc)
    if config is None:
        dto_recipe = DtoCard(
            id=template.id,
            desc='{0}\nERROR: {1}'.format(template.desc, datetime.utcnow().strftime('%B %d %Y - %H:%M:%S')),

        )

        trello_cards_service.update_card(dto_recipe)
        return

    for key in tags_days_sequence:
        current_cards, id_list, target_board = get_board_data(trello_id, board_name, key)

        for c in current_cards:
            trello_cards_service.archive_card(c)

        for schedule in config['LABELS']:
            for tag_food in config['LABELS'][schedule]:

                # try split with OR or AND
                if '|' in tag_food:
                    items = [x.strip() for x in tag_food.split('|')]
                    parsed_labels = [l.id for l in QList(service_trello_boards.get_board_labels(target_board))
                        .where(lambda v: v.name in items)]
                elif '&' in tag_food:
                    items = [x.strip() for x in tag_food.split('&')]
                    parsed_labels = [l.id for l in QList(service_trello_boards.get_board_labels(target_board))
                        .where(lambda v: v.name == [x for x in items])]
                else:
                    parsed_labels = [l.id for l in QList(service_trello_boards.get_board_labels(target_board))
                        .where(lambda v: v.name == tag_food)]

                #  select random from label
                selection = QList(recipes)\
                    .where(lambda v: any(i in v.id_labels for i in parsed_labels))

                if selection:
                    target = random.choice(selection)

                else:
                    continue

                #  create card
                dto_recipe = DtoCard(
                    idList=id_list.id,
                    idCardSource=target.id,
                )

                parsed_labels = [l.id for l in QList(service_trello_boards.get_board_labels(target_board))
                    .where(lambda v: v.name == schedule)]

                new_card = trello_cards_service.add_card(dto_recipe)

                #  add meal schedule tag
                new_card.id_labels = [parsed_labels[0], ]
                dto_update = DtoCard(
                    id=new_card.id,
                    idLabels=new_card.id_labels,
                )
                trello_cards_service.update_card(dto_update)

                #  remove to recipes to prevent duplicates
                if not allow_repeat:
                    recipes = QList(recipes).where(lambda x: x.id != target.id)


