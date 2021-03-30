# -*- coding: utf-8 -*-
from appium import webdriver
import time
import random
from appium.webdriver.common.touch_action import TouchAction

desired_cap = {
        "platformName": "Android",
        "deviceName": "LMG900Nfe25231e",
        "appPackage": "com.snowcorp.soda.android",
        "appActivity": "com.linecorp.sodacam.android.camera.CameraActivity",
        "noReset": True
    }


# element 의 bounds 속성을 사용하여 해당 element 의 가운데 좌표 return
def get_center(bounds):
    split_bounds_1 = bounds.split('][')[0].split(',')
    split_bounds_2 = bounds.split('][')[1].split(',')

    x = int(split_bounds_1[0][1:]) + (int(split_bounds_2[0]) - int(split_bounds_1[0][1:])) / 2
    y = int(split_bounds_1[1]) + (int(split_bounds_2[1][:-1]) - int(split_bounds_1[1])) / 2

    return x, y


# element 의 bounds 속성을 사용하여 해당 element 의 너비 return
def get_width(bounds):
    split_bounds_1 = bounds.split('][')[0].split(',')
    split_bounds_2 = bounds.split('][')[1].split(',')

    width = int(split_bounds_2[0]) - int(split_bounds_1[0][1:])

    return width


# shell 명령어 사용하여 특정 경로의 용량 return
def check_storage(driver_inuse, path):
    du_result = None
    du_result = driver_inuse.execute_script('mobile: shell', {
        'command': 'du',
        'args': [path],
        'includeStderr': True,
        'timeout': 5000
    })

    if du_result['stderr'] != '':
        print('error detect!')
        return du_result
    else:
        return du_result['stdout'].split('\t')[0]


def TC_ID_01():
    global desired_cap

    driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_cap)
    driver.implicitly_wait(30)
    time.sleep(2)

    before_storage = check_storage(driver, '/sdcard/DCIM/Camera')

    driver.find_element_by_id('com.snowcorp.soda.android:id/circle').click()
    time.sleep(5)

    after_storage = check_storage(driver, '/sdcard/DCIM/Camera')

    if int(after_storage) - int(before_storage) > 0:
        print('Photo shoot success')
    else:
        print('Photo shoot failure')

    driver.quit()


def TC_ID_02():
    global  desired_cap

    driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_cap)
    driver.implicitly_wait(30)
    time.sleep(2)

    before_storage = check_storage(driver, '/sdcard/DCIM/Camera')

    # 필터 아이콘 선택
    driver.find_element_by_id('com.snowcorp.soda.android:id/take_filters').click()
    time.sleep(3)

    # 모든 필터 카테고리 보이도록 5번째 필터 모음 선택
    fifth_item_xpath = driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout/android.widget.FrameLayout[3]/android.widget.RelativeLayout/android.view.ViewGroup[2]/androidx.recyclerview.widget.RecyclerView[1]/android.widget.TextView[5]')
    fifth_item_xpath.click()

    # 선택할 필터 모음 고르기
    filter_category = ['Natural', 'Original', 'Selfie', 'Mood', 'Bright', 'Deep', 'Spring']
    select_filter_category = filter_category[random.randrange(0, len(filter_category))]
    print('i will select ' + select_filter_category)
    time.sleep(2)

    # 랜덤 선택한 필터 모음 클릭
    filter_category_elements = driver.find_elements_by_id('com.snowcorp.soda.android:id/category_text_view')
    for type in filter_category_elements:

        type_text = type.get_attribute("text")

        if type_text == select_filter_category:
            type_xpath = type.get_attribute("bounds")

            split_bounds_1 = type_xpath.split('][')[0].split(',')
            split_bounds_2 = type_xpath.split('][')[1].split(',')

            x = int(split_bounds_1[0][1:]) + (int(split_bounds_2[0]) - int(split_bounds_1[0][1:])) / 2
            y = int(split_bounds_1[1]) + (int(split_bounds_2[1][:-1]) - int(split_bounds_1[1])) / 2

            #driver.tap([(x, y)], 1)
            TouchAction(driver).tap(None, x, y, 1).perform()
            break

    time.sleep(3)

    # 해당 필터 카테고리에서 랜덤으로 필터 변경
    random_index = str(random.randrange(1, 8))
    filter_item_xpath = '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout/android.widget.FrameLayout[3]/android.widget.RelativeLayout/android.view.ViewGroup[2]/androidx.recyclerview.widget.RecyclerView[2]/android.widget.RelativeLayout[' + random_index + ']/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.ImageView'
    print('i will select ' + random_index + 'th item')
    driver.find_element_by_xpath(filter_item_xpath).click()
    time.sleep(2)

    # 사진 촬영
    driver.find_element_by_id('com.snowcorp.soda.android:id/circle').click()
    time.sleep(5)

    # 저장소 용량 체크
    after_storage = check_storage(driver, '/sdcard/DCIM/Camera')

    if int(after_storage) - int(before_storage) > 0:
        print('Photo shoot success')
    else:
        print('Photo shoot failure')

    driver.quit()


