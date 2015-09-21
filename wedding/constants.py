LANGUAGES = (
    ('en', 'English'),
    ('es', 'Spanish'),
)

NO_RSVP = 'no_rsvp'
CONFIRMED = 'confirmed'
DECLINED = 'declined'
REJECTED = 'rejected'

INVITATION_STATUSES = (
    (NO_RSVP, 'No RSVP'),
    (CONFIRMED, 'Confirmed'),
    (DECLINED, 'Declined'),
    (REJECTED, 'Rejected'),
)

INVITATION_STATUSES_DICT = {
    NO_RSVP: 'No RSVP',
    CONFIRMED: 'Confirmed',
    DECLINED: 'Declined',
    REJECTED: 'Rejected',
}

INVITER_CHOICES = (
    ('both', 'Both'),
    ('javi', 'Javi'),
    ('magda', 'Magda'),
)
