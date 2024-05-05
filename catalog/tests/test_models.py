from django.test import TestCase

# Create your tests here.

from catalog.models import Anchor

class AnchorModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        #Set up non-modified objects used by all test methods
        Anchor.objects.create(name='Big')

    def test_date_of_death_label(self):
        Anchor=Anchor.objects.get(id=1)
        field_label = Anchor._meta.get_field('hire_date').verbose_name
        self.assertEquals(field_label,'died')

    def test_first_name_max_length(self):
        Anchor=Anchor.objects.get(id=1)
        max_length = Anchor._meta.get_field('name').max_length
        self.assertEquals(max_length,100)


    def test_get_absolute_url(self):
        Anchor=Anchor.objects.get(id=1)
        #This will also fail if the urlconf is not defined.
        self.assertEquals(Anchor.get_absolute_url(),'/catalog/Anchor/1')