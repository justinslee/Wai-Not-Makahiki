from django import template

register = template.Library()

def user_tickets(raffle_prize, user):
  return raffle_prize.allocated_tickets(user)
  
def user_odds(raffle_prize, user):
  total_tickets = raffle_prize.allocated_tickets()
  if total_tickets == 0:
    return "0%"
    
  user_tickets = raffle_prize.allocated_tickets(user)
  odds = (float(user_tickets) * 100.0 ) / float(total_tickets)
  return "%0.1f%%" % (odds,)

register.filter("user_tickets", user_tickets)
register.filter("user_odds", user_odds)

# Borrowed from http://djangosnippets.org/snippets/552/
import locale
locale.setlocale(locale.LC_ALL, 'en_US') 
 
@register.filter()
def currency(value):
  return locale.currency(value, grouping=True)