import time
import logging

import data      # import the data.py file which contains the constant values
import helpers   # import the helpers.py file which contains networking functions

from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.options import Options

from pages import UrbanRoutesPage

'''
Class TestUrbanRoutes

This class is used to test the functionality of the Urban Routes web app
'''
class TestUrbanRoutes:
    # Name: setup_class
    # Parameters: None
    # Return: None
    #
    # This is the class constructor. It establishes the connection with the Urban Routes web service
    @classmethod
    def setup_class(cls):
        # Add in S8
        # do not modify - we need additional logging enabled in order to retrieve phone confirmation code
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}

        chrome_options = Options()
        chrome_options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
        cls.driver = webdriver.Chrome(options=chrome_options)

        logging.basicConfig(filename="logs/log.txt",
                            filemode='a',
                            format='%(asctime)s,%(msecs)03d %(name)s %(levelname)s %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S',
                            level=logging.INFO)

        # Check if the URL specified by constant URBAN_ROUTES_URL in the data.py file is reachable
        # and print a message accordingly
        if helpers.is_url_reachable(data.URBAN_ROUTES_URL):
            cls.driver.get(data.URBAN_ROUTES_URL)
            cls.urban_routes_page = UrbanRoutesPage(cls.driver)
            logging.log(logging.INFO, "Connected to the Urban Routes server")
        else:
            # Connection to Urban Routes web service failed
            logging.log(logging.ERROR, "Cannot connect to Urban Routes. Check the server is on and still running")

    def reload_page(self):
        # Check if the URL specified by constant URBAN_ROUTES_URL in the data.py file is reachable
        # and print a message accordingly
        self.driver.get(data.URBAN_ROUTES_URL)
        self.urban_routes_page = UrbanRoutesPage(self.driver)

        time.sleep(5)

    def set_addresses(self):
        self.urban_routes_page.enter_from_location("East")
        self.urban_routes_page.enter_to_location("1300")

    def call_taxi(self, quit=False):
        self.set_addresses()
        time.sleep(2)
        self.urban_routes_page.click_custom_option()
        time.sleep(2)
        self.urban_routes_page.click_taxi_icon()
        time.sleep(5)
        self.urban_routes_page.click_call_taxi_button()

    def set_phone_number(self, phone_number):
        time.sleep(5)
        self.urban_routes_page.click_phone_number_button()
        time.sleep(3)
        self.urban_routes_page.set_phone_number_text(phone_number)

    def get_phone_number(self):
        self.urban_routes_page.click_phone_number_button()
        time.sleep(3)
        return self.urban_routes_page.get_phone_number_text()

    def add_credit_card_payment(self):
        self.urban_routes_page.click_payment_method()
        try:
            time.sleep(4)
            self.urban_routes_page.click_add_credit_card()
            time.sleep(4)
            self.urban_routes_page.set_credit_card_text("1234 5678 9012")
            time.sleep(4)
            self.urban_routes_page.set_credit_card_code("4970")
            time.sleep(4)
            self.urban_routes_page.submit_credit_card_add()
            time.sleep(4)
            self.urban_routes_page.close_payment_method_dialog()
            time.sleep(4)
            logging.log(logging.INFO, "Successfully filled card: add credit card")
        except:
            logging.log(logging.ERROR, "Failed to fill card: add credit card")


    def toggle_payment_method_selection(self):
        # Add in S8
        self.urban_routes_page.click_payment_method()
        time.sleep(2)
        self.urban_routes_page.select_cash_payment()
        time.sleep(2)
        self.urban_routes_page.close_payment_dialog()

        try:
            assert "Cash" in self.urban_routes_page.get_selected_payment_method()
            logging.log(logging.INFO, "Successfully selected cash payment method")
        except:
            logging.log(logging.ERROR, "Failed to select cash payment method")

        time.sleep(2)

        self.urban_routes_page.click_payment_method()
        time.sleep(2)
        self.urban_routes_page.select_cc_payment()
        time.sleep(2)
        self.urban_routes_page.close_payment_dialog()

        try:
            assert "Card" in self.urban_routes_page.get_selected_payment_method()
            logging.log(logging.INFO, "Successfully selected card payment method")
        except:
            logging.log(logging.ERROR, "Failed to select card payment method")

    # Name: test_set_route
    # Parameters: None
    # Return: None
    #
    # This method tests the set_route method of the Urban Routes web service
    def test_set_route(self):
        # Add in S8
        address_from = "East"
        address_to = "1300"

        try:
            self.urban_routes_page.enter_from_location(address_from)
            self.urban_routes_page.enter_to_location(address_to)

            actual_from_location = self.urban_routes_page.get_from_location()
            actual_to_location = self.urban_routes_page.get_to_location()

            assert actual_from_location == address_from
            assert actual_to_location == address_to

            logging.log(logging.INFO, "Successfully set route")
        except:
            logging.log(logging.ERROR, "Failed to set route")

        self.reload_page()


    # Name: test_select_plan
    # Parameters: None
    # Return: None
    #
    # This method tests the select_plan method of the Urban Routes web service
    def test_select_plan(self):
        # Add in S8
        self.set_addresses()
        time.sleep(5)
        self.urban_routes_page.click_optimal_option()

        try:
            assert "active" in self.urban_routes_page.get_optimal_option_status()
            logging.log(logging.INFO, "Successfully selected optimal plan")
        except:
            logging.log(logging.ERROR, "Failed to select optimal plan")

        time.sleep(5)

        self.urban_routes_page.click_fastest_option()

        try:
            assert "active" in self.urban_routes_page.get_fastest_option_status()
            logging.log(logging.INFO, "Successfully selected fastest plan")
        except:
            logging.log(logging.ERROR, "Failed to select fastest plan")

        self.urban_routes_page.click_custom_option()

        try:
            assert "active" in self.urban_routes_page.get_custom_option_status()
            logging.log(logging.INFO, "Successfully selected custom plan")
        except:
            logging.log(logging.ERROR, "Failed to select custom plan")

        self.reload_page()

    # Name: test_fill_phone_number
    # Parameters: None
    # Return: None
    #
    # This method tests the fill_phone_number method of the Urban Routes web service
    def test_fill_phone_number(self):
        # Add in S8
        self.call_taxi()
        phone_number = "+1 519 555 1212"
        self.set_phone_number(phone_number)
        self.urban_routes_page.click_phone_number_close()
        retrieved_phone_number = self.get_phone_number()

        try:
            assert retrieved_phone_number == phone_number
            logging.log(logging.INFO, "Successfully set phone number")
        except:
            logging.log(logging.ERROR, "Failed to set phone number. Expecting " + str(phone_number) + ", Retrieved: " + str(retrieved_phone_number))

        self.reload_page()

    # Name: test_fill_card
    # Parameters: None
    # Return: None
    #
    # This method tests the fill_card method of the Urban Routes web service
    def test_fill_card(self):
        self.call_taxi()
        time.sleep(4)
        try:
            self.add_credit_card_payment()
            logging.log(logging.INFO, "Successfully filled card: add credit card")
        except:
            logging.log(logging.ERROR, "Failed to fill card: add credit card")

        time.sleep(4)
        self.toggle_payment_method_selection()

        self.reload_page()

    # Name: test_comment_for_driver
    # Parameters: None
    # Return: None
    #
    # This method tests the comment_for_driver method of the Urban Routes web service
    def test_comment_for_driver(self):
        # Add in S8
        self.call_taxi()

        comment_for_driver = "Do not be late!"
        self.urban_routes_page.send_message_to_driver(comment_for_driver)

        retrieved_comment_for_driver = self.urban_routes_page.get_message_to_driver()

        try:
            assert comment_for_driver == retrieved_comment_for_driver
            logging.log(logging.INFO, "Successfully commented for driver")
        except:
            logging.log(logging.ERROR, "Failed to commented for driver")

        self.reload_page()

    # Name: test_order_blanket_and_handkerchiefs
    # Parameters: None
    # Return: None
    #
    # This method tests the order_blanket_and_handkerchiefs method of the Urban Routes web service
    def test_order_blanket_and_handkerchiefs(self):
        # Add in S8
        self.call_taxi()
        self.urban_routes_page.click_supportive_tariff_card()
        time.sleep(2)

        self.urban_routes_page.click_order_requirements()
        time.sleep(2)
        first_value = self.urban_routes_page.get_blanket_and_handkerchiefs_checkbox_value()

        self.urban_routes_page.click_blanket_and_handkerchiefs()
        second_value = self.urban_routes_page.get_blanket_and_handkerchiefs_checkbox_value()
        time.sleep(2)
        self.urban_routes_page.click_blanket_and_handkerchiefs()
        third_value = self.urban_routes_page.get_blanket_and_handkerchiefs_checkbox_value()

        try:
            assert first_value != second_value and second_value != third_value and first_value == third_value
            logging.log(logging.INFO, "Successfully set blanket and handkerchiefs")
        except:
            logging.log(logging.ERROR, "Failed to set blanket and handkerchiefs")

        self.reload_page()

    # Name: test_order_2_ice_creams
    # Parameters: None
    # Return: None
    #
    # This method tests the order_2_ice_creams method of the Urban Routes web service
    def test_order_2_ice_creams(self):
        # Add in S8
        self.call_taxi()
        self.urban_routes_page.click_supportive_tariff_card()
        time.sleep(2)
        self.urban_routes_page.click_order_requirements()
        time.sleep(2)

        # A variable should be defined and then loop should iterate twice ...
        number_of_ice_creams = 2   # the number of ice creams to order
        for i in range(number_of_ice_creams):
            # Add in S8
            self.urban_routes_page.click_add_icecream()
            time.sleep(1)
        pass

        try:
            assert str(number_of_ice_creams) == self.urban_routes_page.get_icecream_count()
            logging.log(logging.INFO, "Successfully set icecream count")
        except:
            msg = f"Failed to set icecream count; Number of ice creams needed: {number_of_ice_creams}, Number of ice creams set: {self.urban_routes_page.get_icecream_count()}."
            logging.log(logging.ERROR, msg)

        self.reload_page()

    # Name: test_car_search_model_appears
    # Parameters: None
    # Return: None
    #
    # This method tests the car_search_model_appears method of the Urban Routes web service
    def test_car_search_model_appears(self):
        # Add in S8
        self.set_addresses()
        time.sleep(2)
        self.urban_routes_page.click_custom_option()
        time.sleep(2)
        self.urban_routes_page.click_drive_icon()
        time.sleep(4)
        self.urban_routes_page.click_book_button()
        time.sleep(2)
        try:
            assert self.urban_routes_page.is_tariff_picker_shown() == True
            logging.log(logging.INFO, "Successfully shown car search model")
        except:
            logging.log(logging.ERROR, "Failed to show car search model")

        self.reload_page()

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()



test_urban_routes = TestUrbanRoutes()
test_urban_routes.setup_class()
test_urban_routes.test_set_route()
test_urban_routes.test_select_plan()
test_urban_routes.test_fill_phone_number()
test_urban_routes.test_comment_for_driver()
test_urban_routes.test_order_blanket_and_handkerchiefs()
test_urban_routes.test_order_2_ice_creams()
test_urban_routes.test_car_search_model_appears()
test_urban_routes.test_fill_card()
time.sleep(10)
test_urban_routes.teardown_class()

