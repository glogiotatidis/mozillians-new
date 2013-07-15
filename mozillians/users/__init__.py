# from mozillians.groups.models import Group, Skill, Language

PRIVILEGED = 1
EMPLOYEES = 2
MOZILLIANS = 3
PUBLIC = 4
PRIVACY_CHOICES = (# (PRIVILEGED, 'Privileged'),
    # (EMPLOYEES, 'Employees'),
    (MOZILLIANS, 'Mozillians'),
    (PUBLIC, 'Public'))
PUBLIC_INDEXABLE_FIELDS = ['full_name', 'ircname', 'email']
DEFAULT_PRIVACY_FIELDS = {
    'photo': None,
    'full_name': '',
    'ircname': '',
    'email': '',
    'website': '',
    'bio': '',
    'city': '',
    'region': '',
    'country': '',
    'groups': None, #Group.objects.none(),
    'skills': None, #Skill.objects.none(),
    'languages': None, #Language.objects.none(),
    'vouched_by': None}
