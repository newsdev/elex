#!/bin/bash

# S3 url: MUST be set to your bucket and path.
ELEX_S3_URL='mybucket.tld/output/path.json'

# Get results and upload to S3
elex results 2012-11-06 --results-level state -o json \
| jq -c '[
            .[] |
            select(.level == "state" ) |
            select(.officename == "President") |
            {
              officename: .officename,
              statepostal: .statepostal,
              first: .first,
              last: .last,
              party: .party,
              votecount: .votecount,
              votepct: .votepct,
              winner: .winner,
              level: .level
            }
         ]' \
| gzip -vc \
| aws s3 cp - s3://$ELEX_S3_URL \
    --acl public-read \
    --content-type=application/json \
    --content-encoding gzip

# Check response headers
curl -I $ELEX_S3_URL

# Get first entry of uploaded json
curl -s --compressed $ELEX_S3_URL | jq '[.[]][0]'
