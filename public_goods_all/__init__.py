
from otree.api import *
c = cu

doc = '\nThis is a one-period public goods game with all players in the same group.\n'
class Constants(BaseConstants):
    name_in_url = 'public_goods_all'
    players_per_group = None
    num_rounds = 10
    endowment = cu(20)
    multiplier = 2
    admin_report_template = 'public_goods_all/admin_report.html'
    instructions_template = 'public_goods_all/instructions.html'

def vars_for_admin_report(subsession):
    avg_contribs_all = []
    max_contribs_all = []
    min_contribs_all = []
    rounds = subsession.in_all_rounds()

    for i in range(0, Constants.num_rounds, 1):
        round_i = rounds[i]
        contributions = [p.contribution for p in round_i.get_players() if p.contribution != None]
        mean_contribution = (float(sum(contributions))) / len(contributions)
        max_contribution = int(max(contributions))
        min_contribution = int(min(contributions))
        avg_contribs_all.append(mean_contribution)
        max_contribs_all.append(max_contribution)
        min_contribs_all.append(min_contribution)

    return dict(
        avg_contribs = avg_contribs_all,
        max_contribs = max_contribs_all,
        min_contribs = min_contribs_all,
        )

class Subsession(BaseSubsession):
    pass
def set_payoffs(group):
    group.total_contribution = sum([p.contribution for p in group.get_players()])
    group.individual_share = (
        group.total_contribution * Constants.multiplier / len(group.get_players())
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

page_sequence = [Contribute, ResultsWaitPage, Results]
