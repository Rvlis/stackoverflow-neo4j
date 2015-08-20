## Import stackexchange in neo4j

steps:

- Download the dump from archive.org: https://archive.org/details/stackexchange
- extract the community you want in `extracted/<name of the community>/` with `Posts.xml` & co. in the dir
- `python to_csv.py extracted/<name of the community>` to get the csvs in `csvs/`
- `sh import.sh` to import the csvs in neo4j
   - assuming that neo4j is in the `../neo/` directory
   - **the script assume that you want to remove you old database** (at the end)

Look at the scripts before using them to understand what they do :)

*Have fun!*