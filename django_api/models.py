from django.db import models


class Rental(models.Model):
    title = models.CharField(max_length=1024)
    owner = models.CharField(max_length=1024)
    city = models.CharField(max_length=1024)
    type = models.CharField(max_length=1024)
    image = models.CharField(max_length=1024)
    bedrooms = models.CharField(max_length=1024)


class Area(models.Model):
    """
    A climbing area. Contains several crags. A parking or more.
    """
    name = models.CharField(max_length=150, unique=True)

    @property
    def faces(self):
        return len(RockFace.objects.filter(area__exact=self))

    @property
    def routes(self):
        return Route.objects.filter(rock_face__exact=RockFace.objects.filter(area__exact=self)).count()

   # @property
   # def position(self):
   #     faces = RockFace.objects.filter(area__exact=self)
   #     lat = 0
   #     lon = 0
   #     n = 0
   #     for face in faces:
   #         lat += face.position.latitude
   #         lon += face.position.longitude
   #         n += 1
   #     if n != 0:
   #         lat /= n
   #         lon /= n
   #     return lat, lon

    def __str__(self):
        return self.name


class RockFace(models.Model):
    """
    A rockface holds a set of routes. One area can have several Rockfaces.
    """
    name = models.CharField(max_length=150)
    area = models.ForeignKey(Area, related_name="rockfaces")
    #position = GeopositionField()

    @property
    def routes(self):
        return len(Route.objects.filter(rock_face__exact=self))

    def __str__(self):
        return self.name


class Parking(models.Model):
    area = models.ForeignKey(Area, related_name="parking")
    position = models.PositiveIntegerField(default=5)  # TODO: Implement a soultion.


class Route(models.Model):
    """
    A route belongs to a rockface.
    """
    name = models.CharField(max_length=150)
    rock_face = models.ForeignKey(RockFace, related_name="routes")

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
    grade = models.CharField(max_length=3,
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
    type = models.CharField(max_length=2,
                            choices=TYPE_CHOICES,
                            default=TYPE_SPORT,
                            blank=False)

    #routeline = models.CharField(max_length=300, default="[]", null=True, blank=True)

    def __str__(self):
        return self.name + ' (' + self.rock_face.area.name + ')'