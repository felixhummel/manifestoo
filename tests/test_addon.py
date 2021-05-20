import pytest

from manifestoo.addon import (
    Addon,
    AddonNotInstallable,
    InvalidManifest,
    NoManifestFound,
    NotADirectory,
)


def test_basic(tmp_path):
    addon_dir = tmp_path / "theaddon"
    addon_dir.mkdir()
    (addon_dir / "__manifest__.py").write_text("{'name': 'the addon'}")
    addon = Addon.from_addon_dir(addon_dir)
    assert addon.name == "theaddon"
    assert addon.path == addon_dir
    assert addon.manifest == {"name": "the addon"}


def test_not_a_directory(tmp_path):
    with pytest.raises(NotADirectory):
        Addon.from_addon_dir(tmp_path / "not-a-dir")


def test_not_installable(tmp_path):
    (tmp_path / "__manifest__.py").write_text("{'installable': False}")
    with pytest.raises(AddonNotInstallable):
        Addon.from_addon_dir(tmp_path)
    assert Addon.from_addon_dir(tmp_path, allow_not_installable=True)


def test_invalid_manifest(tmp_path):
    (tmp_path / "__manifest__.py").write_text("[]")
    with pytest.raises(InvalidManifest):
        Addon.from_addon_dir(tmp_path)


def test_manifest_syntax_error(tmp_path):
    (tmp_path / "__manifest__.py").write_text("{'installable':}")
    with pytest.raises(InvalidManifest):
        Addon.from_addon_dir(tmp_path)


def test_no_manifest(tmp_path):
    with pytest.raises(NoManifestFound):
        Addon.from_addon_dir(tmp_path)
