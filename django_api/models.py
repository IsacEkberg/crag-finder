import os

from django.core.validators import RegexValidator
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.utils import timezone
from pagedown.widgets import AdminPagedownWidget
from reversion import revisions as reversion
from django.db import models
from django.contrib.auth.models import User
from django.utils.dateformat import format as date_format
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

def _image_file_path(instance, filename):
    """Returns the subfolder in which to upload images for articles. This results in media/article/img/<filename>"""
    return os.path.join(
        'images', "{:}_{:}".format(date_format(timezone.now(), 'U'), filename)
    )

# These two doesn't show on the site
BEING_REVIEWED_CHANGE = 'c'
BEING_REVIEWED_NEW = 'n'

# These two does show up on the site
BEING_REVIEWED_DELETE = 'd'
APPROVED = 'a'

STATUSES = (
    (BEING_REVIEWED_CHANGE, "Ändring som väntar på godkännande"),
    (BEING_REVIEWED_NEW, "Ny som väntar på godkännande"),
    (BEING_REVIEWED_DELETE, "Väntar på att bli borttagen"),
    (APPROVED, "Godkänt")
)

class MarkDownTextField(models.TextField):
    widget = AdminPagedownWidget


class MarkDownCharField(models.CharField):
    widget = AdminPagedownWidget


class AreaImage(models.Model):
    image = models.ImageField(
        upload_to=_image_file_path,
        null=False,
        blank=False,
        verbose_name="bild", )

    area = models.ForeignKey('Area', related_name="image")

    status = models.CharField(
        max_length=1,
        choices=STATUSES,
        default=APPROVED,
        blank=False,
        null=False)

    class Meta:
        verbose_name = 'områdes bild'
        verbose_name_plural = 'områdes bild'  # limited to 1 image in admin page.

    def __str__(self):
        return os.path.basename(self.image.name)


class RockFaceImage(models.Model):
    image = models.ImageField(
        upload_to=_image_file_path,
        null=False,
        blank=False,
        verbose_name="bild", )
    rockface = models.ForeignKey('RockFace', related_name="image")
    name = models.CharField(verbose_name="namn", max_length=255, null=True, blank=False)
    description = models.TextField(verbose_name="kort beskrivning av bilden", null=True, blank=True)

    status = models.CharField(
        max_length=1,
        choices=STATUSES,
        default=APPROVED,
        blank=False,
        null=False)

    class Meta:
        verbose_name = 'bild på klippan'
        verbose_name_plural = 'bilder på klippan'

    def __str__(self):
        try:
            return "{:}-{:}".format(self.rockface.name, self.name)
        except:
            return "{:}-{:}".format(self.rockface.name,  os.path.basename(self.image.name))


class Area(models.Model):
    """
    A climbing area. Contains several crags. A parking or more.
    """
    name = models.CharField(verbose_name="namn", max_length=150)
    short_description = models.CharField(verbose_name="kort beskrivning", max_length=300, null=True, blank=False)
    long_description = MarkDownTextField(verbose_name="lång beskrivning", max_length=4000, null=True, blank=False)
    road_description = models.CharField(verbose_name="väg beskrivning", max_length=4000, null=True, blank=False)
    clubs = models.ManyToManyField('Club', verbose_name="ansvarig klubb/klubbar", blank=False)
    replacing = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        default=None,
        on_delete=models.SET_NULL)

    status = models.CharField(
        max_length=1,
        choices=STATUSES,
        default=APPROVED,
        blank=False,
        null=False)

    class Meta:
        verbose_name = 'område'
        verbose_name_plural = 'områden'

    @property
    def faces(self):
        return len(RockFace.objects.filter(area__exact=self))

    @property
    def routes(self):
        return Route.objects.filter(rock_face__exact=RockFace.objects.filter(area__exact=self)).count()

    def __str__(self):
        return self.name


