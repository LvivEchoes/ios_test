"""
This module contains a few tests:
    - testing a native iOS settings (connection of Cochlear's hearing device).
    - testing a Cochlear's application in Demo mode(volume changes).
"""

import time
import unittest

from random import randint

from appium.webdriver.common.touch_action import TouchAction
from appium.webdriver.webdriver import WebDriver


SELECTOR_MAPPING = {
    "cell": "XCUIElementTypeCell",
    "switch": "XCUIElementTypeSwitch",
    "other": "XCUIElementTypeOther",
    "button": "XCUIElementTypeButton",
}


class BaseTests(unittest.TestCase):
    def setUp(self, application):
        # TODO: I guess, it would be better to use some configuration file or similar solution.
        hub_url = "http://0.0.0.0:4723/wd/hub"
        # FIXME: there should some better solution for `app` capability.
        desired_capabilities = {
            "deviceName": "iPhone SE",
            "udid": "f4946b2b36e4b7a64fe1405e1c8456bac9e4bca0",
            "platformName": "iOS",
            "automationName": "XCUITest",
            "app": application,
            "xcodeSigningId": "iPhone Developer",
            "updatedWDABundleId": "com.afkTestTeam.WebDriverAgentLib",
            "shouldWaitForQuiescence": "False",
            "fastReset": True
        }
        # Configure WebDriver.
        self.driver = WebDriver(hub_url, desired_capabilities=desired_capabilities)

    def swipe_element(self, direction="up"):
        """Swipe element in the appropriate direction."""
        self.driver.execute_script("mobile: swipe", {"direction": direction})

    def click_on_element(self, element):
        """Click on the element or swipe while it's not displayed."""
        while not element.is_displayed():
            self.swipe_element()

        # Click on displayed element.
        element.click()

    def get_xcui_element(self, element_type, name, contains=False):
        """Find XCUI item by element's type and name."""
        xpath = '//{}[@name="{}"]'
        if contains:
            xpath = '//{}[contains(@name, "{}")'
        return self.driver.find_element_by_xpath(xpath.format(
            SELECTOR_MAPPING[element_type],
            name
        ))

    def activate_menu(self, name):
        """
        Activate menu with an appropriate name.
        Examples: "General", "Accessibility.
        """
        element = self.get_xcui_element("cell", name)
        self.click_on_element(element)

    def enable_demo_mode(self, title):
        """Enable demo mode by clicking on the button with the `title`."""
        demo_mode_button = self.driver.find_element_by_name(title)
        demo_mode_button.click()

    def change_value(self, slider):
        """Change value on the slider."""
        # TODO: it might be useless, if the value is still on the same level.
        # (same positions for x and y are set).
        action = TouchAction(self.driver)
        action.tap(slider, x=randint(0, 50), y=10)
        action.perform()

    def verify_value_change_slider(self, slider):
        """Verify if value changes after moves through slider."""
        value = slider.get_attribute('value')

        self.change_value(slider)
        updated_value = slider.get_attribute('value')

        # Check if slider value changed.
        assert value != updated_value, "Value was not changed!"

    @staticmethod
    def verify_value_change_plus_minus(element, button):
        """Verify if value changes after click on `+` or `-` button."""
        value = element.get_attribute("value")
        button.click()

        time.sleep(1)
        updated_value = value.get_attribute('value')
        assert value != updated_value, "Value was not changed!"


