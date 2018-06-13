import time

from appium.webdriver.common.touch_action import TouchAction
from appium.webdriver.webdriver import WebDriver


def click_on_element(driver, element, direction='up'):
    while not element.is_displayed():
        driver.execute_script("mobile: swipe", {"direction": direction})

    element.click()


def test_test():
    capabilities = {
        "deviceName": "iPhone SE",
        "udid": "f4946b2b36e4b7a64fe1405e1c8456bac9e4bca0",
        "platformName": "iOS",
        "automationName": "XCUITest",
        "app": "Settings",
        "xcodeSigningId": "iPhone Developer",
        "updatedWDABundleId": "com.afkTestTeam.WebDriverAgentLib",
        "shouldWaitForQuiescence": "False",
        "fastReset": True
    }

    driver = WebDriver("http://0.0.0.0:4723/wd/hub", desired_capabilities=capabilities)
    driver.implicitly_wait(5)
    general = driver.find_element_by_xpath('//XCUIElementTypeCell[@name="General"]')

    click_on_element(driver, general)
    accessability = driver.find_element_by_xpath('//XCUIElementTypeCell[@name="Accessibility"]')
    click_on_element(driver, accessability)

    time.sleep(5)
    hearing_devoces = driver.find_element_by_name('Hearing Devices')
    while not hearing_devoces.is_displayed():
        driver.execute_script("mobile: swipe", {"direction": "up"})

    while hearing_devoces.is_displayed():
        hearing_devoces = driver.find_element_by_name('Hearing Devices')
        hearing_devoces.click()

    bluetooth_switch = driver.find_elements_by_xpath('//XCUIElementTypeSwitch[@name="Bluetooth"]')

    if bluetooth_switch:
        bluetooth_switch[0].click()

    driver.back()
    time.sleep(1)

    driver.execute_script("mobile: swipe", {"direction": "up"})

    slider = driver.find_element_by_xpath('//XCUIElementTypeOther[@name="Left-Right Stereo Balance"]')

    old_value = slider.get_attribute('value')

    action = TouchAction(driver)
    action.tap(slider, x=50, y=10)
    action.perform()

    new_value = slider.get_attribute('value')
    assert old_value != new_value

    time.sleep(3)
    driver.background_app(-1)
    driver.execute_script("mobile: swipe", {"direction": "left"})
    app_icon = driver.find_element_by_accessibility_id('Nucleus Smart')
    app_icon.click()

    for _ in range(5):
        driver.execute_script("mobile: swipe", {"direction": "left"})
        time.sleep(0.125)

    demo_mode_button = driver.find_element_by_name('demoModeButton')
    demo_mode_button.click()

    volume_open_button = driver.find_element_by_xpath('//XCUIElementTypeCell[@name="volume"]')
    volume_open_button.click()

    plus_button = driver.find_element_by_xpath('//XCUIElementTypeApplication[@name="Nucleus Smart"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeCollectionView/XCUIElementTypeCell[2]/XCUIElementTypeOther/XCUIElementTypeOther[4]/XCUIElementTypeOther/XCUIElementTypeButton[1]')
    minus_button = driver.find_element_by_xpath('//XCUIElementTypeApplication[@name="Nucleus Smart"]/XCUIElementTypeWindow[1]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeCollectionView/XCUIElementTypeCell[2]/XCUIElementTypeOther/XCUIElementTypeOther[4]/XCUIElementTypeOther/XCUIElementTypeButton[2]')

    value_element = driver.find_element_by_xpath('//XCUIElementTypeCell[@name="volume"]')
    old_value = value_element.get_attribute('value')

    plus_button.click()
    time.sleep(1)
    new_value = value_element.get_attribute('value')
    assert old_value != new_value

    minus_button.click()
    time.sleep(1)
    new_value = value_element.get_attribute('value')
    assert old_value == new_value

    menu_button = driver.find_element_by_xpath('//XCUIElementTypeButton[@name="Settings menu"]')
    menu_button.click()
    time.sleep(1)

    exit_button = driver.find_element_by_xpath('//XCUIElementTypeCell[@name="exitPracticeMode"]')
    exit_button.click()
    time.sleep(1)

    for _ in range(5):
        driver.execute_script("mobile: swipe", {"direction": "right"})
        time.sleep(0.125)

    driver.background_app(-1)

    driver.quit()

if __name__ == "__main__":
    test_test()