class RockFace(models.Model):
    """
    A rockface holds a set of routes. One area can have several Rockfaces.
    """
    name = models.CharField(verbose_name="namn", max_length=150)
    area = models.ForeignKey(Area, verbose_name="område", related_name="rockfaces")
    geo_data = models.CharField(verbose_name="plats för klippan",
                                max_length=3000,
                                blank=False,
                                null=True,
                                validators=[
                                    RegexValidator(
                                        regex=r"^(\(\d{1,3}\.\d+, \d{1,3}\.\d+\);)*$",
                                        message="Geo-data is malformed.",
                                        code="invalid",
                                        ),
                                    ]
                                )

    short_description = models.CharField(verbose_name="kort beskrivning", max_length=300, null=True, blank=True)
    long_description = models.CharField(verbose_name="lång beskrivning", max_length=4000, null=True, blank=True)

    replacing = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        default=None,
        on_delete=models.SET_NULL)

    status = models.CharField(
        max_length=1,
        choices=STATUSES,
        default=APPROVED,
        blank=False,
        null=False)

    class Meta:
        verbose_name = 'klippa'
        verbose_name_plural = 'klippor'

    @property
    def routes(self):
        return len(Route.objects.filter(rock_face__exact=self))

    def __str__(self):
        return self.area.name + " | " + self.name


class Parking(models.Model):
    area = models.ForeignKey(Area, verbose_name="område", related_name="parking")
    position = models.PositiveIntegerField(verbose_name="position", default=5)  # TODO: Implement a solution.

    class Meta:
        verbose_name = 'parkering'
        verbose_name_plural = 'parkeringar'


