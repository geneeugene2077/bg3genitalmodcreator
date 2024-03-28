import os
import argparse
import uuid
import xml.etree.ElementTree as ET
from pathlib import Path
import pprint


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
    "HalfOrcs": "5c39a726-71c8-4748-ba8d-f768b3c11a91",
    "Humans": "0eb594cb-8820-4be6-a58d-8be7a1a98fba",
    "Tieflings": "b6dccbed-30f3-424b-a181-c4540cf38197",
}

skeleton = {
    "DragonbornMale": "b161e591-2d57-5392-d764-f9ca80e695df",
    "DragonbornFemale": "733b0bff-3f62-bb0b-d128-846de19836ed",
    "DwarvesMale": "953138ec-0b3f-e45d-4221-619165c41bb3",
    "DwarvesFemale": "2d87542b-da2a-ecd0-9238-dc87e60553b6",
    "GithyankiMale": "f2c913fa-574f-1838-d334-0b9b9fb02aeb",
    "GithyankiFemale": "26cd0916-bee0-d901-642b-2d384d6ebb0b",
    "GnomesMale": "91c98338-d0db-190c-7e7c-8e60533e4fd3",
    "GnomesFemale": "25a0e700-dd2d-68d4-0a8e-c68d8360569a",
    "HalflingsMale": "213bb548-4870-7c4f-d725-b5f0f005d81c",
    "HalflingsFemale": "b8c3036d-d5bd-6b28-cfef-ea490ec4e517",
    "HalfOrcsMale": "a9348ac1-62d4-df89-3696-2b1fe190c038",
    "HalfOrcsFemale": "c54de5d4-1cf3-c062-95c1-bea05504617a",
    "HumansMale": "eccc7e98-f303-0bc1-0450-bf0d7120d55e",
    "HumansMaleStrong": "be442c7c-a48d-5aad-3a7e-fc50eec96385",
    "HumansFemale": "4d3627bc-ccbc-e855-6b4f-d5d74d715d22",
    "HumansFemaleStrong": "35e347bc-dd74-7e7e-2fb8-a2de0c8be49a",
    "TieflingsMale": "fb6ba2ab-36be-6d95-7494-11d31e949b09",
    "TieflingsMaleStrong": "85fecf6a-79f6-16f7-66a8-ca0f67d8ae34",
    "TieflingsFemale": "ffc8d503-a5de-0f8d-c60b-a018cd47a1a6",
    "TieflingsFemaleStrong": "49339153-0f6a-3fef-3327-b373547e9a22",
}

