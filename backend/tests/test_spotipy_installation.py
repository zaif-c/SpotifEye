import spotipy

def test_spotipy_installation() -> None:
    """Test that Spotipy is installed and can be imported and instantiated."""
    sp = spotipy.Spotify()
    assert sp is not None, "Spotipy client instantiation failed." 