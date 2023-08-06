cemconvert
Tool for converting CEM hourly data to hourly FF10 and scaling annual FF10 to CEM values

Install from package "pip install cemconvert_VERSION_.tar.gz --user"



Usage: cemconvert [options] egu_annual_ff10

Options:
  -h, --help            show this help message and exit
  -p CEMPOLLS, --cempolls=CEMPOLLS
                        List of pollutants in hourly CEM files to process
  -y YEAR, --year=YEAR  Year to process
  -i INPUT_PATH, --input_path=INPUT_PATH
                        Hourly CEM input path
  -o OUTPUT_PATH, --output_path=OUTPUT_PATH
                        FF10 inventory output path
  -c, --write_cems      Write hourly CEM data in old SMOKE format
  -g, --gmt             Output hourly FF10 to GMT instead of local time
  -r, --ramp_up         Timeshift hours for the year after the designated year
                        back one year
  -t TEMPORALVAR, --temporal_var=TEMPORALVAR
                        Variable name used for temporal activity
  -n CALCPOLLS, --inven_polls=CALCPOLLS
                        List of inventory pollutants to temporalize using the
                        CEM activity
  -m MONTHS, --months=MONTHS
                        List of CEM months to process as a comma-delimited
                        list of integers            Default behavior is an
                        annual run
  -l LABEL, --label=LABEL
                        Output inventory label
  -k, --keep_annual     Keep and temporalize annual temporal values in FF10
                        that match CEMs.            Default is to replace the
                        emissions values with CEMs.
  -e, --cemcorrect      Apply CEMCorrect to the CEMS




Download annual 2021 CEMS from CAMPD bulk download site using provided download tool:
get_camd_cems_bulk -y 2021 -o ./cems/2021 -a "YOURAPIKEY"

Example 1. Generate 2021 base year EGU inventories from annual 2021 FF10 and 2021 CEMS for SMOKE with CEMCorrect
cemconvert -y 2021 -i ./cems/2021 -o ./output -g -n PM25-PRI -l 2021_egu_2021cems -e ptegu_2021_annual_FF10.csv


Example 2. Generate 2032 summer season EGU inventories from annual 2032 FF10 and 2021 CEMS for SMOKE with CEMCorrect. Scale hourly CEMS values to 2032 values.
cemconvert -y 2032 -i ./cems/2021 -o ./output -g -n PM25-PRI -m "5,6,7,8,9" -e -k -l 2032_egu_2021cems ptegu_2032_annual_FF10.csv


Example 3. Convert 2021 CEMS from new format to old and apply CEMCorrect
cemconvert -y 2021 -i ./cems/2021 -o ./output -c -e ptegu_2021_annual_FF10.csv
