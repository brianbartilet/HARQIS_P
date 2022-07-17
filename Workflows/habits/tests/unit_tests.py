from Workflows.habits import *


class UnitTests(TestCase):

    def test_create_reminder(self):
        trello_id = "Trello"
        card_reminder = create_trello_reminder(
            trello_id=trello_id,
            board_name="Daily Dashboard",
            list_name="EXECUTE",
            card_title="*HFL {0}*".format(datetime.datetime.now().strftime("%m/%d/%Y")),
            position='top',
            description="son of a bitch",
            labels_list=['TEST', 'HAHA'],
            attachment_url='https://trello-attachments.s3.amazonaws.com/56b8e0bf15387324b8ecf695/5d555e20eb376b0de7693ef9/c6746bbf62c2bb612536ee2ca1dce053/image.png')

        card_service = ApiServiceCards(trello_id)
        card_service.archive_card(card_reminder)

    def test_clean_homework(self):
        args = [
            "Trello",
            "Daily Dashboard",
            "EXECUTE",
            "HOMEWORK FOR LIFE",
            "*HFL"
        ]
        move_cards_with_title_to_target_list(*args)

    def test_clean_blank_homework_for_life(self):
        clean_blank_homework_for_life('Trello', 'Daily Dashboard', 'HOMEWORK FOR LIFE')

    def test_create_homework_for_life(self):
        create_homework_for_life("Trello", "Daily Dashboard", "EXECUTE")

    def test_create_meal_plan_board(self):
        create_meal_planning("Trello", "WHAT'S MY ULAM TODAY?", "RECIPES LIST", False)

    def test_create_agon_weekly_reminder(self):
        trello_id = "Trello"
        strenuous_id = 'StrenuousLife'
        card_agon = create_trello_reminder_from_weekly_agons(
            strenuous_id=strenuous_id,
            trello_id=trello_id,
            board_name="Daily Dashboard",
            list_name="REMINDERS",
            attachment_url='https://media.giphy.com/media/pw7qE5fPNrNWo/giphy.gif'
        )

        card_service = ApiServiceCards(trello_id)
        card_service.archive_card(card_agon)

    def test_create_reminders(self):
        trello_id = "Trello"
        create_trello_reminders_from_habit_cards(
            trello_id=trello_id,
            board_name="Daily Dashboard",
            habit_list_name="GRIND",
            reminders_list_name="EXECUTE"
        )

    def test_archive_trello_reminders_from_habit_cards(self):
        archive_trello_reminders_from_habit_cards(
            trello_id='Trello',
            board_name="Daily Dashboard",
            reminders_list_name="EXECUTE",
            completed_list_name="COMPLETED",
            filter_tag_recur='RECURRING',
            filter_tag_done='DONE'

        )

    def test_get_habits_quadrant_priority(self):
        self.assertEqual('Q4', get_habits_quadrant_priority(['TEST', 'TEST']))
        self.assertEqual('Q2', get_habits_quadrant_priority(['TEST', 'TEST', 'IMPORTANT']))
        self.assertEqual('Q3', get_habits_quadrant_priority(['TEST', 'URGENT']))
        self.assertEqual('Q1', get_habits_quadrant_priority(['TEST', 'TEST', 'URGENT', 'IMPORTANT']))
        self.assertEqual('Q4', get_habits_quadrant_priority(['TEST', 'TEST']))
        self.assertEqual('Q4', get_habits_quadrant_priority([]))

    def test_create_daily_tasks_metrics(self):
        create_daily_tasks_metrics(
            elastic_id='ElasticSearch',
            trello_id='Trello',
            board_name='Daily Dashboard',
            list_name='EXECUTE'

        )