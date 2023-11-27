import os
import argparse
import uuid
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
import re

from pathlib import Path


saved_path_file = ".cache.pk"

# RaceUUID
race = {
    "Dragonborn": "9c61a74a-20df-4119-89c5-d996956b6c66",
    "Drows": "4f5d1434-5175-4fa9-b7dc-ab24fba37929",
    "Dwarves": "0ab2874d-cfdc-405e-8a97-d37bfbb23c52",
    "Elves": "6c038dcb-7eb5-431d-84f8-cecfaf1c0c5a",
    "Githyanki": "bdf9b779-002c-4077-b377-8ea7c1faa795",
    "Gnomes": "f1b3f884-4029-4f0f-b158-1f9fe0ae5a0d",
    "HalfElfs": "45f4ac10-3c89-4fb2-b37d-f973bb9110c0",
    "Halflings": "78cd3bcc-1c43-4a2a-aa80-c34322c16a04",
    "Half-Orcs": "5c39a726-71c8-4748-ba8d-f768b3c11a91",
    "Humans": "0eb594cb-8820-4be6-a58d-8be7a1a98fba",
    "Tieflings": "b6dccbed-30f3-424b-a181-c4540cf38197",
}

# Private Parts UUID
genital = {
    "penis": "d27831df-2891-42e4-b615-ae555404918b",
    "vagina": "a0738fdf-ca0c-446f-a11d-6211ecac3291",
}

genitals = {
    # "Humans": {"material": "a019b9c1-7b97-9fdd-5469-fb04aecded1f", "pubes": ""}
    "Humans": {
        "Female_Genital_A": {
            "material": "07168a77-9294-35f1-a78d-04ee9b8c46ad",
            "pubes": "79c3b32b-a243-b949-4aea-4ff285d50fca",
        },
        "Female_Genital_B": {
            "material": "827afee2-dd5e-8663-ba8b-7c184e7de228",
            "pubes": "79c3b32b-a243-b949-4aea-4ff285d50fca",
        },
        "Female_Genital_C": {
            "material": "a019b9c1-7b97-9fdd-5469-fb04aecded1f",
            "pubes": "79c3b32b-a243-b949-4aea-4ff285d50fca",
        },
        "Male_Genital_A": {
            "material": "6dfda8c4-6d14-4538-2994-8b0fedc1dc61",
            "pubes": "79c3b32b-a243-b949-4aea-4ff285d50fca",
        },
        "Male_Genital_B": {
            "material": "4add0105-0d3a-f68a-5484-660c0be7eecc",
            "pubes": "79c3b32b-a243-b949-4aea-4ff285d50fca",
        },
        "Male_Genital_C": {
            "material": "da8311de-fd7d-2012-d853-99cfa07a9dfc",
            "pubes": "79c3b32b-a243-b949-4aea-4ff285d50fca",
        },
    },
    # "Elves": {
    #     "Female_Genital_A": {
    #         {
    #             "material": "4976fb80-b3b2-adb3-5318-3cb1ef649ed0",
    #             "pubes": "79c3b32b-a243-b949-4aea-4ff285d50fca",
    #         },
    #     },
    #     "Female_Genital_B": {
    #         {
    #             "material": "0fcbfb16-9551-0ea0-f97e-ff499a408b01",
    #             "pubes": "79c3b32b-a243-b949-4aea-4ff285d50fca",
    #         },
    #     },
    #     "Female_Genital_C": {
    #         {
    #             "material": "4938541f-b59a-8cce-77b2-e875b5c3a6c6",
    #             "pubes": "79c3b32b-a243-b949-4aea-4ff285d50fca",
    #         },
    #     },
    # },
}

# BodyShape
BodyShape = {
    "Average": 0,
    "Strong": 1,
}

# BodyType
BodyType = {
    "Male": 0,
    "Female": 1,
}

# Texture
VisualResource = {
    "circumcised": {
        "female": "0fcbfb16-9551-0ea0-f97e-ff499a408b01",
        "male": "0fcbfb16-9551-0ea0-f97e-ff499a408b01",
    },
    "uncircumcised": {
        "female": "0fcbfb16-9551-0ea0-f97e-ff499a408b01",
        "male": "0fcbfb16-9551-0ea0-f97e-ff499a408b01",
    },
}

CharacterCreationAppearanceVisualsXML = """
<save>
  <version major="4" minor="0" revision="9" build="328" />
  <region id="CharacterCreationAppearanceVisuals">
    <node id="root">
      <children></children>
    </node>
  </region>
</save>
"""

