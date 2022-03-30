# -*- coding: utf-8 -*-

# This demonstrates handling privacy data from an Alexa skill and using the
# Alexa Skills Kid SDK (v2)

import requests
import logging
import calendar
from datetime import datetime
from pytz import timezone

from ask_sdk_s3.adapter import S3Adapter
from ask_sdk_core.skill_builder import CustomSkillBuilder
from ask_sdk_core.dispatch_components import (
    AbstractRequestHandler, AbstractExceptionHandler
)
from ask_sdk_core.utils import is_request_type, is_intent_name

from ask_sdk_model import (
Response, IntentRequest, DialogState, IntentConfirmationStatus, Slot)

s3_adapter = S3Adapter(bucket_name="pizza-sniffer-testing")
sb = CustomSkillBuilder(persistence_adapter=s3_adapter)

logger = logging.getLogger("main")
logger.setLevel(logging.INFO)


class LaunchRequestIntentHandler(AbstractRequestHandler):
    """
    Handler for Skill Launch
    """
    def can_handle(self, handler_input):
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        speech = ('Hello! Welcome to Pizza Sniffer. What do you want to order? ')
        reprompt = "We have two types of Pizza: pepperoni and mozzarella. What type of Pizza do you want?"

        handler_input.response_builder.speak(speech).ask(reprompt)
        return handler_input.response_builder.response

class PizzaIntentHandler(AbstractRequestHandler):
    """
    Handler for Capturing the Pizza Type
    """
    def can_handle(self, handler_input):
        return is_intent_name("CapturePizzaIntent")(handler_input)

    def handle(self, handler_input):
        slots = handler_input.request_envelope.request.intent.slots

        # extract slot values
        pizzatype = slots["pizzaType"].value
        
        # save slots into session attributes
        session_attr = handler_input.attributes_manager.session_attributes
        session_attr['pizzaType'] = pizzatype

        speech = 'Thanks, I will order a {pizzatype} pizza for you. Do you want to add more \
            '.format(pizzatype=pizzatype)
        reprompt = "Do you want to add more"
        handler_input.response_builder.speak(speech).ask(reprompt)
        return handler_input.response_builder.response
    

class BirthdayIntentHandler(AbstractRequestHandler):
    """
    Handler for Capturing the Birthday
    """
    def can_handle(self, handler_input):
        return (is_intent_name("CaptureBirthdayIntent")(handler_input))
            
    def handle(self, handler_input):
        slots = handler_input.request_envelope.request.intent.slots
        speech = ""
        # extract slot values
        month = slots["month"].value
        day = slots["day"].value
        
        logger.info("confirmation status {}".format(handler_input.request_envelope.request.intent.confirmation_status))

        if (handler_input.request_envelope.request.intent.confirmation_status == IntentConfirmationStatus.CONFIRMED):
            # save slots into session attributes
            session_attr = handler_input.attributes_manager.session_attributes
            session_attr['month'] = month
            session_attr['day'] = day
        
            # Notify user that it had learnt about a Birthday
            speech = ('Thanks, I will remember that your Birthday {month} {day} \
                    ' '<audio src="soundbank://soundlibrary/alarms/back_up_beeps/back_up_beeps_07"/> for your next order'.format(month=month, day=day)
                    )
        else:
            speech = "I will not remember your Birthday"
        
        handler_input.response_builder.speak(speech)
        return handler_input.response_builder.response

class NoIntentHandler(AbstractRequestHandler):
    """
    Handler for AMAZON.NoIntent
    """
    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.NoIntent")(handler_input)

    def handle(self, handler_input):
        speak_output = "Ok. Thank you for the order"

        handler_input.response_builder.speak(
            speak_output)
        return handler_input.response_builder.response

class HelpIntentHandler(AbstractRequestHandler):
    """
    Handler for AMAZON.HelpIntent
    """
    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        speak_output = "You can say hello to me! How can I help?"

        handler_input.response_builder.speak(
            speak_output
            ).ask(speak_output)
        return handler_input.response_builder.response


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """
    Catch all exception handler, log exception and
    respond with custom message.
    """
    def can_handle(self, handler_input, exception):
        return True

    def handle(self, handler_input, exception):

        speak_output = "Sorry, I couldn't understand what you said. Please try again."
        handler_input.response_builder.speak(speak_output).ask(speak_output)
        return handler_input.response_builder.response


class CancelAndStopIntentHandler(AbstractRequestHandler):
    """
    Handler for AMAZON.CancelIntent and AMAZON.StopIntent
    """
    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.CancelIntent")(handler_input) \
            and is_intent_name("AMAZON.StopIntent")(handler_input)

    def handle(self, handler_input):
        speak_output = "Goodbye!"
        handler_input.response_builder.speak(speak_output)
        return handler_input.response_builder.response


class SessionEndedRequestHandler(AbstractRequestHandler):
    """
    Handler for SessionEndedRequest
    """
    def can_handle(self, handler_input):
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # Any cleanup logic goes here
        return handler_input.response_builder.response

# register request / intent handlers
sb.add_request_handler(LaunchRequestIntentHandler())
sb.add_request_handler(PizzaIntentHandler())
sb.add_request_handler(BirthdayIntentHandler())
sb.add_request_handler(NoIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelAndStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

# register exception handlers
sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()
