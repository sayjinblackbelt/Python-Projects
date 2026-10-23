from pathlib import Path

import pytest

from organizer import category_for, organize_files, plan_organization


def test_category_uses_case_insensitive_extensions():
    assert category_for(Path("photo.JPG")) == "Imagens"
    assert category_for(Path("report.pdf")) == "Documentos"
    assert category_for(Path("song.mp3")) == "Audio"
    assert category_for(Path("clip.MP4")) == "Videos"
    assert category_for(Path("archive.zip")) == "Compactados"
    assert category_for(Path("mystery.xyz")) == "Outros"
    assert category_for(Path("README")) == "Outros"


def test_plan_lists_files_without_moving_them(tmp_path):
    source = tmp_path / "photo.png"
    source.write_text("image", encoding="utf-8")

    plan = plan_organization(tmp_path)

    assert len(plan) == 1
    assert plan[0] == (source, tmp_path / "Imagens" / "photo.png")
    assert source.exists()
    assert not (tmp_path / "Imagens").exists()


def test_organize_moves_files_to_category_folders(tmp_path):
    (tmp_path / "report.pdf").write_text("pdf", encoding="utf-8")
    (tmp_path / "notes.txt").write_text("text", encoding="utf-8")
    (tmp_path / "mystery.xyz").write_text("other", encoding="utf-8")

    results = organize_files(tmp_path)

    assert len(results) == 3
    assert (tmp_path / "Documentos" / "report.pdf").read_text(encoding="utf-8") == "pdf"
    assert (tmp_path / "Documentos" / "notes.txt").exists()
    assert (tmp_path / "Outros" / "mystery.xyz").exists()


def test_existing_filename_is_not_overwritten(tmp_path):
    (tmp_path / "report.pdf").write_text("new", encoding="utf-8")
    target = tmp_path / "Documentos"
    target.mkdir()
    (target / "report.pdf").write_text("existing", encoding="utf-8")

    organize_files(tmp_path)

    assert (target / "report.pdf").read_text(encoding="utf-8") == "existing"
    assert (target / "report_1.pdf").read_text(encoding="utf-8") == "new"


def test_missing_or_non_directory_path_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        plan_organization(tmp_path / "missing")
    file_path = tmp_path / "file.txt"
    file_path.write_text("content", encoding="utf-8")
    with pytest.raises(NotADirectoryError):
        plan_organization(file_path)


def test_subdirectories_are_not_moved_or_scanned(tmp_path):
    subfolder = tmp_path / "photos"
    subfolder.mkdir()
    (subfolder / "photo.png").write_text("image", encoding="utf-8")
    (tmp_path / "notes.txt").write_text("notes", encoding="utf-8")

    plan = plan_organization(tmp_path)

    assert len(plan) == 1
    assert plan[0][0].name == "notes.txt"
    assert (subfolder / "photo.png").exists()
