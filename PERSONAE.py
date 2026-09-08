# ~VAULT/PERSONAE.py

# get "Path" tool
from pathlib import Path
# get "Move"" tool
from shutil import move
# get "Instant" tool
from whenever import Instant

# define "vault" as directory without exclamation
vault = next(p for p in Path(__file__).resolve().parents if "!" not in p.name)

# define "folders" as vault directories
folders = [path for path in vault.iterdir() if path.is_dir()]
# define "bangdir" as folder named exclamation
bangdir = [path for path in folders if path.name == "!"]
# define "dotdirs" as folders with leading period
dotdirs = [path for path in folders if path.name.startswith(".")]

# define "moor" as
def moor(target):
    # write identity "target"' at "timestamp" now
    target.write_text(identity.format(timestamp=Instant.now()), encoding="utf-8")

# define "identify" as
def identify(target):
    # unless misencoded
    try:
    # using "timestamp" found at "target" anchor leaving out everything in "identity" but end "timestamp" without newlines
        timestamp = (target.read_text(encoding="utf-8").removeprefix(identity.removesuffix("{timestamp}\n\n")).removesuffix("\n\n"))
        # check timestamp syntax
        try:
        # is timestamp ISO
            Instant.parse_iso(timestamp)
        # if false
        except ValueError:
            # quick fail
            return False
        # is timestamp UTC
        if not timestamp.endswith("Z"):
            # quick fail
            return False
        # check anchorfile identity
        return (target.read_text(encoding="utf-8") == identity.format(timestamp=timestamp))
    # or if misencoded
    except UnicodeDecodeError:
        # quick fail
        return False
        
# define "punch" as stub write
def punch(target):
    # fix missing or malformed stub
    print(f"Stubbing {persona.name}...")
    # write to "target" ¿!? with newline
    target.write_bytes(b"\xc2\xbf!?\n")

# LOOP: define "persona" as any dotdir
for persona in dotdirs:
# example persona = ".example"

    # define persona "name" as allcaps folder stem
    name = persona.name.removeprefix('.').upper()
    # name = "EXAMPLE"

    # define "anchor" as anchorfile
    anchor = persona / f"{name}.md"
    # anchor = ".example/EXAMPLE.md"

    # define "identity" as anchorfile layout
    identity = ("---\n"
        f"title: {name}\n"
        f"path: ./{anchor.relative_to(vault).as_posix()}\n"
        "---\n"
        "\n"
        "Persona Anchored at {timestamp}\n"
        "\n"
        )

    # define "stub" as stubfile
    stub = persona / "stub.txt"

    # check stub and contents
    if not stub.is_file() or stub.read_bytes() != b"\xc2\xbf!?\n":
        # write stubfile
        punch(stub)
        # stub = ".example/stub.txt"

    # check for anchorfile
    if not anchor.is_file():
        # create anchor if missing
        print(f"Anchoring {persona.name}...")
        # set "target" anchorfile
        moor(anchor)
    # check anchor if existing
    elif not identify(anchor):
        # append underscore to anchor
        chain = anchor.with_stem(anchor.stem + "_")
        # check for filename collision
        while chain.exists():
            # append underscore to anchorfile
            chain = chain.with_stem(chain.stem + "_")
        # relocate anchorfile
        move(anchor, chain)
        # write fresh anchor
        print(f"Reanchoring {persona.name}...")
        # set "target" anchorfile
        moor(anchor)

# end LOOP
