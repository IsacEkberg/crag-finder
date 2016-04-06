from django.db import models
from django.contrib.auth.models import User


class Area(models.Model):
    """
    A climbing area. Contains several crags. A parking or more.
    """
    name = models.CharField(verbose_name="namn", max_length=150, unique=True)
    short_description = models.CharField(verbose_name="kort beskrivning", max_length=300, null=True, blank=False)
    long_description = models.CharField(verbose_name="lång beskrivning",max_length=4000, null=True, blank=False)
    road_description = models.CharField(verbose_name="väg beskrivning",max_length=4000, null=True, blank=False)
    clubs = models.ManyToManyField('Club', verbose_name="ansvarig klubb/klubbar", blank=False)

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
    geo_data = models.CharField(verbose_name="plats för klippan", max_length=3000, blank=False, null=True)

    short_description = models.CharField(verbose_name="kort beskrivning", max_length=300, null=True, blank=True)
    long_description = models.CharField(verbose_name="lång beskrivning", max_length=4000, null=True, blank=True)

    class Meta:
        verbose_name = 'klippa'
        verbose_name_plural = 'klippor'

    @property
    def routes(self):
        return len(Route.objects.filter(rock_face__exact=self))

    def __str__(self):
        return self.name


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
    name = models.CharField(verbose_name="namn", max_length=150)
    rock_face = models.ForeignKey(RockFace, verbose_name="klippa", related_name="routes")
    short_description = models.CharField(verbose_name="kort beskrivning", max_length=160, blank=True, null=True)
    first_ascent_name = models.CharField(verbose_name="första bestigarens namn", max_length=160, blank=True, null=True)
    first_ascent_year = models.PositiveIntegerField(verbose_name="år för första bestigning", blank=True, null=True)
    length = models.PositiveIntegerField(verbose_name="längd", blank=True, null=True)

    #Grade constans
    PROJECT = 'no'
    FOUR_A = '4a'
    FOUR_B = '4b'
    FOUR_C = '4c'
    FIVE_A = '5a'
    FIVE_B = '5b'
    FIVE_C = '5c'

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
        (FOUR_A, '4a'),
        (FOUR_B, '4b'),
        (FOUR_C, '4c'),
        (FIVE_A, '5a'),
        (FIVE_B, '5b'),
        (FIVE_C, '5c'),
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


class Club(models.Model):
    name = models.CharField(verbose_name="namn", max_length=255)
    address = models.TextField(verbose_name="adress")
    email = models.EmailField(verbose_name="epost",)
    info = models.TextField(verbose_name="Information om klubben",)

    class Meta:
        verbose_name = 'klubb'
        verbose_name_plural = 'klubbar'

    def __str__(self):
        return self.name


class ClubAdmin(models.Model):
    club = models.ForeignKey(Club, verbose_name="klubb")
    user = models.ForeignKey(User, verbose_name="användare")

    class Meta:
        verbose_name = 'klubbadministratör'
        verbose_name_plural = 'klubbadministratörer'

    def __str__(self):
        return str(self.user)
