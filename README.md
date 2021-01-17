## Import stackexchange in neo4j

__Attention__: 

my neo4j's version is 4.2.2 and OS is win10, so the command of import.sh is unsuitable for me. For this reason, I have changed the step5. In 4.x's neo4j, the default db's name is "neo4j" instead of "graph".

Because the "stackoverflow" dump data is  too large to download, I choose the lighter "meta-stackoverflow" dump data to construct my kg.

__Steps__:

- Download the dump from archive.org: https://archive.org/details/stackexchange
- extract the community you want in `extracted/<name of the community>/` with `Posts.xml` & co. in the dir
   - you can `dtrx` on linux
- you need to `sudo pip3 install xmltodict`
- `python3 to_csv.py extracted/<name of the community>` to get the csvs in `csvs/`
- arrive at __your/path/neo4j-4.x.x/bin/__, then copy the content of __cmd.txt__ to your command line prompt.

Look at the scripts before using them to understand what they do :)

*Have fun!*
