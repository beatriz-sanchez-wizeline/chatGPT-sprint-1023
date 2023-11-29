import inquirer


class Inventionary:

    system_prompt = "You are a skilled marketing expert"

    def __init__(self):
        self.answers = None

    def setup(self):
        print("============")
        print("INVENTIONARY")
        print("============")
        print("Welcome to Inventionary! Looking for names for your business or product? You are in the right place!")
        print("Let's get started! Answer the following questions:")
        print("")

        questions = [
            inquirer.Text(name="purpose", message="What is the core purpose of your business?"),
            inquirer.List(name="type", message="What do you want to name?", choices=["Product", "Service", "Company"]),
            inquirer.Text(name="distinct", message="What sets your brand apart from competitors?"),
        ]
        self.answers = inquirer.prompt(questions)
        return self.user_prompt()

    def user_prompt(self):
        # PROMPTS
        type_and_task_prompt = "Propose 3 names for a {type}. \n"
        purpose_prompt = "The core purpose of this {type} is to: {purpose}.\n"

        # ANSWER VARIABLES
        name_type = self.answers["type"].lower()

        return (
                type_and_task_prompt.format(type=name_type)
                + purpose_prompt.format(type=name_type, purpose=self.answers["purpose"])
        )