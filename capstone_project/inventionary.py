import inquirer
import sys
import logging


class Inventionary:
    """
    Entrypoint for the prompts that go into ChatGPT

    Because we want to reduce costs, we need to ensure both requests and responses are as concise as they can be.
    To accomplish this, we validate user input to be limited to specific character lengths, request the responses
    to be short (i.e. a comma separated list), and ensure that the formulated prompt that goes into ChatGPT is concise.
    """

    def __init__(self, bot):
        self._answers = None
        self._type = None
        self._messages = []
        self._bot = bot
        # logging.basicConfig(level=logging.DEBUG)

    def __setup(self):
        self.__user_welcome()

        # DEFINE THE TYPE OF NAME
        type_question = [
            inquirer.List(name="type", message="What do you want to name?", choices=["Product", "Service", "Company"]),
        ]
        self._type = inquirer.prompt(type_question)['type'].lower()

        # DEFINE OTHER IMPORTANT ASPECTS
        personality_choices = ["adaptable", "adorable", "agreeable", "alert", "alluring", "ambitious",
                               "boundless", "brave", "bright", "calm", "capable", "charming", "cheerful",
                               "coherent", "confident", "cooperative", "courageous", "credible", "cultured",
                               "dashing", "dazzling", "debonair", "decisive", "decorous", "delightful",
                               "determined", "diligent", "discreet", "dynamic", "eager", "efficient",
                               "enchanting", "encouraging", "enduring", "energetic", "entertaining",
                               "enthusiastic", "excellent", "excitable", "exuberant", "fabulous", "fair",
                               "faithful", "fantastic", "fearless", "frank", "friendly", "funny", "generous",
                               "gentle", "good", "happy", "harmonious", "helpful", "hilarious", "honorable",
                               "impartial", "industrious", "instinctive", "innovative", "jolly", "joyous",
                               "knowledgeable", "likable", "lively", "lovely", "loving", "lucky", "mature",
                               "modern", "nice", "obedient", "painstaking", "peaceful", "perfect", "placid",
                               "plausible", "pleasant", "plucky", "productive", "protective", "proud",
                               "punctual", "quiet", "receptive", "reflective", "relieved", "resolute",
                               "responsible", "righteous", "romantic", "sedate", "selective", "self-assured",
                               "sensitive", "shrewd", "silly", "sincere", "skillful", "splendid", "steadfast",
                               "stimulating", "talented", "thoughtful", "thrifty", "tough", "trustworthy",
                               "unbiased", "unusual", "upbeat", "vigorous", "vivacious", "warm", "willing",
                               "wise", "witty", "wonderful", "zany", "zealous", "kind-hearted", "amusing",
                               "professional", "kind"]
        emotion_choices = ["admiration", "adoration", "aesthetic appreciation", "amusement", "anger", "anxiety", "awe",
                           "awkwardness", "boredom", "calmness", "confusion", "craving", "disgust", "empathic pain",
                           "entrancement", "excitement", "fear", "horror", "interest", "joy", "nostalgia", "relief",
                           "romance", "sadness", "satisfaction", "sexual desire", "surprise"]

        personality_choices.sort()
        emotion_choices.sort()

        questions = [
            inquirer.Text(name="purpose", message="What is the core purpose of your {type}?".format(type=self._type),
                          validate=lambda answers, current: 0 < len(current) < 150),
            inquirer.Text(name="distinct",
                          message="What sets your {type} apart from competitors?".format(type=self._type),
                          validate=lambda answers, current: 0 < len(current) < 150),
            inquirer.Text(name="target",
                          message="Describe your target audience (demographics, interests, behaviours, location, "
                                  "culture)?",
                          validate=lambda answers, current: 0 < len(current) < 200),
            inquirer.Checkbox(name="personality",
                              message="Choose up to 5 words that describe the personality of your {type}"
                              .format(type=self._type),
                              choices=personality_choices,
                              validate=lambda answers, current: 0 < len(current) <= 5),
            inquirer.Checkbox(name="emotions",
                              message="Choose up to 5 emotions that your {type} evokes"
                              .format(type=self._type),
                              choices=emotion_choices,
                              validate=lambda answers, current: 0 < len(current) <= 5),
            inquirer.List(name="length", message="How long do you want the name to be?",
                          choices=["Short (1-5 characters)", "Medium (6-10 characters)", "Long (11+ characters)"]),
            inquirer.Text(name="include", message="Are there any words or themes to include?",
                          validate=lambda answers, current: 0 <= len(current) < 70),  # Nullable
            inquirer.Text(name="avoid", message="Are there any words or themes to avoid?",
                          validate=lambda answers, current: 0 <= len(current) < 70),  # Nullable
        ]
        self._answers = inquirer.prompt(questions)
        return self.__initial_prompt()

    def __initial_prompt(self):
        if self._answers is not None and self._type is not None:

            # PROMPTS
            type_and_task_prompt = "Propose 3 names for a {type} as a markdown enumerated list. Consider: \n"
            purpose_prompt = "- This is the core purpose of the {type}: {purpose}.\n"
            distinct_prompt = "- This is what sets apart the {type} from competitors: {different}.\n"
            length_prompt = "- The length of the name shall be {length}.\n"
            target_prompt = "- The target market is: {target}.\n"
            personality_prompt = "- The personality of the {type} is: {personality}.\n"
            emotions_prompt = "- The emotions that the {type} evokes are: {emotions}.\n"
            include_prompt = "- Include the following words or themes: {include}.\n"
            avoid_prompt = "- Avoid the following words or themes: {avoid}.\n"

            # Variables
            avoid = self._answers["avoid"]
            include = self._answers["include"]

            prompt = (
                    type_and_task_prompt.format(type=self._type)
                    + purpose_prompt.format(type=self._type, purpose=self._answers["purpose"])
                    + distinct_prompt.format(type=self._type, different=self._answers["distinct"])
                    + length_prompt.format(length=self._answers["length"])
                    + target_prompt.format(target=self._answers["target"])
                    + personality_prompt.format(type=self._type, personality=", ".join(self._answers["personality"]))
                    + emotions_prompt.format(type=self._type, emotions=", ".join(self._answers["emotions"]))
                    + (avoid_prompt.format(type=self._type, avoid=self._answers["avoid"]) if avoid != "" else "")
                    + (include_prompt.format(type=self._type,
                                             include=self._answers["include"]) if include != "" else "")
            )

            self._messages.append({"role": "system", "content": "You are a skilled marketing expert"})
            self._messages.append({"role": "user", "content": prompt})

            return prompt

    def start(self):
        if len(self._messages) == 0:
            logging.debug("No messages")
            self.__setup()  # Setup and prompt the user for details
        else:
            self._bot.close_client()
            print("Hope you liked the inventionary! See ya!")
            sys.exit()

        logging.debug(self._messages)
        response = self._bot.request_openai(self._messages)
        self.__process_response(response)

        for x in range(3):
            retry_question = inquirer.Confirm(name="retry", message="Would you like to request other name options?",
                                              default=False)
            retry = inquirer.prompt([retry_question])
            logging.debug("Retry: {retry}".format(retry="True" if retry['retry'] else "False"))
            if retry['retry']:
                self._messages.append({"role": "user", "content": "Propose other 3 names"})

                logging.debug(self._messages)
                response = self._bot.request_openai(self._messages)
                self.__process_response(response)
            else:
                self._bot.close_client()
                print("Hope you liked the inventionary! See ya!")
                sys.exit()

    def __process_response(self, response):
        logging.debug(response)

        answer = response.choices[0].message.content

        print("\nProposition:")
        print("-----------")
        print(answer)
        print("")  # line break

        self._messages.append({"role": "assistant", "content": answer})

        return answer

    @staticmethod
    def __user_welcome():
        print("============")
        print("INVENTIONARY")
        print("============")
        print("Welcome to Inventionary! Looking for names for your business or product? You are in the right place!")
        print("Let's get started! Answer the following questions:")
        print("")
        