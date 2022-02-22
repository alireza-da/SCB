class User:
    # Instantiate an Object
    def __init__(self, username, social_credit, level, discord_id):
        self.username = username
        self.social_credit = social_credit
        self.level = level
        self.id = discord_id

    def increase_social_credit(self, amount):
        self.social_credit += amount

    def decrease_social_credit(self, amount):
        self.social_credit -= amount

    @staticmethod
    def user_decoder(obj):
        return User(obj['username'], obj['social_credit'], obj['level'], obj['id'])

    @staticmethod
    def user_decoder_static(query_res):
        return User(query_res[0], query_res[1], query_res[3], query_res[2])


class Admin(User):
    @staticmethod
    def reduce(user, amount):
        user.decrease_social_credit(amount)

    @staticmethod
    def increase(user, amount):
        user.increase_social_credit(amount)
