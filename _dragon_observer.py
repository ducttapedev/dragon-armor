import logging

from dragonfly import RecognitionObserver
from dragonfly.engines.backend_natlink.dictation_format import WordFormatter, WordParserDns11

from arduino.environment import USE_ARDUINO
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

    def on_begin(self):
        """
        Method called when the observer is registered and speech start is
        detected.
        """
        LOGGER.info("Begin recognition")

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
        # for x in [words, rule, node]:
        #     print("on_recognition: " + str(repr(x)))
        recognition_list = results.getResults(0)
        dictation_words = [
            word.split("\\")[0]
            for word, recognition_type in recognition_list
            if recognition_type == 0
        ]
        dictation_words_raw = [
            word
            for word, recognition_type in recognition_list
            # if recognition_type == 0
        ]
        LOGGER.info(f"On recognition: {recognition_list}")
        LOGGER.info(f"dictation_words: {dictation_words}")
        combined_format = format_dictation_dns11(dictation_words_raw)
        LOGGER.info(f"format_dns_11 combined: {combined_format}")
        # for word in dictation_words:
        #     LOGGER.info(f"format_dns_11: {format_dictation_dns11(word)}")

    # for letter in " ".join(dictation_words):
        #     LOGGER.info(f"Writing to arduino: {letter} + {TYPE} + (null char)")
            # ARDUINO.write(letter + TYPE + "\x00")

    def on_failure(self, results):
        """
        Method called when speech failed to decode to a grammar rule or to
        dictation.

        :param results: *optional* engine recognition results object
        :type results: :ref:`engine-specific type<RefGrammarCallbackResultsTypes>`
        """
        LOGGER.error("Failure: " + str(repr(results.getResults(0))))

    def on_end(self, results):
        """
        Method called when speech ends, either with a successful
        recognition (after ``on_recognition``) or in failure (after
        ``on_failure``).

        :param results: *optional* engine recognition results object
        :type results: :ref:`engine-specific type<RefGrammarCallbackResultsTypes>`
        """
        LOGGER.info("End: " + str(repr(results.getResults(0))))

    def on_post_recognition(self, words, rule, node, results):
        """
        Method called when speech successfully decoded to a grammar rule or
        to dictation.

        This is called *after* grammar rule processing (i.e.
        ``Rule.process_recognition()``).

        :param words: recognized words
        :type words: tuple
        :param rule: *optional* recognized rule
        :type rule: Rule
        :param node: *optional* parse tree node
        :type node: Node
        :param results: *optional* engine recognition results object
        :type results: :ref:`engine-specific type<RefGrammarCallbackResultsTypes>`
        """
        for x in [words, rule, node]:
            LOGGER.info("on_post_recognition: " + str(repr(x)))
        LOGGER.info("on_post_recognition: " + str(repr(results.getResults(0))))


if USE_ARDUINO:
    Observer().register()