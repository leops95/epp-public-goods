
from otree.api import *
c = cu

doc = '\nThis is a one-period public goods game with 4 players per group.\n'
class Constants(BaseConstants):
    name_in_url = 'public_goods_4'
    players_per_group = 4
    num_rounds = 10
    endowment = cu(20)
    multiplier = 2
    admin_report_template = 'public_goods_4/admin_report.html'
    instructions_template = 'public_goods_4/instructions.html'
def vars_for_admin_report(subsession):
    session = subsession.session
    contributions = [p.contribution for p in subsession.get_players() if p.contribution != None]
    if contributions:
        return dict(
            avg_contribution=sum(contributions) / len(contributions),
            min_contribution=min(contributions),
            max_contribution=max(contributions),
        )
    else:
        return dict(
            avg_contribution='(no data)',
            min_contribution='(no data)',
            max_contribution='(no data)',
        )
class Subsession(BaseSubsession):
    pass
def set_payoffs(group):
    group.total_contribution = sum([p.contribution for p in group.get_players()])
    group.individual_share = (
        group.total_contribution * Constants.multiplier / Constants.players_per_group
    )
    for p in group.get_players():
        p.payoff = (Constants.endowment - p.contribution) + group.individual_share
class Group(BaseGroup):
    total_contribution = models.CurrencyField()
    individual_share = models.CurrencyField()
class Player(BasePlayer):
    contribution = models.CurrencyField(doc='The amount contributed by the player', label='How much will you contribute to the project from 0 to 20', max=Constants.endowment, min=0)
class Introduction(Page):
    form_model = 'player'
class Contribute(Page):
    form_model = 'player'
    form_fields = ['contribution']
class ResultsWaitPage(WaitPage):
    after_all_players_arrive = 'set_payoffs'
    body_text = 'Waiting for other participants to contribute.'
class Results(Page):
    form_model = 'player'
    @staticmethod
    def vars_for_template(player):
        group = player.group
        return dict(total_earnings=group.total_contribution * Constants.multiplier)
page_sequence = [Introduction, Contribute, ResultsWaitPage, Results]