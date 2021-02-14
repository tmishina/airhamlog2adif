# airhamlog2esl - Log Entry Converter from Airhamlog CSV to eSQL ADIF


## Architecture


## CLI
### Options
If no option is specified, all of the log entries are converted.

```
-m month to be converted (default: nothing)
-y year (default: this year)
```

Examples
If you run following commands in 2021, then...

```
airhamlog2esql              # convert all log entries in a CSV file.
airhamlog2esql -m 2         # convert log entries in February 2021.
airhamlog2esql -y 2020      # convert log entries in 2020.
airhamlog2esql -m 2 -y 2020 # convert log entries in December 2020.
airhamlog2eqsl -d 20210214  # convert log entries on Februrary 14, 2021.
airhamlog2eqsl --today      #convert today's log entries.
```