_merged = """
<save>
  <version major="4" minor="0" revision="7" build="2" lslib_meta="v1,bswap_guids" />
  <region id="VisualBank">
    <node id="VisualBank">
      <children></children>
    </node>
  </region>
</save>
"""


def MetaLSX(mod_uuid):
    return f"""
<save>
<version major="4" minor="0" revision="0" build="77" />
<region id="Config">
<node id="root">
  <children>
    <node id="Dependencies"/>
    <node id="ModuleInfo">
      <attribute id="Author" type="LSWString" value="{args.author}"/>
      <attribute id="CharacterCreationLevelName" type="FixedString" value=""/>
      <attribute id="Description" type="LSWString" value="{args.name}"/>
      <attribute id="Folder" type="LSWString" value="{args.name}"/>
      <attribute id="GMTemplate" type="FixedString" value=""/>
      <attribute id="LobbyLevelName" type="FixedString" value=""/>
      <attribute id="MD5" type="LSString" value=""/>
      <attribute id="MainMenuBackgroundVideo" type="FixedString" value=""/>
      <attribute id="MenuLevelName" type="FixedString" value=""/>
      <attribute id="Name" type="FixedString" value="{args.name}"/>
      <attribute id="NumPlayers" type="uint8" value="16"/>
      <attribute id="PhotoBooth" type="FixedString" value=""/>
      <attribute id="StartupLevelName" type="FixedString" value=""/>
      <attribute id="Tags" type="LSWString" value=""/>
      <attribute id="Type" type="FixedString" value="Add-on"/>
      <attribute id="UUID" type="FixedString" value="{mod_uuid}"/>
      <attribute id="Version64" type="int64" value="36028799166447616"/>
      <children>
        <node id="PublishVersion">
          <attribute id="Version64" type="int64" value="36028799166447616"/>
        </node>
        <node id="Scripts"/>
        <node id="TargetModes">
          <children>
            <node id="Target">
              <attribute id="Object" type="FixedString" value="Story"/>
            </node>
          </children>
        </node>
      </children>
    </node>
  </children>
</node>
</region>
</save>
"""


class Folder:
    def __init__(self, name):
        self.name = name
        self.dir = None

    def __enter__(self):
        self.dir = os.getcwd()
        new_dir = os.path.join(self.dir, self.name)
        os.makedirs(new_dir, exist_ok=True)
        os.chdir(new_dir)

    def __exit__(self, exc_type, exc_value, traceback):
        os.chdir(self.dir)


class File:
    def __init__(self, name):
        self.name = name
        self._lines = []
        self.indent = 0

    def __enter__(self):
        self._lines = []
        return self

    def clear(self):
        self._lines = []

    def __exit__(self, exc_type, exc_value, traceback):
        with open(self.name, "w") as f:
            f.writelines(self._lines)

    def add_line(self, text: str):
        self._lines.append("\t" * self.indent + text)


class XMLFile(File):
    def __enter__(self):
        ret = super().__enter__()
        self.add_line("")
        return ret


# Generate folders for models.
def create_folders(name):
    # Dragonborn
    mkdir(f"Generated/Public/{name}/Dragonborn/_Female")
    mkdir(f"Generated/Public/{name}/Dragonborn/_Male")

    # Dwarves
    mkdir(f"Generated/Public/{name}/Dwarves/_Female")
    mkdir(f"Generated/Public/{name}/Dwarves/_Male")

    # Elves
    # mkdir(f"Generated/Public/{name}/Elves/_Female")
    # mkdir(f"Generated/Public/{name}/Elves/_Male")

    # Githyanki
    mkdir(f"Generated/Public/{name}/Githyanki/_Female")
    mkdir(f"Generated/Public/{name}/Githyanki/_Male")

    # Gnomes
    mkdir(f"Generated/Public/{name}/Gnomes/_Female")
    mkdir(f"Generated/Public/{name}/Gnomes/_Male")

    # Halflings
    mkdir(f"Generated/Public/{name}/Halflings/_Female")
    mkdir(f"Generated/Public/{name}/Halflings/_Male")

    # HalfOrcs
    mkdir(f"Generated/Public/{name}/HalfOrcs/_Female")
    mkdir(f"Generated/Public/{name}/HalfOrcs/_Male")

    # Humans
    mkdir(f"Generated/Public/{name}/Humans/_Female")
    mkdir(f"Generated/Public/{name}/Humans/_Male")
    mkdir(f"Generated/Public/{name}/Humans/_FemaleStrong")
    mkdir(f"Generated/Public/{name}/Humans/_MaleStrong")
    # mkdir(f"Public/{name}/Content/Assets/Humans")

    # Tieflings
    mkdir(f"Generated/Public/{name}/Tieflings/_Female")
    mkdir(f"Generated/Public/{name}/Tieflings/_Male")
    mkdir(f"Generated/Public/{name}/Tieflings/_FemaleStrong")
    mkdir(f"Generated/Public/{name}/Tieflings/_MaleStrong")


