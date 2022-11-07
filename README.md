# Preservica Checksum Checker

A lot of our AV material had checksums generated at the point of digitisation - and whilst some preservica ingest methods do do fixity checking at point of ingest, some of our earlier ingests were done without fixity checking against the legacy checksum.

The script pulls checksums from Preservica using the pyPreservica library - and then checks them against the legacy md5 files that are held in folders with the digitised files

Very specific to our use case, but some of the functions could be useful

For example, the script saves the checksums to a .csv which means they can be re-used, as fetching them from the Preservica API each time can be time consuming
