import unittest

from music_ontology.ontology import MusicOntologyProvider
import owlready2 as owl

class OntologyTests(unittest.TestCase):
    def test_create_save_load_produces_same_ontology(self):
        """Test that create, save, load produces the same ontology."""

        sut = MusicOntologyProvider()

        ontology0 = sut.load()
        ontology = sut.create()
        ontology.save()
        ontology2 = sut.load()

        self.assertEqual(ontology, ontology2)
        self.assertEqual(ontology0, ontology2)
        self.assertEqual(ontology0, ontology)

    def test_inverse_properties(self):
        """Test that inverse properties are correctly set."""

        provider = MusicOntologyProvider()
        onto = provider.load()
        limelight = onto.Limelight
        moving_pictures = onto["Moving Pictures"]
        limelight_lyrics = onto["'Limelight' Lyrics"]
        neil = onto["Neil Peart"]
        rush = onto.Rush

        self.assertIn(limelight, moving_pictures.tracks)
        self.assertIn(moving_pictures, limelight.albums)

        self.assertEqual(limelight_lyrics, limelight.lyrics)
        self.assertEqual(limelight, limelight_lyrics.track)

        self.assertIn(neil, limelight_lyrics.written_by)
        self.assertIn(limelight_lyrics, neil.lyrics_written)

        self.assertIn(moving_pictures, rush.discography)
        self.assertEqual(rush, moving_pictures.artist)

    def test_indirect_parents(self):
        """Test that the indirect inheritance relationships are correct."""

        provider = MusicOntologyProvider()
        onto = provider.load()

        rush = onto.Rush

        self.assertIn(onto.Artist, rush.INDIRECT_is_a)

    def test_indirect_subclasses(self):
        """Test that the indirect subclass relationships are correct."""

        provider = MusicOntologyProvider()
        onto = provider.load()

        with onto:
            class InstrumentalBand(onto.MusicalEnsemble):
                equivalent_to = [onto.MusicalEnsemble & onto.has_album_in_discography.only(
                    onto.InstrumentalAlbum)]

        self.assertIn(onto.Artist, InstrumentalBand.INDIRECT_is_a)


if __name__ == "__main__":
    unittest.main()