class SettingsTests(BaseTests):
    def setUp(self):
        super(SettingsTests, self).setUp("Settings")

    def connect_to_cochlear_device(self):
        """Connect to Cochlear's hearing device."""
        cochlear_device = self.get_xcui_element("cell", "Cochlear", contains=True)
        if not cochlear_device:
            # There is no hearing device.
            raise EnvironmentError

        # Connect to hearing device.
        cochlear_device[0].click()

    def verify_live_listen_button(self, button, is_start_button=True):
        # Start/Stop LIVE LISTEN on iOS Mobile Device.
        button.click()
        time.sleep(1)

        if is_start_button:
            assert not self.get_xcui_element("other", "Start", contains=True)
        else:
            assert not self.get_xcui_element("other", "Stop", contains=True)
            assert self.get_xcui_element("other", "Start", contains=True)

    def test_hearing_device(self):
        # TODO: selectors in this function may be not correct,
        # need to re-check them with real device.
        try:
            self.connect_to_cochlear_device()
        except EnvironmentError:
            # Skip the test if there is no device.
            return

        # Change between available Presets.
        # FIXME: is it a valid title for presets? It looks like it should be something
        # like that: `Presets`. Please verify it via real device.
        presets = self.get_xcui_element("other", "Master Volume")

        # Use one of presets if there are more than 1 preset.
        if len(presets) > 1:
            presets[-1].click()
            time.sleep(1)

            assert not presets[0].is_selected()

        # Change "Master Volume"//XCUIElementTypeCell[contains(@name, "Cochlear")]
        master_volume_slider = self.get_xcui_element("other", "Master Volume")
        self.verify_value_change_slider(master_volume_slider)

        # Allow/disallow streaming to paired Sound Processor.
        streaming_switch = self.get_xcui_element("switch", "Streaming", contains=True)

        # Disallow streaming value.
        if streaming_switch.is_selected():
            streaming_switch.click()
            time.sleep(1)

        # Check if streaming disallowed.
        assert not streaming_switch.is_selected()

        # Allow streaming, and check if it allowed.
        streaming_switch.click()
        time.sleep(1)

        assert streaming_switch.is_selected()

        # Start/Stop LIVE LISTEN on iOS Mobile Device.
        start_live_listen_button = self.get_xcui_element("other", "Start", contains=True)
        self.verify_live_listen_button(start_live_listen_button, is_start_button=True)

        stop_live_listen_button = self.get_xcui_element("other", "Stop", contains=True)
        self.verify_live_listen_button(stop_live_listen_button, is_start_button=False)

        self.driver.back()

    def test_settings(self):
        # TODO: do we really need this wait?
        self.driver.implicitly_wait(5)
        # Move to `General` menu.
        self.activate_menu("General")
        # Move to `Accessibility` menu.
        self.activate_menu("Accessibility")

        # FIXME: why do we use time.sleep instead of Thread.sleep?
        time.sleep(5)

        # Open all paired hearing devices.
        hearing_devices = self.get_xcui_element("cell", "Hearing Devices", contains=True)
        self.click_on_element(hearing_devices)

        # Turn on `Bluetooth` if it's disabled.
        bluetooth_switch = self.get_xcui_element("switch", "Bluetooth")
        if bluetooth_switch:
            bluetooth_switch[0].click()

        self.test_hearing_device()

        self.driver.back()

        # TODO: do we really need this sleep?
        time.sleep(1)

        # Swipe up.
        self.swipe_element()

        slider = self.get_xcui_element("other", "Left-Right Stereo Balance")
        self.verify_value_change_slider(slider)

        time.sleep(2)

    def tearDown(self):
        self.driver.quit()


class ApplicationTests(BaseTests):
    def setUp(self):
        # FIXME: there should some better solution for `app` capability.
        super(ApplicationTests, self).setUp("/Users/pavlo.tsyupka/Downloads/Nucleus Smart 1.431.2.zip")

    def swipe_all_screens(self, direction="up"):
        for _ in range(5):
            self.swipe_element(direction=direction)
            time.sleep(0.125)

    def test_application(self):
        self.swipe_element(direction="left")

        # Swipe to the left(first?) screen.
        self.swipe_all_screens(direction="left")

        self.enable_demo_mode("demoModeButton")

        # Click on `volume`.
        volume_open_button = self.get_xcui_element("cell", "volume")
        self.click_on_element(volume_open_button)

        # FIXME: need a testing environment to understand what, how we're going to get.
        # But this xPath looks awful.
        plus_button = self.driver.find_element_by_xpath(
            '//XCUIElementTypeOther[4]/XCUIElementTypeOther/XCUIElementTypeButton[1]'
        )
        minus_button = self.driver.find_element_by_xpath(
            '//XCUIElementTypeOther[4]/XCUIElementTypeOther/XCUIElementTypeButton[2]'
        )

        value_element = self.get_xcui_element("cell", "volume")
        self.verify_value_change_plus_minus(value_element, plus_button)
        self.verify_value_change_plus_minus(value_element, minus_button)

        # Activate menu.
        menu_button = self.get_xcui_element("button", "Settings menu")
        menu_button.click()
        time.sleep(1)

        # Exit the practice mode.
        exit_button = self.get_xcui_element("cell", "exitPracticeMode")
        self.click_on_element(exit_button)
        time.sleep(1)

        self.swipe_all_screens()

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(SettingsTests)
    application_suite = unittest.TestLoader().loadTestsFromTestCase(ApplicationTests)
    all_tests = unittest.TestSuite((suite, application_suite))
    unittest.TextTestRunner(verbosity=2).run(all_tests)
