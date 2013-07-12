import factory

from mozillians.groups.models import Group, GroupAlias, Language, Skill


class GroupFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Group
    name = factory.Sequence(lambda n: 'Group {0}'.format(n))


class LanguageFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Language
    name = factory.Sequence(lambda n: 'Language {0}'.format(n))


class SkillFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Skill
    name = factory.Sequence(lambda n: 'Skill {0}'.format(n))


class GroupAliasFactory(factory.DjangoModelFactory):
    FACTORY_FOR = GroupAlias
    url = factory.Sequence(lambda n: 'alias-{0}'.format(n))