def TC_ID_03():
    global desired_cap

    driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_cap)
    driver.implicitly_wait(30)
    time.sleep(2)

    window_size = driver.get_window_size()
    screen_width = window_size['width']
    print("screen width : " + str(screen_width))

    # 필터 아이콘 선택
    driver.find_element_by_id('com.snowcorp.soda.android:id/take_filters').click()
    time.sleep(3)

    # Natural 카테고리 선택 (가장 첫번째 카테고리)
    filter_category_elements = driver.find_elements_by_id('com.snowcorp.soda.android:id/category_text_view')
    for type in filter_category_elements:

        type_text = type.get_attribute("text")

        if type_text == "Natural":
            x, y = get_center(type.get_attribute("bounds"))
            TouchAction(driver).tap(None, x, y, 1).perform()
            # TouchAction.tap(None, x, y).perform()
            # driver.tap([(x, y)], 1)
            break

    time.sleep(3)

    # Original 선택 (가장 첫번째 필터)
    filter_text_elements = driver.find_elements_by_id('com.snowcorp.soda.android:id/filter_text_view')
    for type in filter_text_elements:

        type_text = type.get_attribute("text")

        if type_text == "Original":
            x, y = get_center(type.get_attribute("bounds"))
            TouchAction(driver).tap(None, x, y, 1).perform()
            # driver.tap([(x, y)], 1)
            break

    time.sleep(3)

    # 반복 시작 (Original 포함 최대 51개)
    for filter_repeat in range(1, 51):

        # 촬영 먼저
        before_storage = check_storage(driver, '/sdcard/DCIM/Camera')
        driver.find_element_by_id('com.snowcorp.soda.android:id/circle').click()
        time.sleep(5)
        after_storage = check_storage(driver, '/sdcard/DCIM/Camera')
        # 저장소 용량 확인
        if int(after_storage) - int(before_storage) > 0:
            print('Photo shoot success (order : ' + str(filter_repeat) + ' )')
        else:
            print('Photo shoot failure (order : ' + str(filter_repeat) + ' )')

        # check_view 이용해서 그 옆 필터 좌표 얻기
        check_view_element = driver.find_element_by_id('com.snowcorp.soda.android:id/filter_checked_view')
        check_view_bounds = check_view_element.get_attribute("bounds")
        check_view_width = get_width(check_view_bounds)
        x, y = get_center(check_view_bounds)
        x = x + check_view_width

        # 화면 크기 벗어나면 끝
        if x > screen_width:
            print("my x is " + str(x) + ". I quit.")
            break

        # 필터 선택
        TouchAction(driver).tap(None, x, y, 1).perform()
        # TouchAction.tap(None, x, y).perform()
        # driver.tap([(x, y)], 1)
        time.sleep(3)

    driver.quit()