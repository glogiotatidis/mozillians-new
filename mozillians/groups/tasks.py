from django.db.models import Count

from celery.task import task

from mozillians.groups.models import AUTO_COMPLETE_COUNT, Group, Language, Skill


@task
def assign_autocomplete_to_groups():
    """Set auto_complete to True when member count is larger than
    AUTO_COMPLETE_COUNT.

    Note: no_members includes both vouched and unvouched users ATM. We
    should count only vouched users.

    """
    for model in [Group, Language, Skill]:
        group = (model.objects
                .filter(always_auto_complete=False)
                .annotate(no_members=Count('members'))
                .filter(no_members__gte=AUTO_COMPLETE_COUNT))
        if isinstance(model, Group):
            group = group.filter(system=False)

        model.objects.update(auto_complete=False)
        model.objects.filter(pk=group).update(auto_complete=True)

@task
def remove_empty_groups():
    """Remove empty groups."""
    for model in [Group, Skill]:
        (model.objects
         .annotate(mcount=Count('members')).filter(mcount=0).delete())
