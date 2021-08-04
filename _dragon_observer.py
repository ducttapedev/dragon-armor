from dragonfly import RecognitionObserver
from arduino_serial import ARDUINO, USE_ARDUINO, TYPE


class Observer(RecognitionObserver):
    def __init__(self):
        super(Observer, self).__init__()

    def on_begin(self):
        """
        Method called when the observer is registered and speech start is
        detected.
        """
        print("Begin recognition")

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
        :type node: Node
        :param results: *optional* engine recognition results object
        :type results: :ref:`engine-specific type<RefGrammarCallbackResultsTypes>`
        """
        # for x in [words, rule, node]:
        #     print("on_recognition: " + str(repr(x)))
        recognition_list = results.getResults(0)
        dictation_words = [word for word, recognition_type in recognition_list if recognition_type == 0]
        for letter in " ".join(dictation_words):
            ARDUINO.write(letter + TYPE + "\x00")

    def on_failure(self, results):
        """
        Method called when speech failed to decode to a grammar rule or to
        dictation.

        :param results: *optional* engine recognition results object
        :type results: :ref:`engine-specific type<RefGrammarCallbackResultsTypes>`
        """
        print("Failure: " + str(repr(results.getResults(0))))

    def on_end(self, results):
        """
        Method called when speech ends, either with a successful
        recognition (after ``on_recognition``) or in failure (after
        ``on_failure``).

        :param results: *optional* engine recognition results object
        :type results: :ref:`engine-specific type<RefGrammarCallbackResultsTypes>`
        """
        print("End: " + str(repr(results.getResults(0))))

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
        # for x in [words, rule, node]:
        #     print("on_post_recognition: " + str(repr(x)))
        # print("on_post_recognition: " + str(repr(results.getResults(0))))


if USE_ARDUINO:
    Observer().register()
