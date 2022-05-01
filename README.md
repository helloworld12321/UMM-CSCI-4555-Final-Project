# UMM CSCI 4555 Final Project

This repository analyzes data from the [Million Song Dataset](http://millionsongdataset.com) project.

The raw data from this project isn't included here, but you can get it at the
following links:

- Song metadata (HDF5 files): <http://labrosa.ee.columbia.edu/~dpwe/tmp/millionsongsubset.tar.gz>
- Genre information (SQLite database): <http://millionsongdataset.com/sites/default/files/lastfm/lastfm_tags.db>

Once you have that data, you can run the various Python scripts to pre-process it. Usage instructions are included at the top of each script. For these scripts to work, you will need to install the Python packages in `requirements.txt`.

The Python scripts aggregate the raw data into the `SongsWithGenres.csv` file. The `neural-networks.Rmd` script reads this file and tries to categorize the data. You can run `neural-networks.Rmd` in RStudio; you will need to install some R packages first.
