import time

from random import randint
from appium.webdriver.common.touch_action import TouchAction
from appium.webdriver.webdriver import WebDriver


def click_on_element(driver, element, direction='up'):
    while not element.is_displayed():
        driver.execute_script("mobile: swipe", {"direction": direction})

    element.click()


def test_hearing_device(driver: WebDriver):
    # TODO: selectors in this function may be isn't correct, need recheck them with real device
    cochlear_device = driver.find_elements_by_xpath('//XCUIElementTypeCell[contains(@name, "Cochlear")]')

    if not cochlear_device:
        # If no device found will skip test
        return

    # Connect to hearing device
    cochlear_device[0].click()

    # Change between available Presets
    presets = driver.find_elements_by_xpath('//XCUIElementTypeOther[@name="Master Volume"]')

    # If available more than 1 Presets will change one them
    if len(presets) > 1:
        presets[-1].click()
        time.sleep(1)

        assert not presets[0].is_selected()

    # Change "Master Volume"//XCUIElementTypeCell[contains(@name, "Cochlear")]
    master_volume_slider = driver.find_element_by_xpath('//XCUIElementTypeOther[@name="Master Volume"]')

    old_value = master_volume_slider.get_attribute('value')
    action = TouchAction(driver)
    action.tap(master_volume_slider, x=50, y=10)
    action.perform()
    new_value = master_volume_slider.get_attribute('value')

    # Check if slider value changed
    assert old_value != new_value

    # Allow/disallow streaming to paired Sound Processor
    streaming_switch = driver.find_element_by_xpath('//XCUIElementTypeSwitch[contains(@name, "Streaming")')

    # Disallow streaming value
    if streaming_switch.is_selected():
        streaming_switch.click()
        time.sleep(1)

    # Check if streaming disallowed
    assert not streaming_switch.is_selected()

    # Allow streaming, and check if it allowed
    streaming_switch.click()
    time.sleep(1)

    assert streaming_switch.is_selected()

    # Start/Stop LIVE LISTEN on iOS Mobile Device
    start_live_listen_button = driver.find_element_by_xpath('//XCUIElementTypeOther[contains(@name, "Start")]')
    start_live_listen_button.click()
    time.sleep(1)

    assert not driver.find_elements_by_xpath('//XCUIElementTypeOther[contains(@name, "Start")]')

    stop_live_listen_button = driver.find_element_by_xpath('//XCUIElementTypeOther[contains(@name, "Stop")]')
    stop_live_listen_button.click()
    time.sleep(1)

    assert not driver.find_elements_by_xpath('//XCUIElementTypeOther[contains(@name, "Stop")]')
    assert driver.find_elements_by_xpath('//XCUIElementTypeOther[contains(@name, "Start")]')

    driver.back()


def test_setting():
    capabilities = {
        "deviceName": "iPhone SE",
        "udid": "b3346f9b0c4797e7a68fffb4532e1727bc23ad76",
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
    accessibility = driver.find_element_by_xpath('//XCUIElementTypeCell[@name="Accessibility"]')
    click_on_element(driver, accessibility)

    time.sleep(5)
    hearing_devoces = driver.find_element_by_xpath('//XCUIElementTypeCell[contains(@name, "Hearing Devices")]')
    while not hearing_devoces.is_displayed():
        driver.execute_script("mobile: swipe", {"direction": "up"})

    while hearing_devoces.is_displayed():
        hearing_devoces = driver.find_element_by_xpath('//XCUIElementTypeCell[contains(@name, "Hearing Devices")]')
        hearing_devoces.click()

    bluetooth_switch = driver.find_elements_by_xpath('//XCUIElementTypeSwitch[@name="Bluetooth"]')

    if bluetooth_switch:
        bluetooth_switch[0].click()

    test_hearing_device(driver)

    driver.back()
    time.sleep(1)

    driver.execute_script("mobile: swipe", {"direction": "up"})

    slider = driver.find_element_by_xpath(
        '//XCUIElementTypeCell[@name="Left-Right Stereo Balance"]/XCUIElementTypeOther[3]'
    )

    old_value = slider.get_attribute('value')

    action = TouchAction(driver)
    action.tap(slider, x=randint(0, 50), y=10)
    action.perform()

    new_value = slider.get_attribute('value')
    assert old_value != new_value

    time.sleep(2)
    driver.quit()


def test_application():
    capabilities = {
        "deviceName": "iPhone SE",
        "udid": "b3346f9b0c4797e7a68fffb4532e1727bc23ad76",
        "platformName": "iOS",
        "automationName": "XCUITest",
        "app": "/Users/pavlo.tsyupka/Downloads/Nucleus Smart 1.431.2.zip",
        "xcodeSigningId": "iPhone Developer",
        "updatedWDABundleId": "com.afkTestTeam.WebDriverAgentLib",
        "shouldWaitForQuiescence": "False",
        "fastReset": True
    }

    driver = WebDriver("http://0.0.0.0:4723/wd/hub", desired_capabilities=capabilities)
    driver.implicitly_wait(5)

    for _ in range(5):
        driver.execute_script("mobile: swipe", {"direction": "left"})
        time.sleep(0.125)

    demo_mode_button = driver.find_element_by_name('demoModeButton')
    demo_mode_button.click()

    volume_open_button = driver.find_element_by_xpath('//XCUIElementTypeCell[@name="volume"]')
    volume_open_button.click()

    plus_button = driver.find_element_by_xpath(
        '//XCUIElementTypeOther[4]/XCUIElementTypeOther/XCUIElementTypeButton[1]'
    )
    minus_button = driver.find_element_by_xpath(
        '//XCUIElementTypeOther[4]/XCUIElementTypeOther/XCUIElementTypeButton[2]'
    )

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

    driver.quit()


if __name__ == "__main__":
    test_setting()
    test_application()