# Objects: lod, materialID, objectId
genitals = {
    "Dragonborn": {
        "Female_Genital_A": [
            [0, "2c75ec63-da78-af8c-ab43-25b5bb2586ee", 0],
            [1, "2c75ec63-da78-af8c-ab43-25b5bb2586ee", 1],
        ],
        "Female_Genital_B": [
            [0, "a5c39d9c-de70-9796-2d87-f4d08652c790", 0],
            [1, "a5c39d9c-de70-9796-2d87-f4d08652c790", 1],
        ],
        "Male_Genital_A": [
            [0, "822f90a6-6a04-7c61-018a-134ff67fa5a5", 0],
            [1, "822f90a6-6a04-7c61-018a-134ff67fa5a5", 1],
        ],
        "Male_Genital_B": [
            [0, "84b4ba3d-4e01-b78a-2698-5a844afab398", 0],
            [1, "84b4ba3d-4e01-b78a-2698-5a844afab398", 1],
        ],
    },
    "Dwarves": {
        "Female_Genital_A": [
            [0, "4147f0f8-b3d9-4409-846f-73c28f109e52", 0],
            [0, "79c3b32b-a243-b949-4aea-4ff285d50fca", 1],
            [1, "4147f0f8-b3d9-4409-846f-73c28f109e52", 2],
            [1, "79c3b32b-a243-b949-4aea-4ff285d50fca", 3],
        ],
        "Female_Genital_B": [
            [0, "60ee8123-fff4-14c3-5a55-3d249773abb7", 0],
            [0, "79c3b32b-a243-b949-4aea-4ff285d50fca", 1],
            [1, "60ee8123-fff4-14c3-5a55-3d249773abb7", 2],
            [1, "79c3b32b-a243-b949-4aea-4ff285d50fca", 3],
        ],
        "Male_Genital_A": [
            [0, "98b23715-b994-e3fa-7abd-9a8944be39d7", 0],
            [0, "79c3b32b-a243-b949-4aea-4ff285d50fca", 1],
            [1, "98b23715-b994-e3fa-7abd-9a8944be39d7", 2],
            [1, "79c3b32b-a243-b949-4aea-4ff285d50fca", 3],
        ],
        "Male_Genital_B": [
            [0, "ff81adfe-996f-76e4-1cc2-87f5a927cf30", 0],
            [0, "79c3b32b-a243-b949-4aea-4ff285d50fca", 1],
            [1, "ff81adfe-996f-76e4-1cc2-87f5a927cf30", 2],
            [1, "79c3b32b-a243-b949-4aea-4ff285d50fca", 3],
        ],
    },
    "Elves": {
        # Female
        "Female_Genital_A": [
            [0, "4976fb80-b3b2-adb3-5318-3cb1ef649ed0", 0],
            [0, "79c3b32b-a243-b949-4aea-4ff285d50fca", 1],
            [1, "4976fb80-b3b2-adb3-5318-3cb1ef649ed0", 2],
            [1, "79c3b32b-a243-b949-4aea-4ff285d50fca", 3],
        ],
        "Female_Genital_B": [
            [0, "0fcbfb16-9551-0ea0-f97e-ff499a408b01", 0],
            [0, "79c3b32b-a243-b949-4aea-4ff285d50fca", 1],
        ],
        # Female Strong
        "FemaleStrong_Genital_A": [
            [0, "921879e2-35da-1c9f-c15e-4b7e59d10feb", 0],
            [0, "921879e2-35da-1c9f-c15e-4b7e59d10feb", 1],
            [1, "79c3b32b-a243-b949-4aea-4ff285d50fca", 0],
            [1, "79c3b32b-a243-b949-4aea-4ff285d50fca", 1],
        ],
        "FemaleStrong_Genital_B": [
            [0, "48540d0d-341c-bc9c-1319-efdedb6d1dfd", 0],
            [0, "79c3b32b-a243-b949-4aea-4ff285d50fca", 1],
        ],
        # MALE
        "Male_Genital_A": [
            [0, "b4548d94-0fd8-b3af-436a-dd2d86cf47f1", 0],
            [0, "79c3b32b-a243-b949-4aea-4ff285d50fca", 1],
            [1, "b4548d94-0fd8-b3af-436a-dd2d86cf47f1", 2],
            [1, "79c3b32b-a243-b949-4aea-4ff285d50fca", 3],
        ],
        "Male_Genital_B": [
            [0, "68917227-ef70-cf2e-3bb5-6bd553454bb9", 0],
            [0, "79c3b32b-a243-b949-4aea-4ff285d50fca", 1],
            [1, "68917227-ef70-cf2e-3bb5-6bd553454bb9", 2],
            [1, "79c3b32b-a243-b949-4aea-4ff285d50fca", 3],
        ],
        # Male Strong
        "MaleStrong_Genital_A": [
            [0, "79c3b32b-a243-b949-4aea-4ff285d50fca", 0],
            [0, "79c3b32b-a243-b949-4aea-4ff285d50fca", 1],
            [1, "7c3f090b-ca3c-542d-2468-7c8d2c964359", 2],
            [1, "7c3f090b-ca3c-542d-2468-7c8d2c964359", 3],
        ],
        "MaleStrong_Genital_B": [
            [0, "47aa6d48-c209-4e04-bcb2-dbbae68df2ec", 0],
            [0, "79c3b32b-a243-b949-4aea-4ff285d50fca", 1],
        ],
    },
    "Githyanki": {
        "Female_Genital_A": [
            [0, "286aa6b2-fa78-f9a1-f35c-d037dd5d290a", 0],
            [0, "79c3b32b-a243-b949-4aea-4ff285d50fca", 1],
            [1, "286aa6b2-fa78-f9a1-f35c-d037dd5d290a", 2],
            [1, "79c3b32b-a243-b949-4aea-4ff285d50fca", 3],
        ],
        "Female_Genital_B": [
            [0, "0d8c7a4b-c02a-ea56-d392-0bc38c232a70", 0],
            [0, "79c3b32b-a243-b949-4aea-4ff285d50fca", 1],
            [1, "0d8c7a4b-c02a-ea56-d392-0bc38c232a70", 2],
            [1, "79c3b32b-a243-b949-4aea-4ff285d50fca", 3],
        ],
        "Male_Genital_A": [
            [0, "6b500f9b-eb8d-39f3-b853-f3fc60a35dd5", 0],
            [0, "79c3b32b-a243-b949-4aea-4ff285d50fca", 1],
            [1, "6b500f9b-eb8d-39f3-b853-f3fc60a35dd5", 2],
            [1, "79c3b32b-a243-b949-4aea-4ff285d50fca", 3],
        ],
        "Male_Genital_B": [
            [0, "f65ad014-9202-4dd0-57df-62179cc6ca63", 0],
            [0, "79c3b32b-a243-b949-4aea-4ff285d50fca", 1],
            [1, "f65ad014-9202-4dd0-57df-62179cc6ca63", 2],
            [1, "79c3b32b-a243-b949-4aea-4ff285d50fca", 3],
        ],
    },
    "Gnomes": {
        "Female_Genital_A": [
            [0, "af0dca83-21a7-a8d9-0ddc-28467eb30ab4", 0],
            [0, "79c3b32b-a243-b949-4aea-4ff285d50fca", 1],
            [1, "af0dca83-21a7-a8d9-0ddc-28467eb30ab4", 2],
            [1, "79c3b32b-a243-b949-4aea-4ff285d50fca", 3],
        ],
        "Female_Genital_B": [
            [0, "a5be54f4-264d-874d-3197-ad1d8a787df9", 0],
            [0, "79c3b32b-a243-b949-4aea-4ff285d50fca", 1],
            [1, "a5be54f4-264d-874d-3197-ad1d8a787df9", 2],
            [1, "79c3b32b-a243-b949-4aea-4ff285d50fca", 3],
        ],
        "Male_Genital_A": [
            [0, "0447e07f-dbec-9ef3-ebb3-10e23a20d50e", 0],
            [0, "79c3b32b-a243-b949-4aea-4ff285d50fca", 1],
            [1, "0447e07f-dbec-9ef3-ebb3-10e23a20d50e", 2],
            [1, "79c3b32b-a243-b949-4aea-4ff285d50fca", 3],
        ],
        "Male_Genital_B": [
            [0, "7a356c17-aff6-c532-bc19-c63ed294b14c", 0],
            [0, "79c3b32b-a243-b949-4aea-4ff285d50fca", 1],
            [1, "7a356c17-aff6-c532-bc19-c63ed294b14c", 2],
            [1, "79c3b32b-a243-b949-4aea-4ff285d50fca", 3],
        ],
    },
    "Halflings": {
        "Female_Genital_A": [
            [0, "bc299bb1-f033-3d89-dcc0-c00b4b6f61d8", 0],
            [0, "79c3b32b-a243-b949-4aea-4ff285d50fca", 1],
            [1, "bc299bb1-f033-3d89-dcc0-c00b4b6f61d8", 2],
            [1, "79c3b32b-a243-b949-4aea-4ff285d50fca", 3],
        ],
        "Female_Genital_B": [
            [0, "eb449b09-a900-1ac8-d414-d867726d8c7c", 0],
            [0, "79c3b32b-a243-b949-4aea-4ff285d50fca", 1],
            [1, "eb449b09-a900-1ac8-d414-d867726d8c7c", 2],
            [1, "79c3b32b-a243-b949-4aea-4ff285d50fca", 3],
        ],
        "Male_Genital_A": [
            [0, "0da12a47-dd52-2de3-0fe4-8f944c72b414", 0],
            [0, "79c3b32b-a243-b949-4aea-4ff285d50fca", 1],
            [1, "0da12a47-dd52-2de3-0fe4-8f944c72b414", 2],
            [1, "79c3b32b-a243-b949-4aea-4ff285d50fca", 3],
        ],
        "Male_Genital_B": [
            [0, "ad43d0f8-462c-9dd3-6283-b682986b4f09", 0],
            [0, "79c3b32b-a243-b949-4aea-4ff285d50fca", 1],
            [1, "ad43d0f8-462c-9dd3-6283-b682986b4f09", 2],
            [1, "79c3b32b-a243-b949-4aea-4ff285d50fca", 3],
        ],
    },
    "HalfOrcs": {
        "Female_Genital_A": [
            [0, "e65bbd33-a62d-a944-f8c0-b8bd0daea2e4", 0],
            [0, "79c3b32b-a243-b949-4aea-4ff285d50fca", 1],
            [1, "e65bbd33-a62d-a944-f8c0-b8bd0daea2e4", 2],
            [1, "79c3b32b-a243-b949-4aea-4ff285d50fca", 3],
        ],
        "Female_Genital_B": [
            [0, "bf0f148c-5eea-bd82-a470-b8777d180fa7", 0],
            [0, "79c3b32b-a243-b949-4aea-4ff285d50fca", 1],
            [1, "bf0f148c-5eea-bd82-a470-b8777d180fa7", 2],
            [1, "79c3b32b-a243-b949-4aea-4ff285d50fca", 3],
        ],
        "Male_Genital_A": [
            [0, "9c6fbff9-3733-ca3f-e149-af0736e22f85", 0],
            [0, "79c3b32b-a243-b949-4aea-4ff285d50fca", 1],
            [1, "9c6fbff9-3733-ca3f-e149-af0736e22f85", 2],
            [1, "79c3b32b-a243-b949-4aea-4ff285d50fca", 3],
        ],
        "Male_Genital_B": [
            [0, "51d4a9eb-1d28-a6fb-1b6d-6d8d30064253", 0],
            [0, "79c3b32b-a243-b949-4aea-4ff285d50fca", 1],
            [1, "51d4a9eb-1d28-a6fb-1b6d-6d8d30064253", 2],
            [1, "79c3b32b-a243-b949-4aea-4ff285d50fca", 3],
        ],
    },
    "Humans": {
        # Female
        "Female_Genital_A": [
            [0, "07168a77-9294-35f1-a78d-04ee9b8c46ad", 0],
            [0, "79c3b32b-a243-b949-4aea-4ff285d50fca", 1],
            [1, "07168a77-9294-35f1-a78d-04ee9b8c46ad", 2],
            [1, "79c3b32b-a243-b949-4aea-4ff285d50fca", 3],
        ],
        "Female_Genital_B": [
            [0, "827afee2-dd5e-8663-ba8b-7c184e7de228", 0],
            [0, "79c3b32b-a243-b949-4aea-4ff285d50fca", 1],
        ],
        # Female Strong
        "FemaleStrong_Genital_A": [
            [0, "79c3b32b-a243-b949-4aea-4ff285d50fca", 0],
            [0, "79c3b32b-a243-b949-4aea-4ff285d50fca", 1],
            [1, "7c3f090b-ca3c-542d-2468-7c8d2c964359", 2],
            [1, "7c3f090b-ca3c-542d-2468-7c8d2c964359", 3],
        ],
        "FemaleStrong_Genital_B": [
            [0, "d9793d7d-440d-469c-84db-9e884dfba645", 0],
            [0, "79c3b32b-a243-b949-4aea-4ff285d50fca", 1],
        ],
        # MALE
        "Male_Genital_A": [
            [0, "b4548d94-0fd8-b3af-436a-dd2d86cf47f1", 0],
            [0, "79c3b32b-a243-b949-4aea-4ff285d50fca", 1],
            [1, "b4548d94-0fd8-b3af-436a-dd2d86cf47f1", 2],
            [1, "79c3b32b-a243-b949-4aea-4ff285d50fca", 3],
        ],
        "Male_Genital_B": [
            [0, "4add0105-0d3a-f68a-5484-660c0be7eecc", 0],
            [0, "79c3b32b-a243-b949-4aea-4ff285d50fca", 1],
            [1, "4add0105-0d3a-f68a-5484-660c0be7eecc", 2],
            [1, "79c3b32b-a243-b949-4aea-4ff285d50fca", 3],
        ],
        # Male Strong
        "MaleStrong_Genital_A": [
            [0, "79c3b32b-a243-b949-4aea-4ff285d50fca", 0],
            [0, "79c3b32b-a243-b949-4aea-4ff285d50fca", 1],
            [1, "7c3f090b-ca3c-542d-2468-7c8d2c964359", 2],
            [1, "7c3f090b-ca3c-542d-2468-7c8d2c964359", 3],
        ],
        "MaleStrong_Genital_B": [
            [0, "ffd51198-92dc-e904-5771-48e60675b0e8", 0],
            [0, "79c3b32b-a243-b949-4aea-4ff285d50fca", 1],
        ],
    },
    "Tieflings": {
        # Female
        "Female_Genital_A": [
            [0, "016ccd7e-6163-74a3-24fd-f34209a467da", 0],
            [0, "79c3b32b-a243-b949-4aea-4ff285d50fca", 1],
        ],
        "Female_Genital_B": [
            [0, "379accf4-28fb-646b-34cf-5b40739eb866", 0],
            [0, "79c3b32b-a243-b949-4aea-4ff285d50fca", 1],
            [1, "379accf4-28fb-646b-34cf-5b40739eb866", 2],
            [1, "79c3b32b-a243-b949-4aea-4ff285d50fca", 3],
        ],
        # FS
        "FemaleStrong_Genital_A": [
            [0, "5ddb6d82-965e-3908-f8de-db9792fd9890", 0],
            [0, "5ddb6d82-965e-3908-f8de-db9792fd9890", 1],
            [1, "7c3f090b-ca3c-542d-2468-7c8d2c964359", 2],
            [1, "7c3f090b-ca3c-542d-2468-7c8d2c964359", 3],
        ],
        "FemaleStrong_Genital_B": [
            [0, "79def482-e3d9-e7ee-03dd-3b64030fd20a", 0],
            [0, "79c3b32b-a243-b949-4aea-4ff285d50fca", 1],
        ],
        # MALE
        "Male_Genital_A": [
            [0, "79c3b32b-a243-b949-4aea-4ff285d50fca", 0],
            [0, "03ff3d11-7cb4-bd11-a6f7-52024e725a79", 1],
            [1, "79c3b32b-a243-b949-4aea-4ff285d50fca", 2],
            [1, "03ff3d11-7cb4-bd11-a6f7-52024e725a79", 3],
        ],
        "Male_Genital_B": [
            [0, "68c4fb93-a8e1-2a2b-d19c-0ffa853bc365", 0],
            [0, "79c3b32b-a243-b949-4aea-4ff285d50fca", 1],
            [1, "68c4fb93-a8e1-2a2b-d19c-0ffa853bc365", 2],
            [1, "79c3b32b-a243-b949-4aea-4ff285d50fca", 3],
        ],
        # Male Strong
        "MaleStrong_Genital_A": [
            [0, "03ff3d11-7cb4-bd11-a6f7-52024e725a79", 0],
            [0, "03ff3d11-7cb4-bd11-a6f7-52024e725a79", 1],
            [1, "7c3f090b-ca3c-542d-2468-7c8d2c964359", 2],
            [1, "7c3f090b-ca3c-542d-2468-7c8d2c964359", 3],
        ],
        "MaleStrong_Genital_B": [
            [0, "68c4fb93-a8e1-2a2b-d19c-0ffa853bc365", 0],
            [0, "79c3b32b-a243-b949-4aea-4ff285d50fca", 1],
        ],
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
    mkdir(f"Generated/Public/{name}/Dragonborn/Female")
    mkdir(f"Generated/Public/{name}/Dragonborn/Male")

    # Dwarves
    mkdir(f"Generated/Public/{name}/Dwarves/Female")
    mkdir(f"Generated/Public/{name}/Dwarves/Male")

    # Githyanki
    mkdir(f"Generated/Public/{name}/Githyanki/Female")
    mkdir(f"Generated/Public/{name}/Githyanki/Male")

    # Gnomes
    mkdir(f"Generated/Public/{name}/Gnomes/Female")
    mkdir(f"Generated/Public/{name}/Gnomes/Male")

    # Halflings
    mkdir(f"Generated/Public/{name}/Halflings/Female")
    mkdir(f"Generated/Public/{name}/Halflings/Male")

    # HalfOrcs
    mkdir(f"Generated/Public/{name}/HalfOrcs/Female")
    mkdir(f"Generated/Public/{name}/HalfOrcs/Male")

    # Humans
    mkdir(f"Generated/Public/{name}/Humans/Female")
    mkdir(f"Generated/Public/{name}/Humans/Male")
    mkdir(f"Generated/Public/{name}/Humans/FemaleStrong")
    mkdir(f"Generated/Public/{name}/Humans/MaleStrong")

    # Tieflings
    mkdir(f"Generated/Public/{name}/Tieflings/Female")
    mkdir(f"Generated/Public/{name}/Tieflings/Male")
    mkdir(f"Generated/Public/{name}/Tieflings/FemaleStrong")
    mkdir(f"Generated/Public/{name}/Tieflings/MaleStrong")


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
        private_parts_id = file_split[0]

        gender = file_path[4]

        private_parts = gender + "_Genital_" + private_parts_id

        raceName = file_path[3]
        raceUUID = race[file_path[3]]
        skeletonUUID = skeleton[file_path[3] + file_path[4]]

        # 0 = Male, 1 = Female
        bodyType = str(1 if "Female" in file_path[4] else 0)

        # 0 = Average, 1 = Strong
        bodyShape = str(1 if "Strong" in file_path[4] else 0)

        # Private Parts UUID
        penis = "d27831df-2891-42e4-b615-ae555404918b"
        vagina = "a0738fdf-ca0c-446f-a11d-6211ecac3291"
        genital_id = str(vagina if private_parts_id == "A" else penis)

        paths.append(
            {
                "bodyShape": bodyShape,
                "bodyType": bodyType,
                "dir": dirname,
                "genital_id": genital_id,
                "genitals": private_parts,
                "name": name.replace("_", " "),
                "raceName": raceName,
                "raceUUID": raceUUID,
                "skeletonUUID": skeletonUUID,
                "stem": path.stem,
                "suffix": path.suffix,
            }
        )
        pprint.pprint(paths)
    return paths


# Insert XML for CharacterCreationAppearanceVisuals.lsx
def insert_dick_character_creation(model, handle, uuid):
    character_uuid = generate_uuid()
    xml = f"""
<node id="CharacterCreationAppearanceVisual">
  <attribute id="BodyShape" type="uint8" value="{model['bodyShape']}" />
  <attribute id="BodyType" type="uint8" value="{model['bodyType']}" />
  <attribute id="DisplayName" type="TranslatedString" handle="{handle}" version="1" />
  <attribute id="RaceUUID" type="guid" value="{model['raceUUID']}" />
  <attribute id="SlotName" type="FixedString" value="Private Parts" />
  <attribute id="UUID" type="guid" value="{character_uuid}" />
  <attribute id="VisualResource" type="guid" value="{uuid}" />
  <children>
    <node id="Tags">
      <attribute id="Object" type="guid" value="{model['genital_id']}" />
    </node>
  </children>
</node>
      """
    dick = ET.XML(xml)
    return dick


def genital_mesh_xml(meshObject, stem):
    meshXML = ""
    for mesh in meshObject:
        meshXML += f"""
<node id="Objects">
  <attribute id="LOD" type="uint8" value="{mesh[0]}" />
  <attribute id="MaterialID" type="FixedString" value="{mesh[1]}" />
  <attribute id="ObjectID" type="FixedString" value="{stem}.Genital_Mesh.{mesh[2]}" />
</node>
        """
    return meshXML


# Insert XML for _merged.lsx
def insert_dick_merged(model, uuid):
    path = model["dir"]
    print(model["raceName"] + " " + model["genitals"])
    print(genitals[model["raceName"]][model["genitals"]])
    junk = genitals[model["raceName"]][model["genitals"]]
    meshXML = genital_mesh_xml(junk, model["stem"])

    xml = f"""
<node id="Resource">
  <attribute id="AttachBone" type="FixedString" value="" />
  <attribute id="AttachmentSkeletonResource" type="FixedString" value="" />
  <attribute id="BlueprintInstanceResourceID" type="FixedString" value="" />
  <attribute id="BoundsMax" type="fvec3" value="0.04660766 1.031223 0.05886364" />
  <attribute id="BoundsMin" type="fvec3" value="-0.04640537 0.8961504 -0.1221507" />
  <attribute id="ClothColliderResourceID" type="FixedString" value="" />
  <attribute id="HairPresetResourceId" type="FixedString" value="8f234279-a95b-0dba-d2d4-2aa9fed3b8f2" />
  <attribute id="HairType" type="uint8" value="0" />
  <attribute id="ID" type="FixedString" value="{uuid}" />
  <attribute id="MaterialType" type="uint8" value="0" />
  <attribute id="Name" type="LSString" value="{model['name']}" />
  <attribute id="NeedsSkeletonRemap" type="bool" value="False" />
  <attribute id="RemapperSlotId" type="FixedString" value="" />
  <attribute id="ScalpMaterialId" type="FixedString" value="" />
  <attribute id="SkeletonResource" type="FixedString" value="{model['skeletonUUID']}" />
  <attribute id="SkeletonSlot" type="FixedString" value="Genitals" />
  <attribute id="Slot" type="FixedString" value="Private Parts" />
  <attribute id="SoftbodyResourceID" type="FixedString" value="" />
  <attribute id="SourceFile" type="LSString" value="{path}/{model['stem']}{model['suffix']}" />
  <attribute id="SupportsVertexColorMask" type="bool" value="True" />
  <attribute id="Template" type="FixedString" value="{path}/{model['stem']}.Dummy_Root.0" />
  <attribute id="_OriginalFileVersion_" type="int64" value="144115207403209033" />
  <children>
    <node id="AnimationWaterfall">
      <attribute id="Object" type="FixedString" value="" />
    </node>
    <node id="Base" />
    <node id="ClothProxyMapping" />
    {meshXML}
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
        with Folder(f"Public/{name}/Content/Assets/Characters/[PAK]_Genitals"):
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
        merged = (
            f"Public/{name}/Content/Assets/Characters/[PAK]_Genitals/_merged.lsf.lsx"
        )
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
                    model["raceUUID"] = race["Elves"]
                    model["raceName"] = "Elves"
                    model["name"] = data.text + " Elves"
                    uuid = generate_uuid()

                    # Insert content nodes to character creation visuals.
                    for element in visuals_children:
                        element.append(
                            insert_dick_character_creation(model, handle, uuid)
                        )

                    # Insert content nodes to merged.lsx.
                    for element in merged_children:
                        element.append(insert_dick_merged(model, uuid))

                    model["raceUUID"] = race["Drows"]
                    model["raceName"] = "Elves"
                    model["name"] = data.text + " Drows"
                    uuid = generate_uuid()

                    # Insert content nodes to character creation visuals.
                    for element in visuals_children:
                        element.append(
                            insert_dick_character_creation(model, handle, uuid)
                        )

                    # Insert content nodes to merged.lsx.
                    for element in merged_children:
                        element.append(insert_dick_merged(model, uuid))

                    model["raceUUID"] = race["HalfElfs"]
                    model["raceName"] = "Humans"
                    model["name"] = data.text + " HalfElfs"
                    uuid = generate_uuid()

                    # Insert content nodes to character creation visuals.
                    for element in visuals_children:
                        element.append(
                            insert_dick_character_creation(model, handle, uuid)
                        )

                    # Insert content nodes to merged.lsx.
                    for element in merged_children:
                        element.append(insert_dick_merged(model, uuid))

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