class Route(models.Model):
    """
    A route belongs to a rockface.
    """
    route_nr = models.CharField(verbose_name="Lednummer", max_length=50, blank=True, null=True)
    name = models.CharField(verbose_name="namn", max_length=150)
    rock_face = models.ForeignKey(RockFace, verbose_name="klippa", related_name="routes")
    short_description = models.CharField(verbose_name="kort beskrivning", max_length=160, blank=True, null=True)
    first_ascent_name = models.CharField(verbose_name="första bestigarens namn", max_length=160, blank=True, null=True)
    first_ascent_year = models.PositiveIntegerField(verbose_name="år för första bestigning", blank=True, null=True)
    length = models.PositiveIntegerField(verbose_name="längd", blank=True, null=True)
    image = models.ForeignKey(RockFaceImage, verbose_name="bild", blank=True, null=True)
    nr_of_bolts = models.PositiveIntegerField(verbose_name="antal bultar", blank=True, null=True)

    replacing = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        default=None,
        on_delete=models.SET_NULL)

    status = models.CharField(
        max_length=1,
        choices=STATUSES,
        default=APPROVED,
        blank=False,
        null=False)

    #Grade constans
    PROJECT = 'no'

    FOUR_A_MINUS = '4a-'
    FOUR_A = '4a'
    FOUR_A_PLUS = '4a+'
    FOUR_B_MINUS = '4b-'
    FOUR_B = '4b'
    FOUR_B_PLUS = '4b+'
    FOUR_C_MINUS = '4c-'
    FOUR_C = '4c'
    FOUR_C_PLUS = '4c+'

    FIVE_A_MINUS = '5a-'
    FIVE_A = '5a'
    FIVE_A_PLUS = '5a+'
    FIVE_B_MINUS = '5b-'
    FIVE_B = '5b'
    FIVE_B_PLUS = '5b+'
    FIVE_C_MINUS = '5c-'
    FIVE_C = '5c'
    FIVE_C_PLUS = '5c+'

    SIX_A_MINUS = '6a-'
    SIX_A = '6a'
    SIX_A_PLUS = '6a+'
    SIX_B_MINUS = '6b-'
    SIX_B = '6b'
    SIX_B_PLUS = '6b+'
    SIX_C_MINUS = '6c-'
    SIX_C = '6c'
    SIX_C_PLUS = '6c+'

    SEVEN_A_MINUS = '7a-'
    SEVEN_A = '7a'
    SEVEN_A_PLUS = '7a+'
    SEVEN_B_MINUS = '7b-'
    SEVEN_B = '7b'
    SEVEN_B_PLUS = '7b+'
    SEVEN_C_MINUS = '7c-'
    SEVEN_C = '7c'
    SEVEN_C_PLUS = '7c+'

    EIGHT_A_MINUS = '8a-'
    EIGHT_A = '8a'
    EIGHT_A_PLUS = '8a+'
    EIGHT_B_MINUS = '8b-'
    EIGHT_B = '8b'
    EIGHT_B_PLUS = '8b+'
    EIGHT_C_MINUS = '8c-'
    EIGHT_C = '8c'
    EIGHT_C_PLUS = '8c+'

    NINE_A_MINUS = '9a-'
    NINE_A = '9a'
    NINE_A_PLUS = '9a+'
    NINE_B_MINUS = '9b-'
    NINE_B = '9b'
    NINE_B_PLUS = '9b+'
    NINE_C_MINUS = '9c-'
    NINE_C = '9c'
    NINE_C_PLUS = '9c+'

    GRADE_CHOICES = (  # fun.
        (PROJECT, 'Ej graderad'),

        (FOUR_A_MINUS, '4a-'),
        (FOUR_A, '4a'),
        (FOUR_A_PLUS, '4a+'),
        (FOUR_B_MINUS, '4b-'),
        (FOUR_B, '4b'),
        (FOUR_B_PLUS, '4b+'),
        (FOUR_C_MINUS, '4c-'),
        (FOUR_C, '4c'),
        (FOUR_C_PLUS, '4c+'),

        (FIVE_A_MINUS, '5a-'),
        (FIVE_A, '5a'),
        (FIVE_A_PLUS, '5a+'),
        (FIVE_B_MINUS, '5b-'),
        (FIVE_B, '5b'),
        (FIVE_B_PLUS, '5b+'),
        (FIVE_C_MINUS, '5c-'),
        (FIVE_C, '5c'),
        (FIVE_C_PLUS, '5c+'),

        (SIX_A_MINUS, '6a-'),
        (SIX_A, '6a'),
        (SIX_A_PLUS, '6a+'),
        (SIX_B_MINUS, '6b-'),
        (SIX_B, '6b'),
        (SIX_B_PLUS, '6b+'),
        (SIX_C_MINUS, '6c-'),
        (SIX_C, '6c'),
        (SIX_C_PLUS, '6c+'),

        (SEVEN_A_MINUS, '7a-'),
        (SEVEN_A, '7a'),
        (SEVEN_A_PLUS, '7a+'),
        (SEVEN_B_MINUS, '7b-'),
        (SEVEN_B, '7b'),
        (SEVEN_B_PLUS, '7b+'),
        (SEVEN_C_MINUS, '7c-'),
        (SEVEN_C, '7c'),
        (SEVEN_C_PLUS, '7c+'),

        (EIGHT_A_MINUS, '8a-'),
        (EIGHT_A, '8a'),
        (EIGHT_A_PLUS, '8a+'),
        (EIGHT_B_MINUS, '8b-'),
        (EIGHT_B, '8b'),
        (EIGHT_B_PLUS, '8b+'),
        (EIGHT_C_MINUS, '8c-'),
        (EIGHT_C, '8c'),
        (EIGHT_C_PLUS, '8c+'),

        (NINE_A_MINUS, '9a-'),
        (NINE_A, '9a'),
        (NINE_A_PLUS, '9a+'),
        (NINE_B_MINUS, '9b-'),
        (NINE_B, '9b'),
        (NINE_B_PLUS, '9b+'),
        (NINE_C_MINUS, '9c-'),
        (NINE_C, '9c'),
        (NINE_C_PLUS, '9c+'),
    )
    grade = models.CharField(verbose_name="gradering",
                             max_length=3,
                             choices=GRADE_CHOICES,
                             default=PROJECT,
                             blank=False)

    TYPE_BOULDER = 'Bo'
    TYPE_SPORT = 'Sp'
    TYPE_TRAD = 'Tr'
    TYPE_AID = 'Ai'
    TYPE_DWS = 'DW'

    TYPE_CHOICES = (
        (TYPE_BOULDER, 'Boulder'),
        (TYPE_SPORT, 'Sport'),
        (TYPE_TRAD, 'Trad'),
        (TYPE_AID, 'Aid'),
        (TYPE_DWS, 'DWS'),
    )
    type = models.CharField(verbose_name="typ",
                            max_length=2,
                            choices=TYPE_CHOICES,
                            default=TYPE_SPORT,
                            blank=False)

    #routeline = models.CharField(max_length=300, default="[]", null=True, blank=True)
    class Meta:
        verbose_name = 'led'
        verbose_name_plural = 'leder'

    def __str__(self):
        return self.name + ' (' + self.rock_face.area.name + ')'

    @property
    def grade_hr(self):
        return [item for item in Route.GRADE_CHOICES if item[0] == self.grade][0][1]

    @property
    def type_hr(self):
        return [item for item in Route.TYPE_CHOICES if item[0] == self.type][0][1]