# Add indentation to XML.
def indent(elem, level=0):
    indent_size = "  "
    i = "\n" + level * indent_size
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + indent_size
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


# Pretty print XML.
def pretty_print_xml(xml_string):
    root = ET.fromstring(xml_string)
    indent(root)

    # Convert the XML element back to a string
    pretty_xml = ET.tostring(root, encoding="unicode")

    # Insert XML encoding
    encoding = '<?xml version="1.0" encoding="utf-8"?>'
    return encoding + "\n" + pretty_xml


# e.g. b3a212d7-e669-4f3d-aa2f-3a629d00ba01
def generate_uuid():
    return str(uuid.uuid4())


# TranslationString handles.
# They are GUIDs prepended with the letter "h"
# each hyphen is replaced with an "f".
# https://github.com/ShinyHobo/BG3-Modders-Multitool/issues/9
def generate_handle():
    return "h" + generate_uuid().replace("-", "f")


# no error if existing, make parent directories as needed
def mkdir(path):
    Path(path).mkdir(parents=True, exist_ok=True)


# Recursively search for GR2 models.
def rec_walk(dir):
    paths = []
    for path in Path(dir).rglob("*.GR2"):
        dirname = path.as_posix()
        file_path = dirname.split("/")
        dirname, fname = os.path.split(dirname)

        # Get name
        file_split = path.stem.split("_Genital_", 1)
        name = file_split[0]

        # Get private parts
        file_split = file_split[1]
        file_split = file_split.split("_")
        private_parts = file_split[0]

        # pubes = "_No_Hair" if 1 < len(file_split) else ""
        pubes = 0 if 1 < len(file_split) else 1
        gender = "Female" if file_path[4] == "_Female" else "Male"
        private_parts = gender + "_Genital_" + private_parts

        raceName = file_path[3]
        raceUUID = race[file_path[3]]

        paths.append(
            {
                "stem": path.stem,
                "suffix": path.suffix,
                "sex": str(1 if file_path[4] == "_Female" else 0),
                "raceUUID": raceUUID,
                "raceName": raceName,
                "dir": dirname,
                "genitals": private_parts,
                "materials": genitals[raceName][private_parts],
                "pubes": pubes,
                "name": name.replace("_", " "),
            }
        )

    return paths


# Insert XML for CharacterCreationAppearanceVisuals.lsx
def insert_dick_character_creation(model, handle, uuid):
    character_uuid = generate_uuid()
    xml = f"""
<node id="CharacterCreationAppearanceVisual">
  <!-- 0 = Average, 1 = Strong -->
  <attribute id="BodyShape" type="uint8" value="0" />
  <!-- 0 = Male, 1 = Female -->
  <attribute id="BodyType" type="uint8" value="{model['sex']}" />
  <!-- Name for your genital option, established in XXX.loca.xml -->
  <attribute id="DisplayName" type="TranslatedString" handle="{handle}" version="1" />
  <!-- Race -->
  <attribute id="RaceUUID" type="guid" value="{model['raceUUID']}" />
  <!-- What Slot the option goes in -->
  <attribute id="SlotName" type="FixedString" value="Private Parts" />
  <!-- Unique ID for each option, generated in Modders' Multitool -->
  <attribute id="UUID" type="guid" value="{character_uuid}" />
  <!-- Visual information (mesh, textures, etc.) for your genital option, established in _merged.lsf.lsx -->
  <attribute id="VisualResource" type="guid" value="{uuid}" />
  <children>
    <node id="Tags">
      <!-- Tags genital option as penis or vulva. IDK what the vulva one is and don't feel like finding it sorry. -->
      <attribute id="Object" type="guid" value="d27831df-2891-42e4-b615-ae555404918b" />
    </node>
  </children>
</node>
      """
    dick = ET.XML(xml)
    return dick


