import logging

from dragonfly import RecognitionObserver
from dragonfly.engines.backend_natlink.dictation_format import WordFormatter, WordParserDns11
from dragonfly.test.element_tester import ElementTester, Literal

import arduino.environment
from arduino.environment import USE_ARDUINO, TYPE
from arduino.w2ndragon import mixed_word_to_number

LOGGER = logging.getLogger(__name__)


def format_dictation_dns11(words):
    formatted = WordFormatter(parser=WordParserDns11()).format_dictation(words)

    if not formatted:
        LOGGER.error(f"Cannot parse to format: {formatted}")
        return None

    return " ".join(mixed_word_to_number(formatted))


class Observer(RecognitionObserver):
    def __init__(self):
        super(Observer, self).__init__()

    def on_recognition(self, words, rule, node, results):
        """
        Method called when speech successfully decoded to a grammar rule or
        to dictation.

        This is called *before* grammar rule processing (i.e.
        ``Rule.process_recognition()``).

        :param words: recognized words
        :type words: tuple
        :param rule: *optional* recognized rule
        :type rule: Rule
        :param node: *optional* parse tree node
        :type node: NodeIt just returns the same thing
        :param results: *optional* engine recognition results object
        :type results: :ref:`engine-specific type<RefGrammarCallbackResultsTypes>`
        """
        LOGGER.info(f"words: {words}")
        # LOGGER.info(f"rule: {rule}")
        # LOGGER.info(f"node: {node}")
        LOGGER.info(f"result: {results.getResults(0)}")

        # Don't forward dictation for commands, as we want the actual output produced by the command,
        # which is captured in dragon_listener.py
        results = results.getResults(0)
        if rule or node or results[0][1] != 0:
            LOGGER.info(f"Not forwarding dictation for rule {rule}: {results}")
            return

        formatted = format_dictation_dns11(words)
        LOGGER.info(f"format_dns_11: {formatted}")
        for character in formatted:
            arduino_commands = bytes(character, 'ascii') + TYPE + b"\x00"
            LOGGER.debug(f"Sending command: {arduino_commands}")
            arduino.environment.connection.send(arduino_commands)


if USE_ARDUINO:
    Observer().register()


# observer = Observer()
# observer.register()
# test = ElementTester(Literal("hello world"))
# test.recognize("hello world")
# test.recognize("hello universe")
# observer.unregister()
