# Performance

Some notes about performance (on Eads' 2014 Macbook Pro with a fairly speedy Fios connection).

```bash
$ time elex get-results 11-3-2015 -o json > /tmp/res.json

real	0m6.568s
user	0m5.180s
sys	0m0.155s

$ time elex get-results 11-3-2015 > /tmp/res.csv

real	0m4.850s
user	0m3.834s
sys	0m0.144s
```