# Insert XML for _merged.lsx
def insert_dick_merged(model, uuid):
    path = model["dir"]
    visual_id = model["materials"]["material"]
    pubes = model["pubes"]

    pubesXML = ""

    if pubes:
        pubesXML = f"""
<node id="Objects">
  <attribute id="LOD" type="uint8" value="0" />
  <attribute id="MaterialID" type="FixedString" value="{model["materials"]["pubes"]}" />
  <attribute id="ObjectID" type="FixedString" value="{model['stem']}.HUM_F_NKD_Body_Genital_D_Pubes_Mesh.1" />
</node>
"""
    xml = f"""
<node id="Resource">
  <attribute id="AttachBone" type="FixedString" value="" />
  <attribute id="AttachmentSkeletonResource" type="FixedString" value="" />
  <attribute id="BlueprintInstanceResourceID" type="FixedString" value="" />
  <attribute id="BoundsMax" type="fvec3" value="0.04660766 1.031223 0.05886364" />
  <attribute id="BoundsMin" type="fvec3" value="-0.04640537 0.8961504 -0.1221507" />
  <attribute id="ClothColliderResourceID" type="FixedString" value="" />
  <!-- Info for pubes. Leave this empty ("") if no (3D) pubes. -->
  <attribute id="HairPresetResourceId" type="FixedString" value="" />
  <attribute id="HairType" type="uint8" value="0" />
  <!-- Unique ID for combined visual information, generated in Modders' Multitool -->
  <attribute id="ID" type="FixedString" value="{uuid}" />
  <attribute id="MaterialType" type="uint8" value="0" />
  <!-- Filename for your model without the extension -->
  <attribute id="Name" type="LSString" value="{model['name']}" />
  <attribute id="NeedsSkeletonRemap" type="bool" value="False" />
  <attribute id="RemapperSlotId" type="FixedString" value="" />
  <attribute id="ScalpMaterialId" type="FixedString" value="" />
  <attribute id="SkeletonResource" type="FixedString" value="" />
  <attribute id="SkeletonSlot" type="FixedString" value="" />
  <attribute id="Slot" type="FixedString" value="Private Parts" />
  <attribute id="SoftbodyResourceID" type="FixedString" value="" />
  <!-- File location for your model. You can reuse the same file for races with identical body types. -->
  <attribute id="SourceFile" type="LSString" value="{path}/{model['stem']}{model['suffix']}" />
  <attribute id="SupportsVertexColorMask" type="bool" value="True" />
  <!-- Same as above but change the extension -->
  <attribute id="Template" type="FixedString" value="{path}/{model['stem']}.Dummy_Root.0" />
  <attribute id="_OriginalFileVersion_" type="int64" value="144115207403209033" />
  <children>
    <node id="AnimationWaterfall">
      <attribute id="Object" type="FixedString" value="" />
    </node>
    <node id="Base" />
    <node id="ClothProxyMapping" />
    <node id="Objects">
      <attribute id="LOD" type="uint8" value="0" />
      <!-- Material that should be applied to your mesh -->
      <attribute id="MaterialID" type="FixedString" value="{visual_id}" />
      <attribute id="ObjectID" type="FixedString" value="{model['stem']}.HUM_F_NKD_Body_Genital_F_Mesh.0" />
    </node>
    {pubesXML}
  </children>
</node>
      """

    dick = ET.XML(xml)
    return dick


