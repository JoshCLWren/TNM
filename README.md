# TNM

# Objects:
# Circuits.
# Circuits have brands
# Brands have shows
# Shows have matches
# Circuits also have super shows
# Shows have regular matches and main events.
# Matches have Wrestlers
# Wrestlers have a Circuit/Brand/Gender/Name/Tag Teams/Stables
# Tag Teams have two Wrestlers
# Stables have more than two Wrestlers
# Regular matches are single/tag/multi-man/battle royal/ and are 1v1/triangle/4way
# Main Events are single/tag/multi-man/ with #1 contender spot or title shot and are 1v1/triangle/4way
# Feuds are a wrestler/tag-team/stable vs wrestler/tag-team/stable
# Super shows have multiple main events and gimmick matches
# Royal Rumbles/war games/elimination chambers have wrestlers and are only on Super Shows


Need to keep python version below 3.3.1 builds keep failing in pyenv... compiling to exe will be more difficult the more packages I use though.

Need to add postgres and migrations

Need to read .dat files and make them db rows.

Need to make a wrestlers table, a tag team table, and a stable table

Can't seem to find out how to use .dat to determine what circuit they are in so may need to ingest that manually with roster files.

Need to also have a circuit table so that

Notes for adding brands/titles to circuits
looks like brands are stored in circuit/brands.dat
championships are stored in circuit/details.ttl with brand info as well
circuit/wwcl.dat looks liek breakdown of who is in each brand