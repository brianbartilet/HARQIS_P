from Applications import *
from enum import Enum
from datetime import datetime
import random
import base64


@app.task()
@notify_work()
@elastic_logging()
def punch_in(source_id):
    webdriver_config = apps_config[source_id]['webdriver']
    wdf = WebDriverFactory

    with wdf.create_webdriver(**webdriver_config) as driver:
        pl = PageLoginAllSec(driver=driver, source_id=source_id)
        pl.login(pl.parameters['username'], pl.parameters['password'])

        ph = PageHomeAllSec(driver=driver, source_id=source_id)
        ph.wait_for_page_to_load(time_sec=5)
        ph.punch_in()
        ph.wait_for_page_to_load(time_sec=5)
        ph.logout()


@app.task()
@notify_work()
@elastic_logging()
def punch_out(source_id):
    webdriver_config = apps_config[source_id]['webdriver']
    wdf = WebDriverFactory

    with wdf.create_webdriver(**webdriver_config) as driver:
        pl = PageLoginAllSec(driver=driver, source_id=source_id)
        pl.login(pl.parameters['username'], pl.parameters['password'])

        ph = PageHomeAllSec(driver=driver, source_id=source_id)
        ph.wait_for_page_to_load(time_sec=5)
        ph.punch_out()
        ph.wait_for_page_to_load(time_sec=5)
        ph.logout()


@app.task()
@notify_work()
@elastic_logging()
def check_absent_days(source_id, notifications_id):
    webdriver_config = apps_config[source_id]['webdriver']
    wdf = WebDriverFactory

    days_ = []
    with wdf.create_webdriver(**webdriver_config) as driver:
        pl = PageLoginAllSec(driver=driver, source_id=source_id)
        pl.login(pl.parameters['username'], pl.parameters['password'])

        ph = PageHomeAllSec(driver=driver, source_id=source_id)
        ph.wait_for_page_to_load(time_sec=5)

        for absent_ in ph.div_day_absent():
            days_.append(absent_.text)

        ph.wait_for_page_to_load(time_sec=5)
        ph.logout()

    if len(days_) > 0:
        notification = CurlServicePushNotifications(notifications_id)
        dump = 'DAYS ABSENT: '
        for day in days_:
            dump = dump + '{0}{1} '.format(day, ', ' if len(days_) > 1 else '')
        try:
            notification.send_notification(dump)
        except:
            log.warning("Error encountered in push notifications.")

    return days_


@app.task()
@notify_work("Oracle Timesheet Creation")
@elastic_logging()
def create_timesheet(source_id):
    webdriver_config = apps_config[source_id]['webdriver']
    wdf = WebDriverFactory
    with wdf.create_webdriver(**webdriver_config) as driver:
        pt = PageTimeSheetOracle(driver, source_id)
        pt.navigate_to_page()
        pt.wait_for_page_to_load(5)
        pt.select_side_menu_link("Self-Service Time & Expense - PH 3103")
        pt.select_side_menu_child_link("Create Timecard")
        pt.select_template("Last Timecard")
        pt.set_timesheet(pt.parameters['timesheet'])
        pt.submit()


class SurveyAnswerMap(Enum):
    WORK_LOCATION = 1
    SYMPTOM_SORE_THROAT = 5
    SYMPTOM_BODY_PAIN = 8
    SYMPTOM_HEADACHE = 11
    SYMPTOM_FEVER = 14
    SYMPTOM_DIZZINESS = 17
    SYMPTOM_BODY_WEAKNESS = 20
    SYMPTOM_JOINT_PAINS = 23
    SYMPTOM_JOINT_COUGH = 26
    SYMPTOM_JOINT_COLDS = 29
    SYMPTOM_JOINT_LOSS_SMELL = 32
    SYMPTOM_JOINT_DIFF_BREATHING = 35
    SYMPTOM_JOINT_DIARRHEA = 38
    SYMPTOM_JOINT_CLOSE_ENV = 40
    SYMPTOM_JOINT_CLOSE_CONTACT = 42
    SYMPTOM_JOINT_TRAVEL_OUTSIDE_PH = 44
    SYMPTOM_JOINT_TRAVEL_OUTSIDE_HOME = 46
    SYMPTOM_JOINT_AUTH = 47
    INPUT_TEMP = 80
    SUBMIT_FINISH = 84


