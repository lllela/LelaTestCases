import pytest
from pathlib import Path
from src.media_indexing.folder_index import (
    get_artist,
    remove_artist,
    Media,
    Folder,
    get_folders,
    get_folder_files,
    get_updated_media_paths,
    apply_new_media_paths,
    reindex_folders,
    remove_counter,
)
from src.const import VARIOUS_ARTISTS_NAME


def test_get_artist():
    assert get_artist("song [Artist A]") == "Artist A"
    assert get_artist("track [Linkin Park]") == "Linkin Park"
    
    assert get_artist("song.mp3") is None
    
    with pytest.raises(ValueError):
        get_artist("song [Artist A] [Artist B]")


def test_remove_artist():
    assert remove_artist("song [Artist A]") == "song"
    assert remove_artist("track [Linkin Park]") == "track"
    
    assert remove_artist("song.mp3") == "song.mp3"


def test_media_class(tmp_path):
    test_file = tmp_path / "test_song [Artist A].mp3"
    test_file.touch()
    
    media = Media(test_file)
    assert media.artist_name == "Artist A"
    assert media.title == "test_song"
    
    media.rename_update()
    assert media.path.name == "test_song [Artist A].mp3"
    
    with pytest.raises(ValueError):
        Media(tmp_path)


def test_folder_class(tmp_path):
    test_dir = tmp_path / "Test Folder"
    test_dir.mkdir()
    (test_dir / "song1 [Artist A].mp3").touch()
    (test_dir / "song2 [Artist B].mp3").touch()
    
    folder = Folder(test_dir)
    assert folder.title == "Test Folder"
    assert folder.get_counter() == 2
    
    folder.rename_with_counter()
    assert folder.path.name == "Test Folder (2)"
    
    with pytest.raises(ValueError):
        Folder(test_dir / "song1 [Artist A].mp3")


def test_get_folders(tmp_path):
    (tmp_path / "Folder 1").mkdir()
    (tmp_path / "Folder 2").mkdir()
    (tmp_path / ".hidden").mkdir()
    (tmp_path / "file.txt").touch()
    
    folders = get_folders(tmp_path)
    assert len(folders) == 2
    assert all(isinstance(f, Folder) for f in folders)
    assert {f.title for f in folders} == {"Folder 1", "Folder 2"}


def test_get_folder_files(tmp_path):
    (tmp_path / "file1.txt").touch()
    (tmp_path / "file2.mp3").touch()
    (tmp_path / ".hidden").touch()
    
    files = get_folder_files(tmp_path)
    assert len(files) == 2
    assert {f.name for f in files} == {"file1.txt", "file2.mp3"}


def test_get_updated_media_paths(tmp_path):
    folder1 = tmp_path / "Folder 1"
    folder1.mkdir()
    (folder1 / "song1 [Artist A].mp3").touch()
    (folder1 / "song2 [Artist B].mp3").touch()
    (folder1 / "song3.mp3").touch()
    
    folder2 = tmp_path / "Folder 2"
    folder2.mkdir()
    (folder2 / "track1 [Artist A].mp3").touch()
    (folder2 / "track2.mp3").touch()
    
    mapping = get_updated_media_paths(tmp_path)
    
    artist_a_files = [p for p in mapping.values() if p.parent.name == "Artist A"]
    artist_b_files = [p for p in mapping.values() if p.parent.name == "Artist B"]
    va_files = [p for p in mapping.values() if p.parent.name == VARIOUS_ARTISTS_NAME]
    
    assert len(artist_a_files) == 2
    assert len(artist_b_files) == 1
    assert len(va_files) == 2


def test_apply_new_media_paths(tmp_path):
    folder = tmp_path / "Source"
    folder.mkdir()
    (folder / "song1 [Artist A].mp3").touch()
    (folder / "song2 [Artist B].mp3").touch()
    
    mapping = {
        folder / "song1 [Artist A].mp3": tmp_path / "Artist A" / "song1 [Artist A].mp3",
        folder / "song2 [Artist B].mp3": tmp_path / "Artist B" / "song2 [Artist B].mp3",
    }
    
    apply_new_media_paths(mapping)
    
    assert (tmp_path / "Artist A" / "song1 [Artist A].mp3").exists()
    assert (tmp_path / "Artist B" / "song2 [Artist B].mp3").exists()
    assert not folder.exists()


def test_reindex_folders(tmp_path):
    folder_path_before_reindex = tmp_path / "Test Folder"
    folder_path_before_reindex.mkdir()
    (folder_path_before_reindex / "song1 [Artist A].mp3").touch()
    (folder_path_before_reindex / "song2 [Artist B].mp3").touch()

    initial_folder_object = Folder(folder_path_before_reindex)
    reindex_folders([initial_folder_object])
    

    assert initial_folder_object.path.name == "Test Folder (2)"
    assert (initial_folder_object.path / "song1 [Artist A].mp3").exists()
    assert (initial_folder_object.path / "song2 [Artist B].mp3").exists()


def test_remove_counter():
    assert remove_counter("Folder (2)") == "Folder"
    assert remove_counter("Test Folder (10)") == "Test Folder"
    assert remove_counter("Folder without counter") == "Folder without counter"


def test_folder_get_media_list(tmp_path):
    test_dir = tmp_path / "Test Folder"
    test_dir.mkdir()
    (test_dir / "song1 [Artist A].mp3").touch()
    (test_dir / "song2 [Artist B].mp3").touch()
    (test_dir / ".hidden").touch()
    
    folder = Folder(test_dir)
    media_list = folder.get_media_list()
    
    assert len(media_list) == 2
    assert all(isinstance(m, Media) for m in media_list)
    assert {m.title for m in media_list} == {"song1", "song2"}


def test_folder_get_new_folder_name(tmp_path):
    test_dir = tmp_path / "Test Folder"
    test_dir.mkdir()
    (test_dir / "song1 [Artist A].mp3").touch()
    (test_dir / "song2 [Artist B].mp3").touch()
    
    folder = Folder(test_dir)
    new_name = folder.get_new_folder_name()
    assert new_name == "Test Folder (2)"


def test_apply_new_media_paths_with_directory_error(tmp_path):
    folder = tmp_path / "Source"
    folder.mkdir()
    (folder / "song1 [Artist A].mp3").touch()
    (folder / "subfolder").mkdir()
    
    mapping = {
        folder / "song1 [Artist A].mp3": tmp_path / "Artist A" / "song1 [Artist A].mp3",
    }
    
    apply_new_media_paths(mapping)
    
    assert folder.exists()
    assert (folder / "subfolder").exists()
    assert not (folder / "song1 [Artist A].mp3").exists()
    assert (tmp_path / "Artist A" / "song1 [Artist A].mp3").exists()
