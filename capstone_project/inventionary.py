import inquirer
import sys
import logging


class Inventionary:
    """
    Entrypoint for the prompts that go into ChatGPT

    Because we want to reduce costs, we need to ensure both requests and responses are as concise as they can be.
    To accomplish this, we validate user input to be limited to specific character lengths, request the responses
    to be short, and ensure that the formulated prompt that goes into ChatGPT is concise.
    """

    def __init__(self, bot):
        """
        Constructor of the Inventionary class

        Args:
        - bot (object): The ChatGPT bot
        """
        self._messages = []
        self._bot = bot

    def __setup(self):
        """

        """
        # Print welcome and instructions message for the user
        self.__user_welcome()

        # DEFINE THE TYPE OF NAME TO GENERATE
        # Prompt the user whether he or she wants to name a product, service or company
        type_question = [
            inquirer.List(name="type", message="What do you want to name?", choices=["Product", "Service", "Company"]),
        ]
        # Store the type as we need to use it in some of the upcoming user questions
        name_type = inquirer.prompt(type_question)['type'].lower()

        # DEFINE OTHER IMPORTANT ASPECTS THAT WILL INFLUENCE THE NAMES TO BE PROPOSED
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

        # USER QUESTIONS
        questions = [
            inquirer.Text(name="purpose", message="What is the core purpose of your {type}?".format(type=name_type),
                          validate=lambda q_answers, current: 0 < len(current) < 150),
            inquirer.Text(name="distinct",
                          message="What sets your {type} apart from competitors?".format(type=name_type),
                          validate=lambda q_answers, current: 0 < len(current) < 150),
            inquirer.Text(name="target",
                          message="Describe your target audience (demographics, interests, behaviours, location, "
                                  "culture)?",
                          validate=lambda q_answers, current: 0 < len(current) < 200),
            inquirer.Checkbox(name="personality",
                              message="Choose up to 5 words that describe the personality of your {type}"
                              .format(type=name_type),
                              choices=personality_choices,
                              validate=lambda q_answers, current: 0 < len(current) <= 5),
            inquirer.Checkbox(name="emotions",
                              message="Choose up to 5 emotions that your {type} evokes"
                              .format(type=name_type),
                              choices=emotion_choices,
                              validate=lambda q_answers, current: 0 < len(current) <= 5),
            inquirer.List(name="length", message="How long do you want the name to be?",
                          choices=["Short (1-5 characters)", "Medium (6-10 characters)", "Long (11+ characters)"]),
            inquirer.Text(name="include", message="Are there any words or themes to include? (Optional)",
                          validate=lambda q_answers, current: 0 <= len(current) < 70),  # Nullable
            inquirer.Text(name="avoid", message="Are there any words or themes to avoid? (Optional)",
                          validate=lambda q_answers, current: 0 <= len(current) < 70),  # Nullable
        ]
        
        # Store answers
        answers = inquirer.prompt(questions)
        # Build the ChatGPT with the answers
        self.__initial_prompt(answers, name_type)

    def __initial_prompt(self, answers, name_type):
        """
        Builds the main ChatGPT instructions using the user answers.
        """
        # Validate that the user has already answered
        if answers is not None and name_type is not None:

            # PROMPTS: The main sentences of the main ChatGPT instruction prompt
            type_and_task_prompt = "Propose 3 names for a {type} as a markdown enumerated list. Consider: \n"
            purpose_prompt = "- This is the core purpose of the {type}: {purpose}.\n"
            distinct_prompt = "- This is what sets apart the {type} from competitors: {different}.\n"
            length_prompt = "- The length of the name shall be {length}.\n"
            target_prompt = "- The target market is: {target}.\n"
            personality_prompt = "- The personality of the {type} is: {personality}.\n"
            emotions_prompt = "- The emotions that the {type} evokes are: {emotions}.\n"
            include_prompt = "- Include the following words or themes: {include}.\n"
            avoid_prompt = "- Avoid the following words or themes: {avoid}.\n"

            # Helper variables
            avoid = answers["avoid"]
            include = answers["include"]

            # The ChatGPT prompt
            prompt = (
                    type_and_task_prompt.format(type=name_type)
                    + purpose_prompt.format(type=name_type, purpose=answers["purpose"])
                    + distinct_prompt.format(type=name_type, different=answers["distinct"])
                    + length_prompt.format(length=answers["length"])
                    + target_prompt.format(target=answers["target"])
                    + personality_prompt.format(type=name_type, personality=", ".join(answers["personality"]))
                    + emotions_prompt.format(type=name_type, emotions=", ".join(answers["emotions"]))
                    + (avoid_prompt.format(type=name_type, avoid=answers["avoid"]) if avoid != "" else "")
                    + (include_prompt.format(type=name_type,
                                             include=answers["include"]) if include != "" else "")
            )

            # Initial ChatGPT prompt.
            # System Prompt
            self._messages.append({"role": "system", "content": "You are a skilled marketing expert"})
            # User Prompt
            self._messages.append({"role": "user", "content": prompt})

    def start(self):
        """
        Starts the inventionary process.
        1. Call __setup() to ask the user the questions and prepare the ChatGPT prompt
        2. Send the request and wait for the response
        3. Ask the user if he would like other answers
        4. If so, we prepare the _messages to send a new prompt and process the response.
           Otherwise, we terminate the program.

        We allow the user to repeat steps 3 and 4 three times.
        """
        if len(self._messages) == 0:
            # Initial setup : ask questions to user and build ChatGPT prompt
            self.__setup()
            # _messages should now be populated
            logging.debug(self._messages)
        else:
            # Close connection and say goodbye
            self._bot.close_client()
            print("Hope you liked the inventionary! See ya!")
            sys.exit()

        # Send request to ChatGPT
        print("\nProcessing...")
        response = self._bot.request_openai(self._messages)
        # Process response and add answer to _messages
        self.__process_response(response)

        for x in range(3):
            # Ask whether user wants to get other name options
            retry_question = inquirer.Confirm(name="retry", message="Would you like to request other name options?",
                                              default=False)
            retry = inquirer.prompt([retry_question])

            if retry['retry']:
                # User wants to retry. Adding a new context-aware request to ChatGPT
                self._messages.append({"role": "user", "content": "Propose other 3 names"})
                logging.debug(self._messages)

                # Sending request to ChatGPT
                print("\nProcessing...")
                response = self._bot.request_openai(self._messages)
                # Process response and add answer to _messages
                self.__process_response(response)
            else:
                # User does not want to retry. Close connection and say goodbye
                self._bot.close_client()
                print("Hope you liked the inventionary! See ya!")
                sys.exit()

    def __process_response(self, response):
        """
        Processes the ChatGPT response: parses the returned JSON to get the message content and
        also appends the answer to the self._messages property which carries the history of user prompts and
        assistant answers.

        Args:
        - response (object): The API response to the chat completion request
        """
        logging.debug(response)

        # Extract the answer from the API call response
        answer = response.choices[0].message.content

        # Print the answer for the user
        print("\nProposition:")
        print("-----------")
        print(answer)
        print("-----------")

        # Append the assistant answer to the _messages attribute which contains the history of prompts and answers
        self._messages.append({"role": "assistant", "content": answer})

    @staticmethod
    def __user_welcome():
        """
        Prints the welcome message to the user and provides basic instructions
        """
        print("============")
        print("INVENTIONARY")
        print("============")
        print("Welcome to Inventionary! Looking for names for your business or product? You are in the right place!")
        print("Let's get started! Answer the following questions:")
        print("")
