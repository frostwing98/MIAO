### To view / unpack a miniapp:
`node wuWxapkg.js foobar.wxapkg`

### To initiate:
`./restart.sh`

### To run:
##### On one terminal:
`python3 assigner.py`

##### On the other terminal:
`python3 worker.py`

##### To run multiple worker:
`./runurl.sh`

### Resuming after crash/shutdown
This script supports resuming. Just kill the assigner, wait for workers to die out, and restart with
`assigner.py`, and `worker.py`

To perform a fresh re-run, use
`./restart.sh`

### Post-analysis
The results are in scannedjsons.csv or scannedoverallres.csv.

The scannedallminiapps.csv saves the analyzed miniapp for resuming if analysis is interrupted by system shutdown.

After analysis, there could be multiple weird folders. These residue folders can be cleared by ./cleanweirdfolders.sh
