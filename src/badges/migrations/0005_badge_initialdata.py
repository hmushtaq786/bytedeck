# Generated by Django 2.2.12 on 2020-05-09 05:47

from django.db import migrations, transaction
from django.core.exceptions import ObjectDoesNotExist

# NOT RUN 
# Can't use fixtures because load_fixtures method is janky with django-tenant-schemas
def load_initial_data(apps, schema_editor):
    Badge = apps.get_model('badges', 'Badge')
    BadgeType = apps.get_model('badges', 'BadgeType')
    print("AUTOCOMMIT!!!!:", transaction.get_autocommit())
    db_alias = schema_editor.connection.alias
    print(db_alias)
    db_BadgeManager = Badge.objects.using(db_alias)
    db_BadgeTypeManager = BadgeType.objects.using(db_alias)
    # add an initial Talent type badge
    try:
        badge_type = db_BadgeTypeManager.get(name="Talent")  # created in previous data migration
    except ObjectDoesNotExist:
        badge_type = None

    already_had_badges = db_BadgeManager.exists()

    if not already_had_badges:
        db_BadgeManager.create(
            name="ByteDeck Proficiency",
            xp=2,
            short_description="<p>You have demonstrated your proficiency with this online platform. I hope you enjoy using it for this course!</p>",
            badge_type=badge_type,
            sort_order=10,
            active=True
        )

    # now add some Award type badges
    try:
        badge_type = db_BadgeTypeManager.get(name="Award")  # created in previous data migration
    except ObjectDoesNotExist:
        badge_type = None     

    if not already_had_badges:
        db_BadgeManager.bulk_create([
            Badge(
                name="Penny",
                xp=1,
                short_description="<p>According to the Royal Canadian Mint, the official national term of the coin is the <i>one-cent piece</i>, but in practice the terms penny and cent predominate. Originally, \"penny\" referred to a two-cent coin. When the two-cent coin was discontinued, penny took over as the new one-cent coin's name. </p>\r\n\r\n<p>These cents were originally issued to bring some kind of order to the Canadian monetary system, which, until 1858, relied on British coinage, bank and commercial tokens, U.S. currency and Spanish milled dollars. Canada no longer uses the penny, but we still do!</p>",
                badge_type=badge_type,
                icon="icons/badges/Penny_jxri7my.png",
                sort_order=10,
                active=True
            ),
            Badge(
                name="Nickel",
                xp=5,
                short_description="<p>The nickel as we are familiar with it was introduced in 1922, originally made from 99.9% nickel metal. These coins were magnetic, due to the high nickel content. Versions during World War II were minted in copper-zinc, then chrome and nickel-plated steel, and finally returned again to nickel, at the end of the war. A plated steel version was again made 1951–54 during the Korean War. Rising nickel prices eventually caused another switch to cupronickel in 1982 (an alloy similar to the U.S. nickel), but more recently, Canadian nickels are minted in nickel-plated steel, containing a small amount of copper.</p>",
                badge_type=badge_type,
                icon="icons/badges/Nickel_tbGmjLc.png",
                sort_order=20,
                active=True
            ),
            Badge(
                name="Dime",
                xp=10,
                short_description="<p>According to the Royal Canadian Mint, the official national term of the coin is the <i>10 cent piece</i>, but in practice, the term dime predominates in English-speaking Canada. It is nearly identical in size to the American dime, but unlike its counterpart, the Canadian dime is magnetic due to a distinct metal composition: from 1968 to 1999 it was composed entirely of nickel, and since 2000 it has had a high steel content.</p>",
                badge_type=badge_type,
                icon="icons/badges/dime_9kO69sh.png",
                sort_order=30,
                active=True
            ),
        ])


class Migration(migrations.Migration):

    dependencies = [
        ('badges', '0004_badgetype_initialdata'),
    ]

    operations = [
        #migrations.RunPython(load_initial_data),
        # For some reason having this before 0008 was causing error: cannot DROP TABLE "badges_badge" because it has pending trigger events
        # so duplicated in 0009
    ]