def create_mod(args):
    name = args.name

    # check if this mod already exists and warn against override
    if os.path.exists(os.path.join(os.getcwd(), name)):
        confirm = input(
            f"Mod {name} already exists. Are you sure you want to recreate parts of it? (y/n) "
        ).lower()
        if confirm not in ["y", "yes"]:
            print("Aborting.")
            return

    with Folder(name):
        # Create folders for GR2 models
        create_folders(name)

        # Add localization file.
        with Folder("Localization/English"):
            with XMLFile(f"{name}.loca.xml") as f:
                f.add_line("""<contentList>\n</contentList>""")

        # Add _merged.lsx file.
        with Folder(
            f"Public/{name}/Content/Assets/Characters/Humans/[PAK]_MaleStrong_Body"
        ):
            with XMLFile("_merged.lsf.lsx") as f:
                f.add_line(_merged)

        # Add meta.lsx file
        mod_uuid = generate_uuid()
        with Folder(f"Mods/{name}"):
            with XMLFile("meta.lsx") as f:
                f.add_line(pretty_print_xml(MetaLSX(mod_uuid)))

        # Add CharacterCreationAppearanceVisuals.lsx file.
        with Folder(f"Public/{name}/CharacterCreation"):
            with XMLFile("CharacterCreationAppearanceVisuals.lsx") as f:
                f.add_line(CharacterCreationAppearanceVisualsXML)

        # Edit localization xml
        loca = f"Localization/English/{name}.loca.xml"
        doc = ET.parse(loca)
        root = doc.getroot()

        # Add character creation visuals
        visuals = (
            f"public/{name}/CharacterCreation/CharacterCreationAppearanceVisuals.lsx"
        )
        visuals_doc = ET.parse(visuals)
        visuals_root = visuals_doc.getroot()
        visuals_children = visuals_doc.findall(""".//*children""")

        # Edit _merged.lsx xml
        merged = f"Public/{name}/Content/Assets/Characters/Humans/[PAK]_MaleStrong_Body/_merged.lsf.lsx"
        merged_doc = ET.parse(merged)
        merged_root = merged_doc.getroot()
        merged_children = merged_doc.findall(""".//*children""")

        # Interate over models.
        models = rec_walk(f"Generated/Public/{name}")

        for model in models:
            handle = generate_handle()
            uuid = generate_uuid()

            # Insert content nodes to localization.
            data = ET.Element("content", {"contentuid": handle, "version": "1"})
            data.text = model["name"]
            root.append(data)

            # Insert content nodes to character creation visuals.
            for element in visuals_children:
                element.append(insert_dick_character_creation(model, handle, uuid))

            # Insert content nodes to character creation visuals.
            for element in merged_children:
                element.append(insert_dick_merged(model, uuid))

            if model["raceName"] == "Humans":
                model["raceName"] = "Elves"
                model["raceUUID"] = race[model["raceName"]]

                # Insert content nodes to character creation visuals.
                for element in visuals_children:
                    element.append(insert_dick_character_creation(model, handle, uuid))

                # Insert content nodes to character creation visuals.
                for element in merged_children:
                    element.append(insert_dick_merged(model, uuid))

                model["raceName"] = "HalfElfs"
                model["raceUUID"] = race[model["raceName"]]

                # Insert content nodes to character creation visuals.
                for element in visuals_children:
                    element.append(insert_dick_character_creation(model, handle, uuid))

                # Insert content nodes to character creation visuals.
                for element in merged_children:
                    element.append(insert_dick_merged(model, uuid))

                model["raceName"] = "Drows"
                model["raceUUID"] = race[model["raceName"]]

                # Insert content nodes to character creation visuals.
                for element in visuals_children:
                    element.append(insert_dick_character_creation(model, handle, uuid))

                # Insert content nodes to character creation visuals.
                for element in merged_children:
                    element.append(insert_dick_merged(model, uuid))

            print(model)

        # Beautify _merged.lsx.
        dom = ET.tostring(merged_root)
        dom = pretty_print_xml(dom)

        # Write _merged.lsx.
        with open(merged, "w") as f:
            f.write(dom)

        # Beautify character creation visuals.
        dom = ET.tostring(visuals_root)
        dom = pretty_print_xml(dom)

        # Write character creation visuals xml file.
        with open(visuals, "w") as f:
            f.write(dom)

        # Beautify localization dom.
        dom = ET.tostring(root)
        dom = pretty_print_xml(dom)

        # Write localization xml file.
        with open(loca, "w") as f:
            f.write(dom)

        # Alert user
        print(f"Created mod {name} with UUID {mod_uuid}")


def prompt_for_binary_response(message):
    while True:
        response = input(message).lower()
        if response in ["y", "yes"]:
            return True
        elif response in ["n", "no"]:
            return False
        else:
            print("Invalid response. Please enter y or n.")


if __name__ == "__main__":
    # parse arguments with argparse
    parser = argparse.ArgumentParser(description="Initialize a new mod")
    parser.add_argument("name", help="Name of the mod")
    parser.add_argument("author", help="Author of the mod")
    parser.add_argument(
        "-g", "--generate", help="Generate support for models", action="store_true"
    )

    args = parser.parse_args()

    print("Creating mod folder")
    create_mod(args)

    # if args.generate:
    #   print("generate")
    #   rec_walk(f"{args.name}/Generated/Public/{args.name}")
