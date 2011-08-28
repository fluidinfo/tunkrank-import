Importing Tunkrank data to Fluidinfo
------------------------------------

The file `import.py` reads Tunkrank data from stdin and adds it to Fluidinfo.
Stdin is expected to be CSV with fields

  TwitterID
  ScreenName
  Name
  Location
  URL
  Friends
  Followers
  Statuses
  RawTunkRankScore
  TunkRankScore
  TunkRankComputedAt

For each line, we put the following into Fluidinfo onto the object whose
about tag is the twitter screenname in lowercase, preceeded by an @. The
CSV fields we process and their Fludinfo tags are as follows:

  RawTunkRankScore    -> tunkrank.com/raw-score
  TunkRankScore       -> tunkrank.com/raw-score
  TunkRankComputedAt  -> tunkrank.com/computed-at

The TunkRankComputedAt field has format e.g., 2011-08-03 19:19:11.045452-04
which is converted to a (float) number of seconds from the epoch.

To install
----------

Create a virtualenv and install the requirements:

.. code-block:: sh

    $ virtualenv --no-site-packages env
    $ . env/bin/activate
    $ pip install -r requirements.txt

To run
------

Send the TunkRank CSV file to `import.py` on stdin. The CSV file is not
checked in to this repo as it's huge (60M compressed) and is not public.
You will also need the `tunkrank.com` user's password. Ask Terry for it.