@app.task()
@notify_work("Daily Health Check")
def create_daily_health(source_id, trello_id, board_name, logging_list_name):

    answers_list = {
        (SurveyAnswerMap.WORK_LOCATION.value, 'Yes, I am scheduled to work at WCC'),
        (SurveyAnswerMap.SYMPTOM_SORE_THROAT.value, 'No'),
        (SurveyAnswerMap.SYMPTOM_BODY_PAIN.value, 'No'),
        (SurveyAnswerMap.SYMPTOM_HEADACHE.value, 'No'),
        (SurveyAnswerMap.SYMPTOM_FEVER.value, 'No'),
        (SurveyAnswerMap.SYMPTOM_DIZZINESS.value, 'No'),
        (SurveyAnswerMap.SYMPTOM_BODY_WEAKNESS.value, 'No'),
        (SurveyAnswerMap.SYMPTOM_JOINT_PAINS.value, 'No'),
        (SurveyAnswerMap.SYMPTOM_JOINT_COUGH.value, 'No'),
        (SurveyAnswerMap.SYMPTOM_JOINT_COLDS.value, 'No'),
        (SurveyAnswerMap.SYMPTOM_JOINT_LOSS_SMELL.value, 'No'),
        (SurveyAnswerMap.SYMPTOM_JOINT_DIFF_BREATHING.value, 'No'),
        (SurveyAnswerMap.SYMPTOM_JOINT_DIARRHEA.value, 'No'),
        (SurveyAnswerMap.SYMPTOM_JOINT_CLOSE_ENV.value, 'No'),
        (SurveyAnswerMap.SYMPTOM_JOINT_CLOSE_CONTACT.value, 'No'),
        (SurveyAnswerMap.SYMPTOM_JOINT_TRAVEL_OUTSIDE_PH.value, 'No'),
        (SurveyAnswerMap.SYMPTOM_JOINT_TRAVEL_OUTSIDE_HOME.value, 'No'),
        (SurveyAnswerMap.SYMPTOM_JOINT_AUTH.value, 'Yes'),
        (SurveyAnswerMap.INPUT_TEMP.value, None),
    }

    driver = WebDriverFactory.get_web_driver_instance(**apps_config[source_id]['webdriver'])
    bp = BasePage(driver, source_id)
    bp.driver.get(bp.parameters['url'])
    bp.wait_page_to_load(10)

    labels_survey = bp.driver.find_elements(By.TAG_NAME, 'label')
    for i, label_survey in enumerate(labels_survey):
        print('index: {0} text: {1}'.format(i, label_survey.text))
        for answer in answers_list:
            if i == answer[0]:
                if label_survey.is_displayed():
                    bp.wait_for_element_to_be_visible_e(label_survey)
                    bp.high_light_element(label_survey)
                    bp.scroll_to_element_e(label_survey)
                    bp.wait_page_to_load(1)
                    label_survey.click()
                    label_survey.click()
                    bp.wait_page_to_load(1)
                    break

    inputs_survey = bp.driver.find_elements(By.TAG_NAME, 'input')
    for i, input_survey in enumerate(inputs_survey):
        print('index: {0} text: {1}'.format(i, input_survey.get_attribute('outerHTML')))

    temp = round(random.uniform(35.5, 36.5), 1)
    inputs_survey[SurveyAnswerMap.INPUT_TEMP.value].send_keys('{0}'.format(temp))
    bp.wait_page_to_load(5)

    inputs_survey[SurveyAnswerMap.SUBMIT_FINISH.value].click()
    bp.wait_page_to_load(20)
    time.sleep(20)
    sshot = os.path.join(os.getcwd(), 'HEALTH_TODAY_{0}.png'.format(datetime.today().strftime('%Y-%m-%d')))
    bp.driver.save_screenshot(sshot)

    bp.driver.close()

    trello_cards_service = ApiServiceCards(trello_id)
    current_cards, id_list, target_board = get_board_data(trello_id, board_name, logging_list_name)

    attach_name = 'Health Declaration {0}'.format(datetime.today().strftime('%Y-%m-%d'))
    card_dto = DtoCard(
        name=attach_name,
        idList=id_list.id,
        pos='top'

    )

    card_create = trello_cards_service.add_card(card_dto)

    attachment_dto = DtoAttachment(
        file=sshot,
        name=attach_name,
        mimeType='image/png',
    )

    trello_cards_service.add_file_attachment_to_card(card_create.id, attachment_dto)