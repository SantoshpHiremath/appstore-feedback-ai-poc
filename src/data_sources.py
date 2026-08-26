"""
Synthetic app-store review and customer-ticket generator.

Models the shape of real app-store/customer-feedback data: short,
informal, unstructured text with a star rating (reviews) or a subject
line (tickets), covering a mix of genuine pain points, feature
requests, and neutral/positive feedback -- exactly the two data sources
named in the posting ("App-Store-Reviews und Kundentickets").

All review and ticket text below is hand-written and fictional. This
does not reflect any real BSH, Bosch, Siemens, Gaggenau, or Neff app,
product, or customer.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class AppStoreReview(object):
    review_id: str
    star_rating: int  # 1-5
    text: str
    source: str = "App Store"


@dataclass
class CustomerTicket(object):
    ticket_id: str
    subject: str
    text: str
    source: str = "Customer Support"


# Hand-written, fictional review text -- deliberately informal and
# unstructured, the way real app-store reviews actually read: mixed
# capitalization, no consistent structure, sometimes multiple issues in
# one review, sometimes just praise with no actionable content.
_REVIEWS = [
    ("r001", 1, "App keeps crashing every time I try to connect my oven. Useless, please fix!!"),
    ("r002", 2, "Connection to the washing machine drops constantly. Have to re-pair it almost daily."),
    ("r003", 5, "Works great, love being able to check the dishwasher cycle from work."),
    ("r004", 3, "Nice idea but the notifications are way too delayed. By the time it tells me the laundry is done I've already forgotten about it."),
    ("r005", 1, "Setup was a nightmare. QR code scanner never worked, had to enter everything manually."),
    ("r006", 4, "Would be great if I could set a recipe reminder for the oven. Otherwise solid app."),
    ("r007", 2, "Interface is confusing, too many menus to find basic settings."),
    ("r008", 5, "Simple, does what it says. No complaints."),
    ("r009", 1, "Lost connection to my fridge after the last update. Temperature alerts stopped working entirely."),
    ("r010", 3, "Would love a dark mode option, my eyes hurt using this at night."),
    ("r011", 2, "App crashes on startup about once a week. Have to reinstall."),
    ("r012", 4, "Please add support for scheduling multiple appliances at once, that would save so much time."),
    ("r013", 1, "Battery drain is insane since I installed this. Uninstalling."),
    ("r014", 5, "Love the energy usage tracking feature, very helpful."),
    ("r015", 2, "Push notifications for the dryer never arrive on time, sometimes not at all."),
    ("r016", 3, "Works fine most days but occasionally the app just won't load at all."),
    ("r017", 1, "Pairing with a second oven in the household is basically impossible, very frustrating."),
    ("r018", 4, "Wish it supported voice assistant integration, otherwise really useful."),
    ("r019", 2, "Login constantly times out, have to log in again multiple times a day."),
    ("r020", 5, "Been using it for months, works reliably and looks great."),
]

_TICKETS = [
    ("t001", "App won't connect to washer", "I've tried resetting my router and the app still won't find my washing machine. This has been going on for three days now."),
    ("t002", "Feature request: multi-device scheduling", "It would really help if I could schedule the dishwasher and dryer to run at the same off-peak time from one screen."),
    ("t003", "App crash on login", "Every time I open the app it crashes right after I enter my password. Happens on two different phones."),
    ("t004", "Delayed notifications", "The done-cycle notification for my oven usually arrives 15-20 minutes late. Makes the feature almost pointless."),
    ("t005", "Cannot pair second appliance", "I bought a second fridge and the app will only let me connect one at a time. Is this a known limitation?"),
    ("t006", "Positive feedback", "Just wanted to say the energy tracking dashboard is genuinely useful, thanks for building it."),
    ("t007", "QR setup fails", "The QR code scanner during setup never recognizes the code on my dishwasher. Had to call support to finish setup."),
    ("t008", "Feature request: dark mode", "Would appreciate a dark theme option for using the app at night."),
    ("t009", "Battery drain complaint", "My phone's battery life dropped noticeably after installing this app, background usage seems very high."),
    ("t010", "Voice assistant support", "Any plans to add Alexa or Google Assistant integration? Would be a great addition."),
]


def generate_reviews() -> list[AppStoreReview]:
    return [AppStoreReview(review_id=rid, star_rating=stars, text=text) for rid, stars, text in _REVIEWS]


def generate_tickets() -> list[CustomerTicket]:
    return [CustomerTicket(ticket_id=tid, subject=subj, text=text) for tid, subj, text in _TICKETS]