class Club(models.Model):
    name = models.CharField(verbose_name="namn", max_length=255)
    address = models.TextField(verbose_name="adress")
    email = models.EmailField(verbose_name="epost",)
    info = models.TextField(verbose_name="Information om klubben",)
    replacing = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        default=None,
        on_delete=models.SET_NULL)

    status = models.CharField(
        max_length=1,
        choices=STATUSES,
        default=APPROVED,
        blank=False,
        null=False)

    class Meta:
        verbose_name = 'klubb'
        verbose_name_plural = 'klubbar'

    def __str__(self):
        return self.name


class Change(models.Model):
    user = models.ForeignKey(User, verbose_name="användare")
    description = models.TextField(verbose_name="beskrivning", blank=False, null=True)
    content_type = models.ForeignKey(ContentType, verbose_name="typ", on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    creation_date = models.DateTimeField(verbose_name="datum", auto_created=True, auto_now_add=True)

    class Meta:
        verbose_name = 'ändring'
        verbose_name_plural = 'ändringar'

    def __str__(self):
        return str(self.content_object)

    @property
    def status(self):
        return self.content_object.get_status_display

    @property
    def changed_object_fields(self):
        my_model_fields = self.content_object._meta.get_all_field_names()
        replacing = self.content_object.replacing
        field_list = []
        for f in my_model_fields:
            field_list.append({'field': f,
                               'new': getattr(self.content_object, f, None),
                               'old': getattr(replacing, f, None)})
        return field_list


# Adds field is_trusted to the built in user model.
class CragfinderProfile(models.Model):
    user = models.OneToOneField(User, related_name='cf_profile')
    is_trusted = models.BooleanField(default=False, verbose_name="är betrodd")


class Access(models.Model):
    short_message = models.CharField(null=False, blank=False, verbose_name="kort meddelande", max_length=255)
    long_message = models.TextField(null=True, blank=True, verbose_name="längre version av meddelandet")
    start_date = models.DateField(verbose_name="startdatum", null=True, blank=True)
    stop_date = models.DateField(verbose_name="stoppdatum", null=True, blank=True)
    rock_face = models.ManyToManyField("RockFace", verbose_name="klippa", blank=False, related_name="access")

    class Meta:
        verbose_name = 'accessdata'
        verbose_name_plural = 'accessdata'

    def __str__(self):
        rf = self.rock_face.values('name', 'area__name')
        tmp = ""
        for r in rf:
            tmp += "(" + r['area__name'] + ", " + r['name'] + ") "
        return tmp + " | " + self.short_message


reversion.register(Area, follow=["rockfaces", "parking", "image"])
reversion.register(RockFace, follow=["routes", "image"])
reversion.register(Parking)
reversion.register(Route)
reversion.register(AreaImage)
reversion.register(RockFaceImage)
reversion.register(Club, follow=['area_set'])
